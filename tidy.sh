#!/bin/bash
for f in `find build/ -type f`; do echo $f; tidy -i -asxhtml -f tmp/$f.error -o $f $f; done | tee logs/tidy-`date +%Y%m%d%H%M%S`.log