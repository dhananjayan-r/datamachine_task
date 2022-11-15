finalized=[]
import csv
import urllib
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'), ('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'), ('Accept-Encoding','gzip, deflate, br'),\
        ('Accept-Language','en-US,en;q=0.5' ), ("Connection", "keep-alive"), ("Upgrade-Insecure-Requests",'1')]
urllib.request.install_opener(opener)  
browser = webdriver.Chrome(r"C:\Users\Dhananjayan\Downloads\chromedriver_win32\chromedriver.exe")
browser.get('https://www.asos.com/fr/femme/costumes-et-pieces-depareillees/blazers/cat/?cid=11896')
#getting the pagesource and reading the source
pageSource = browser.page_source
soup = BeautifulSoup(pageSource, 'lxml')
location_containers = soup.find_all('article')
#location_containers
data=[]
for job in location_containers:
    linkers = job.find("a")
    data.append(linkers['href'])
    print(linkers['href'])
    #print(job)

for i in data:
    if len(finalized) < 15:
        try:
            browser.get(i)
            #getting the pagesource and reading the source
            pageSource = browser.page_source
            soup2 = BeautifulSoup(pageSource, 'lxml')
            diction = {}
            extracts = soup2.find(id="chrome-breadcrumb").find_all('a')
            diction['Product_URL'] = i
            diction['Brand'] = soup2.find_all(id='pdp-react-critical-app')[0].find_all('h1')[0].text.split(" - ")[0]
            diction['Collection'] = extracts[1].text
            diction['Category'] = extracts[3].text
            diction['Color'] = soup2.find_all(id='pdp-react-critical-app')[0].find_all('div')[-1].find('p').text
            diction['Designation'] = soup2.find_all(id='pdp-react-critical-app')[0].find_all('h1')[0].text.split(" - ")[1]
            strrer = []
            for tex in soup2.find(class_='product-description').find('ul').find_all('li'):
                strrer.append(tex.text)
            diction['Description'] = ", ".join(strrer)
            diction['Product Code'] = soup2.find(class_='product-code').find('p').text
            diction['Current Price'] = soup2.find_all(id='pdp-react-critical-app')[0].find_all('div')[0].find_all('span')[0].text
            finalized.append(diction)
        except:
            continue

with open('datasscraped.csv', 'w+') as csvfile:
    writer = csv.DictWriter(csvfile,fieldnames=['Product_URL', 'Brand', 'Collection', 'Category', 'Color', 'Designation', 'Description', 'Product Code', 'Current Price'])
    writer.writeheader()
    writer.writerows(finalized)