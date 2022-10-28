import argparse
import glob

def getArgs():
	parser = argparse.ArgumentParser(description='AWF workflow for TDA/DVM.')
	parser.add_argument("-i", "--inputDir",
						help="path to input directory")
	parser.add_argument("-o", "--outputDir",
						help="path to output directory")
	args = parser.parse_args()
	return args

def readFile(args):
	filePath = glob.glob(f"{args.inputDir}/*.txt")[0]
	with open(filePath) as f: 
		data = f.read()
	return data

def reverseString(data):
	return data[::-1]

def writeFile(args, data):
	with open(f"{args.outputDir}/output.txt", "w") as f: 
		f.write(data) 

def main():
	args = getArgs()
	# data = readFile(args)
	# data = reverseString(data)
	# writeFile(args, data)
	

if __name__ == "__main__":
	main()	