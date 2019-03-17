import convertapi

path_pdf = input("Enter the path of PDF file: ")

dirs = path_pdf.split("\\")
name_pdf = dirs[len(dirs)-1]
dir_doc = path_pdf.replace(name_pdf, "")
name_doc = name_pdf.replace(".pdf", ".doc")
path_doc = dir_doc + name_doc

convertapi.api_secret = 'JvAUsZV9gfILDwQ7'
result = convertapi.convert(
	'doc', 
	{ 'File': path_pdf }, 
	from_format = 'pdf'
	)

result.save_files(path_doc)

print("Converting finishes.")

quit = input("Press Enter to exit: ")