import argparse
import glob
import json

def getArgs():
	parser = argparse.ArgumentParser(description='AWF workflow for TDA/DVM.')
	parser.add_argument("-i", "--inputDir",
						help="path to input directory")
	parser.add_argument("-o", "--outputDir",
						help="path to output directory")
	args = parser.parse_args()
	return args

def readFile(args):
	dvi_filePath = glob.glob(f"{args.inputDir}/*.dvi")[0]
	csv_filePath = glob.glob(f"{args.inputDir}/*.csv")[0]
	return [dvi_filePath, csv_filePath]

def dvm_exec(data):
	res = json.dumps(data)
	return res

def writeFile(args, data):
	with open(f"{args.outputDir}/output.txt", "w") as f: 
		f.write(data) 

def main():
	args = getArgs()
	
	data = readFile(args)
	data = dvm_exec(data)
	writeFile(args, data)
	

if __name__ == "__main__":
	main()	