# whatsapp-bot
<h3>About this app?</h3>
<p style="margin-top:5px;">So, this is an whatsapp bot which has basic functionality like,<br>1.send a text.<br>2.send an image.<br>3.send an document.<br>4.send your whatsapp name.</p>
<hr>
<h3>Creation & Technologies?</h3>
<p style="margin-top:5px;">To create this I have us flask for serving webserver and https://twilio.com (we have to do basic setp for this) to make an basic bot number.Whenever an user send msg to bot number provided by twilio then an post request from twilio will be send to our weburl (note that to give callbackurl your url should have hosted ..localhost
will not be allowed .to tackle this problem I have used https://ngrok.com/download .)and then the responses,user_name ,msg_status I have stored in mongoDb as cloud database.To deal
with mongoDb you can use pymongo an python module.<br>So,yeah this was an basic steps I have followed to create this</p>
<h3>output</h3>
<img src="assets/ss.jpeg">
