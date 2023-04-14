import argparse
import glob
import json
import subprocess
import shutil
import os 
from pathlib import Path
from inspect import getsourcefile
from os.path import abspath
import platform
import uuid
import sys

def invoke_at(path: str):
    def parameterized(func):
        def wrapper(*args, **kwargs):
            cwd = os.getcwd()
            os.chdir(path)
            try:
                ret = func(*args, **kwargs)
            finally:
                os.chdir(cwd)
            return ret
        return wrapper
    return parameterized 

def run_cli(exe, path, cwd):
	print(f"starting {path}")
	# subprocess.run([exe, path], cwd=cwd) # slow 
	cwd_original = os.getcwd()
	os.chdir(cwd) # change to working directory. required for result files to go to correct location.
	os.chmod(cwd, 0o777) # give permission to worker to execute
	os.chmod(exe, 0o777) # give permission to worker to execute
	# os.chmod("arup.lic", 0o777) # give permission to worker to execute
	proc = subprocess.Popen(args=[exe, path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
	outs, errs = proc.communicate()
	print(outs, errs)
	os.chdir(cwd_original)

def run_cli_alt(exe, path, cwd):
	print(f"starting {path}")
	@invoke_at(cwd) # decorator to get worker to execute in a correct directory
	def run_cli_dir(exe, path, cwd):
		# proc = subprocess.Popen(args=[exe, path], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
		proc = subprocess.Popen(args=[exe, path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
		outs, errs = proc.communicate()
		print(outs, errs)
	run_cli_dir(exe, path, cwd)
	
def getArgs():
	parser = argparse.ArgumentParser(description='AWF workflow for TDA/DVM.')
	parser.add_argument("-i", "--inputDir", help="path to input directory")
	parser.add_argument("-p", "--dvi_path", help="path to dvi file")
	parser.add_argument("-o", "--outputDir", help="path to output directory")
	parser.add_argument("-m", "--modelDir", help="path to model directory")
	args = parser.parse_args()
	return args

def findFiles(inputDir, inputKey):
	return glob.glob(f"{inputDir}/{inputKey}")
	
def findFilesWithExt(inputDir, ext):
	return glob.glob(f"{inputDir}/*.{ext}")

def writeFile(args, data):
	with open(f"{args.outputDir}/output.txt", "w") as f: 
		f.write(data) 

def copy_file_to_directory(file_path, directory_path):
	print('copy_file_to_directory', file_path, directory_path)
	if not os.path.exists(directory_path):
		Path(directory_path).mkdir(parents=True, exist_ok=True)
	shutil.copy(file_path, directory_path)

def main():
	args = getArgs()
	
	working_directory = Path(args.inputDir)
	# model_directory = Path(args.modelDir)  # $MODEL-DIR$
	dvi_path = args.dvi_path.lstrip('/')

	print("working_directory", working_directory)
	# print("model_directory", model_directory)

	dvi_filePath = findFilesWithExt(working_directory, "dvi")[0]
	csv_filePath = findFilesWithExt(working_directory, "csv")[0]

	# check OS
	# return the path of dvm exe on the target project directory
	if platform.system() == "Windows" or platform.system() == "win32":
		dvm_exe = os.path.join(working_directory, "DvmWindows.exe")
	elif platform.system() == "Linux" or platform.system() == "linux2":
		dvm_exe = os.path.join(working_directory, "DvmLinux.exe")
	else:
		print('OS not surported')
		return

	temp_dvi_directory = os.path.join(working_directory, dvi_path)
	
	copy_file_to_directory(dvi_filePath, temp_dvi_directory)
	copy_file_to_directory(csv_filePath, temp_dvi_directory)
	
	temp_dvm_exe = os.path.join(working_directory, os.path.basename(dvm_exe))
	
	dvi_file_name = os.path.basename(dvi_filePath)
	dvi_file_partial_path = os.path.join(dvi_path, dvi_file_name)
	
	# check permission to execute from directory
	print('working_directory', os.access(working_directory, os.X_OK))
	print('dvi_file_partial_path', os.access(dvi_file_partial_path, os.X_OK))

	print('dvm_exe', temp_dvm_exe, 'dvi_file_partial_path', dvi_file_partial_path, 'working_directory', working_directory)
	
	# run dvm
	run_cli(temp_dvm_exe, os.path.join(working_directory, dvi_file_partial_path), working_directory)
		
	results1 = findFilesWithExt(working_directory, 'dvp')
	results2 = findFilesWithExt(working_directory, 'log')
	results3 = findFilesWithExt(working_directory, 'csv')
	results4 = findFilesWithExt(working_directory, 'ptf')

	results_all = results1 + results2 + results3 + results4

	for result_file in results_all:
		copy_file_to_directory(result_file, args.outputDir)

if __name__ == "__main__":
	main()	
