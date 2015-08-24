#!/usr/bin/env python3

import sys

def is_sorted(array):
	for x in range(len(array)-1):
		if array[x] > array[x+1]:
			return False
	return True

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


def bubblesort(old_array):

	array = old_array[:]

	while not is_sorted(array):

		for x in range(len(array)-1):
			if array[x] > array[x+1]:
				array[x], array[x+1] = array[x+1], array[x]
	return array


def asort(array):

	if len(array) == 1:
		return array
	elif len(array) == 0:
		return []

	middle = (max(array) + min(array)) // 2
	lower = []
	higher = []
	for element in array:
		if element > middle:
			higher.append(element)
		else:
			lower.append(element)
	return asort(lower) + asort(higher)



if __name__ == "__main__":
	print(asort([ int(x) for x in sys.argv[1:]]))
