#!/usr/bin/env python3

import sys

def recursive_fib(n):
	if n == 1:
		return 1
	elif n == 0:
		return 0
	else:
		return recursive_fib(n-1) + recursive_fib(n-2)

if __name__ == "__main__":
	print(recursive_fib(int(sys.argv[1])))
