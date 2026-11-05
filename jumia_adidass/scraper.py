import smtplib
import schedule
import pandas as pd
import os
from dotenv import load_dotenv
import time
from email.message import EmailMessage
from playwright.sync_api import sync_playwright
load_dotenv()
limite=300
def sifet_rapport():
    with sync_playwright()as p:
        browser=p.chromium.launch(headless=False)
        page=browser.new_page()
        data=[]
        for n in range(1,4):
            url=f'https://www.jumia.ma/catalog/?q=adidas&page={n}'
            page.goto(url,wait_until='domcontentloaded',timeout=60000)
            page.wait_for_timeout(5000)
            page.mouse.wheel(0,3000)
            page.wait_for_timeout(2000)
            adidas=page.locator('article.prd').all()
            print(len(adidas))
            for i in adidas:
                try:
                    tatel=i.locator('h3.name').first.inner_text(timeout=1000)
                    prex=i.locator('div.prc').first.inner_text(timeout=1000)
                    lenc_adidas=i.locator('a.core').first.get_attribute('href',timeout=1000)
                    prex=prex.replace('Dhs','').replace('Dès','').replace(',','').strip()
                    
                    data.append([tatel,prex,lenc_adidas])
                except Exception as e:
                    print(e)
        browser.close()
    df = pd.DataFrame(data,columns=['tatle','prex','lenc_adidas'])
    df = df.drop_duplicates()
    df = df.dropna()
    df ['prex']= df ['prex'].astype(float)
    print(df['prex'].head())
    df = df.sort_values(by='prex', ascending=False)
    df_alerte = df[df['prex']<=limite]
    print(df_alerte)
    with pd.ExcelWriter('adidass_clena.xlsx',engine='openpyxl') as writer:
        df.to_excel(writer,index=False,sheet_name='BOOKS')
    df.to_csv('jumia_adidass/adidass_result.csv',index=False,encoding='utf-8-sig')
    gmail=os.getenv('GMAIL')
    gmail_persson= os.getenv('GMAIL_TO')
    pasword_gmail= os.getenv('GMAIL_PASSWORD')
    msg=EmailMessage()
    msg['from']=gmail
    msg['to']=gmail_persson
    if len(df_alerte)>0:
        msg['subject'] = 'adidass price alert'
        msg.set_content(f'price drop alert!{len(df_alerte)} products are at or below {limite} dhs.')
    else:
        msg['subject'] = 'adidass price report'
        msg.set_content('no price drops today .')
    
    with open('adidass_clena.xlsx','rb')as f:
        msg.add_attachment(f.read(),maintype='application',subtype='octet_stream',filename='adidass_clena.xlsx')
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(gmail,pasword_gmail)
    server.send_message(msg)
    server.quit()
sifet_rapport()
schedule.every().day.at("09:00").do(sifet_rapport)
while True:
    schedule.run_pending()
    time.sleep(60)
    print('mcha ')