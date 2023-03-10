import argparse
import glob
import os

def getArgs():
	parser = argparse.ArgumentParser(description='Tutorial workflow for AWF.')
	parser.add_argument("-i", "--inputFile",
						help="path to input directory")
	parser.add_argument("-o", "--outputDir",
						help="path to output directory")
	args = parser.parse_args()
	return args

def readFile(args):
	filename = os.listdir(glob.glob(f"{args.inputFile}")[0])[0]
	with open(args.inputFile+f"/{filename}") as f:
		data = f.read()
	return data

def reverseString(data):
	return data[::-1]

def writeFile(args, data):
	with open(f"{args.outputDir}/output.txt", "w") as f: 
		f.write(data) 

def main():
	args = getArgs()
	data = readFile(args)
	data = reverseString(data)
	writeFile(args, data)

if __name__ == "__main__":
	main()	