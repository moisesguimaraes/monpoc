#!/bin/bash

mkdir -p csv
./data_to_csv.py Abilities > csv/abilities.csv
./data_to_csv.py Buildings > csv/buildings.csv
./data_to_csv.py Units     > csv/units.csv
./data_to_csv.py Monsters  > csv/monsters.csv