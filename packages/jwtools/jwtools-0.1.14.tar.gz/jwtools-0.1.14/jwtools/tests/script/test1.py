from jwtools.func import *

mm5 = get_text_md5("dddd333")
# print(mm5)

result = write_text_to_file("D:/test/test123.txt", mm5)
print(result)

cc = read_text_from_file("D:/test/test123.txt")
print(cc)