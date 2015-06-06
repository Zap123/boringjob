#
# Indeed: require free Publisher account 
# http://www.indeed.com/jsp/apiinfo.jsp
# 

import requests
import json
import smtplib
import time
from email.mime.message import MIMEMessage
from email.mime.text import MIMEText

class IndeedFetcher:
    url = "http://api.indeed.com/ads/apisearch"
    with open("modules/fetchers/indeed/prefs.json") as prefs:
        params = json.load(prefs)
        query = params["query"] 
    
    def __init__(self):
        self.query["q"] = self.inOR(self.params["keyword"])

    def inOR(self,keyword):
        ORString = "("
        size = len(keyword)
        for (i,item) in enumerate(keyword):
            ORString += item
            if(i < size -1):
                ORString += " OR "
        return ORString + ")"

    def get(self):
        """ Query indeed interface"""
        print(self.query)
        r = requests.get(self.url, params=self.query)
        print(r.url)
        self.sendToMail(self.results(json.loads(r.content.decode('utf-8'))), 
                "JOB OPPORTUNITIES " + time.strftime("%d/%m/%Y"))
    
    def results(self, dict_json):
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
        print(msg)
        return msg
    
    def sendToMail(self,TEXT, SUBJECT):
        msg = MIMEText(TEXT,'html','utf-8')
        msg['Subject'] = SUBJECT
        FROM = self.params["email"]["from"]
        msg['From'] = FROM
        TO = self.params["email"]["to"]
        msg['To'] = TO
        smtp_server = self.params["email"]["smtp"]

        server = smtplib.SMTP(smtp_server)
        #server.starttls()
        server.set_debuglevel(1)
        print(TEXT)
        server.sendmail(FROM, TO, msg.as_string())
        server.quit()


if __name__ == "__main__":
    IndeedFetcher().get()
