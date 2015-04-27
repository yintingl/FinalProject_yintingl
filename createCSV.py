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

def load_rating_data(category):
    with open("data/{0}_B.json".format(category),"r") as f:
        cat = f.read()
    cat = json.loads(cat)
    pizza_rating = []
    for i in xrange(len(cat[category])):
        score = cat[category][i].values()
        pizza_rating.append(score[0]["rating"])
    return pizza_rating
    


with open('data/wisker.csv', 'wb') as csvfile:
#    fieldnames = ['first_name', 'last_name']
#    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#
#    writer.writeheader()
#    writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
#    writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
#    writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})
    writer = csv.writer(csvfile)
    writer.writerow(["chinese","mexican","pizza","bars","bbq","southern","steak"])
    
    pizza_rating=load_rating_data("pizza")
    mexican_rating=load_rating_data("mexican")
    chinese_rating=load_rating_data("chinese")
    bar_rating=load_rating_data("bars") 
    bbq_rating=load_rating_data("southern")
    southern_rating=load_rating_data("bbq")
    steak_rating= load_rating_data("steak")
   
        
    total=[]
    for i in xrange(len(mexican_rating)):
        temp=[]
        temp.append(chinese_rating[i])
        temp.append(mexican_rating[i])
        temp.append(pizza_rating[i])
        temp.append(bar_rating[i])
        temp.append(bbq_rating[i])
        temp.append(southern_rating[i])
        temp.append(steak_rating[i])
        total.append(temp)
    writer.writerows(total)
     
    