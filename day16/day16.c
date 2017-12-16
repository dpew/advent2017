
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int bufsize = 0;
char *programs;
int offset = 0;

char *split(char *);


void
exchange(int x, int y) {
    int x2, y2;
    x2 = (x + offset) % bufsize;
    y2 = (y + offset) % bufsize;
    char t = programs[x2];
    programs[x2] = programs[y2];
    programs[y2] = t;
}

void
spin(int swap) {
    offset += bufsize - swap;
    offset = offset % bufsize;
}

void
partner(char x, char y) {
    int i;
    int matches = 0;
    for (i = 0; i < bufsize && matches < 2; i++) {
        if (programs[i] == x) {
            programs[i] = y;
            matches ++;
            continue;
        }

        if (programs[i] == y) {
            programs[i] = x;
            matches ++;
            continue;
        }
    }
}

void
apply(char *code) {
    char *a1 = code+1;
    char *a2;
    switch(code[0]) {
       case 's': spin(atoi(a1));
                 break;
       case 'x': a2 = split(a1);
                 exchange(atoi(a1), atoi(a2));
                 break;
       case 'p': a2 = split(a1);
                 partner(a1[0], a2[0]);
                 break;
    }
}

char *
split(char *str) {
    while (*str != '/')
        str++;
    return str+1;
}

void 
output(void) {
    char *b = programs + offset;

    for (int i = offset; i < bufsize; i++) {
       putchar(*b++);
    }
    b = programs;
    for (int i = 0; i < offset; i++) {
       putchar(*b++);
    }
    putchar('\n');
}
    

int
main(int argc, char *argv[]) {
    char **tokens = (char **)calloc(15000, sizeof(char *));
    char **tokptr = tokens;
    programs = strdup(argv[1]);
    bufsize = strlen(programs);
    char *pch = strtok(argv[2], ",");
    while (pch != NULL) {
       *tokptr++ = strdup(pch);
       pch = strtok(NULL, ",");
    }
    *tokptr++ = NULL;

    for (tokptr = tokens; *tokptr != NULL; tokptr++) {
        apply(*tokptr);
    }

    output();
    return 0;
}
    
    
