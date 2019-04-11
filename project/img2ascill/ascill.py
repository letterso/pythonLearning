#!/usr/bin/env python
#coding=utf-8

from PIL import Image
import argparse

# order input
parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('-o','--output')
parser.add_argument('--width',type=int,default=80)
parser.add_argument('--height',type=int,default=80)
args = parser.parse_args()

IMG = args.file
OUTPUT = args.output
WIDTH = args.width
HEIGHT = args.height

# change pixel in ascill
ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
uint = (256.0+1)/len(ascii_char)

def get_char(r,g,b,alpha=256):
	if alpha==0:
		return ' '
	gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
	return ascii_char[int(gray/uint)]
	
# main
if __name__ == '__main__':
	# read img
	img = Image.open(IMG)
	img = img.convert('RGBA')
	img = img.resize((WIDTH,HEIGHT),Image.NEAREST)
	
	# change in ascill
	txt = ""
	for i in range(HEIGHT):
		for j in range(WIDTH):
			txt += get_char(*img.getpixel((j,i)))
		txt +='\n'
		
	print(txt)
	
	# save txt
	if OUTPUT:
		with open(OUTPUT,'w') as f:
			f.write(txt)
	else:
		with open ('output.txt','w') as f:
			f.write(txt)
	

