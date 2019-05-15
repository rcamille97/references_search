#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 19:11:37 2019

@author: camillemac
"""

from modules import Search as Search

def search():
    s1 = Search.Microsoft("multi-objective optimization", 50)
    s2 = Search.SagePub("multi-objective optimization", 10)
    s1.search()
    s2.search()
    i=0
    for p in s1.getListOfResults():
        i = i+1
        print(p.displayData())
    print(i) #Check the number of results


search()
