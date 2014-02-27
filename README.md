#Indonesian Law Documents Linking Project

This is a small project to download collections of Indonesian law documents, then parse and annotate links between the documents.

##Directory
```
/
|--- build             currently contains list of html documents
|--- logs              list of my logfile
+--- tmp               just a place for working
```

##Requirements
Some scripts in this project will need
- Python 2.7
- PhantomJS 1.4.0

##Steps
So far steps I have made

```
$#This will download files from www.djpp.kemenkumham.go.id
$./downloader.js

$#This will move the documents for rendering
$cp downloads/data-* tmp/renderinput

$#Since most the HTML files use Javascript obfuscation, this will render the final HTML result using PhantomJS
$./render.js tmp/renderinput build/renderoutput

$#This will remove unused HTML tags and output renamed files
$./clean_html.python tmp/renderoutput tmp/cleaned

$#So far
$cp tmp/cleaned build

```

##Changelog
2014.02.27 Started the project