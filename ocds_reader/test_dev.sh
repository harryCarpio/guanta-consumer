#!/bin/sh

pip3 uninstall ocds-reader
pip3 install .
# ocds-reader -m batch -y 2023 -k CUMBAYA
ocds-reader -y 2023 -m batch  -f "/Users/harry/Code/OjoSeco/guanta-consumer/ocds_reader/util/data/ciudades.txt"