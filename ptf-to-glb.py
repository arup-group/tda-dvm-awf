
# https://www.oasys-software.com/dyna/wp-content/uploads/2022/12/D3PLOT_Viewer_Documentation.pdf
# d3plot18_x64.exe -glb=D3PLOT.glb -states=even -frame_rate=5 d3plot/results.ptf


def run_cli(args, cwd):
	cwd_original = os.getcwd()
	os.chdir(cwd)
	
    # By default, subprocess.Popen commands are supplied as a list of strings.
    # However, you can also you can use the shell argument to execute a command "formatted exactly as it would be when typed at the shell prompt."

    proc = subprocess.Popen(args=args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
	outs, errs = proc.communicate()
	print(outs, errs)
	os.chdir(cwd_original)


def main():
	args = getArgs()
	
	working_directory = Path(args.inputDir)
    
    args = ['d3plot18_x64.exe', '-glb=D3PLOT.glb', '-states=even', '-frame_rate=5', 'input.ptf']

    # run dvm
	run_cli(args, working_directory)



if __name__ == "__main__":
	main()	