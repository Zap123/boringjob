import requests
import json
import smtplib
from getpass import getpass
import time
from email.mime.message import MIMEMessage
from email.mime.text import MIMEText

class IndeedFetcher:
    """ Query indeed interface 
        Indeed: require free Publisher account 
        http://www.indeed.com/jsp/apiinfo.jsp
    """
    url = "http://api.indeed.com/ads/apisearch"
    def __init__(self):
        self.query["q"] = self.inOR(self.params["keyword"])
    
    with open("fetchers/indeed/prefs.json") as prefs:
        params = json.load(prefs)
        query = params["query"] 

    def inOR(self,keyword):
        ORString = "("
        size = len(keyword)
        for (i,item) in enumerate(keyword):
            ORString += item
            if(i < size -1):
                ORString += " OR "
        return ORString + ")"

    def get(self):
        r = requests.get(self.url, params=self.query)
        text = "JOB OPPORTUNITIES " + time.strftime("%d/%m/%Y")
        self.sendToMail(self.message(r.content),text)
    
    def message(self, content):
        dict_json = json.loads(content.decode('utf-8'))
        msg = "Hej! Here your latest job opportunities for the last " 
        msg += str(self.query["fromage"]) + " day/s"
        msg += "<ol>"
        for (i,item) in enumerate(dict_json[u'results']):
            el = dict_json[u'results'][i]
            msg += "<li>"
            msg += el[u'jobtitle']+"<br>"  
            msg += el[u'company']+"<br>"  
            msg += el[u'city'] +"<br>"  
            msg += el[u'snippet'] +"<br>"  
            msg += "<a href="+ el[u'url'] +">Read more<a>"
            msg += "</li><br>"
        msg += "</ol> <br>"
        return msg
    
    def sendToMail(self, TEXT, SUBJECT):
        msg = MIMEText(TEXT,'html','utf-8')
        msg['Subject'] = SUBJECT
        msg['From'] = self.params["email"]["from"]
        msg['To'] = self.params["email"]["to"]

        smtp_server = self.params["email"]["smtp"]
        server = smtplib.SMTP(smtp_server)
        server.ehlo()
        #server.starttls()
        if self.params["email"]["password"] == "":
            self.params["email"]["password"] = getpass("Insert SMTP password: ")
        server.login(self.params["email"]["user"],str(self.params["email"]["password"]))
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
