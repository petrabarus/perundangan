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

def rename4(dir):
    for f in listdir(dir):
        r = match('([a-zA-Z]+)-?(\d+)-(\d{4})([A-Za-z\-0-9]+).html', f)
        if (r):
            print f
            newfilename = r.group(1).upper() + '-' + r.group(2) + '-' + r.group(3) + '.html'
            if (isfile(join(dir, newfilename))):
                print '\tfile %s exists' % newfilename
            else:
                print '\trenaming %s to %s' % (f, newfilename)
                rename(join(dir, f), join(dir, newfilename))
def grep1(dir):
    for f in listdir(dir):
        r1 = match('([A-Z]+)-(\d+)-(\d{4})(-([A-Z]+))?.html', f)
        r2 = match('PBI-(\d+)-(\d+)-(\d{4})(-([A-Z]+))?.html', f)
        if (not r1 and not r2):
            print f

def rename4(dir):
    for f in listdir(dir):
        r1 = match('([A-Z]+)-(\d+)-(\d{4})(-([A-Z]+))?.html', f)
        r2 = match('PBI-(\d+)-(\d+)-(\d{4})(-([A-Z]+))?.html', f)
        if (not r1 and not r2):
            r3 = match('pbi(\d+)-(\d+)-(\d{4}).html', f)
            if (r3):
                newfilename = 'PBI-' + r3.group(1) + '-' + r3.group(2) + '-' + r3.group(3) + '.html'
                if (isfile(join(dir, newfilename))):
                    print 'file %s exists' % newfilename
                else:
                    print 'renaming %s to %s' % (f, newfilename)
                    rename(join(dir, f), join(dir, newfilename))

def rename5(dir):
    for f in listdir(dir):
        r1 = match('([A-Z]+)-(\d+)-(\d{4})(-([A-Z]+))?.html', f)
        r2 = match('PBI-(\d+)-(\d+)-(\d{4})(-([A-Z]+))?.html', f)
        if (not r1 and not r2):
            r3 = match('pbi(\d+)-(\d+)-(\d{4})([A-Za-z]+).html', f)
            if (r3):
                newfilename = 'PBI-' + r3.group(1) + '-' + r3.group(2) + '-' + r3.group(3) + '.html'
                print 'renaming %s to %s' % (f, newfilename)
                if (isfile(join(dir, newfilename))):
                    newfilename = 'PBI-' + r3.group(1) + '-' + r3.group(2) + '-' + r3.group(3) + '-' + r3.group(4).upper() + '.html'
                    print '\tfile %s exists' % newfilename
                else:
                    print '\trenaming %s to %s' % (f, newfilename)
                rename(join(dir, f), join(dir, newfilename))

if __name__ == '__main__':
    rename5('build')