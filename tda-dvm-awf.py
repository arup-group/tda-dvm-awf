import argparse
import glob
import json
import subprocess
import shutil
import os 
from pathlib import Path
from inspect import getsourcefile
from os.path import abspath
from sys import platform
import uuid

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
	# proc = subprocess.Popen(args=[exe, path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
	proc = subprocess.Popen(f"{exe} {path}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	outs, errs = proc.communicate()
	print(outs, errs)

	# python_unix 12 b'************************************************* OasysDVM version 2.************************************************* ... Checking security for ****' None

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
	args = parser.parse_args()
	return args

def findFiles(inputDir):
	dvi_filePath = glob.glob(f"{inputDir}/*.dvi")[0]
	csv_filePath = glob.glob(f"{inputDir}/*.csv")[0]
	DvmWindowsPath = glob.glob(f"{inputDir}/DvmWindows.exe")[0]
	DvmLinuxPath = glob.glob(f"{inputDir}/DvmLinux.exe")[0]
	return dvi_filePath, csv_filePath, DvmWindowsPath, DvmLinuxPath

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
	# subprocess.run(['cp', file_path, directory_path])

def main():
	args = getArgs()
	
	working_directory = Path(args.inputDir)
	
	dvi_filePath, csv_filePath, DvmWindowsPath, DvmLinuxPath = findFiles(working_directory)
	# copy the files into path (this is redundant nescessary)
	# for example r'0deg\21Mps\'
	
	# check OS
	# return the path of dvm exe on the target project directory
	if platform == "win32":
		dvm_exe = DvmWindowsPath
	elif platform == "linux" or platform == "linux2":
	  	dvm_exe = DvmLinuxPath
	else:
		print('OS not surported')
		return

	temp_dvi_directory = os.path.join(working_directory, args.dvi_path)
	
	copy_file_to_directory(dvi_filePath, temp_dvi_directory)
	copy_file_to_directory(csv_filePath, temp_dvi_directory)
	
	
	# dvm_exe = 'OasysDVM_linux_LMXPrimer.exe'
	
	# curr_dir_path = os.path.dirname(abspath(getsourcefile(lambda:0)))
	
	# print('current files directory ', curr_dir_path)
	# current files directory  C:\Users\yun.sung\awf-1\awf_worker\runs\tda-dvm-awf-1.0.3

	# dvm_path = os.path.join(curr_dir_path, dvm_exe)
	
	# copy dvm into path
	# copy_file_to_directory(dvm_path, working_directory)
	# copy_file_to_directory C:\Users\yun.sung\awf-1\awf_worker\runs\tda-dvm-awf-1.0.3\requirements.txt C:\Users\yun.sung\awf-1\awf_worker\dumps/run_5860/input

	dvi_file_name = os.path.basename(dvi_filePath)
	dvi_file_partial_path = os.path.join(args.dvi_path, dvi_file_name)
	# -10deg\10Mps\C9_-10deg_10Mps.dvi
	
	# check permission to execute from directory
	print('working_directory', os.access(working_directory, os.X_OK))
	print('dvi_file_partial_path', os.access(dvi_file_partial_path, os.X_OK))

	print('dvm_exe', dvm_exe, 'dvi_file_partial_path', dvi_file_partial_path, 'working_directory', working_directory)
	
	# run dvm
	run_cli(dvm_exe, os.path.join(working_directory, dvi_file_partial_path), working_directory)
	
	# temp_dvm_path = os.path.join(working_directory, dvm_exe)
	
	results1 = findFilesWithExt(working_directory, 'dvp')
	results2 = findFilesWithExt(working_directory, 'log')
	results3 = findFilesWithExt(working_directory, 'csv')
	results4 = findFilesWithExt(working_directory, 'ptf')

	results_all = results1 + results2 + results3 + results4

	# writeFile(args, data)
	for result_file in results_all:
		copy_file_to_directory(result_file, args.outputDir)

	# delete the working_directory
	# shutil.rmtree(working_directory)

	# # zip directory and return string
	# archive_filename = str(uuid.uuid4())
	# archive_res = shutil.make_archive(archive_filename, 'zip', args.outputDir)
	
	# print(archive_res)

	# # zip file to byte
	# with open(archive_res, 'rb') as file_data:
    # 	bytes_content = file_data.read()

	# print(bytes_content)

if __name__ == "__main__":
	main()	
