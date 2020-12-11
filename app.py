from flask import Flask, render_template, url_for, flash, session
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import numpy 
from dataframe import orderDF
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/stats')
def stats():
    return render_template('stats.html')

@app.route('/ordered', methods=['POST'])
def order():

    orderDF()
    order = pd.read_csv(r'path\to\csv\order.csv')

    heads = order.head(1)
    end = order.tail(1)

    heads.to_csv('path\to\csv\head.csv')
    end.to_csv('path\to\csv\end.csv')

    heads = pd.read_csv('path\to\csv\head.csv')
    end = pd.read_csv('path\to\csv\end.csv')

    a = heads.loc[0,:]
    b = end.loc[0,:]

    a = list(a)
    b = list(b)

    dictionary = dict(zip(a,b))

    k = []
    v = []

    timestamp = dictionary['Timestamp']
    del(dictionary['Timestamp'])

    email = dictionary['Email address']
    del(dictionary['Email address'])

    name = dictionary['Name']
    del(dictionary['Name'])

    address = dictionary['Address']
    del(dictionary['Address'])

    phoneNumber = dictionary['Phone number']
    del(dictionary['Phone number'])

    request = dictionary["Any requests? We'll try our best to pass it on to the kitchen."]
    del(dictionary["Any requests? We'll try our best to pass it on to the kitchen."])

    for key, value in dict(dictionary).items():
        if type(value) != numpy.float64:
            k.append(key)
            v.append(value)

    k.pop(0)
    v.pop(0)
    
    order = ''
    for i in range(0,len(k)):
        dqty = str(k[i]) + ' : ' + str(v[i]) + '\n'
        order = order + dqty

    details = [
        {
        'Name':name, 
        'Timestamp':timestamp, 
        'Address':address, 
        'Number':phoneNumber, 
        'Email':email, 
        'Request':request,
        }
    ]

    footer = 'Your order was ordered at ' + str(timestamp) + '\n Address: ' + str(address) + '\n Customer Phone Number: ' + str(phoneNumber) + '\n Customer Email ID: ' + str(email) + '\n You requested for: ' + str(request)
    footer = str(footer)
    body = '\n Hi '+ name +', greetings from The Grubbery. Your order is: \n'
    body = body + order + footer
    print(body)

    recieverEmail = email, "<sender email>"
    serverEmail = "smtp.gmail.com"   
    senderEmail = "<sender email>"
    senderPassword = "<sender email account password>"


    msg = MIMEMultipart()
    msg['From'] = senderEmail
    msg['To'] = recieverEmail
    msg['Subject'] = "Thanks for ordering from The Grubbery"
    msg.attach(MIMEText(body,'plain'))

    try:
        s = smtplib.SMTP(serverEmail, 587)
        s.starttls()
        s.login(senderEmail, senderPassword)                                                                                                                                  
        s.sendmail(senderEmail, recieverEmail, body)
        s.quit()
        print("SUCCESS - Email sent")
        print(recieverEmail)                                                                                                       

    except Exception as e:
        print("FAILURE - Email not sent")
        print(e)
    
    emailed = 'Your order details have been emailed!'
    return render_template('ordered.html', email_status=emailed, details=details)
if __name__ == '__main__':
    app.run(debug=True)