# coding=utf-8
import sys
import os
import re
from pypinyin import lazy_pinyin

# store differnet types of BibTex files' attributes
# some unusual type is left blank
attrs = dict()
attrs['article'] = ['title', 'author', 'journal', 'volume', 
		'number', 'pages', 'year', 
		'month', 'keywords']
attrs['book'] = ['title', 'publisher', 'year', 'author', 
		'editor', 'volume', 'number', 'series', 
		'address', 'edition', 'month', 'keywords']
attrs['booklet'] = ['title', 'author', 'howpublished', 
			'address', 'month', 
			'year', 'keywords']
attrs['commented'] = ['author', 'title', 'publisher', 
			'year', 'volumetitle', 
			'editor', 'keywords']
attrs['conference'] = ['author', 'title', 'booktitle', 
			'year', 'editor', 'volume', 
			'pages', 'number', 'organization', 
			'series', 'publisher', 'address', 
			'month', 'keywords']
attrs['glossdef'] = []
attrs['inbook'] = []
attrs['incollection'] = []
attrs['inproceedings'] = []
attrs['jurthesis'] = []
attrs['manual'] = []
attrs['mastersthesis'] = ['author', 'title', 'school', 
			'year', 'address', 'month', 
			'type', 'keywords']
attrs['misc'] = []
attrs['periodical'] = []
attrs['phdthesis'] = ['author', 'title', 'school', 'year', 
			'address', 'month', 'type', 'keywords']
attrs['proceedings'] = []
attrs['techreport'] = ['author', 'title', 'institution', 'year', 
			'type', 'number', 'address', 'month'
			'keywords']
attrs['unpublished'] = []
attrs['url'] = []
attrs['electronic'] = []
attrs['webpage'] = []

# there some special characters which need to be removed
spec_chars = ['']

# get the height and width of terminal for later display
rows, cols = os.popen('stty size', 'r').read().split()
rows = int(rows)
cols = int(cols)

# print ATTENTION
print('=' * cols)
print('ATTENTION: This script will process ' +  
	'all the .bib files which include Chinese ' +
	'under the target folder.')

print('=' * cols)
# get Python version
if sys.version_info[0] < 3:
	py_ver = 2
	# use raw_input() in Python versions 2.x
	# to get the target directory
	top = raw_input('input the path of target folder:')
else:
	# use input() in Python versions 3.x
	# to get the target directory
	py_ver = 3
	top = input('input the path of target folder:')

# record the number of processed files
file_num = 0

# Traverse the target directory
for parent, dirnames, filenames in os.walk(top):

	# Traverse all files
	for filename in filenames:

		# only process txt file
		if re.search('.txt', filename) == None:
			continue

		# print the log
		print('Start to process ' + filename)

		# open each file to check whether it fit 
		# the requirement of processing
		with open(os.path.join(parent, filename), 'r') as f:

			# read all content of file
			con = str(f.read())

			# check if the file includes Chinese character
			if re.search(r'[\u4e00-\u9fa5]+', con) == None:
				# if it does not, exit this turn of loop
				continue

			# get the type of BibTex file
			if re.search('@article', con):
				bib_type = 'article'
			elif re.search('@book', con):
				bib_type = 'book'
			elif re.search('@conference', con):
				bib_type = 'conference'
			elif re.search('@mastersthesis', con):
				bib_type = 'mastersthesis'
			elif re.search('@phdthesis', con):
				bib_type = 'phdthesis'
			elif re.search('@techreport', con):
				bib_type = 'techreport'

			f.close()
		
		# reopen the file to extract attritube values
		with open(os.path.join(parent, filename), 'r') as f:

			# store attritube values in dictionary info
			info = dict()

			# read file line by line
			for line in f.readlines():

				# find string between '{' and '}'
				value = re.findall(r'[{](.*?)[}]', line)
				value = ''.join(value)

				# need to transform value to unicode 
				# in Python versions 2.x
				if py_ver == 2:
					value = unicode(value, 'utf-8')

				# remove the space in value
				value = value.replace(' ', '')

				# traverse all attributes of this 
				# type of BibTex file
				for attr in attrs[bib_type]:

					# search matched attribute
					if re.search(attr, line):

						# remove special characters
						for char in spec_chars:
							value = value.replace(char, '')

						# do additional process to  the 
						# value of 'author' attribute
						if attr == 'author':
							value = value.replace('and', u'，')

						# if a chinese title contains capitalized english letters
						# that are not at the beginning of title
						# they will be lowercase english letters
						# use the '{' and '}' to protect them
						if attr == 'title':
							
							# count the number of '{' and '}'
							left_num = len(re.findall('{', value))
							right_num = len(re.findall('}', value))

							# title has not been added '{' and '}'
							if left_num == 0 and right_num == 0:
								value = '{' + value + '}'
							# title has been added '{' and '}'
							elif left_num == 1 and right_num == 1:
								# do nothing
								pass
							# there are too many '{' and '}'
							else:
								# clear all '{' and '}'
								value = value.replace('{', '')
								value = value.replace('}', '')
								# add a pair of '{' and '}'
								value = '{' + value + '}'

						# push the value of attribute into dictionary
						info[attr] = value

			# get first author
			author_1st = info['author'].split(u'，')[0]

			# transfrom it into pinyin without tone
			author_1st = lazy_pinyin(author_1st)
			author_1st = ''.join(author_1st)

			# link the pinyin of first author and year with ':'
			# use it as cite key
			info['cite_key'] = author_1st + ":" + info['year']

			if bib_type == 'mastersthesis':
				info['type'] = u'硕士论文'
			elif bib_type == 'phdthesis':
				info['type'] = u'博士论文'

			f.close()

		# write into the file
		# with the mode 'w', clear old content then write new content
		with open(os.path.join(parent, filename), 'w') as f:
			
			# first line is about type of BibTex and cite key
			f.write('@' + bib_type + '{' + info['cite_key'] + ',\n')

			# write all attritubes that has value
			# in the form of 'attribute={value},'
			for attr in attrs[bib_type]:
				if attr in info:
 					f.write(attr + '={' + info[attr] + '},\n')

			f.write('}\n')
			
			f.close()
		
		# print the log
		print(filename + ' processing completed.')

		file_num += 1

print('=' * cols)
print('Process ' + str(file_num) +' files.')
print('=' * cols)
