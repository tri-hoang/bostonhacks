import re
def filterfunction(string):
	search = re.findall(r"\(?\b[2-9][0-9]{2}\)?[-. ]?[2-9][0-9]{2}[-. ]?[0-9]{4}\b", string)
	phonenum = re.sub(r"[^\w]", "", search[0])
	song = string.replace(search[0], "").lstrip()
	return phonenum,song
