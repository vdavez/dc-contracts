#!/bin/bash
echo "------"
HOME=/home/vzvenyach
date
cd ~/Coding/dc-contracts
git checkout master
python scrapers/solesource.py
git checkout gh-pages
git rebase master
git push origin gh-pages
git checkout master