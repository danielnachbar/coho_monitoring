#!/usr/bin/python

import os
import sys

datadir="/home/pi/mm/data"

sys.stdout.write("http://mm.mojotron.com/mm.py?action=report")

os.chdir(datadir)

for fname in os.listdir(datadir):
  f = open(fname,"r")
  if fname == "action":
    fname = 'action_BOGUS'
  lines = f.readlines()
  cleaned = []
  for l in lines:
    cleaned.append(l.strip().replace(" ","-").replace("\t","-"))
  sys.stdout.write("&" + fname + "=" + "+".join(cleaned))
  f.close()
