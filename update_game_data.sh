#!/bin/bash

set -eux

SRC="modelData.js"
DST="modelData.py"
URI="https://monpoc.net/MonpocListBuilder/js/$SRC"
HEADER="# Source: $URI\n# flake8: noqa\n"

# fetches data from monpoc.net list builder skipping BOM
echo -e $HEADER > $SRC
curl $URI | dd bs=1 skip=3 >> $SRC

# add line breaks instead of ;
tr ";" "\n" < $SRC > $DST

# translate null to ""
sed -i.bak "s/null/\"\"/g" $DST

# translate variable names
sed -i.bak "s/var monsters/MONSTERS_DATA/g" $DST
sed -i.bak "s/var units/UNITS_DATA/g" $DST
sed -i.bak "s/var buildings/BUILDINGS_DATA/g" $DST
sed -i.bak "s/var abilities/ABILITIES_DATA/g" $DST

# cleanup
rm $SRC *.bak

# prettify Python code
black $DST

# update module
mv $DST monpoc/game_data.py
