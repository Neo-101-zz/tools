import exifread
import os
import datetime

jpg_paths = []
 
for filename in os.listdir():
	if filename.endswith('.jpg'):
		jpg_paths.append(filename)

print("jpg_paths: " + str(jpg_paths))

for jpg in jpg_paths:
	print("jpg_name: " + jpg)
	with open(jpg, 'rb') as jpg_img:
		exif = exifread.process_file(jpg_img)
		dt = str(exif.get('EXIF DateTimeOriginal'))
		if dt == 'None':
			continue
		# segment string dt into date and time
		day, dtime = dt.split(" ", 1)
		year, month, day = day.split(":")
		# segment time into hour, minute, second
		hour, minute, second = dtime.split(":", 2)
		# MACOS BASH 
		date_name = year + month + day + '-'\
			+ hour + minute + second + ".jpg";
		cmd = "mv " + jpg + " " + date_name
		os.system(cmd)
