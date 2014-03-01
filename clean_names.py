#!/usr/bin/env python
from os import rename, listdir
from os.path import isfile, join
from re import match

"""
Renaming lower case document typename to upper case
"""
def rename1(dir):
    for f in listdir(dir):
        r = match('([a-zA-Z]+)-(\d+)-(\d{4}).html', f)
        if (r):
            newfilename = r.group(1).upper() + '-' + r.group(2) + '-' + r.group(3) + '.html'
            print 'renaming %s to %s' % (f, newfilename)
            rename(join(dir, f), join(dir, newfilename))

def rename2(dir):
    for f in listdir(dir):
        r = match('([a-zA-Z]+)(\d+)-(\d{4}).html', f)
        if (r):
            newfilename = r.group(1).upper() + '-' + r.group(2) + '-' + r.group(3) + '.html'
            print 'renaming %s to %s' % (f, newfilename)
            rename(join(dir, f), join(dir, newfilename))


def rename3(dir):
    for f in listdir(dir):
        r = match('([a-zA-Z]+)-?(\d+)-(\d{4})(\w+).html', f)
        if (r):
            newfilename = r.group(1).upper() + '-' + r.group(2) + '-' + r.group(3) + '.html'
            print 'renaming %s to %s' % (f, newfilename)
            if (isfile(join(dir, newfilename))):
                print '\tfile %s exists' % newfilename
                newfilename = r.group(1).upper() + '-' + r.group(2) + '-' + r.group(3) + '-' + r.group(4).upper() + '.html'
                print '\trenaming alternative %s to %s' % (f, newfilename)
            rename(join(dir, f), join(dir, newfilename))

if __name__ == '__main__':
    rename3('build')