import requests
from bs4 import BeautifulSoup
import re
import smtplib

def info(url_temp,max_price,mail_id,password1):
    url = url_temp
    #user agaent is important otherwiase ur req is classifed as robofied
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"}

    req = requests.Session()
    res = req.get(url,headers=header)
    #print(res.text)
    price(max_price,mail_id,password1,res)

def price(max_price,mail_id,password1,res):
    soup = BeautifulSoup(res.text,features='html.parser')
    price_find = soup.find(id='priceblock_ourprice').get_text()
    #print(price_find)
    price_find = float(re.sub('\,','',price_find[2:]))
    title = soup.find(id='productTitle').get_text()
    title = title.strip()
    print(title,': ',price_find)

    if(price_find<max_price):
        mail_it(price_find,title,mail_id,password1)
    else:
        print('High price')

def mail_it(cost,heading,mail_id,passw):
    serv = smtplib.SMTP('smtp.gmail.com',587)
    serv.ehlo()
    serv.starttls()
    serv.ehlo()
    #print('Hello')
    try:
        serv.login(mail_id,password='passw')
        subject = 'Falling prices!!'
        body = 'Prices are down!! \n\n Product: ' + str(heading) + ' Price now: ' + str(cost)

        msg = 'subject: '+subject +'\n\n' + body

        serv.sendmail(
            mail_id,
            mail_id,
            msg
        )
        print('mail sent')
    except:
        print('Some error')

###amazon usrl for product
url = input('Enter url for product: ')
###what is the max price you can adfford the product for
max_price = int(input('Enter max price: '))
####your email id
email = input('Enter your email: ')
###your laptop/pc app password for gmail you can generate it by reading this link : https://support.google.com/accounts/answer/185833
passw = input('Enter google app password: ')
info(url,max_price,email,passw)
#price(max_price=max_price,mail_id=email,password1=passw)
