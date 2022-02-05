
from flask import Flask,request
import requests
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime

##globals
Random_Image_URL = (
    "https://source.unsplash.com/random/1080x1080?creator"
)
document_URL = (
    "assets/WhatsBot.pdf"
)
is_list_select = False
now = datetime.now()

app = Flask(__name__,
            static_url_path='/assets', 
            static_folder='assets')


##mongoDb
from pymongo import MongoClient
cluster =  MongoClient("mongodb+srv://<your username>:<password>@cluster0.eeqz4.mongodb.net/mydb?retryWrites=true&w=majority")
db = cluster["mydb"]
collection = db["whatsBot"]
# collection.insert_one({"_id":993201171,"name":"Amar"})


##Inserting user_info in mongoDb
def insert_values(id,time,msg_status,response):
    user_msg_details_acc_to_time={"time":time,"is_received":msg_status,"response":response}
    collection.update_one({"_id":id},{"$push":{f"user_msg_details":user_msg_details_acc_to_time}})


@app.route("/" )
def index():
    return "Hello"



# chatbot logic
@app.route("/sms",methods=["POST","GET"])
def bot():
    cursor =  collection.find({})
    phoneN = [i["_id"] for i in cursor]
    if request.values.get('WaId') not in phoneN:
        collection.insert_one({"_id":request.values.get('WaId'),"name":request.values.get('ProfileName')})
        
    global is_list_select
  
    # user input
    user_msg = request.values.get('Body', '').lower()

    response = MessagingResponse()
    if user_msg == "hi" or user_msg == "hello" or user_msg == "hey" or user_msg == "hii":
        
        msg = response.message("Hey, WhatsBot here!! Please choose from below options: \n1.Send text message \n2.send image \n3.send document \n4.send a list of options ")
        is_list_select = False
        insert_values(request.values.get('WaId'),now.strftime("%H:%M:%S"),request.values.get('SmsStatus',''),user_msg)
        return str(response)
    if not is_list_select:
        if user_msg == "1":
            msg = response.message("Hey,there!!")
            insert_values(request.values.get('WaId'),now.strftime("%H:%M:%S"),request.values.get('SmsStatus',''),user_msg)
            return str(response)
        if user_msg == "2":
            msg = response.message("Thanks for the selecting image. Here's one randomly selected for you!")
            insert_values(request.values.get('WaId'),now.strftime("%H:%M:%S"),request.values.get('SmsStatus',''),user_msg)
            msg.media(Random_Image_URL)
            return str(response)
        if user_msg == "3":
            msg = response.message("Thanks for the selecting document Here's one for you!")
            msg.media(document_URL)
            insert_values(request.values.get('WaId'),now.strftime("%H:%M:%S"),request.values.get('SmsStatus',''),user_msg)
            return str(response)
        if user_msg == "4":
            is_list_select = True
            msg = response.message("You choose from below list options:  \n1.send image \n2.send document \n3.send my name ")
            insert_values(request.values.get('WaId'),now.strftime("%H:%M:%S"),request.values.get('SmsStatus',''),user_msg)
            return str(response)
    else:
        if user_msg == "3":
            msg = response.message(f"So here is your name in whatsapp '{request.values.get('ProfileName', '')}'")
            insert_values(request.values.get('WaId'),now.strftime("%H:%M:%S"),request.values.get('SmsStatus',''),user_msg)
            return str(response)
        if user_msg == "1":
            msg = response.message("Thanks for the selecting image. Here's one randomly selected for you!")
            msg.media(Random_Image_URL)
            insert_values(request.values.get('WaId'),now.strftime("%H:%M:%S"),request.values.get('SmsStatus',''),user_msg)
            return str(response)
        if user_msg == "2":
            msg = response.message("Thanks for the selecting document Here's one for you!")
            msg.media(document_URL)
            insert_values(request.values.get('WaId'),now.strftime("%H:%M:%S"),request.values.get('SmsStatus',''),user_msg)
            return str(response)



  
    # displaying result
    q="Something went wrong, please try again"
    msg = response.message(q)

    insert_values(request.values.get('WaId'),now.strftime("%H:%M:%S"),request.values.get('SmsStatus',''),q)
    return str(response)
  
  
if __name__ == "__main__":
    app.run()