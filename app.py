from flask import Flask, render_template, request
app = Flask(__name__)
from bot import medbot

@app.route("/")
@app.route("/home")
def home_page():
    sen1="Chat with me!"
    sen2="Hi, I am Medbot and I'm here to help you!"
    lang =[{"name": "English", "code": "en"}, {"name": "Hindi", "code": "hi"},{"name": "Spanish", "code": "es"},{"name": "German", "code": "de"}, {"name": "Chinese", "code": "zh-cn"}]
    return render_template('home.html', languages=lang, sen1=sen1, sen2=sen2 )



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
