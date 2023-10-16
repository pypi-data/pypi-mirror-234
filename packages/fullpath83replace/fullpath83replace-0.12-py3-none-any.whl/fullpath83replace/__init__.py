import functools
import os
from itertools import zip_longest
import ctypes
import re

try:
    from ctypes import wintypes

    windll = ctypes.LibraryLoader(ctypes.WinDLL)
    kernel32 = windll.kernel32

    _GetShortPathNameW = kernel32.GetShortPathNameW
    _GetShortPathNameW.argtypes = [
        wintypes.LPCWSTR,
        wintypes.LPWSTR,
        wintypes.DWORD,
    ]
    _GetShortPathNameW.restype = wintypes.DWORD
except Exception:
    # linux
    pass
drivereg = re.compile(r"\b([a-z]:\\)", flags=re.I)


@functools.cache
def get_short_path_name(long_name):
    try:
        if not os.path.exists(long_name):
            return long_name

        output_buf_size = 4096
        output_buf = ctypes.create_unicode_buffer(output_buf_size)
        _ = _GetShortPathNameW(long_name, output_buf, output_buf_size)
        pa = output_buf.value
        return pa if os.path.exists(pa) else long_name
    except Exception:
        return long_name


def absolut_wpath_to_83(
    string, valid_string_ends=("<", ">", ":", '"', "|", "?", "*", "\n", "\r", " ")
):
    r"""
    Convert long Windows file paths to their short 8.3 format in a string where applicable.

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

    """
    charssep = {*valid_string_ends}
    string = string + " "

    resplits = [x for x in drivereg.finditer(string)]
    stringlen = len(string)
    indscan = [
        [x[0].start(), x[1].start() if x[1] else stringlen - 1]
        for x in list(zip_longest(resplits, resplits[1:]))
    ]
    toreplace = []
    alli = set(range(stringlen))
    for i in indscan:
        for r in range(i[1], i[0], -1):
            p = string[i[0] : r]
            if os.path.exists(p):
                if not (charssep.intersection({string[r]})):
                    continue
                toreplace.append([i[0], r, p, get_short_path_name(p)])
                alli = alli ^ set(range(i[0], r))
                break
    allstri = [""]
    alli = sorted(list(alli))
    alli_len = []
    for x in zip_longest(alli, alli[1:]):

        try:
            allstri[-1] = allstri[-1] + (string[x[0]])
            if x[1] - x[0] > 1:
                allstri.append("")
                alli_len.append(x[0])
        except Exception:
            alli_len.append(x[0])
            allstri.append("")
    return "".join(
        [
            y[-1]
            for y in sorted(
                [list(x) for x in (zip(alli_len, allstri))]
                + [[x[0], x[-1]] for x in toreplace],
                key=lambda q: q[0],
            )
        ]
    )
