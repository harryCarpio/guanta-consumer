#!/bin/sh

input="data/ciudades_full.txt"
while IFS= read -r line
do
  ocds-reader -m batch -y 2023 -k "$line"
  wait
done < "$input"



ocds-reader -y 2023 -m batch  -f "/Users/harry/Code/OjoSeco/guanta-consumer/ocds_reader/util/data/ciudades.txt"