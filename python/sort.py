#!/usr/bin/env python3

import sys

def sort(array):

	unsorted = array[:]
	sorted_array = []

	for x in array:
		biggest = -1

		for index, element in enumerate(unsorted):
			if element > biggest:
				biggest = element
				biggest_index = index

		sorted_array.insert(0, biggest)
		unsorted[biggest_index] = -1

	return sorted_array

if __name__ == "__main__":
	print(sort([ int(x) for x in sys.argv[1:]]))
