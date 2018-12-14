
#include <stdio.h>
#include <string.h>

#define rmax 100000000

int len = 0;
char recipies[rmax];
char *ref;
int p1 = 0;
int p2 = 1;

void combine(void) {
    int i1 = (int) recipies[p1] - '0';
    int i2 = (int) recipies[p2] - '0';
    char new[10];
    sprintf(new, "%d", i1 + i2);
    strcat(ref, new);
    len += strlen(new);
    p1 = (p1 + i1 + 1) % len;
    p2 = (p2 + i2 + 1) % len;
    if (p1 == p2) {
       p2 = (p2 + 1) % len;
    }
}

int main(int argc, char *argv[]) {
    int i;
    //char *find="330121";
    char *find=argv[1];
    char *pos;
    strcat(recipies, "37");
    len=strlen(recipies);
    while (len < rmax - 5) {
        ref = recipies + ((len - 10) > 0 ? (len - 10) : 0); 
        combine();
        if (len % 10000 == 0)
            printf("%d\n", len);
        if (pos = strstr(ref, find)) {
            printf("Found %ld\n", pos - recipies); 
            break;
        }
    }
    //printf("Recipies: %s\n", recipies);
}

    
