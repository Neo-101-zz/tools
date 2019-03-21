import convertapi

path_txt = r'TEMP.txt'
path_pdf = input('Input the path of pdf file:') 
convertapi.api_secret = 'JvAUsZV9gfILDwQ7'
result = convertapi.convert(
	'txt', 
	{ 'File': path_pdf }, 
	from_format = 'pdf'
	)

result.save_files(path_txt)
