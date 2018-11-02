import re
import locale ##### added for assignment 2
import pprint ##### added for assignment 2

import input_output

def beolingus_as_list(file):
    lines = []
    with open(file, mode='r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip()
            if not line.startswith('#'):
                lines.append(line)
    return lines

def txt_as_list(file):  ####### NEW - almost the same as beolingus_as_list but maybe useful in the future
    lines = []
    with open(file, mode='r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip()
            lines.append(line)
    return lines

def split_beolingus(lines):
    beo_dict = {}
    for i, line in enumerate(lines):
        i += 1
        line_dict = {}
        line = line.split('::')
        german = line[0]
        english = line[1]
        german = german.split('|')
        english = english.split('|')
        # if len(german) != len(english):
        #    print(line)
        for e, l in enumerate(german):
            line_dict[german[e]] = english[e]
        beo_dict[i] = line_dict
    return beo_dict


#beo_list = beolingus_as_list('data/de-en.txt') # auskommentiert
#beo_dict = split_beolingus(beo_list) #auskommentiert
#input_output.write_dict('data/splitted_beolingus.txt', beo_dict) # auskommentiert
#input_output.serialize('data/splitted_beolingus.pickle', beo_dict) # auskommentiert
beo_dict = input_output.deserialize('data/splitted_beolingus.pickle')
pos_pattern = re.compile(r'\{\w+\}')
usg_pattern = re.compile(r'\[\w+\.?\]')
usg_set = set()
counter = 0
for k, v in beo_dict.items():
    # if counter < 10:
    usg_matches = usg_pattern.findall(str(v))
    for match in usg_matches:
        usg_set.add(match)
    counter += 1

usg_set = sorted(usg_set)

#for e in usg_set:
    #print(e)

#######ASSIGNMENT 2#########
almost_sorted_set=usg_set

####### 2. 2. SOLVING THE SORTING PROBLEMS WITH UMLAUTE/UPPERCASE
# I could not really make sense of locale.setlocale(locale.LC_ALL, 'de_DE') etc., so I just tried out
# writing something on my own :-)
# The methods sorts ä after a and before b (not as 'ae' after 'ad' and before 'af') etc. and ignores uppercase.
# Otherwise the Uppercase words would all appear before the lowercase words.

def prepare_word_for_sorting(word): ### Take a word, remove Umlaute and ß, change Upper to Lower case
    word_as_list = []
    umlaute = {
        'ä': 'aä',      #'ä': 'ae',
        'ö': 'oö',      #'ö': 'oe',
        'ü': 'uü',      #'ü': 'ue',
        #'Ä': 'AÄ',      #'Ä': 'Ae',
        #'Ö': 'OÖ',      #'Ü': 'Ue',
        #'Ü': 'UÜ',      #'Ö': 'Oe',
        'ß': 'ss'
    }
    counter = 0
    letter = ''
    for char in word:
        if char.isupper():
            char=char.lower()
        if char in umlaute:
            letter = umlaute.get(char, char)
            word_as_list.append(letter)
        else:
            word_as_list.append(char)
        counter += 1
    word = ''.join(word_as_list)
    return (word)

def sort_list(list):
#creates dictionary {word: word_without_umlaute_or_uppercase} sorts the values (words without umlaute or uppercase)
#and returns list with sorted keys (words with umlaute)
    word_without_umlaute={}
    sorted_list=[]
    for word in list:
        word_without_umlaute[word]=prepare_word_for_sorting(word)
    sorted_list=sorted(word_without_umlaute.items(), key=lambda x: x[1])
    counter=0
    for entry in sorted_list:
        sorted_list[counter]=entry[0]
        counter+=1
    return(sorted_list)

###### 2.1. ADD METHOD FOR WRITING A SET INTO A TEXT FILE#######
sorted_set=sort_list(almost_sorted_set)
input_output.write_set('data/sorted_set.txt', sorted_set)
sorted_set=txt_as_list('data/sorted_set.txt')
#input_output.serialize('data/sorted_set.pickle', sorted_set)
#sorted_set=input_output.deserialize('data/sorted_set.pickle')
pprint.pprint(sorted_set)

#locale.setlocale(locale.LC_ALL, 'de_DE')
#sorted_set=set.sort(key=lambda i: locale.strxfrm(i[0]))

