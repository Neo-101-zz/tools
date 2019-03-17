# coding=utf-8
import sys
import os
import re
from pypinyin import lazy_pinyin

attrs = dict()
attrs['article'] = ['title', 'author', 'journal', 'volume', 
		'number', 'pages', 'year', 
		'month', 'keywords']

spec_chars = ['']

rows, cols = os.popen('stty size', 'r').read().split()
rows = int(rows)
cols = int(cols)

print('=' * cols)
print('ATTENTION: This script will process ' +  
	'all the .bib files which include Chinese ' +
	'under the target folder.')

print('=' * cols)
if sys.version_info[0] < 3:
	py_ver = 2
	# use raw_input in Python versions 2.x
	top = raw_input('input the path of target folder:')
else:
	py_ver = 3
	top = input('input the path of target folder:')

for parent, dirnames, filenames in os.walk(top):
	for filename in filenames:
		with open(os.path.join(parent, filename), 'r') as f:
			con = str(f.read())
			if re.search(r'[\u4e00-\u9fa5]+', con):
				print('found chinese character in ' + str(parent) + str(filename))
			if re.search('@article', con):
				bib_type = 'article'
			f.close()
		with open(os.path.join(parent, filename), 'r') as f:
			info = dict()
			for line in f.readlines():
				value = re.findall(r'[{](.*?)[}]', line)
				value = ''.join(value)
				if py_ver == 2:
					value = unicode(value, 'utf-8')
				value = value.replace(' ', '')
				for attr in attrs[bib_type]:
					if re.search(attr, line):
						for char in spec_chars:
							value = value.replace(char, '')
						if attr == 'author':
							value = value.replace('and', u'，')
						info[attr] = value
						print(value)
			print(info)
			author_1st = info['author'].split(u'，')[0]
			author_1st = lazy_pinyin(author_1st)
			author_1st = ''.join(author_1st)
			info['cite_key'] = author_1st + ":" + info['year']
			print(info['cite_key'])
			f.close()
		with open(os.path.join(parent, filename), 'w') as f:
			f.write('@' + bib_type + '{' + info['cite_key'] + ',\n')
			for attr in attrs[bib_type]:
				if attr in info:
 					f.write(attr + '={' + info[attr] + '},\n')
			f.write('}\n')
print('=' * cols)
print('Process complete')
print('=' * cols)
