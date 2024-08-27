import random
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os

# Carregue seu modelo e dados
model = load_model('model.h5')

# Defina palavras e classes
words = [...]  # Liste suas palavras aqui
classes = [...]  # Liste suas classes aqui

lemmatizer = WordNetLemmatizer()

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence, model):
    bow = bag_of_words(sentence, words)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    if isinstance(intents_json, list):
        list_of_intents = [i for i in intents_json]
    else:
        list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            return random.choice(i['responses'])
    return "Desculpe, não entendi o que você disse."

@csrf_exempt
def chat(request):
    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get('message')
        if message:
            with open('path/to/intents.json') as file:
                intents = json.load(file)
            ints = predict_class(message, model)
            res = get_response(ints, intents)
            return JsonResponse({"response": res})
    return JsonResponse({"error": "Invalid request"}, status=400)

def home(request):
    return render(request, 'chat.html')  # Substitua 'chat.html' pelo nome correto do seu template HTML
