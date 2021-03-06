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

clean8regex1 = re.compile('(<br />\s+)+</center>');
clean8regex2 = re.compile('<center>(\s+<br />)+');
clean8regex3 = re.compile('</center>((\s+)?<br />)+');
def clean8(filename, content):
    new_content = clean8regex1.sub('</center>', content)
    new_content = clean8regex2.sub('<center>', new_content)
    new_content = clean8regex3.sub('</center>', new_content)
    if (new_content != content):
        print filename
    return new_content

#Parse string PASAL XX in <center></center> and replace it with h4
clean9regex1 = re.compile('Pasal (\w+)(\s+)</center>')
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
    has_changed = False
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
                has_changed = has_changed or True
            elif (clean10regex2.match(text)):
                element = html.Element('h2', {'class': 'bab'})
                element.text = text
                part.addprevious(element)
                part.drop_tree()
                has_changed = has_changed or True
            
    if has_changed:
        print filename
        content = etree.tostring(html_content)
    return content    

def clean11(filename, content):
    html_content = html.fromstring(content)
    h4_parts = html_content.xpath('//h4')
    has_changed = False
    for h4_part in h4_parts:
        if (h4_part.tail and len(h4_part.tail.strip()) > 0 and 
            h4_part.getnext() is not None and h4_part.getnext().tag == 'br'):
            has_changed = has_changed or True
            text = h4_part.tail.strip()
            element = html.Element('div', {'class': 's14'})
            element.text = text
            h4_part.tail = ''
            h4_part.addnext(element)
    
    if has_changed:
        print filename
        content = etree.tostring(html_content)

    return content


clean12regex1 = re.compile('</div>(<br />)(\s+<br />)?');
def clean12(filename, content):
    new_content = clean12regex1.sub('</div>', content)
    if (new_content != content):
        print filename
    return new_content

def clean13(filename, content):
    html_content = html.fromstring(content)
    center_parts = html_content.xpath('//center')
    for center_part in center_parts:
        children = center_part.getchildren()
        for child in children:
            print child.tail
    return content

def clean14(filename, content):
    html_content = html.fromstring(content)
    s140s = html_content.xpath('//div[@class=\'s140\']')
    for s140 in s140s:
        children = s140.getchildren()
        no_extra_text = not any(child.tail and child.tail.strip() for child in children)
        no_text = s140.text and not s140.text.strip()
        all_s12 = all(child.get('class') == 's12' for child in children)
        if children and no_extra_text and no_text and all_s12:
            print filename
            parentelement = html.Element('ol', {'class': 'sx14-s140'})
            for child in children:
                element = html.Element('li', {'class': 'sx14-s12'})
                element.text = child.text
                child.drop_tree()
                parentelement.append(element)
            s140.addprevious(parentelement)
            s140.drop_tree()
            content = etree.tostring(html_content)
    return content

clean15regex1 = re.compile('^\(\d+\)')
clean15regex2 = re.compile('^d+\.')
clean15regex3 = re.compile('^d+\)')
def clean15(filename, content):
    html_content = html.fromstring(content)
    s14s = html_content.xpath('//div[@class=\'s14\']')
    has_changed = False
    for s14 in s14s:
        if (s14.tail and len(s14.tail.strip()) > 0):
            text = []
            text.append(s14.tail.strip())
            next = s14.getnext()
            to_drop = []
            while (next is not None and next.tag == 'br' and next.tail is not None):
                text.append(next.tail.strip())
                to_drop.append(next)
                next = next.getnext()

            if (next is not None):
                to_drop.append(next)
            
            match_bulleting = (all(clean15regex1.match(t) for t in text) 
                or all(clean15regex2.match(t) for t in text)
                or all(clean15regex3.match(t) for t in text))
            if match_bulleting:
                has_changed = has_changed or True
                prev = s14
                s14.tail = ''
                for t in text:
                    element = html.Element('div', {'class': 's14'})
                    element.text = t
                    prev.addnext(element)
                    prev = element

                for drop in to_drop:
                    drop.tail = ''
                    drop.drop_tree()

        elif (not s14.tail and s14.getnext() is not None and s14.getnext().tag == 'br'):
            has_changed = has_changed or True
            s14.getnext().drop_tree()

    if (has_changed):
        print filename
    return etree.tostring(html_content)


clean16regex1 = re.compile('^\(\d+\)')
clean16regex2 = re.compile('^d+\.')
clean16regex3 = re.compile('^[a-z]\.')
clean16regex4 = re.compile('^[a-z]\)')
clean16regex5 = re.compile('^d+\)')
def clean16(filename, content):
    html_content = html.fromstring(content)
    s12s = html_content.xpath('//div[@class=\'s12\']')
    has_changed = False
    for s12 in s12s:
        if (s12.tail and len(s12.tail.strip()) > 0):
            text = []
            text.append(s12.tail.strip())
            next = s12.getnext()
            to_drop = []
            while (next is not None and next.tag == 'br' and next.tail is not None):
                text.append(next.tail.strip())
                to_drop.append(next)
                next = next.getnext()

            if (next is not None):
                to_drop.append(next)
            
            match_bulleting = (all(clean16regex1.match(t) for t in text) 
                or all(clean16regex2.match(t) for t in text)
                or all(clean16regex3.match(t) for t in text)
                or all(clean16regex4.match(t) for t in text)
                or all(clean16regex5.match(t) for t in text)
                )
            if match_bulleting:
                has_changed = has_changed or True
                prev = s12
                s12.tail = ''
                for t in text:
                    element = html.Element('div', {'class': 's12'})
                    element.text = t
                    prev.addnext(element)
                    prev = element

                for drop in to_drop:
                    drop.tail = ''
                    drop.drop_tree()

        elif (not s12.tail and s12.getnext() is not None and s12.getnext().tag == 'br'):
            has_changed = has_changed or True
            s12.getnext().drop_tree()

    if (has_changed):
        print filename
    return etree.tostring(html_content)


clean17regex1 = re.compile('^(\d+)\.')
clean17regex2 = re.compile('^([a-z])\.')
def clean17(filename, content):
    html_content = html.fromstring(content)
    s140s = html_content.xpath('//div[@class=\'s140\']')
    has_changed = False
    for s140 in s140s:
        if (s140.text and len(s140.text.strip()) > 0 and
            len(s140.getchildren()) > 0 and all(child.tag == 'br' for child in s140.getchildren())):
            text = []
            text.append(s140.text.strip())
            for child in s140.getchildren():
                if (child.tail and len(child.tail.strip())):
                    text.append(child.tail.strip())

            if (all(clean17regex1.match(t) for t in text) or
                all(clean17regex2.match(t) for t in text)):
                has_changed = has_changed or True
                s140.text = ''
                for child in s140.getchildren():
                    s140.remove(child)
                for t in text:
                    element = html.Element('li')
                    element.text = t
                    s140.append(element)
                s140.tag = 'ol'

    if has_changed:
        print filename
        content = etree.tostring(html_content)
    return content

clean18regex1 = re.compile('^(\d+)\.')
clean18regex2 = re.compile('^([a-z])\.')
def clean18(filename, content):
    html_content = html.fromstring(content)
    s140s = html_content.xpath('//div[@class=\'s140\']')
    has_changed = False
    for s140 in s140s:
        if (s140.text and len(s140.text.strip()) > 0 and
            len(s140.getchildren()) > 0 and 
            all((child.tag == 'br' or (child.tag == 'div' and child.get('class') == 's12' and len(child.getchildren()) == 0))
                for child in s140.getchildren())
            and any(child.get('class') == 's12' for child in s140.getchildren())):
            text = []
            if (s140.text and len(s140.text.strip()) > 0):
                text.append(s140.text.strip())
            for child in s140.getchildren():
                if child.tag == 'br':
                    if child.tail and len(child.tail.strip()) > 0:
                        text.append(child.tail.strip())
                elif child.tag == 'div':
                    if child.text and len(child.text.strip()) > 0:
                        text.append(child.text.strip())
                    if child.tail and len(child.tail.strip()) > 0:
                        text.append(child.tail.strip())

            if (all(clean18regex1.match(t) for t in text) or
                all(clean18regex2.match(t) for t in text)):
                has_changed = has_changed or True
                s140.text = ''
                for child in s140.getchildren():
                    s140.remove(child)
                for t in text:
                    element = html.Element('li')
                    element.text = t
                    s140.append(element)
                s140.tag = 'ol'

    if has_changed:
        print filename
        content = etree.tostring(html_content)
    return content

"""
Finding all element with class 'sx11' from previous parsing and check whether
it's a part of list of s14.
"""
clean19regex1 = re.compile('^\(\d+')
clean19regex2 = re.compile('\d+\.')
def clean19(filename, content):
    html_content = html.fromstring(content)
    sx11s = html_content.xpath('//div[@class=\'sx11\']')
    has_changed = False
    for sx11 in sx11s:
        if (sx11.text and 
            (clean19regex1.match(sx11.text.strip()) or clean19regex2.match(sx11.text.strip()))
            and ((sx11.getprevious() is not None and sx11.getprevious().get('class') == 's14') or 
                ((sx11.getnext() is not None and sx11.getnext().get('class') == 's14')))):
            has_changed = has_changed or True
            sx11.set('class', 's14')
    if has_changed:
        print filename
        content = etree.tostring(html_content)
    return content

"""
Cleaning up tail from sx11 and change the sx11 to s14 if it's a list with (\d+) bullet
"""
clean20regex1 = re.compile('^\(\d+\)')
def clean20(filename, content):
    html_content = html.fromstring(content)
    sx11s = html_content.xpath('//div[@class=\'sx11\']')
    has_changed = False
    for sx11 in sx11s:
        if (sx11.tail and sx11.tail.strip() and
            clean20regex1.match(sx11.text.strip()) and
            clean20regex1.match(sx11.tail.strip())):
            element = html.Element('div', {'classs': 's14'})
            element.text = sx11.tail.strip()
            sx11.set('class', 's14')
            sx11.tail = ''
            sx11.addnext(element)
            has_changed = has_changed or True

    if has_changed:
        print filename
        content = etree.tostring(html_content)
    return content

"""
Remove tailing BR
"""
def clean21(filename, content):
    new_content = content.replace('</div><br />', '</div>')
    if (new_content != content):
        print filename
    return new_content

"""
Cleaning up tail from s14 and put the tail to s14 if it's a list with (\d+) bullet
"""
clean22regex1 = re.compile('^\(\d+\)')
def clean22(filename, content):
    html_content = html.fromstring(content)
    s14s = html_content.xpath('//div[@class=\'s14\']')
    has_changed = False
    for s14 in s14s:
        if (s14.tail and s14.tail.strip() and
            clean20regex1.match(s14.text.strip()) and
            clean20regex1.match(s14.tail.strip())):
            #print s14.text.strip()
            #print s14.tail.strip()
            element = html.Element('div', {'classs': 's14'})
            element.text = s14.tail.strip()
            s14.tail = ''
            s14.addnext(element)
            has_changed = has_changed or True

    if has_changed:
        print filename
        content = etree.tostring(html_content)
    return content

clean23regex1 = re.compile('^(BAB|Bab|Bagian|Paragraf)')
def clean23(filename, content):
    html_content = html.fromstring(content)
    center_parts = html_content.xpath('//center')
    has_changed = False
    for center_part in center_parts:
        if (center_part.getchildren() is not None and
            len(center_part.getchildren()) == 3 and
            all((child.tag == 'br' and child.tail and len(child.tail.strip()) > 0) for child in center_part.getchildren())):
            children = center_part.getchildren()
            text1 = center_part.text.strip()
            text2 = children[0].tail.strip()
            text3 = children[1].tail.strip()
            text4 = children[2].tail.strip()

            match1 = clean23regex1.match(text1)
            match2 = clean23regex1.match(text3)
            if(match1 and match2):
                has_changed = has_changed or True
                element1 = html.Element('h2', {'class': match1.group(1).lower()})
                element1.text = text1 + ': ' + text2
                element2 = html.Element('h2', {'class': match2.group(1).lower()})
                element2.text = text3 + ': ' + text4
                center_part.addprevious(element1)
                center_part.addprevious(element2)
                center_part.drop_tree()

    if has_changed:
        print filename
        content = etree.tostring(html_content)
    return content

def clean24(filename, content):
    html_content = html.fromstring(content)
    sx11s = html_content.xpath('//div[@class=\'sx11\']')
    has_changed = False
    for sx11 in sx11s:
        if (sx11.getprevious() is not None and (sx11.getprevious().tag == 'h2' or sx11.getprevious().tag == 'h4') and
            sx11.getnext() is not None and (sx11.getnext().tag == 'h2' or sx11.getnext().tag == 'h4') and
            not sx11.getchildren()):
            sx11.set('class', 's14')
            has_changed = has_changed or True

    if has_changed:
        print filename
        content = etree.tostring(html_content)
    return content

def clean25(filename, content):
    html_content = html.fromstring(content)
    sx11s = html_content.xpath('//div[@class=\'sx11\']')
    has_changed = True
    for sx11 in sx11s:
        if (sx11.getprevious() is not None and (sx11.getprevious().tag == 'h2' or sx11.getprevious().tag == 'h4')):
            sx11.set('class', 's14')
            has_changed = has_changed or True
    
    if has_changed:
        print filename
        content = etree.tostring(html_content)            
    return content

"""
Detect tail that begins with bullet
"""
clean26regex1 = re.compile('^[a-z]{1}\.')
def clean26(filename, content):
    html_content = html.fromstring(content)
    s14s = html_content.xpath('//div[@class=\'s14\']')
    has_changed = False
    for s14 in s14s:
        if (s14.text and s14.text.strip() and s14.text.strip()[-1] == ':'
            and s14.tail is not None and len(s14.tail.strip()) > 0 and 
            (s14.getchildren() is None or len(s14.getchildren()) == 0)
            and s14.getnext() is not None):
            if (clean26regex1.match(s14.tail.strip())):
                has_changed = has_changed or True
                element = html.Element('div', {'class': 's12'})
                element.text = s14.tail.strip()
                s14.tail = ''
                s14.addnext(element)

    if has_changed:
        print filename
        content = etree.tostring(html_content)

    return content


clean27regex1 = re.compile('^[a-z]{1,2}\.')
def clean27(filename, content):
    html_content = html.fromstring(content)
    s12s = html_content.xpath('//div[@class=\'s12\']')
    has_changed = False
    for s12 in s12s:
        if ((s12.getchildren() is None or len(s12.getchildren()) == 0) and
            s12.tail is not None and len(s12.tail.strip()) > 0 and clean27regex1.match(s12.tail.strip())):
            has_changed = has_changed or True
            element = html.Element('div', {'class' : 's12'})
            element.text = s12.tail.strip()
            s12.tail = ''
            s12.addnext(element)
            while (element.getnext() is not None and element.getnext().tag == 'br' and 
                element.getnext().tail is not None and len(element.getnext().tail.strip()) > 0 and
                clean27regex1.match(element.getnext().tail.strip())):
                new_element = html.Element('div', {'class' : 's12'})
                new_element.text = element.getnext().tail.strip()
                element.getnext().tail = ''
                element.getnext().drop_tree()
                element.addnext(new_element)
                element = new_element

    if has_changed:
        print filename
        content = etree.tostring(html_content)
    return content


clean28regex1 = re.compile('^\d+\.')
def clean28(filename, content):
    html_content = html.fromstring(content)
    s12s = html_content.xpath('//div[@class=\'s12\']')
    has_changed = False
    for s12 in s12s:
        if ((s12.getchildren() is None or len(s12.getchildren()) == 0) and
            s12.tail is not None and len(s12.tail.strip()) > 0 and clean28regex1.match(s12.tail.strip())):
            has_changed = has_changed or True
            element = html.Element('div', {'class' : 's12'})
            element.text = s12.tail.strip()
            s12.tail = ''
            s12.addnext(element)
            while (element.getnext() is not None and element.getnext().tag == 'br' and 
                element.getnext().tail is not None and len(element.getnext().tail.strip()) > 0 and
                clean28regex1.match(element.getnext().tail.strip())):
                new_element = html.Element('div', {'class' : 's12'})
                new_element.text = element.getnext().tail.strip()
                element.getnext().tail = ''
                element.getnext().drop_tree()
                element.addnext(new_element)
                element = new_element

    if has_changed:
        print filename
        content = etree.tostring(html_content)
    return content

"""
Putting amandement to blockquotes
"""
def clean29(filename, content):
    html_content = html.fromstring(content)
    s120s = html_content.xpath('//div[@class=\'s120\']')
    has_changed = False
    for s120 in s120s:
        if (s120.getchildren() and len(s120.getchildren()) > 0 and (s120.getchildren()[0].tag == 'h4' or s120.getchildren()[0].tag == 'center')):
            s120.tag = 'blockquote'
            if (len(s120.getchildren()) > 0):
                first = s120.getchildren()[0]
                last = s120.getchildren()[-1]
                if (first.tag == 'center' and len(first.text.strip()) == 1
                    and last.text and len(last.text.strip()) > 0 and last.text.strip()[-1] == first.text.strip()):
                    last.text = last.text.strip()[:-1]
                    first.drop_tree()
            has_changed = has_changed or True

    if has_changed:
        print filename
        content = etree.tostring(html_content)
    return content        

"""
Group a closing statement
"""
clean30regex1 = re.compile('^Agar setiap orang mengetahuinya')
def clean30(filename, content):
    html_content = html.fromstring(content)
    s14s = html_content.xpath('//div[@class=\'s14\']')
    has_changed = False
    for s14 in s14s:
        if s14.tail is not None and len(s14.tail.strip()) != 0:
            if (clean30regex1.match(s14.tail.strip())):
                has_changed = has_changed or True
                text = s14.tail.strip()
                s14.tail = ''
                element = html.Element('div', {'class':'s14x'})
                element.text = text
                s14.addnext(element)
    if has_changed:
        print filename
        content = etree.tostring(html_content)
    return content

"""
Dividing h2 to two subchildren, num and heading
"""
def clean31(filename, content):
    html_content = html.fromstring(content)
    h2s = html_content.xpath('//h2')
    has_changed = False
    for h2 in h2s:
        text = h2.text.strip().split(':')
        if len(text) == 2:
            h2.text = ''
            elmt1 = html.Element('span', {'class': 'num'})
            elmt1.text = text[0]
            elmt2 = html.Element('span', {'class': 'title'})
            elmt2.text = text[1]
            h2.append(elmt1)
            h2.append(elmt2)
            has_changed = has_changed or True

    if has_changed:
        print filename
        content = etree.tostring(html_content)
    return content

"""
Breaking the "Paragraf" heading
"""
clean32regex1 = re.compile('^(PASAL|Pasal|Paragraf|ARTICLE|Bab)')
def clean32(filename, content):
    html_content = html.fromstring(content)
    centers = html_content.xpath('//center')
    has_changed = False
    for center in centers:
        if (center.getchildren() and center.text and len(center.getchildren()) == 1 
            and center.getchildren()[0].tag == 'br'
            and center.getchildren()[0].tail):
            text1 = center.text.strip()
            text2 = center.getchildren()[0].tail.strip()
            match = clean32regex1.match(text1)
            if (match):
                c = match.group(1).lower()
                if c == 'pasal':
                    element = html.Element('h4')
                else:
                    element = html.Element('h2', {'class': c})
                num = html.Element('span', {'class': 'num'})
                num.text = text1
                heading = html.Element('span', {'class': 'title'})
                heading.text = text2
                element.append(num)
                element.append(heading)
                center.addnext(element)
                center.drop_tree()
                has_changed = has_changed or True

    if has_changed:
        print filename
        content = etree.tostring(html_content)

    return content

def processfile(filename):
    fi = open(filename, "rb")
    content = fi.read()
    fi.close()
    new_content = clean12(filename, content)
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