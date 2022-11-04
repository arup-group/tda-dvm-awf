import argparse
import glob
import json
import subprocess
import shutil

def run_cli(exe, path):
    print(f"starting {path}")
    try:
        subprocess.run([exe, path])
        print(f"succeed {path}")
    except: 
        print(f"failed {path}")
        return

def getArgs():
	parser = argparse.ArgumentParser(description='AWF workflow for TDA/DVM.')
	parser.add_argument("-i", "--inputDir", help="path to input directory")
	parser.add_argument("-p", "--dvi_path", help="path to dvi file")
	parser.add_argument("-o", "--outputDir", help="path to output directory")
	args = parser.parse_args()
	return args

def findFiles(inputDir):
	dvi_filePath = glob.glob(f"{inputDir}/*.dvi")[0]
	csv_filePath = glob.glob(f"{inputDir}/*.csv")[0]
	return dvi_filePath, csv_filePath

def dvm_exec(data):
	res = json.dumps(data)
	return res

def writeFile(args, data):
	with open(f"{args.outputDir}/output.txt", "w") as f: 
		f.write(data) 

def copy_file_to_directory(file_path, directory_path):
	shutil.copy(file_path, directory_path)

def main():
	args = getArgs()
	
	dvi_filePath, csv_filePath = findFiles(args.inputDir)
	# copy the files into path (this is redundant nescessary)
	# for example r'0deg\21Mps\'
	
	temp_dvi_path = os.path.join(args.inputDir, args.dvi_path)
	temp_csv_path = os.path.join(args.inputDir, args.dvi_path)

	copy_file_to_directory(dvi_filePath, temp_dvi_path)
	copy_file_to_directory(csv_filePath, temp_csv_path)
	
	dvm_exe = 'OasysDVM.exe'

	# copy dvm into path
	copy_file_to_directory(os.path.join('.', dvm_exe), args.dvi_path)
	
	temp_dvm_path = os.path.join(args.dvi_path, dvm_exe)

	# run dvm
	run_cli(temp_dvm_path, temp_dvi_path)

	# delete dvm from path
	os.remove(temp_dvm_path)

	# writeFile(args, data)
	

if __name__ == "__main__":
	main()	
