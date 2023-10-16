# Converts long Windows file paths to their short 8.3 format in a string where applicable.

## Tested against Windows / Python 3.11 / Anaconda

## pip install fullpath83replace

```python
absolut_wpath_to_83(
    string, valid_string_ends=("<", ">", ":", '"', "|", "?", "*", "\n", "\r", " ")
):
    r"""

This function takes a string containing file paths and attempts to convert long
Windows file paths to their short 8.3 format where applicable. It identifies file
paths in the input string, checks if they exist, and if they do, replaces them
with their short 8.3 format versions.

Parameters:
- string (str): The input string containing file paths.
- valid_string_ends (tuple): A tuple of valid string endings 'c:\some long path' will not be converted if "'" is not in valid_string_ends

Returns:
- str: The input string with long file paths replaced by their short 8.3 format
  versions, while preserving valid string endings.

Example Usage:
	from fullpath83replace import absolut_wpath_to_83
	string1 = r'"C:\Users\hansc\Downloads\scrapingthreading.mp4" c:\babaexistsbutnottherest  "C:\Users\hansc\Downloads\Roger LeRoy Miller, Daniel K. Benjamin, Douglass C. North - The Economics of Public Issues-Pearson College Div (2017).pdf" c:\baba c:\Windows'
	str1 = absolut_wpath_to_83(
		string1, valid_string_ends=("<", ">", ":", '"', "|", "?", "*", "\n", "\r", " ")
	)


	string2 = r'C:\Users\hansc\Downloads\scrapingthreading.mp4 c:\babaexists butnot therest  C:\Users\hansc\Downloads\Roger LeRoy Miller, Daniel K. Benjamin, Douglass C. North - The Economics of Public Issues-Pearson College Div (2017).pdf c:\baba "c:\Windows" '
	str2 = absolut_wpath_to_83(
		string2, valid_string_ends=("<", ">", ":", '"', "|", "?", "*", "\n", "\r", " ")
	)

	string3 = r''' C:\Users\hansc\Downloads\scrapingthreading.mp4 c:\babaxxxas\asfasdxx\bi  'C:\Users\hansc\Downloads\Roger LeRoy Miller, Daniel K. Benjamin, Douglass C. North - The Economics of Public Issues-Pearson College Div (2017).pdf' xxxxxxxxxxxxxxxxxx "c:\baba" c:\Windows'''
	str3 = absolut_wpath_to_83(
		string3, valid_string_ends=("<", ">", ":", '"', "|", "?", "*", "\n", "\r", " ", "'")
	)


	print(str1)
	print(string1)
	# "C:\Users\hansc\DOWNLO~1\SCRAPI~1.MP4" c:\babaexistsbutnottherest  "C:\Users\hansc\DOWNLO~1\ROGERL~1.PDF" c:\baba c:\Windows
	# "C:\Users\hansc\Downloads\scrapingthreading.mp4" c:\babaexistsbutnottherest  "C:\Users\hansc\Downloads\Roger LeRoy Miller, Daniel K. Benjamin, Douglass C. North - The Economics of Public Issues-Pearson College Div (2017).pdf" c:\baba c:\Windows
	print(str2)
	print(string2)
	# C:\Users\hansc\DOWNLO~1\SCRAPI~1.MP4 c:\babaexists butnot therest  C:\Users\hansc\DOWNLO~1\ROGERL~1.PDF c:\baba "c:\Windows
	# C:\Users\hansc\Downloads\scrapingthreading.mp4 c:\babaexists butnot therest  C:\Users\hansc\Downloads\Roger LeRoy Miller, Daniel K. Benjamin, Douglass C. North - The Economics of Public Issues-Pearson College Div (2017).pdf c:\baba "c:\Windows"
	print(str3)
	print(string3)
	#  C:\Users\hansc\DOWNLO~1\SCRAPI~1.MP4 c:\babaxxxas\asfasdxx\bi  'C:\Users\hansc\DOWNLO~1\ROGERL~1.PDF' xxxxxxxxxxxxxxxxxx "c:\baba" c:\Windows
	#  C:\Users\hansc\Downloads\scrapingthreading.mp4 c:\babaxxxas\asfasdxx\bi  'C:\Users\hansc\Downloads\Roger LeRoy Miller, Daniel K. Benjamin, Douglass C. North - The Economics of Public Issues-Pearson College Div (2017).pdf' xxxxxxxxxxxxxxxxxx "c:\baba" c:\Windows

```