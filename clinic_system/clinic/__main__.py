import os
import sys
sys.path.insert(0, 'C:/Users/Commander-Rex/Documents/Seng/group069/a5')
from clinic.cli.clinic_cli import ClinicCLI
import clinic.gui.clinic_gui

def main():
	# You can run either a command-line interface (CLI) 
	# or a graphical user interface (GUI) to your clinic.
	if len(sys.argv) != 2:
		print('ERROR: wrong number of arguments')
		print('\nCorrect Command usage:')
		print('python -m clinic option')
		print('where option is either cli or gui')
		sys.exit()

	if sys.argv[1] == 'cli':
		ClinicCLI()
	elif sys.argv[1] == 'gui':
		clinic.gui.clinic_gui.main()
	else:
		print('ERROR: Wrong argument')
		print('\nCorrect Command usage:')
		print('python -m clinic option')
		print('where option is either cli or gui')


if __name__ == '__main__':
	main()
