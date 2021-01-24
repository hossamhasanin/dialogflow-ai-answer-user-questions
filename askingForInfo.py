import requests
from flask import make_response , jsonify
import random
from bs4 import BeautifulSoup
import re

class askingForInfo:

    def getRightName(self , q):
        url = 'https://www.google.com/search?q='+ q +'+wiki'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        finallName = "koko"
        for f in soup.find_all("div" , "g"):
            g = f.div.div.text.encode("utf-8")
            if b'https://en.wikipedia.org/' in g:
                finallName = g.decode().replace('https://en.wikipedia.org/wiki/' , '').replace("CachedSimilar","")
                return finallName        
                break  
        return finallName   

    def whatIsThat(self , req):
        data = req.get_json(silent=True)
        theThing = data["queryResult"]["parameters"]["thing"]
        res = ["Well i have tried to find more infos about this but unfortunatlly i couldn't , maybe you entered a wrong name",
                "Ops , i think that you might type something wrong and in that case i think you should be sure about what you are saying before saying it"]
        try:
            rightName = self.getRightName(theThing)
        except:
            print("Error while searching")
            return "Error in searching"
        wikiApi = requests.get("https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles={}&exsentences=4&explaintext=1".format(rightName)).json()
        for p in wikiApi["query"]["pages"]:
            if p != "-1":
                extractedData = wikiApi["query"]["pages"][p]["extract"].encode('ascii', errors='ignore').strip().decode('ascii')
                if extractedData == "":
                    extractedData = res[random.randint(0 , len(res)-1)]
                else:
                    extractedData = "According to my knowledge : " + extractedData
            else :
                extractedData = "Well i have tried to find more infos about this but unfortunatlly i couldn't , maybe you entered a wrong name"
        return make_response(jsonify({'fulfillmentText': extractedData}))        

    def giveMoreLinks(self , req , query):
        data = req.get_json(silent=True)           
        url = "https://www.google.com/search?q="+query
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        extractedData = "I think i have some links for you look at those : \n \n "
        count = 0
        for f in soup.find_all("div" , "g"):
            try:
                g = f.div.div.a.get("href").encode("utf-8").decode()
                if "webcache" in g:
                    clean = re.findall("https:.*%252" , g)[0].replace("%252" , "")
                elif "q=" in g:
                    clean = re.findall("q=.*.html&" , g)[0].replace("q=" , "").replace("&" , "")
                else:
                    extractedData = "I think that i have some bad news here , i didn't find links for you !"
                    count = 0
                    break        
                count += 1
                extractedData += clean + "\n \n" 
            except:
                print("this is Error")            
        if count == 0:
                extractedData = "I think that i have some bad news here , i didn't find links for you !"
        else:
                extractedData += "\n \n .... that is all that i have got for now"         
        return make_response(jsonify({'fulfillmentText': extractedData}))  

    def whoIsHe(self , req):
        data = req.get_json(silent=True)
        name1 = data["queryResult"]["parameters"]["name1"].replace("?" , "").lower().title()
        name2 = data["queryResult"]["parameters"]["name2"].replace("?" , "").lower().title()
        res = ["Well i have tried to find more infos about this but unfortunatlly i couldn't , maybe you entered a wrong name",
                "Ops , i think that you might type something wrong and in that case i think you should be sure about what you are saying before saying it"]
        if name2 != "":
            fullName = name1 + "_" + name2
        else :
            fullName = name1 
        rightName = fullName   
        try:
            rightName = self.getRightName(fullName)
        except:
            print("Error while searching")
        wikiApi = requests.get("https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles={}&exsentences=4&explaintext=1".format(rightName)).json()
        for p in wikiApi["query"]["pages"]:
            if p != "-1":
                extractedData = wikiApi["query"]["pages"][p]["extract"].encode('ascii', errors='ignore').strip().decode('ascii')
                if extractedData == "":
                    extractedData = res[random.randint(0 , len(res)-1)]
                else:
                    extractedData = "According to my knowledge : " + extractedData
            else :
                extractedData = "Well i have tried to find more infos about this but unfortunatlly i couldn't , maybe you entered a wrong name"
        return make_response(jsonify({'fulfillmentText': extractedData}))    

    def howTo(self , req):
        data = req.get_json(silent=True)
        actions = data["queryResult"]["parameters"]["thing"].replace("?" , "").lower()
        url = 'https://www.google.com/search?q=how to '+actions+' ?'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        extractedData = "I know something : \n \n"
        try:
            g = soup.find("div" , "g").find_all("li")
            for f in g:
                extractedData += f.text + "\n \n"
        except:
            print("I have just links for you")
        if extractedData == "I know something : \n \n":
            return self.giveMoreLinks(req , actions)
        else:                    
            return make_response(jsonify({'fulfillmentText': extractedData}))     
            
