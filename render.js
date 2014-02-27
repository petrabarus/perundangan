#!/usr/bin/env phantomjs
/**
 * Script to render the page since most of the pages have to be evaluated using Javascript.
 * To use it
 * phantomjs render.js [inputdir] [outputdir]
 */

var page = require('webpage').create(), 
    fs = require('fs');

var loadInProgress = false,
    htmlFiles = new Array();
 
 
var inputdir = phantom.args[0];
var outputdir = phantom.args[1];

console.log('Input : '  + inputdir + ', Output : ' + outputdir);

var inputdirlist = fs.list(inputdir);
console.log('Input file count: ' + inputdirlist.length);
 
// loop through files and folders //
for(var i = 0; i< inputdirlist.length; i++) {
    var fullpath = inputdir + fs.separator + inputdirlist[i];
    // check if item is a file //
    if(fs.isFile(fullpath)) {
        // check that file is html //
        if(fullpath.toLowerCase().indexOf('.html') != -1) {
            // show full path of file //
            console.log('File path: ' + fullpath);
            htmlFiles.push(fullpath);
            // todo: make this more async (i.e. pop on/off stack WHILE rending pages)
        }
    }
}

var totalCount = htmlFiles.length;
console.log('HTML files found: ' + totalCount);

var pageindex = 0;
var fileName = '';

var interval = setInterval(function() {
    if (!loadInProgress && pageindex < htmlFiles.length) {
        fileName = htmlFiles[pageindex];
        page.open(htmlFiles[pageindex]);
    }
    if (pageindex == htmlFiles.length) {
        phantom.exit();
    }
}, 250);

page.onLoadStarted = function() {
    loadInProgress = true;
    console.log('Page ' + (pageindex + 1) + '/' + totalCount + ' load started');
};

page.onLoadFinished = function(status) {
    loadInProgress = false;
    var outputFileName = fileName.replace(inputdir, outputdir);
    console.log('Writing output to ' + outputFileName);
    var file = fs.open(outputFileName, "w");
    file.write(page.content);
    file.close();
    pageindex++;
}