#!/Users/christmas/opt/anaconda3/bin/python3
# -*- coding: utf-8 -*-
#  日期 : 2023/3/9 14:06
#  作者 : Christmas
#  邮箱 : 273519355@qq.com
#  项目 : Project
#  版本 : python 3
#  摘要 :
"""

"""
import os
# /Users/christmas/opt/anaconda3/lib/python3.9/site-packages

os.chdir('/Users/christmas/Documents/Code/Project/christmas/')
os.system('rm -rf dist build')
os.system('python3 setup.py sdist bdist_wheel')
os.system('twine upload dist/*')
