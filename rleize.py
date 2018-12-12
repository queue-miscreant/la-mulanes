#!/usr/bin/env python

def oneline(filename, columns):
	ret = ""
	with open(filename) as a:
		while True: 
			b = a.readline()
			if not b:
				break
			for i, j in enumerate(b):
				if j == '\n':
					ret += ' ' * (columns - i)
				else:
					ret += j
	return ret


def rleize(string, maxcolumns, convert={}):
	ret = []
	last = string[0]
	length = 1
	generator = 0
	for i, j in enumerate(string):
		if generator:
			generator -= 1
			continue

		if convert.get(j):
			j = convert[j]

		if j == last:
			length += 1
			if length == maxcolumns:
				ret.append((j, length))
				length = 1
		else:
			if last.isdigit():
				ret.append((int(last), "gen"))
				length = 1
				last = j
				continue

			ret.append((last, length))
			length = 1
			last = j

		if j.isdigit():
			generator = 3

	ret.append((last, length))
	return ret

def byteize(rle, spritenums):
	ret = []
	for i,j in rle:
		if j == "gen":
			i = (i<<1) | 129
			ret.append("$%02X" % i)
			continue

		i = (spritenums[i]<<1)+1
		if j % 2:
			j -= 1
			if j:
				ret.append("$%02X" % j)
				ret.append("$%02X" % i)
			else:
				ret.append("$%02X" % i)
				continue
		else:
			ret.append("$%02X" % j)
		ret.append("$%02X" % i)
	return ret
defaults = {
	 ' ': 0		#nothing
	,'_': 1		#ground effect
	,'-': 2		#ground
	,'[': 3		#fake wall left
	,']': 4		#fake wall right
	,'<': 7		#ladder left
	,'>': 8		#ladder right
}

def main():
	import sys
	filename = sys.argv[1]

	run_lengths = rleize(oneline(filename, 32), 254, {'T': ' '})
	table_data = byteize(run_lengths, defaults)
	if len(table_data) > 256:
		print("TABLE DATA TOO LARGE: %d bytes" % table_data, file=sys.stderr)
		exit()
	print(".byte " + ','.join(table_data))

if __name__ == "__main__":
	main()
