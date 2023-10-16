# This Package is a collection of Christmas related packages.
## Authors : Christmas
## Maintainer : Christmas

To install this package, run:

    pip install baysalt_christmas
or

    pip3 install baysalt_christmas

# Packages
## baysalt_christmas

### commonCode.py
#### ddt = converToTime(str)
```python
from christmas.commonCode import convertToTime
ddt = convertToTime('20230330')
ddt = convertToTime('2023033001')
ddt = convertToTime('202303300101')
ddt = convertToTime('20230330010101')
ddt = convertToTime('2022-11-09_01:00:00')
```
#### filename = new_filename(_pre,lon, _lat, _lat, _date, _res)
```python
from christmas.commonCode import new_filename
import numpy as np 
_lon = np.linspace(100,120)
_lat = np.linspace(10,20)
filename = new_filename('wave', _lon, _lat, _date, 10)
```
#### date = get_date()
```python
from christmas.commonCode import get_date
date = get_date()
```
#### make_dir(path)
```python
from christmas.commonCode import make_dir
make_dir('/home/ocean/zcy/1/2/3/4')
```
#### class: FTPUploadTracker (deprecated)
#### path = split_path(_path)
```python
from christmas.commonCode import split_path
path = split_path('/home/ocean/zcy/1/2/3/4/')
```
#### osprint(_str)
```python
from christmas.commonCode import osprint
x = '123'
osprint(f'{x}SSS')
```
#### osprints(_str)
```python
from christmas.commonCode import osprints
x = '123'
osprints('INFO',f'{x}SSS')
```
#### timer(func)

### processBar.py
#### class: SftpProcessbar
```python
from christmas.processBar import SftpProcessbar
import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='47.105.220.136', port=22, username='wave', password='wave', timeout=100)
sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
sftp_obj =SftpProcessbar()
Sprocess_bar = sftp_obj.process_bar
sftp.put('/home/ocean/x.zip', 'x.zip', callback=Sprocess_bar)
```
#### translate_byte(B)
#### class: FtpProcessBar
```python
from christmas.processBar import FtpProcessbar
import os, ftplib

buf_size = 1024
ftp = ftplib.FTP()
ftp.encoding = 'utf-8'
ftp.set_debuglevel(0)
ftp.connect(host='47.105.220.136', port=22)
ftp.login('wave', 'wave')
Ftp_obj = FtpProcessbar(os.path.getsize('/home/ocean/x.zip'))
Fprocess_bar = Ftp_obj.process_bar()
with open('/home/ocean/x.zip', 'rb') as fp:
  ftp.storbinary(f'STOR x.zip', fp, buf_size, Fprocess_bar)
```


### read_conf.py
#### Conf = read_conf(_conf_file, ele=None)
```python
from christmas.read_conf import read_conf
Conf = read_conf('Post_fvcom.conf')
```
#### key, value = char_fill_dic(_key,_str)
#### TF = is_number(_str)
```python
from christmas.read_conf import is_number
TF = is_number('12')
TF = is_number('-12')
TF = is_number('1e10')
TF = is_number('.5')
```
#### flattened_lst = flatten_list(_lst, flattened_lst)

### S_dateTime.py
#### Nearby_date = build_date(_date)
```python
from christmas.S_DateTime import build_date
Nearby_date = build_date('20230324')
```

### server_info.py
#### pid = grep_from_top(_exe)
```python
from christmas.server_info import grep_from_top
pid = grep_from_top('python3 forecast.py')
```
#### mpi_num = grep_from_top_mpi(_exe)
```python
from christmas.server_info import grep_from_top_mpi
pid = grep_from_top_mpi('wrf.exe')
```
#### cpu_num, free_cpu_num = get_free_core()
```python
from christmas.server_info import get_free_core
cpu_num, free_cpu_num = get_free_core()
```
#### user, hostname, ip = get_server_info()
```python
from christmas.server_info import get_serve_info
user, hostname, ip = get_serve_info()
```
### mncPy
#### class: MncPy
```python
from christmas.mncPy.compress import mnc_Py
mnc = mnc_Py('/home/ocean/wave_without_compress.nc',o_path = True, d_rm=True)
mnc.compress_files()
```
