# ******************************************************************************
# Author:           Proxima-L3
# Date:             Marcch 28, 2022
# Description:      A program that uses web scraping to make lists of names
#                   from websites and uses them to help the user create anagrams.
# Goal/purpose:     Learn how to use web scraping, practice searching for and
#                   using random libraries/modules/functions that solve a problem
#                   in my algorithm,
# Sources:          https://en.wikipedia.org/wiki/List_of_Greek_mythological_figures.
#                   (And minimal review from one of my Udemy courses)
# ******************************************************************************


import requests
import bs4
import bisect

# assigning the html page to a variable via get request
wiki_request1 = requests.get('https://en.wikipedia.org/wiki/List_of_Greek_mythological_figures')

# using beautiful soup to make raw html code organized
wiki_soup = bs4.BeautifulSoup(wiki_request1.text, 'lxml')

# making a list of all a tags in the html document
raw_atag_list = wiki_soup.select('a')


# for loop with several if statements that filter out the unwanted things in my code, specifically names with ints,
#single letters, and repeats of names

keyword_gibberish_list = ['',' ','q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m',"'",'`','~','!','@','#','$','%','^','&','*','(',')','-','=','_','+','[',']','{','}','|',';',':','"',',','.','/','<','>','?']
filtered_atag_list = []
int_list = [1,2,3,4,5,6,7,8,9,0]
has_int = False

for item in raw_atag_list:
    item = item.getText()

    for num in int_list:
        if str(num) in item:
            has_int = True
            break
        else:
            has_int = False

    if has_int == True:
        continue
    if item.lower() in keyword_gibberish_list:
        pass
    elif item in filtered_atag_list:
        pass
    else:
        bisect.insort(filtered_atag_list, item)


print(filtered_atag_list)
