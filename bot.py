import json
import nltk
import numpy
import random
import tensorflow
import tflearn
import pickle
from bs4 import BeautifulSoup
import requests
from nltk.stem.lancaster import LancasterStemmer
from googletrans import Translator
translator = Translator()


nltk.download('punkt')


stemmer = LancasterStemmer()

with open('intents.json') as file:
    data = json.load(file)

try:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)


    training = numpy.array(training)
    output = numpy.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

tensorflow.compat.v1.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

# model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
# model.save("model.tflearn")

try:
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)


class medbot:
    def chat(inputText): 
        # detecting language
        detectLang= translator.detect(inputText).lang
        if(detectLang=='en'):
            inp= inputText
            results = model.predict([bag_of_words(inp, words)])[0]
            results_index = numpy.argmax(results)
            tag = labels[results_index]

            if (results[results_index] > 0.8):
                for tg in data["intents"]:
                    if tg['tag'] == tag:
                        responses = tg['responses']

                return random.choice(responses)
            else:
                url=f"https://www.google.com/search?q={inp}+healthline&num=5"
                headers ={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'  
                }
                trustable_urls=['healthline.com' ]
                response = requests.get(url, headers=headers).text
                soup = BeautifulSoup(response, 'lxml')
                keep_going= True
                paras= soup.findAll('div', class_="yuRUbf")
                response = requests.get(url, headers=headers).text
                soup = BeautifulSoup(response, 'lxml')
                if(paras):
                    output_str= ""
                    current_url = ""
                    selected_url = ""
                    target_url = ""
                    for para in paras:
                        if keep_going:
                            current_url=para.a['href']
                            for url in trustable_urls:
                                if(current_url.find(url) !=-1):
                                    keep_going= False
                                    target_url=current_url
                                    selected_url= url
                                    break
                if(selected_url == 'healthline.com'):
                    response = requests.get(target_url, headers=headers).text
                    soup = BeautifulSoup(response, 'lxml')
                    article=soup.find('div', class_='css-z468a2')
                    str= article.text
                    forbidden_str= "Last medically reviewed"
                    excluded_str="We include products we think are useful for our readers. If you buy through links on this page, we may earn a small commission. Here’s our process."
                    newstr= str.split(forbidden_str)[0]

                    tags=soup.find_all('p' or 'ul' or 'h3' or 'h1' or 'li')
                    for tag in tags:
                        if(newstr.find(tag.text)!= -1 and tag.text!= excluded_str):
                            output_str= output_str + tag.text +" "
                else:
                    output_str = "Sorry, we are not able to resolve your queries. Try typing more relevant queries."
                return output_str
        else:
            # converting to english
            inp= translator.translate(inputText, src=detectLang, dest='en').text

            results = model.predict([bag_of_words(inp, words)])[0]
            results_index = numpy.argmax(results)
            tag = labels[results_index]

            if (results[results_index] > 0.8):
                for tg in data["intents"]:
                    if tg['tag'] == tag:
                        responses = tg['responses']
                
                langResponse=random.choice(responses)
                return translator.translate(langResponse, src='en', dest=detectLang).text
            else:
                url=f"https://www.google.com/search?q={inp}+healthline&num=5"
                headers ={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'  
                }
                trustable_urls=['healthline.com' ]
                response = requests.get(url, headers=headers).text
                soup = BeautifulSoup(response, 'lxml')
                keep_going= True
                paras= soup.findAll('div', class_="yuRUbf")
                response = requests.get(url, headers=headers).text
                soup = BeautifulSoup(response, 'lxml')
                if(paras):
                    output_str= ""
                    current_url = ""
                    selected_url = ""
                    target_url = ""
                    for para in paras:
                        if keep_going:
                            current_url=para.a['href']
                            for url in trustable_urls:
                                if(current_url.find(url) !=-1):
                                    keep_going= False
                                    target_url=current_url
                                    selected_url= url
                                    break
                if(selected_url == 'healthline.com'):
                    response = requests.get(target_url, headers=headers).text
                    soup = BeautifulSoup(response, 'lxml')
                    article=soup.find('div', class_='css-z468a2')
                    str= article.text
                    forbidden_str= "Last medically reviewed"
                    excluded_str="We include products we think are useful for our readers. If you buy through links on this page, we may earn a small commission. Here’s our process."
                    newstr= str.split(forbidden_str)[0]

                    tags=soup.find_all('p' or 'ul' or 'h3' or 'h1' or 'li')
                    for tag in tags:
                        if(newstr.find(tag.text)!= -1 and tag.text!= excluded_str):
                            output_str= output_str + tag.text +" "
                            

                else:
                    output_str = "Sorry, we are not able to resolve your queries. Try typing more relevant queries."
                return translator.translate(output_str, src='en', dest=detectLang).text

           


        

                    
