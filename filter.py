import re
def filterfunction(string):
	text=re.sub("\d","",string)
	text2=re.sub("\(\)","",text)
	text3=re.sub("-","",text2).lstrip()
	c=re.findall(r'[a-zA-Z]',string)
	r=re.findall(r'\d',string)
	result=''.join(r)
	return result,text3
s="(312)-318-6471 headak ehere"
i= "(213) 121 3311 eajehea"
	
z,zz=filterfunction(s)
aa,bb=filterfunction(i)
print aa,bb
print z,zz
