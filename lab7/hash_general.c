#define OPENSSL_SUPPRESS_DEPRECATED
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <openssl/sha.h>

#define ITERS 2000000

typedef struct {
    int idx;
    char** files;
    unsigned long* results;
} job_t;

unsigned long stretch_hash(const char* path) {
    FILE* f = fopen(path, "r");
    if (!f) { perror(path); return 0; }
    fseek(f, 0, SEEK_END);
    long sz = ftell(f);
    fseek(f, 0, SEEK_SET);
    unsigned char* buf = malloc(sz);
    fread(buf, 1, sz, f);
    fclose(f);

    unsigned char digest[32];
    SHA256_CTX ctx;
    SHA256_Init(&ctx);
    SHA256_Update(&ctx, buf, sz);
    SHA256_Final(digest, &ctx);
    free(buf);

    for (int i = 0; i < ITERS; i++) {
        SHA256_Init(&ctx);
        SHA256_Update(&ctx, digest, 32);
        SHA256_Final(digest, &ctx);
    }

    unsigned long sum = 0;
    for (int i = 0; i < 32; i++) sum += digest[i];
    return sum;
}

void* thread_routine(void* arg) {
    job_t* job = (job_t*)arg;
    job->results[job->idx] = stretch_hash(job->files[job->idx]);
    return NULL;
}

int main(int argc, char** argv) {
    if (argc < 3) {
        fprintf(stderr, "Usage: %s <num_threads> <file1> [file2 ...]\n", argv[0]);
        return 1;
    }

    int num_threads = atoi(argv[1]);
    int num_files = argc - 2;
    char** files = argv + 2;
    unsigned long* results = calloc(num_files, sizeof(unsigned long));
    pthread_t* threads = malloc(num_files * sizeof(pthread_t));
    job_t* jobs = calloc(num_files, sizeof(job_t));

    for (int i = 0; i < num_files; i++) {
        jobs[i].idx = i;
        jobs[i].files = files;
        jobs[i].results = results;
    }

    int next = 0;
    while (next < num_files) {
        int active = 0;
        for (int t = 0; t < num_threads && next < num_files; t++) {
            pthread_create(&threads[active++], NULL, thread_routine, &jobs[next]);
            next++;
        }
        for (int t = 0; t < active; t++)
            pthread_join(threads[t], NULL);
    }

    for (int i = 0; i < num_files; i++)
        printf("%s: %lx\n", files[i], results[i]);

    free(results);
    free(threads);
    free(jobs);
    return 0;
}
