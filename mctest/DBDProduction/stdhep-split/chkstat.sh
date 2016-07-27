#!/bin/bash

fn=`(/bin/ls -tr */*.log | tail -1 )`
echo $fn 
tail -10 $fn
