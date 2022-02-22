import requests
from bs4 import BeautifulSoup
import sys
import re
from lxml import etree
import threading

bing = "https://search.aol.com/aol/search?q="
proxy = {"https":"http://proxy.rcub.bg.ac.rs:8080"}
xpth = '/html/body/div[1]/div[3]/div/div/div[1]/div/ol[1]/li/div/div/h5/span'

class Rec:
    def __init__(self, word, number):
        self.word = word
        self.number = number

    def __lt__(self, other):
        return self.number < other.number

def get_number(word):
    page = requests.get(bing + word, proxies=proxy).text
    soup = BeautifulSoup(page,'html.parser')
    gas = etree.HTML(str(soup))
    
    if gas == None:
        return 0

    mid = gas.xpath(xpth)[0].text
    broj_str = re.search(r"([0-9,]+)",mid)
    broj = int(broj_str.groups()[0].replace(',',''))
    return broj
    
ulazni_fajl = open(sys.argv[1],"r")
izlazni_fajl = open(sys.argv[2],"w")
words = ulazni_fajl.readlines()
reci = []

def jobic(wrds):
    for word in wrds:
        broj = get_number(word)
        reci.append(Rec(word,broj))
        izlazni_fajl.write(word[:-1] + "," + str(broj) + "\n")
        print("Obradjena rec: " + word[:-1])
        print(threading.active_count())

t_count = int(sys.argv[3])
some_such =  int(len(words) / t_count)

threads = []

for i in range(t_count):
    t = threading.Thread(target=jobic,args=(words[i * some_such:(i + 1) * some_such],))
    t.daemon = True
    threads.append(t)

for i in range(t_count):
    threads[i].start()

for i in range(t_count):
    threads[i].join()




