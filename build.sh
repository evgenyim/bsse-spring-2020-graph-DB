#!/bin/bash
if pip3 install -r requirements.txt
then
echo -e "\E[32mComplete"
else
echo -e "\E[31m Error"
fi