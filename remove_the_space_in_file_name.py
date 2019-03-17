import os

rows, cols = os.popen('stty size', 'r').read().split()
rows = int(rows)
cols = int(cols)

print('=' * cols)
print('ATTENTION: This script will remove ' +  
	'the space in ALL files\' name under' + 
	'the target folder.')
print('=' * cols)
# use raw_input in Python versions 2.x
top = raw_input('input the path of target folder:')

for parent, dirnames, filenames in os.walk(top):
	for filename in filenames:
		os.rename(os.path.join(parent, filename), 
			os.path.join(parent, filename.replace(' ','')))

print('=' * cols)
print('Process complete')
print('=' * cols)
