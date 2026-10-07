#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void)
{
    printf("Fool's Domain Audit Utility\n");
    printf("===========================\n");
    printf("Running system audit...\n");

    /*
     * INTENTIONAL CTF VULNERABILITY
     *
     * The helper is resolved through PATH.
     *
     * Because this executable is intended to be installed SUID root,
     * an attacker-controlled PATH entry can cause a different
     * "fool-report" executable to be launched with elevated privileges.
     */
    execlp("fool-report", "fool-report", NULL);

    perror("fool-report");
    return 1;
}
