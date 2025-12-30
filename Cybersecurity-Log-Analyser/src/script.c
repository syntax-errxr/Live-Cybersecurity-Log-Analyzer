#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Node structure for queue
typedef struct Node {
    char program[200];
    struct Node* next;
} Node;

// Queue structure
typedef struct {
    Node* front;
    Node* rear;
} Queue;

// Function to initialize the queue
void initializeQueue(Queue* q) {
    q->front = q->rear = NULL;
}

// Function to enqueue a program
void enqueue(Queue* q, const char* program) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    if (!newNode) {
        printf("Memory allocation failed!\n");
        exit(1);
    }
    strcpy(newNode->program, program);
    newNode->next = NULL;

    if (q->rear == NULL) {
        q->front = q->rear = newNode;
    } else {
        q->rear->next = newNode;
        q->rear = newNode;
    }
}

// Function to dequeue a program (returns dynamically allocated string)
char* dequeue(Queue* q) {
    if (q->front == NULL) return NULL; // Queue is empty

    Node* temp = q->front;
    char* program = (char*)malloc(strlen(temp->program) + 1);
    if (!program) {
        printf("Memory allocation failed for program!\n");
        exit(1);
    }
    strcpy(program, temp->program);

    q->front = q->front->next;
    if (q->front == NULL) q->rear = NULL;

    free(temp);
    return program;
}

// Function to execute programs concurrently in separate terminals
void executeQueue(Queue* q) {
    while (q->front != NULL) {
        char* program = dequeue(q);
        if (program) {
            printf("Starting execution in new terminal: %s\n", program);

            char command[300];
            snprintf(command, sizeof(command), "start cmd /k python \"%s\"", program); // Windows command

            int status = system(command);
            if (status != 0) {
                printf("ERROR: Failed to execute %s\n", program);
            } else {
                printf("Execution started in new terminal: %s\n", program);
            }

            free(program); // Free dynamically allocated memory
        }
    }
    printf("All programs started in separate terminals.\n");
}

int main() {
    Queue q;
    initializeQueue(&q);

    // Enqueue programs in the correct order    
    enqueue(&q, "D:\\Cybersecurity-Log-Analyser\\Generated-Logs\\auth.py");
    enqueue(&q, "D:\\Cybersecurity-Log-Analyser\\Generated-Logs\\network.py");
    enqueue(&q, "D:\\Cybersecurity-Log-Analyser\\Generated-Logs\\application.py");
    enqueue(&q, "D:\\Cybersecurity-Log-Analyser\\Generated-Logs\\firewall.py");
    enqueue(&q, "D:\\Cybersecurity-Log-Analyser\\src\\log_collector.py");
    enqueue(&q, "D:\\Cybersecurity-Log-Analyser\\src\\db_manager.py");
    enqueue(&q, "D:\\Cybersecurity-Log-Analyser\\src\\log_parser.py");
    enqueue(&q, "D:\\Cybersecurity-Log-Analyser\\src\\alert_system.py");
    enqueue(&q, "D:\\Cybersecurity-Log-Analyser\\src\\auto_block.py");
    enqueue(&q, "D:\\Cybersecurity-Log-Analyser\\src\\log_analyzer.py");
    enqueue(&q, "D:\\Cybersecurity-Log-Analyser\\src\\app.py");

    // Execute all enqueued programs in separate terminals
    executeQueue(&q);

    return 0;
}
