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

def clean6(filename, content):
    text = '&Acirc;&nbsp;'
    if (text in content):
        print filename
        content = content.replace(text, ' ')
    return content

clean7regex1 = re.compile("\b\s+|\n\s+|\s+\n|\s+\b");
clean7regex2 = re.compile("^(Menimbang|Mengingat|Menetapkan|Memperhatikan|Mendengar|Kepada)(\s+)?:");
def clean7(filename, content):
    html_content = html.fromstring(content)
    sm_parts = html_content.xpath('//div[@class=\'sm\']')
    for sm_part in sm_parts:
        text = clean7regex1.sub(' ', sm_part.text).strip()
        match = clean7regex2.match(text)
        if (match):
            print filename
            element = html.Element('div', {'class': 'xsm'})
            element.text = ''
            parent = sm_part.getparent()
            
            element2 = html.Element('strong')
            element2.text = match.group(1)


            element.append(element2)
            ol = html.Element('ol')
            li = html.Element('li')
            li.text = clean7regex2.sub('', text).strip() 
            ol.append(li)

            sibling = sm_part.getnext()
            sm_siblings = []
            while (sibling is not None and sibling.get('class') == 'sm1'):
                sm_siblings.append(sibling)
                sibling = sibling.getnext()
            for sibling in sm_siblings:
                if (sibling.text is not None):
                    li = html.Element('li')
                    li.text = clean7regex1.sub(' ', sibling.text).strip()
                    ol.append(li)
                parent.remove(sibling)

            element.append(ol)
            sm_part.addprevious(element)
            sm_part.drop_tree()

    return etree.tostring(html_content)

clean8regex1 = re.compile('(<br>\s+)+</center>');
clean8regex2 = re.compile('<center>(\s+<br>)+');
clean8regex3 = re.compile('</center>((\s+)?<br>)+');
def clean8(filename, content):
    new_content = clean8regex1.sub('</center>', content)
    new_content = clean8regex2.sub('<center>', new_content)
    new_content = clean8regex3.sub('</center>', new_content)
    if (new_content != content):
        print filename
    return new_content

#Parse string PASAL XX in <center></center> and replace it with h4
clean9regex1 = re.compile('Pasal (\d+)(\s+)</center>')
def clean9(filename, content):
    print filename
    content = clean9regex1.sub('</center><h4>Pasal \g<1></h4>', content)
    return content

#Grab all center that have 1 <br> and then convert it to <h2> with class
clean10regex1 = re.compile('^Bagian');
clean10regex2 = re.compile('^BAB');
def clean10(filename, content):
    html_content = html.fromstring(content)
    center_parts = html_content.xpath('//center')
    for part in center_parts:
        child = part.getchildren()
        if (len(child) == 1 and child[0].tag == 'br' and
            part.text and part.text.strip() and child[0].tail and child[0].tail.strip()):
            text = part.text.strip() + ': ' + child[0].tail.strip()
            if (clean10regex1.match(text)):
                element = html.Element('h2', {'class': 'bagian'})
                element.text = text
                part.addprevious(element)
                part.drop_tree()
            elif (clean10regex2.match(text)):
                element = html.Element('h2', {'class': 'bab'})
                element.text = text
                part.addprevious(element)
                part.drop_tree()
            new_content = etree.tostring(html_content)
            if (new_content != content):
                print filename
                content = new_content
    return content    

def clean11(filename, content):
    html_content = html.fromstring(content)
    h4_parts = html_content.xpath('//h4')
    for h4_part in h4_parts:
        if (h4_part.tail and len(h4_part.tail.strip()) > 0 and 
            h4_part.getnext() is not None and h4_part.getnext().tag == 'br'):
            print filename
            text = h4_part.tail.strip()
            element = html.Element('div', {'class': 'sx11'})
            element.text = text
            h4_part.tail = ''
            h4_part.addnext(element)
            content = etree.tostring(html_content)
    return content

def processfile(filename):
    fi = open(filename, "rb")
    content = fi.read()
    fi.close()
    new_content = clean11(filename, content)
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