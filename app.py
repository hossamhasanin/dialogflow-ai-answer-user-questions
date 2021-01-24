import os
from flask import *
import random
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from .askingForInfo import *


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'XYZ')

# Use a service account
cred = credentials.Certificate('/app/flask_heroku_example/hgtms-alpha-1b9a98d55c7b.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

# WelcomeIntent
def welcomeIntent(req):
    username = req["queryResult"]["parameters"]["username"]
    users = db.collection(u"users").where(u"name" , u"==" , username).get()
    if (username != ""):
        welcomeResponsesWithkownName = [
            "Hi {} I am Mr moon in your service and it is my pleasure to talk to you".format(username) ,
            "Hey {} ! I am Mr moon an intelegent assistant and i think it is gonna be a nice relationship between us".format(username)
        ]
        n = 0
        for user in users:
            n = n + 1
        if (n > 0):
           return  make_response(jsonify({'fulfillmentText': welcomeResponsesWithkownName[random.randint(0,(len(welcomeResponsesWithkownName)-1))]})) 
        else :
            additionReply = [
                        "So {} , I have added you to my database so it is my pleasure to know you".format(username)
                        , "{} ! I think you are lucky to know me :) ".format(username)
                    ]
            query = {
                        u"name": username,
                        u"lastname": u"",
                        u"nickname": u"",
                        u"loveScore": 0,
                        u"develpoer": False,
                        u"teachingScore": 0
                    }
            db.collection(u"users").add(query)
            return  make_response(jsonify({'fulfillmentText': additionReply[random.randint(0,(len(additionReply)-1))]})) 
    else:
        welcomeResponsesWithUnkownName = [
                "Hi I am in your service and it is my pleasure to know you but first ... what is your name ?" 
                , "Hey ! I am an intelegent assistant and i think it is gonna be a nice relationship between us but first of all tell me your name !!"
        ]
        return  make_response(jsonify({'fulfillmentText': welcomeResponsesWithUnkownName[random.randint(0,(len(welcomeResponsesWithUnkownName)-1))]})) 

# getUserName-yes intent
def saveUsername(req):
    username = req["queryResult"]["parameters"]["username"]
    responses = [
            "Yupp ! , It is my pleasure to add you to my users this wil give me more experience , How can i help you ?" ,
            "And now i know you , so tell me how can i help you ?"
        ]
    query = {
                u"name": username,
                u"lastname": u"",
                u"nickname": u"",
                u"loveScore": 0,
                u"develpoer": False,
                u"teachingScore": 0
            }
    db.collection(u"users").add(query)
    return  make_response(jsonify({'fulfillmentText': responses[random.randint(0,(len(responses)-1))]})) 

# getUserName intent
def getUserName(req):
    username = req["queryResult"]["parameters"]["username"]
    saveNameResponse = [
            "You have got a nice name {} , do you want me to remember you ?".format(username) ,
            "It is a nice name {} , do you want me to remember you ?".format(username)
        ]
    knowYouResponsess = [
            "Hey , it seems to me that we have met before , i have you name in my database welcome agian {}".format(username)
    ]      
    users = db.collection(u"users").where(u"name" , u"==" , username).get()
    n = 0
    for user in users:
            n = n + 1
    if (n > 0):
        return  make_response(jsonify({'fulfillmentText': knowYouResponsess[random.randint(0,(len(knowYouResponsess)-1))]})) 
    else :
        query = {
                    u"name": username,
                    u"lastname": u"",
                    u"nickname": u"",
                    u"loveScore": 0,
                    u"develpoer": False,
                    u"teachingScore": 0
                }
        db.collection(u"users").add(query)
        return  make_response(jsonify({'fulfillmentText': saveUsername[random.randint(0,(len(saveUsername)-1))]}))
      


@app.route('/' , methods=['POST'])
def index():
    req = request.get_json(silent=True)
    intent = req["queryResult"]["intent"]["displayName"]
    if (intent == "DefaultWelcomeIntent"):
        return welcomeIntent(req)
    if (intent == "getUserName-yes"):
        return saveUsername(req)  
    if (intent == "getUserName"):
        return getUserName(req)
    if (intent == "who_is_he"):
        return askingForInfo().whoIsHe(request)
    if (intent == "what_is_that"):
        return askingForInfo().whatIsThat(request) 
    if (intent == "what_is_that - more"):
        theThing = req["queryResult"]["outputContexts"][0]["parameters"]["thing"]
        return askingForInfo().giveMoreLinks(request , theThing)
    if (intent == "who_is_he - more"):
        name1 = req["queryResult"]["parameters"]["name1"].replace("?" , "").lower().title()
        name2 = req["queryResult"]["parameters"]["name2"].replace("?" , "").lower().title()
        if name2 != "":
            fullName = name1 + "_" + name2
        else :
            fullName = name1 
        rightName = fullName
        return askingForInfo().giveMoreLinks(request , fullName) 
    if (intent == "how_to"):
        return askingForInfo().howTo(request)              
              

@app.route('/test' , methods=['Get'])
def test():
        url = 'https://www.google.com/search?q=ufa+wiki'
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

@app.route('/test2' , methods=['Get'])
def test2():
        import re
        url = 'https://www.google.com/search?q=black holes'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        cleaned = []
        for f in soup.find_all("div" , "g")[1:]:
            g = f.div.a.get("href").encode("utf-8").decode()
            getTheLink = re.findall("https:.*%252" , g)
            if not getTheLink:
                pass
            else:
                cleaned = getTheLink[0].replace("%252" , "")    
                return cleaned         