import re
def filterfunction(string):
	text=re.sub("\d","",string)
	text2=re.sub("\(\)","",text)
	text3=re.sub("-","",text2).lstrip()
	c=re.findall(r'[a-zA-Z]',string)
	r=re.findall(r'\d',string)
	result=''.join(r)
	return result,text3