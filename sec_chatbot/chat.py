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
from .models import Aluno, Professor  # Importação atualizada

# Carregue seu modelo e dados
model = load_model('model.h5')

# Defina palavras e classes
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
intents_path = os.path.join(base_dir, 'sec_chatbot', 'templates', 'sec_chatbot', 'json', 'intents.json')
ignore_words = ["!", "@", "#", "$", "%", "*", "?"]
lemmatizer = WordNetLemmatizer()

with open(intents_path) as file:
    with open(intents_path, 'r', encoding='utf-8') as file:
        intents = json.load(file)
    words = []
    classes = []
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            word_list = nltk.word_tokenize(pattern.lower())
            words.extend(word_list)
        classes.append(intent['tag'])

    words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
    words = sorted(set(words))
    classes = sorted(set(classes))

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence.lower()) # Converte para minúsculas
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
    try:
        aluno = Aluno.objects.get(ra=request.user.ra)
    except Aluno.DoesNotExist:
        aluno = None
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get('message')
           
            if message:
                # Verifica se o chatbot está aguardando o nome de um professor
                if request.session.get('awaiting_professor_name'):
                    professor_name = message.strip().title()
                    try:
                        professor = Professor.objects.get(nome=professor_name)
                        # Formate a resposta com os dados do professor
                        res = (
                            f" - Nome do Professor: {professor.nome}\n"
                            f" - Curso Lecionado: {professor.curso.nome_curso}\n"
                            f" - Formação:  {professor.formacao}\n"
                            f" - Email para contato:  {professor.email}"
                        )
                    except Professor.DoesNotExist:
                        res = "Professor não encontrado. Por favor, verifique o nome e tente novamente."
                    
                    # Reinicia o estado da sessão
                    del request.session['awaiting_professor_name']
                    request.session.modified = True
                    
                    return JsonResponse({"response": res})
                else:
                    # Processamento normal da mensagem
                    ints = predict_class(message, model)
                    print(ints)
                    res = get_response(ints, intents)
                    if "{{ aluno.ra }}" in res and aluno:
                        res = res.replace("{{ aluno.ra }}", aluno.ra)
                    
                    # Verifica se a intent é 'informacoes_professor'
                    if ints and ints[0]['intent'] == 'informacoes_professor':
                        # Define o estado para aguardar o nome do professor
                        request.session['awaiting_professor_name'] = True
                        request.session.modified = True
                        # Resposta para solicitar o nome do professor
                        res = "Por favor, informe o nome do professor que deseja obter informações."
                    
                    return JsonResponse({"response": res})
            
            return JsonResponse({"error": "Mensagem não encontrada"}, status=400)
        except Exception as e:
            # Opcional: Log do erro para depuração
            print(f"Erro no chat: {e}")
            return JsonResponse({"error": "Erro ao processar a mensagem"}, status=500)
    
    return JsonResponse({"error": "Método não permitido"}, status=405)
