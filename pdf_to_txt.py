import convertapi

path_txt = r".\TEMP.txt"
path_pdf = r".\Elawady_Wavelet-Based_Reflection_Symmetry_ICCV_2017_paper.pdf"

convertapi.api_secret = 'JvAUsZV9gfILDwQ7'
result = convertapi.convert(
	'txt', 
	{ 'File': path_pdf }, 
	from_format = 'pdf'
	)

result.save_files(path_txt)