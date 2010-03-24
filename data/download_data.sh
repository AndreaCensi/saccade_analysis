#!/bin/bash
wget http://www.cds.caltech.edu/~andrea/pri/data/20100319-flies.zip
unzip 20100319-flies.zip
mv 20100319-flies/* .
rm 20100319-flies.zip
rmdir 20100319-flies
