import requests
from bs4 import BeautifulSoup

import pandas as pd
data=[]
for book in range(1,10):
    header={'User-Agent':'Mozilla/5.0'}
    url=f"https://books.toscrape.com/catalogue/page-{book}.html"
    wb=requests.get(url,headers=header)
    def mini(wb):
        src=wb.content
        suup=BeautifulSoup(src,'html.parser')
        ctoba=suup.find('ol',{'class':'row'})
        ctobaa=ctoba.find_all('li')
        for n in ctobaa:
            try:
                tatle=n.find('h3').find('a').get('title')
                price=n.find('p',{'class':'price_color'}).text
                price_book=float(price.replace('£','').replace('Â','').strip())
                data.append([tatle,price_book])
                
            except Exception as e:
                print(e)
    mini(wb)
    df = pd.DataFrame(data, columns=['tatle','price_book'])
    df = df.drop_duplicates()
    df = df.dropna()
    expensive = df[df['price_book']>20]
    print(expensive)
    df = df.sort_values(by='price_book', ascending=False)
with pd.ExcelWriter('book_clena.xlsx',engine='openpyxl') as writer:
    df.to_excel(writer,index=False,sheet_name='BOOKS')