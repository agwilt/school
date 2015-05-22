#!/usr/bin/env python3

import sys

def binary(in_list, value):
	if type(in_list) == int:
		if in_list[0] == value:
			return value
		else:
			return -1
	else:
		mid = in_list[len(in_list)//2]
		if mid == value:
			return value
		elif mid > value:
			binary(in_list[:mid], value)
		else:
			binary(in_list[mid:], value)

if __name__ == "__main__":
	print(binary([ int(x) for x in sys.argv[2:]], int(sys.argv[1])))
