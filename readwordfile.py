import docx
doc = docx.Document('mywordfile.docx')
for i in doc.paragraphs:
    print('paragraph:',end='')
    print(i.text)