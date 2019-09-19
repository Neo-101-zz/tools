import os

rows, cols = os.popen('stty size', 'r').read().split()
rows = int(rows)
cols = int(cols)

print('=' * cols)
print('ATTENTION: This script will remove ' +  
	'the space in ALL files\' name under' + 
	'the target folder.')
print('=' * cols)

# use input() in Python 3.x
top = input('input the path of target folder: ')
print('=' * cols)

# ATTENTION: 
# If directly copy directory's path by copy it in Finder in macOS, 
# the path may contain ESCAPE CHARACTERS, which cannot be recongized
# by Python program. 
# So it is necessary to convert the ESCAPE CHARACTERS to normal 
# characters. 

# For example, the target directoy's path copied from Finder is 
# '/Users/lujingze/Library/Mobile\ Documents/com\~apple\~CloudDocs/study/sea_wind_review '.
# However, the true path of directory is 
# '/Users/lujingze/Library/Mobile Documents/com~apple~CloudDocs/study/sea_wind_review'. 
# I didn't find function to convert the original path with escaped characters to
# true path without escaped characters.  
# There are two points need to be noticed:
# 1: '\ ' standing for ' ' and '\~' standing for '~'. 
# It seems that the '\' is useless and can be ignored.
# 2: There is a space in the end of path of directory copied from Finder, 
# and it needs to be removed.

# process the path if it is copied from Finder in macOS 
top = top.replace('\\', '')	# remove all backslash
top = top.strip()		# remove space in the end
if os.path.isdir(top) == False:
	print(top + ' does not exists')
	raise IOError

print('Choose mode: ')
print('1: simply remove all space')
print('2: replace space with underline')
mode = int(input('Enter mode number: '))

for parent, dirnames, filenames in os.walk(top):
	for filename in filenames:
		if mode == 1:
			new_char = ''
		elif mode == 2:
			new_char = '_'

		os.rename(os.path.join(parent, filename), 
			os.path.join(parent, filename.replace(' ', new_char)))


print('=' * cols)
print('Process complete')
print('=' * cols)
