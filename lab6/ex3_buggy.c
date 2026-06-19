/*
 * 3 memory bugs:
 *   1. malloc(strlen(name)) -> missing +1 for null terminator
 *   2. i <= s->count -> off-by-one, should be i < s->count
 *   3. free_student missing free(s->grades)
 * Compile: gcc -g -o ex3_buggy ex3_buggy.c
 * Check: valgrind --leak-check=full ./ex3_buggy
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char* name;
    int*  grades;
    int   count;
} Student;

Student* new_student(const char* name, int grades[], int n) {
    Student* s = malloc(sizeof(Student));
    s->name = malloc(strlen(name));  // BUG 1: missing +1 for '\0'
    strcpy(s->name, name);
    s->grades = malloc(n * sizeof(int));
    memcpy(s->grades, grades, n * sizeof(int));
    s->count = n;
    return s;
}

float average(Student* s) {
    int sum = 0;
    for (int i = 0; i <= s->count; i++) {  // BUG 2: <= should be <
        sum += s->grades[i];
    }
    return (float)sum / s->count;
}

void free_student(Student* s) {
    free(s->name);
    // BUG 3: missing free(s->grades)
    free(s);
}

int main() {
    int grades[] = {85, 90, 78, 92};
    Student* alice = new_student("Alice", grades, 4);
    printf("%s: avg = %.1f\n", alice->name, average(alice));
    free_student(alice);
    return 0;
}
