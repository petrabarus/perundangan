#!/usr/bin/env python
"""
Clean HTML from the downloaded documents
"""
from os import listdir
from os.path import isfile, join
import sys
from lxml.html.clean import Cleaner
from lxml import html, etree

cleaner = Cleaner(
        scripts=True,
        javascript=True,
        comments=True,
        links=True,
        page_structure=False,
        style=True,
        safe_attrs_only=True,
        kill_tags=['a', 'noscript']
    )

inputdir = sys.argv[1]
outputdir = sys.argv[2]
for f in listdir(inputdir):
    filepath = join(inputdir, f)
    if isfile(filepath):
        print "Parsing  " + filepath
        f = open(filepath, "rb")
        html_content = html.fromstring(f.read())
        title = html_content.xpath('/html/head/title')
        body = html_content.xpath('/html/body')
        if (title and title[0].text):
            title_text = title[0].text
            newfilename = join(outputdir, title_text.replace(' ', '-').replace('/', '-') + '.html')
            print "\tTitle: " + title_text
            if (body):
                for b in body:
                    b.attrib.pop('class')
                body_text = '<html><head><title>' + title_text + '</title></head><body>' + \
                    cleaner.clean_html(etree.tostring(body[0])) + '</body></html>'
                print "\tSaving to : %s" % newfilename
                fout = open(newfilename, "w")
                fout.write(body_text)
                fout.close()
            else:
                print "\tError: body doesn't exist"
        else:
            print "\tError: title doesn't exist"


