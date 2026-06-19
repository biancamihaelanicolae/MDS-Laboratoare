# Lab 7 - Threads

.PHONY: all sleep sleep_ex race race_fixed hash hash_general clean

all: sleep race race_fixed

# Basic sleep example
sleep:
	gcc -pthread sleep.c -o sleep && ./sleep

# Race condition
race:
	gcc -pthread race.c -o race

race_fixed:
	gcc -std=c11 -pthread race_fixed.c -o race_fixed

# Test race vs fixed
test_race:
	bash test_race.sh

# Hash exercises (need libssl-dev)
hash:
	gcc -pthread hash.c -o hash1 -lcrypto
	gcc -pthread hash.c -o hash4 -lcrypto -DMULTI

hash_general:
	gcc -pthread hash_general.c -o hash_general -lcrypto

# Benchmark with hyperfine
bench: hash
	hyperfine --warmup 2 ./hash1 ./hash4

# Run hash general with 4 threads on 4 files
run_hash_general: hash_general
	./hash_general 4 a.html b.html c.html d.html

clean:
	rm -f sleep race race_fixed hash1 hash4 hash_general
