#include <stdio.h>
#include <unistd.h>

int main(void)
{
    printf("Fool's Domain System Report\n");
    printf("===========================\n");
    printf("Audit helper executed successfully.\n");
    printf("Real UID : %d\n", getuid());
    printf("Effective UID : %d\n", geteuid());
    printf("System report status: OK\n");

    return 0;
}
