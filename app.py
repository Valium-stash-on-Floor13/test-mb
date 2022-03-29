from flask import Flask, render_template, request, jsonify, session
from googletrans import Translator
translator= Translator()
app = Flask(__name__)
app.secret_key="Hello"
from bot import medbot

@app.route("/")
@app.route("/home")
def home_page():
    session['cd']='en'
    return render_template('home.html')



@app.route("/translate", methods=['POST', "GET"])
def translate():
    data=request.json['code']
   
    s1="Chat With Me! Hi, I am Medbot and I'm here to help you!"
    s1= translator.translate(s1, src="en", dest=data).text
    print("trans:",s1)
   
    return s1

@app.route('/get')
def get_bot_response():
    userText=request.args.get('msg')
    return str(medbot.chat(userText))
    

@app.route('/about')
def about_page():
    return render_template("about.html")




if __name__ == "__main__":
    # turn debug mode off after production   
    app.run(debug=True)
