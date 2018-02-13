import pandas as pd
import json
import csv
from pandas.io.json import json_normalize
import sys
import os
##load json data from /Users/daithang1111/Documents/datasets/Australia-Representatives.json
# data = json.load(open('/Users/daithang1111/Documents/datasets/Australia-Representatives.json','r'))
#print(data.keys())  
#print(json.dumps(data['persons'][0],indent=2))
# print (type(data['persons'][0]['contact_details']))
# print (data['persons'][0].keys()) 
# for item, value in data['persons'][0].items():
#     print (item, type(value))
def flatten_json(y):
        out={} # define out as a dictionary
        def flatten(x, name=''):
            #print('flattening',x)
            if type(x) is dict:
                for a in x:
                    #print(a, 'is a dictionary key')
                    flatten(x[a], name + a + '_')
            elif type(x) is list:
                #print(x, 'is a list')
                i=0
                for a in x:
                    #print (a, 'is a list item')
                    #print (name + str(i) + '_')
                    flatten(a, name + str(i) + '_')
                    i +=1
            else:
                out[name[:-1]] = x
        flatten(y)
        return out
def jsontocsv(data, outfile, tagname):

    data = json.load(open(data,'r'))   
    flat1 = json_normalize(flatten_json(data[tagname][0]))
    for person in data[tagname][1:]:
        flat = json_normalize(flatten_json(person))
        flat1= pd.concat([flat1, flat])
    flat1.to_csv(outfile)

#####################################################
## input single file
# print (sys.argv)
# infile = sys.argv[1]
# outfile=sys.argv[2]
# key=sys.argv[3]
# jsontocsv(infile,outfile,key)
## infile = '/Users/daithang1111/Documents/datasets/Australia-Representatives.json' 
## outfile= '/Users/daithang1111/Documents/datasets/Australia-Representatives.csv'
## jsontocsv(infile,outfile,'persons')

#####################################################
# input entire folder
def json_normalize_onelevel(y):
    out={} # define out as a dictionary
    for a in y:   
        out[a] = str(y[a])
    return json_normalize(out)
tagname = sys.argv[1]
infolder = sys.argv[2]
outfile=sys.argv[3]

i=0
for filename in os.listdir(infolder):
    print('filename',filename)
    try:
        loadfile = json.load(open(infolder + '/' + filename,'r'))
    except Exception as err:
        print("Co loi:",err)
        continue
    
    if i==0:  
        allpersons = json_normalize_onelevel(loadfile[tagname][0])
        #print('allpersons',type(allpersons))
        allpersons['fromfile']=filename
        allpersons['person_number']=0
        c=1
        for person in loadfile[tagname][1:]:
            nextperson = json_normalize_onelevel(person)
            nextperson['fromfile']=filename
            nextperson['person_number']=c
            #print('nextperson',type(nextperson))
            allpersons = pd.concat([allpersons, nextperson])
            c+=1
    else:
        c=0
        for person in loadfile[tagname]:
            nextperson = json_normalize_onelevel(person)
            nextperson['fromfile']=filename
            nextperson['person_number']=c
            allpersons = pd.concat([allpersons, nextperson])
            c +=1
    i += 1
    print(i)
allpersons.to_csv(outfile, encoding='utf-8')
## find out common keys across dictionaries
# keyset=set(allkey[0])
# for k in allkey[1:]:
#     keyset.update(k)
# print(keyset,'len', len(keyset)) ##{'id', 'name'}


 
    