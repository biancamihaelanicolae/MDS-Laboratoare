# Lab 6 - Debugging, Sanitizers, Valgrind, Profiling, Template Errors
#
# Exercises:
#   1. pdb debugger - Python arithmetic parser
#   2. AddressSanitizer - C vector / C++ dependency resolver
#   3. Valgrind - 3 memory bugs in C
#   4. perf profiling - word frequency counter
#   5. C++ template error comprehension

.PHONY: all ex1 ex2 ex2b ex3 ex4 ex5 clean

all: ex1 ex2 ex2b ex4 ex5

# Exercise 1: Python debugger
ex1:
	python3 ex1.py

# Exercise 2a: C vector - AddressSanitizer
ex2:
	gcc -fsanitize=address -g -o ex2_buggy ex2_buggy.c && ./ex2_buggy || true
	@echo "--- Fixed version ---"
	gcc -g -o ex2_fixed ex2.c && ./ex2_fixed

# Exercise 2b: C++ deps - AddressSanitizer
ex2b:
	g++ -std=c++17 -fsanitize=address -o ex2b_buggy ex2b_buggy.cpp && ./ex2b_buggy || true

# Exercise 3: Valgrind
ex3:
	gcc -g -o ex3_buggy ex3_buggy.c
	valgrind --leak-check=full ./ex3_buggy

# Exercise 4: Perf profiling
ex4:
	g++ -std=c++17 -g -O2 -o ex4 ex4.cpp
	perf record -g ./ex4
	perf script report flamegraph
	@echo "Open flamegraph.html in browser"

# Exercise 5: C++ template error
ex5:
	-@echo "=== Buggy version (expected compile error) ==="
	-g++ -std=c++17 -o ex5_buggy ex5_buggy.cpp 2>&1 | head -20 || true
	@echo ""
	@echo "=== Fixed version ==="
	g++ -std=c++17 -o ex5 ex5.cpp && ./ex5

clean:
	rm -f ex2_buggy ex2_fixed ex2b_buggy ex3_buggy ex4 ex5 ex5_buggy perf.data perf.data.old flamegraph.html
