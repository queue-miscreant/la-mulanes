from PIL.BmpImagePlugin import BmpImageFile


def render(b):
	'''
	Convert an assembler macro line to the corresponding bitmap (as a 2
	dimensional array)

	@param b A line of assembly like .byte $00,$FF...(14 more values)[; comment]
	@return 2 dimensional array with entries 0-3
	'''
	if b.find(".byte "):
		return
	c = b[6:].split(',')
	#cutoff the trailing comment
	cutoff = c[-1].find(';')
	if -1 != cutoff:
		c[-1] = c[-1][:cutoff]
	ret = [[0 for i in range(8)] for i in range(8)]
	for i,j in enumerate(c):
		num = int(j[1:],16)
		upper = (i >= 8)
		for k in range(8):
			ret[i % 8][7-k] |= (num&1) << (upper)
			num >>= 1
	return ret


def unrender(bmp):
	'''
	Converts an 8x8 bitmap into the corresponding line of assembly

	@param bmp A 2 dimensional array with entries 0-3
	@return A line of NES 6502 assembly to generate the bitmap in CHR-ROM
	'''
	ret = [0 for i in range(16)]
	for i,j in enumerate(bmp):
		#j is a list of 0,1,2,3
		for k in range(8):
			val = j[k]&3
			ret[i] |= (val&1)<<(7-k)
			ret[i+8] |= (val>>1)<<(7-k)
	return ".byte " + ','.join(["$%02x"%i for i in ret])

def colorize(a):
	'''
	Prints a colorized terminal version of a rendering (output from `render`)

	@param a The output from `render`, a 2 dimensional array corresponding to
			 a bitmap, or the output from `unrender`
	'''
	if isinstance(a,str):
		a = render(a)
	for i in a:
		ret = ""
		for j in i:
			if j != 0:
				ret += f"\x1b[3{j}m \x1b[39m"
			else:
				ret += '.'
		print('\x1b[7m',ret,end="\x1b[m\n",sep="")

def getbytes(filename):
	'''
	Very simple BMP-to-assembly converter. New colors are added to `colordata`,
	which determines which of 0-3 are mapped. Beware if using a complex image.

	@param filename The filename of the BMP file to parse
	@param off An offset to start the numbering from. All integers valid, but %3
	@return A two dimensional array of the return value of `unrender`, organized
			(y,x) in 8 bit chunks
	'''
	with open(filename,"rb") as a:
		image = BmpImageFile(a)
		ret = [[] for i in range(image.height//8)]
		x = 0
		y = 0

		number = 0
		offset = 0

		colordata = []
		while True:
			sprite = [[0 for i in range(8)] for i in range(8)]
			for w in range(8):
				for h in range(8):
					pix = image.getpixel((x*8+w,y*8+h))
					if pix not in colordata:
						colordata.append(pix)
					color = colordata.index(pix)
					if color:
						sprite[h][w] = ((color-1)%3)+1
					else:
						sprite[h][w] = 0
			ret[y].append(unrender(sprite))
			x += 1
			if x*8 >= image.width:
				y += 1
				if y*8 >= image.height:
					return ret
				x = 0
