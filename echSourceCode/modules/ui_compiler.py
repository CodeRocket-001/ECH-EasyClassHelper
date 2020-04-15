import os
file_name=input("输入ui文件名（无后缀）：")
os.system("pyuic5 -o "+file_name+".py "+file_name+".ui")