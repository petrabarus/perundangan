#!/usr/bin/env python
"""
Script to download documents from Kemenkumham
"""
import sqlite3
import urllib
import re
import hashlib
from urlparse import urljoin, urldefrag

conn = sqlite3.connect('links.db')
md5 = hashlib.md5()
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS links (url TEXT, type INT, isCrawled BOOLEAN)')
baseurl = 'http://www.djpp.kemenkumham.go.id/kerja/ln.php?t=2013'

def download_url(baseurl, type = 1):
    page = urllib.urlopen(baseurl)
    content_type = page.info()['Content-Type']

    if (content_type == 'text/html' or content_type == 'text/plain'):
        md5.update(baseurl)
        filename = md5.hexdigest()
        if (type == 2):
            filename = 'data-' + filename

        filename =  filename + '.html'
        content = page.read()
        links = re.findall(r"<a.*?\s*href=\"(.*?)\".*?>(.*?)</a>", content)
        rows = []
        exists = 0
        invalid = 0
        for link in links:
            url = urldefrag(urljoin(baseurl, link[0], False))[0]
            if(c.execute('SELECT COUNT(*) FROM links WHERE url = :url', {'url': url}).fetchone()[0] == 0):
                if 'ln.php' in url:
                    rows.append((url, 1, 0))
                elif 'buka.php' in url:
                    rows.append((url, 2, 0))
                else:
                    invalid += 1
            else:
                exists += 1
        print "\tGot %d links: exists %d, invalid %d, saving %d" % (len(links), exists, invalid, len(rows))

        c.executemany('INSERT INTO links VALUES (?, ?, ?)', rows )
        conn.commit()

        filename = 'downloads/' + filename
        print "\tSaving to file %s" % filename
        f = open(filename, 'w')
        f.write(content)
        f.close()
    else:
        print "\tNot HTML skipped"

    c.execute('UPDATE links SET isCrawled = 1 WHERE url = :url', {'url': baseurl})
    conn.commit()

result = c.execute('SELECT * FROM links WHERE isCrawled = 0 LIMIT 1').fetchone()

if (result is None):
    c.execute('INSERT INTO links VALUES (:url, :type, :isCrawled)', {'url': baseurl, 'type': 1, 'isCrawled': 0})
    conn.commit()

result = c.execute('SELECT * FROM links WHERE isCrawled = 0 LIMIT 1').fetchone()
while result:
    url = result[0]
    print "Downloading %s" % url
    download_url(url, result[1])
    current_count = c.execute('SELECT COUNT(*) FROM links WHERE isCrawled = 0').fetchone()[0]
    print "Current link %s" % current_count
    result = c.execute('SELECT * FROM links WHERE isCrawled = 0 LIMIT 1').fetchone()