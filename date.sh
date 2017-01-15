#!/bin/sh


while true; 
do 
 date=(date + %N);
 watch -n 10 $date
 sleep 10; 
done
