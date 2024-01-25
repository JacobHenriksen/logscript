# Logscript
# By Jacob Henriksen

# Used to parse through event logs exported from DNAC to count the number of unique devices using the 'count' argument
# and export a table with the affected devices using the 'export' argument.

import sys
import os.path


def findDevices(fileName):

    devices=[]
    try:
        with open(fileName, mode='r') as f:
            for line in f:
                if line.find('forestproducts.sca.com') == -1:               #Checking if the device has the older naming standard or not
                    indexEnd=line.find('sca.com')-1
                else:
                    indexEnd=line.find('forestproducts.sca.com')-1 
                indexStart=line[:indexEnd].rfind('"')+1
                device=line[indexStart:indexEnd]
                if device not in devices and line.find('sca.com')!=-1:
                    devices.append(device)
    except FileNotFoundError:
        print(f'Logfile {fileName} not found.')
        return 
    else: 
        return devices


def count(fileName):

    try:
        deviceCount = len(findDevices(fileName))
    except:
        return
    else:
        print(f'\nNumber of unique devices in \'{fileName}\':')
        print(f'{deviceCount}\n')
        return


def export(fileName):

    file_extension_index=fileName.find('.csv')
    outputFileName=fileName[:file_extension_index]+'_logscript_export.csv'

    if os.path.isfile(f'./{outputFileName}') is True:
        raise TypeError(f'\nFile \'{outputFileName}\' already exists.')
        return
    if os.path.isfile(f'./{fileName}') is False:
        raise TypeError(f'\nFile \'{fileName}\' does not exist.')
        return

    try:
        print(f'\nCreating list with unique devices for \'{fileName}\'.')
        file1 = open(outputFileName, mode='a')

        for n in findDevices(fileName):
            file1.write(f'{n}\n')  
              
        file1.close()
    except:
        return
    else:
        print(f'\'{outputFileName}\' created successfully.\n')


def availArgs():
	print('Valid arguments:')
	print('count\t- Print unique device count.')
	print('export\t- Export a list in .csv-format from the provided logfile with the unique device names.')


if __name__ == "__main__":
	if len(sys.argv) == 1:
		print('Missing valid logfile.')
	else:
		fileName = sys.argv[1]
		if len(sys.argv) == 2:
			print('Missing argument.')
			availArgs()
		elif len(sys.argv) == 3:
			argument = sys.argv[2]
			if argument == 'count':
				count(fileName)
			elif argument == 'export':
				export(fileName)
			else:
				print('\nInvalid argument.\n')
				availArgs()
		else:
			print('\nInvalid input.')
