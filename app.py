from flask import Flask, render_template, request
from googletrans import Translator

app = Flask(__name__)
from bot import medbot

@app.route("/")
@app.route("/home")
def home_page():
    sen1="Chat with me!"
    sen2="Hi, I am Medbot and I'm here to help you!"
    lang =[{"name": "English", "code": "en"}, {"name": "Hindi", "code": "hi"},{"name": "Spanish", "code": "es"},{"name": "German", "code": "de"}, {"name": "Chinese", "code": "zh-cn"}]
    return render_template('home.html', languages=lang, sen1=sen1, sen2=sen2 )


@app.route('/translate_lang', methods=['POST'])
def translate_lang():
    if request.method == "POST":
        lang =[{"name": "English", "code": "en"}, {"name": "Hindi", "code": "hi"},{"name": "Spanish", "code": "es"},{"name": "German", "code": "de"}, {"name": "Chinese", "code": "zh-cn"}]
        code= str(request.form["code"])
        translator= Translator()
        s1= translator.translate("Chat With Me!", src="en", dest="code").text
        s2= translator.translate("Hi, I am Medbot and I'm here to help you!", src="en", dest="code").text
    return render_template('home.html',sen1=s1, sen2=s2, code=code, languages=lang)

@app.route('/get')
def get_bot_response():
    userText=request.args.get('msg')
    return str(medbot.chat(userText))
    

@app.route('/about')
def about_page():
    return render_template("about.html")




if __name__ == "__main__":
    # turn debug mode off after production   
    app.run()
