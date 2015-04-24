# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 17:14:29 2015

@author: lorraine
"""

#import csv
#data = ["value %d" % i for i in range(1,10)]
#
#out = csv.writer(open("data/myfile.csv","w"), delimiter=',',quoting=csv.QUOTE_ALL)
#out.writerow(data)

import csv
import json

with open('data/wisker.csv', 'w') as csvfile:
#    fieldnames = ['first_name', 'last_name']
#    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#
#    writer.writeheader()
#    writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
#    writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
#    writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})
    writer = csv.writer(csvfile)
    writer.writerow(["chinese","mexican","pizza","bar"])
    
    with open("data/pizza_B.json","r") as f:
        cat = f.read()
    cat = json.loads(cat)
    pizza_rating = []
    for i in xrange(len(cat["pizza"])):
        score = cat["pizza"][i].values()
        pizza_rating.append(score[0]["rating"])
        
    with open("data/chinese_B.json","r") as f2:
        cat2 = f2.read()
    cat2 = json.loads(cat2)
    chinese_rating = []
    for i in xrange(len(cat2["chinese"])):
        score = cat2["chinese"][i].values()
        chinese_rating.append(score[0]["rating"])
    
    with open("data/mexican_B.json","r") as f3:
        cat3 = f3.read()
    cat3 = json.loads(cat3)
    mexican_rating = []
    for i in xrange(len(cat3["mexican"])):
        score = cat3["mexican"][i].values()
        mexican_rating.append(score[0]["rating"])
        
    with open("data/bars_B.json","r") as f4:
        cat4 = f4.read()
    cat4 = json.loads(cat4)
    bar_rating = []
    for i in xrange(len(cat4["bars"])):
        score = cat4["bars"][i].values()
        bar_rating.append(score[0]["rating"])
        
    total=[]
    for i in xrange(len(mexican_rating)):
        temp=[]
        temp.append(chinese_rating[i])
        temp.append(mexican_rating[i])
        temp.append(pizza_rating[i])
        temp.append(bar_rating[i])
        total.append(temp)
    writer.writerows(total)
     
    