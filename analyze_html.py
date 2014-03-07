#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import rename, listdir
from os.path import isfile, isdir, join
from sys import argv
import re
from lxml import html, etree

def clean1(filename, content):
    test = """
    <table align="left" border="0" cellspacing="0">
      <tbody>
        <tr>
          <td width="43"></td>

          <td></td>
        </tr>
      </tbody>
    </table>

    <p align="right"></p>

    <div align="right" class="d4"></div>
"""
    if (test in content):
        print filename
        content = content.replace(test, '')
        #print content
    return content
        
clean2regex = re.compile("<div class=\"d3\">\s+<small>\(c\)2010 Ditjen PP :: \|\| \|\|</small>\s+</div>")
def clean2(filename, content):
    test = """
    <div class="d3">
      <small>(c)2010 Ditjen PP :: || ||</small>
    </div>
"""
    new_content = clean2regex.sub("", content)
    if (new_content != content):
        print filename
    return new_content

def clean3(filename, content):
    test = "<div class=\"d3\" align=\"right\"></div>"
    if (test in content):
        print filename
        content = content.replace(test, '')
    return content

#Removing tailing br
def clean4(filename, content):
    new_content = content.replace('</div><br>', '</div>')
    if (new_content != content):
        print filename
    return new_content

#Removing unused image
clean5regex = re.compile("<img src=\"([a-zA-Z\./]+)\" border=\"0\">(\s+)?(<br>)?(\s+)?(<br>)?")
def clean5(filename, content):
    new_content = clean5regex.sub("", content)
    if (new_content != content):
        print filename
    return new_content

def processfile(filename):
    fi = open(filename, "rb")
    content = fi.read()
    fi.close()
    new_content = clean5(filename, content)
    fo = open(filename, "w")
    fo.write(new_content)
    fo.close()

if __name__ == '__main__':
    if len(argv) > 1:
        if (isfile(argv[1])):
            processfile(argv[1])
        elif (isdir(argv[1])):
            for f in sorted(listdir(argv[1])):
                filename = join(argv[1], f) 
                processfile(filename)