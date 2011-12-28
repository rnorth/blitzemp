"""
print_table.py

Created by Richard North on 2011-12-28.
Copyright (c) 2011 Richard North.
"""

import sys
import os
from pprint import pprint
from numbers import Number

def print_table(data, underline_header=True, underline_character="-", column_separator="\t"):
	num_columns = 0
	column_widths = {}
	# Determine what the maximum column widths are by scanning down the table
	for row in data:
		num_columns = max(len(row), num_columns)
		for column_index in range(0,len(row)):
			column_value = row[column_index]
			if column_index in column_widths:
				new_max_for_column = max(column_widths[column_index], len(str(column_value)))
			else:
				new_max_for_column = len(str(column_value))
			column_widths[column_index] = new_max_for_column

	# Insert an 'underline' row if required
	if underline_header:
		underlines = []
		for column_index in range(0, num_columns):
			underlines.append(underline_character * column_widths[column_index])
		new_data = [data[0], underlines]
		new_data.extend(data[1:len(data)])
		data = new_data

	# Actually format and print each item in the table
	for row in data:
		formatted_row = []
		for column_index in range(0,len(row)):
			width = column_widths[column_index]
			value = row[column_index]
			if isinstance(value, Number):
				local_format = str.rjust
			else:
				local_format = str.ljust
			formatted_row.append(local_format(str(value), width))
		
		print column_separator.join(formatted_row)


if __name__ == '__main__':
	print_table((("A", "B", "quite long header C"), ("really very long value", 1, "abcdefg"), ("bar", 200000, "a")), underline_header=True)

	print_table((("A", "B", "quite long header C"), ("really very long value", 1, "abcdefg"), ("bar", 200000, "a")), underline_header=True, column_separator="|")

	print_table((("A", "B", "C"), ("42", 100, 200.9), ("bar", "s", 30000.5)), underline_header=True)
