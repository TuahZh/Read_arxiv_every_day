import time
import os
import sys
import pickle as pck
import re
import shutil
def preprocessor(fname='tk_interface.py', body_in=''):
    if (not os.path.isfile(".enea.alive")):
        shutil.copy2(fname, ".enea.alive")
    if (not os.path.isfile("history.pkl")):
        return
    else:
        with open("history.pkl", "rb") as f:
            _hist = pck.load(f)
    if (_hist['day']<=0):
        return
    if (_hist['day']==1):
#    print("Writing to script...")
        body = """###############################################################################
# file name: %s
# Author: Enea
""" % fname
        body += "# Created time: " + time.asctime(time.localtime()) +"\n"
        body += "# Days: %d\n" % _hist['day']
        body += "###############################################################################\n"
        if (body_in==""):
            body_in = body_pre(fname, _hist)
        body += body_in
        with open(fname, 'w') as f:
            f.write(body)
def body_pre(fname, _hist):
    print("Day: %d" % _hist['day'])
    try:
        with open(fname, "r") as f:
            body = f.read()
    except:
        raise NameError("Enea may be dead.")
    pattern = "\#\s+Days\:\s+[0-9]+\s"
    body_d = 0
    for ii in re.finditer(pattern, body):
        body_d = int(ii.group().split(' ')[-1].strip())
    pattern = "^\#+[^\n]*\n|^[\ \t]+\n"
    while (re.match(pattern, body) is not None):
        body = re.sub(pattern, "", body)
#    pattern = "\n\#+[^\n]*\n"
#    body = re.sub(pattern, "\n", body)
    pattern = "\n\n\n*"
    body = re.sub(pattern, "\n", body)
    if (body_d==_hist['day']):
        return body
    with open("days.pkl", "rb") as f:
        _days = pck.load(f)
    try:
        for item in _days[_hist['day']]:
            body = re.sub(item[0],item[1],body)
        print('Updating')
    except KeyError:
        print('Nothing updated.')
    return body
