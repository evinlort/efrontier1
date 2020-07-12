#!/bin/bash

for COUNTER in {10..35}
do

python3.8 run.py $COUNTER
echo "coefficient: $COUNTER - profit:"  `node evaluator.js`

done
