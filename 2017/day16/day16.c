
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int bufsize = 0;
char *programs;
int offset = 0;
static unsigned char *lookup;

char *split(char *);


void
exchange(int x, int y) {
    int x2, y2;
    x2 = (x + offset) % bufsize;
    y2 = (y + offset) % bufsize;
    char yc = programs[x2];
    char xc = programs[x2] = programs[y2];
    programs[y2] = yc;
    lookup[yc] = y2;
    lookup[xc] = x2;
}

void
spin(int swap) {
    offset += bufsize - swap;
    offset = offset % bufsize;
}

void
partner(char x, char y) {
    int y2 = lookup[x];
    int x2 = lookup[y];
    programs[y2] = y;
    programs[x2] = x;
    lookup[x] = x2;
    lookup[y] = y2;
}

void
apply(char *code) {
    switch(code[0]) {
       case 's': spin(code[1]);
                 break;
       case 'x': exchange(code[1], code[2]);
                 break;
       case 'p': partner(code[1], code[2]);
                 break;
    }
}

char *
to_code(char *command) {
    char *code = malloc(4);
    code[0] = command[0];
    code[3] = 0;
    switch (command[0]) {
        case 's':
            code[1] = (char)atoi(command+1);
            break;
        case 'x':
            code[1] = (char)atoi(command+1);
            code[2] = (char)atoi(split(command+1));
            break;
        case 'p':
            code[1] = command[1];
            code[2] = split(command+1)[0];
            break;
    }
    return code;
}


char *
split(char *str) {
    while (*str != '/')
        str++;
    return str+1;
}

void
init_lookup(void) {
    lookup = (unsigned char *)malloc(256);
    for (int i = 0; i < bufsize; i++) {
        lookup[programs[i]] = i;
    }
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
    if (argc < 2) {
        printf("Usage: %s programs moves [repeat]\n", argv[0]);
        return 1;
    }
    char **tokens = (char **)calloc(15000, sizeof(char *));
    char **tokptr = tokens;
    long repeat = argc > 3 ? atoll(argv[3]) : 1;
    programs = strdup(argv[1]);
    bufsize = strlen(programs);
    init_lookup();
    char *pch = strtok(argv[2], ",");
    while (pch != NULL) {
       *tokptr++ = to_code(strdup(pch));
       pch = strtok(NULL, ",");
    }
    *tokptr++ = NULL;

    for (long i; i < repeat; i++) {
        for (tokptr = tokens; *tokptr != NULL; tokptr++) {
            apply(*tokptr);
        }
    }

    output();
    return 0;
}
