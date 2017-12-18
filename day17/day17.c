#include <stdio.h>
#include <stdlib.h>
#include <string.h>


typedef struct node * NodePtr;
typedef struct node {
    int val;
    NodePtr next;
} Node;


void
insert(NodePtr n, int val) {
    NodePtr newnode = (NodePtr)malloc(sizeof(Node));
    newnode->val = val;
    newnode->next = n->next;
    n->next = newnode;
}

NodePtr
skip(NodePtr n, int skipval) {
    for (int i=0;i <= skipval; i++)
        n = n->next;
    return n;
}

NodePtr
find(NodePtr n, int val) {
    while (n->val != val)
        n = n->next;
    return n;
}

int
main(int argc, char *argv[]) {
    int skipval = argc > 2 ? atoi(argv[1]) : 3;
    int after = argc > 2 ? atoi(argv[2]) : 2017;
    int count = argc > 3 ? atoi(argv[3]) : after;

    // Initialize circular buffer
    NodePtr circular = (NodePtr)malloc(sizeof(Node));
    circular->next = circular;
    circular->val = 0;
    
    // Insert
    NodePtr current = circular;
    for (int i = 1; i <= count; i++) {
        current = skip(current, skipval);
        insert(current, i);
        if (i % 100000 == 0) {
            printf("Cir %d %d\n", circular->val, circular->next->val);
        }
    }

    // Find and print
    NodePtr found = find(circular, after);
    printf("%d %d\n", found->val, found->next->val);
        
    return 0;
}
