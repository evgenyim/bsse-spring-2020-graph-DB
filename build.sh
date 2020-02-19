#!/bin/bash
if pip3 install pytest && pip3 install rdflib
then
echo -e "\E[32mComplete"
else
echo -e "\E[31m Error"
fi