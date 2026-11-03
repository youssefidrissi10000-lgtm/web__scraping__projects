import pandas as pd
from playwright.sync_api import sync_playwright
import random
with sync_playwright()as p:
    brosser=p.chromium.launch(headless=False)
    page=brosser.new_page()
    data=[]
    for n in range(1,3):
        url=f"https://www.avito.ma/fr/maroc/ordinateurs_portables/laptop_gamer--%C3%A0_vendre?delivery=true&page={n}"
        try:
            page.goto(url,wait_until='domcontentloaded',timeout=60000)
        except Exception as e:
            print(e)
            break
        page.wait_for_timeout(5000)
        page.mouse.wheel(0,3000)
        page.wait_for_timeout(2000)
        page.wait_for_timeout(random.randint(3000,10000))
        laptop=page.locator('div.listing>div').all()
        print(len(laptop))
        if len(laptop)==0:
            break
        for s in laptop:
            try:
                tatle=s.locator('h3').first.inner_text(timeout=1000)
                prices=s.locator("span:has-text('DH')").first.inner_text(timeout=1000)
                lien_prodwe=s.locator('a').first.get_attribute( 'href' ,timeout=1000)
                price_dh=float(prices.replace('DH','').replace('\u202f','').strip())
                data.append([tatle,price_dh,lien_prodwe])
            except Exception as e:
                print(e)

    brosser.close()
    
df = pd.DataFrame(data,columns=['tatle','price_dh','lien_prodwe'])
df = df.drop_duplicates()
df = df.dropna()
expensive = df[df['price_dh']>6000]
print(expensive)
df = df.sort_values(by='price_dh', ascending=False)
with pd.ExcelWriter('laptop_clena.xlsx',engine='openpyxl') as writer:
    df.to_excel(writer,index=False,sheet_name='BOOKS')
df .to_csv('avito_laptops.csv',index=False,encoding='utf-8-sig')

