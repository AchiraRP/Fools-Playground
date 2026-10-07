from scapy.all import (
    Ether,
    ARP,
    IP,
    ICMP,
    TCP,
    UDP,
    DNS,
    DNSQR,
    DNSRR,
    Raw,
    PcapNgWriter,
)

from pathlib import Path
import base64
import os


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = PROJECT_ROOT / "artifact"
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

PCAP_PATH = ARTIFACT_DIR / "silent-network.pcapng"

# ============================================================
# Fictional network
# ============================================================

GATEWAY_IP = "10.20.30.1"
ANALYST_IP = "10.20.30.10"
OFFICE_IP = "10.20.30.21"
SUSPICIOUS_IP = "10.20.30.37"
DNS_IP = "10.20.30.53"

GATEWAY_MAC = "02:00:00:20:30:01"
ANALYST_MAC = "02:00:00:20:30:10"
OFFICE_MAC = "02:00:00:20:30:21"
SUSPICIOUS_MAC = "02:00:00:20:30:37"
DNS_MAC = "02:00:00:20:30:53"

DNS_DOMAIN = "resolver-cache.internal"

# ============================================================
# Local development FP-06 handoff
# These values can be changed later for deployment.
# ============================================================

FP06_HOST = os.environ.get("FP06_HOST")
FP06_PORT = os.environ.get("FP06_PORT")
FP06_USERNAME = "investigator"
FP06_KEY_NAME = "fp06-player-access.key"

if not FP06_HOST or not FP06_PORT:
    raise RuntimeError(
        "Set FP06_HOST and FP06_PORT before generating the PCAP."
    )


def encode_chunks(message: str) -> list[str]:
    encoded = base64.b32encode(
        message.encode("utf-8")
    ).decode("ascii").rstrip("=")

    chunk_size = 20

    return [
        encoded[i:i + chunk_size]
        for i in range(0, len(encoded), chunk_size)
    ]


def ethernet(src: str, dst: str):
    return Ether(src=src, dst=dst)


def build_arp_packets() -> list:
    packets = []

    packets.append(
        ethernet(ANALYST_MAC, "ff:ff:ff:ff:ff:ff")
        / ARP(
            op=1,
            hwsrc=ANALYST_MAC,
            psrc=ANALYST_IP,
            hwdst="00:00:00:00:00:00",
            pdst=GATEWAY_IP,
        )
    )

    packets.append(
        ethernet(GATEWAY_MAC, ANALYST_MAC)
        / ARP(
            op=2,
            hwsrc=GATEWAY_MAC,
            psrc=GATEWAY_IP,
            hwdst=ANALYST_MAC,
            pdst=ANALYST_IP,
        )
    )

    packets.append(
        ethernet(OFFICE_MAC, "ff:ff:ff:ff:ff:ff")
        / ARP(
            op=1,
            hwsrc=OFFICE_MAC,
            psrc=OFFICE_IP,
            hwdst="00:00:00:00:00:00",
            pdst=GATEWAY_IP,
        )
    )

    packets.append(
        ethernet(GATEWAY_MAC, OFFICE_MAC)
        / ARP(
            op=2,
            hwsrc=GATEWAY_MAC,
            psrc=GATEWAY_IP,
            hwdst=OFFICE_MAC,
            pdst=OFFICE_IP,
        )
    )

    return packets


def build_icmp_packets() -> list:
    packets = []

    packets.append(
        ethernet(ANALYST_MAC, GATEWAY_MAC)
        / IP(src=ANALYST_IP, dst=GATEWAY_IP)
        / ICMP(type="echo-request", id=1, seq=1)
    )

    packets.append(
        ethernet(GATEWAY_MAC, ANALYST_MAC)
        / IP(src=GATEWAY_IP, dst=ANALYST_IP)
        / ICMP(type="echo-reply", id=1, seq=1)
    )

    packets.append(
        ethernet(OFFICE_MAC, GATEWAY_MAC)
        / IP(src=OFFICE_IP, dst=GATEWAY_IP)
        / ICMP(type="echo-request", id=2, seq=1)
    )

    packets.append(
        ethernet(GATEWAY_MAC, OFFICE_MAC)
        / IP(src=GATEWAY_IP, dst=OFFICE_IP)
        / ICMP(type="echo-reply", id=2, seq=1)
    )

    return packets


def build_normal_dns_packets() -> list:
    packets = []

    traffic = [
        (
            OFFICE_IP,
            OFFICE_MAC,
            [
                "portal.example.com",
                "updates.example.com",
                "cdn.example.com",
                "mail.example.com",
                "time.example.com",
                "files.example.com",
                "printer.local",
                "ntp.local",
                "intranet.local",
                "wiki.local",
                "docs.local",
                "chat.local",
                "calendar.local",
            ],
        ),
        (
            ANALYST_IP,
            ANALYST_MAC,
            [
                "portal.example.com",
                "updates.example.com",
                "security.example.com",
                "repo.example.com",
                "mail.example.com",
                "vpn.example.com",
                "ntp.local",
                "docs.local",
                "wiki.local",
                "assets.example.com",
                "cdn.example.com",
            ],
        ),
        (
            SUSPICIOUS_IP,
            SUSPICIOUS_MAC,
            [
                "ntp.local",
                "updates.example.com",
                "repo.example.com",
                "cdn.example.com",
                "intranet.local",
                "mail.example.com",
                "time.example.com",
                "status.local",
                "printer.local",
                "wiki.local",
            ],
        ),
    ]

    packets = []
    dns_id = 100
    sport = 53000

    for source_ip, source_mac, names in traffic:
        for name in names:
            query = (
                ethernet(source_mac, DNS_MAC)
                / IP(src=source_ip, dst=DNS_IP)
                / UDP(sport=sport, dport=53)
                / DNS(
                    id=dns_id,
                    rd=1,
                    qd=DNSQR(qname=name),
                )
            )

            response = (
                ethernet(DNS_MAC, source_mac)
                / IP(src=DNS_IP, dst=source_ip)
                / UDP(sport=53, dport=sport)
                / DNS(
                    id=dns_id,
                    qr=1,
                    aa=1,
                    qd=DNSQR(qname=name),
                    an=DNSRR(
                        rrname=name,
                        type="A",
                        ttl=300,
                        rdata="93.184.216.34",
                    ),
                )
            )

            packets.extend([query, response])
            dns_id += 1
            sport += 1

    return packets


def build_decoy_http_packets() -> list:
    packets = []

    flows = [
        (
            OFFICE_IP,
            OFFICE_MAC,
            41000,
            b"GET /internal/status HTTP/1.1\r\n"
            b"Host: intranet.local\r\n"
            b"User-Agent: Mozilla/5.0\r\n"
            b"Connection: close\r\n\r\n",
            b"HTTP/1.1 200 OK\r\n"
            b"Content-Type: text/plain\r\n"
            b"Content-Length: 21\r\n\r\n"
            b"System status: normal\n",
        ),
        (
            ANALYST_IP,
            ANALYST_MAC,
            41010,
            b"GET /updates HTTP/1.1\r\n"
            b"Host: updates.example.com\r\n"
            b"User-Agent: curl/8.0\r\n"
            b"Connection: close\r\n\r\n",
            b"HTTP/1.1 200 OK\r\n"
            b"Content-Type: text/plain\r\n"
            b"Content-Length: 18\r\n\r\n"
            b"No new updates.\n",
        ),
        (
            SUSPICIOUS_IP,
            SUSPICIOUS_MAC,
            41020,
            b"GET /health HTTP/1.1\r\n"
            b"Host: repo.example.com\r\n"
            b"Connection: close\r\n\r\n",
            b"HTTP/1.1 200 OK\r\n"
            b"Content-Type: text/plain\r\n"
            b"Content-Length: 17\r\n\r\n"
            b"Service healthy.\n",
        ),
    ]

    for index, (
        source_ip,
        source_mac,
        client_port,
        request,
        response,
    ) in enumerate(flows, start=1):

        seq_client = 1000 * index
        seq_server = 5000 * index

        # SYN
        packets.append(
            ethernet(source_mac, GATEWAY_MAC)
            / IP(src=source_ip, dst=GATEWAY_IP)
            / TCP(
                sport=client_port,
                dport=80,
                flags="S",
                seq=seq_client,
            )
        )

        # SYN/ACK
        packets.append(
            ethernet(GATEWAY_MAC, source_mac)
            / IP(src=GATEWAY_IP, dst=source_ip)
            / TCP(
                sport=80,
                dport=client_port,
                flags="SA",
                seq=seq_server,
                ack=seq_client + 1,
            )
        )

        # ACK
        packets.append(
            ethernet(source_mac, GATEWAY_MAC)
            / IP(src=source_ip, dst=GATEWAY_IP)
            / TCP(
                sport=client_port,
                dport=80,
                flags="A",
                seq=seq_client + 1,
                ack=seq_server + 1,
            )
        )

        # HTTP request
        packets.append(
            ethernet(source_mac, GATEWAY_MAC)
            / IP(src=source_ip, dst=GATEWAY_IP)
            / TCP(
                sport=client_port,
                dport=80,
                flags="PA",
                seq=seq_client + 1,
                ack=seq_server + 1,
            )
            / Raw(load=request)
        )

        # HTTP response
        packets.append(
            ethernet(GATEWAY_MAC, source_mac)
            / IP(src=GATEWAY_IP, dst=source_ip)
            / TCP(
                sport=80,
                dport=client_port,
                flags="PA",
                seq=seq_server + 1,
                ack=seq_client + 1 + len(request),
            )
            / Raw(load=response)
        )

        # FIN
        packets.append(
            ethernet(source_mac, GATEWAY_MAC)
            / IP(src=source_ip, dst=GATEWAY_IP)
            / TCP(
                sport=client_port,
                dport=80,
                flags="FA",
                seq=seq_client + 1 + len(request),
                ack=seq_server + 1 + len(response),
            )
        )

    return packets


def build_extra_background() -> list:
    packets = []

    attempts = [
        (ANALYST_IP, ANALYST_MAC, 42001, 22),
        (ANALYST_IP, ANALYST_MAC, 42002, 443),
        (ANALYST_IP, ANALYST_MAC, 42003, 8080),
        (OFFICE_IP, OFFICE_MAC, 42101, 22),
        (OFFICE_IP, OFFICE_MAC, 42102, 443),
        (SUSPICIOUS_IP, SUSPICIOUS_MAC, 42201, 22),
        (SUSPICIOUS_IP, SUSPICIOUS_MAC, 42202, 8080),
    ]

    for index, (
        source_ip,
        source_mac,
        sport,
        dport,
    ) in enumerate(attempts, start=1):

        packets.append(
            ethernet(source_mac, GATEWAY_MAC)
            / IP(src=source_ip, dst=GATEWAY_IP)
            / TCP(
                sport=sport,
                dport=dport,
                flags="S",
                seq=6000 + index,
            )
        )

    return packets

def build_suspicious_dns_packets(
    indicator: str,
    hidden_message: str,
) -> list:
    packets = []

    # The first suspicious query links FP-04's clue to this host.
    indicator_name = f"{indicator}.{DNS_DOMAIN}"

    packets.append(
        ethernet(SUSPICIOUS_MAC, DNS_MAC)
        / IP(src=SUSPICIOUS_IP, dst=DNS_IP)
        / UDP(sport=53037, dport=53)
        / DNS(
            id=500,
            rd=1,
            qd=DNSQR(qname=indicator_name),
        )
    )

    # Small unrelated suspicious-looking queries add noise.
    decoys = [
        "checkin.resolver-cache.internal",
        "status.resolver-cache.internal",
        "beacon.resolver-cache.internal",
    ]

    for index, name in enumerate(decoys, start=1):
        packets.append(
            ethernet(SUSPICIOUS_MAC, DNS_MAC)
            / IP(src=SUSPICIOUS_IP, dst=DNS_IP)
            / UDP(sport=53100 + index, dport=53)
            / DNS(
                id=550 + index,
                rd=1,
                qd=DNSQR(qname=name),
            )
        )

    chunks = encode_chunks(hidden_message)

    for index, chunk in enumerate(chunks, start=1):
        label = f"{index:02d}.{chunk}.{DNS_DOMAIN}"
        sport = 53200 + index
        dns_id = 600 + index

        query = (
            ethernet(SUSPICIOUS_MAC, DNS_MAC)
            / IP(src=SUSPICIOUS_IP, dst=DNS_IP)
            / UDP(sport=sport, dport=53)
            / DNS(
                id=dns_id,
                rd=1,
                qd=DNSQR(qname=label),
            )
        )

        response = (
            ethernet(DNS_MAC, SUSPICIOUS_MAC)
            / IP(src=DNS_IP, dst=SUSPICIOUS_IP)
            / UDP(sport=53, dport=sport)
            / DNS(
                id=dns_id,
                qr=1,
                aa=1,
                qd=DNSQR(qname=label),
            )
        )

        packets.extend([query, response])

    return packets


def main() -> None:
    indicator = "sync-check"

    flag_path = (
        PROJECT_ROOT.parent.parent
        / "flags-private"
        / "FP-05.flag"
    )

    if not flag_path.exists():
        raise FileNotFoundError(
            f"Private FP-05 flag not found: {flag_path}"
        )

    flag = flag_path.read_text(
        encoding="ascii"
    ).strip()

    hidden_message = (
        "FOOL NETWORK TRANSFER\n"
        "---------------------\n"
        "CASE: FP-05\n"
        f"FLAG: {flag}\n"
        "NEXT STAGE: FP-06\n"
        f"SSH HOST: {FP06_HOST}\n"
        f"SSH PORT: {FP06_PORT}\n"
        f"USERNAME: {FP06_USERNAME}\n"
        f"SSH KEY: {FP06_KEY_NAME}\n"
    )

    import random
    import time

    # Build background traffic as conversation-sized groups.
    # Packets inside each conversation stay in protocol order.
    background_groups = []

    arp = build_arp_packets()
    background_groups.extend([
        arp[0:2],
        arp[2:4],
    ])

    icmp = build_icmp_packets()
    background_groups.extend([
        icmp[0:2],
        icmp[2:4],
    ])

    normal_dns = build_normal_dns_packets()
    for index in range(0, len(normal_dns), 2):
        background_groups.append(normal_dns[index:index + 2])

    http = build_decoy_http_packets()
    for index in range(0, len(http), 6):
        background_groups.append(http[index:index + 6])

    extra = build_extra_background()
    for packet in extra:
        background_groups.append([packet])

    # The suspicious DNS channel is also grouped by query/response.
    suspicious = build_suspicious_dns_packets(
        indicator=indicator,
        hidden_message=hidden_message,
    )

    suspicious_groups = []

    # Indicator + three decoy queries.
    for index in range(4):
        suspicious_groups.append([suspicious[index]])

    # Each encoded fragment is a query/response pair.
    for index in range(4, len(suspicious), 2):
        suspicious_groups.append(suspicious[index:index + 2])

    rng = random.Random(20261007)
    rng.shuffle(background_groups)

    packets = []
    suspicious_index = 0

    for group in background_groups:
        packets.extend(group)

        if (
            suspicious_index < len(suspicious_groups)
            and rng.random() < 0.38
        ):
            packets.extend(suspicious_groups[suspicious_index])
            suspicious_index += 1

    for group in suspicious_groups[suspicious_index:]:
        packets.extend(group)

    # Give packets monotonically increasing timestamps so the capture
    # has a realistic chronological order.
    capture_start = time.time()

    for index, packet in enumerate(packets):
        packet.time = capture_start + (index * 0.25)

    writer = PcapNgWriter(str(PCAP_PATH))

    try:
        for packet in packets:
            writer.write(packet)
    finally:
        writer.close()

    print(f"PCAP written to: {PCAP_PATH}")
    print(f"Packet count: {len(packets)}")
    print(f"Hidden message length: {len(hidden_message)}")
    print(f"FP-06 target: {FP06_HOST}:{FP06_PORT}")
    print(f"FP-04 indicator placeholder: {indicator}")


if __name__ == "__main__":
    main()
