#!/usr/bin/python

import datetime
import os
import sys

datadir="/home/pi/mm/ping_data"

def get_count(fullpath):
  with open(fullpath,'r') as f:
    file_contents = f.readlines()
  if len(file_contents) != 1:
    sys.stderr.write('wrong length for ' + fullpath + '\n')
    return('file_read_error')
  last_comma_index = file_contents[0].rfind(',')
  return(file_contents[0][last_comma_index+1:].rstrip('\n'))

def get_hostname():
  with open('/etc/hostname','r') as f:
    file_contents = f.readlines()
  if len(file_contents) != 1:
    sys.stderr.write('wrong length for hostname file\n')
    return('hostname_read_error')
  return(file_contents[0].rstrip('\n'))

sys.stdout.write("http://mm.mojotron.com/hourly.py?action=hourly-report")

now = datetime.datetime.utcnow()
#print(str(now))
one_hour_ago = now - datetime.timedelta(hours=1)
#print("one_hour_ago is:" + str(one_hour_ago))
sys.stdout.write("&year=" + str(one_hour_ago.year))
sys.stdout.write("&month=" + str(one_hour_ago.month).zfill(2))
sys.stdout.write("&day=" + str(one_hour_ago.day).zfill(2))
sys.stdout.write("&hour=" + str(one_hour_ago.hour).zfill(2))

date_prefix = '_'.join([str(one_hour_ago.year),
                        str(one_hour_ago.month).zfill(2),
                        str(one_hour_ago.day).zfill(2),
                        'T',
                        str(one_hour_ago.hour).zfill(2)])
sys.stdout.write("&date_prefix=" + date_prefix)
count = 0
match_count = 0
ip_dict = {}
for fname in os.listdir(datadir):
  count = count+1
  if fname.startswith(date_prefix):
    match_count = match_count + 1
    ip = fname[22:]
    if ip not in ip_dict:
      ip_dict[ip] = {}
    ping_count = str(get_count(os.path.join(datadir,fname))).zfill(2)
    if ping_count not in ip_dict[ip]:
      ip_dict[ip][ping_count] = 1
    else:
      ip_dict[ip][ping_count] = ip_dict[ip][ping_count] + 1

sys.stdout.write("&count=" + str(count))
sys.stdout.write("&match_count=" + str(match_count))
sys.stdout.write("&hostname=" + get_hostname())
for ip in sorted(ip_dict.keys()):
  sys.stdout.write("&" + ip + "=")
  tmp_list = []
  for ping_count in sorted(ip_dict[ip].keys()):
    tmp_list.append(ping_count + "-" + str(ip_dict[ip][ping_count]).zfill(2))
  sys.stdout.write(".".join(tmp_list))
  
