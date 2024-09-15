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
from .models import Aluno, Professor, Materia, HorarioAula


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

def suggest_professors(name_part):
    """Sugere nomes de professores que contenham a parte do nome fornecida."""
    professors = Professor.objects.filter(nome__icontains=name_part).values_list('nome', flat=True)
    return list(professors)

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
                    cont = 0
                    try:
                        professor = Professor.objects.get(nome=professor_name)
                        cursos = ', '.join([curso.nome_curso for curso in professor.cursos.all()])
                        turmas = ', '.join([turma.sigla_turma for turma in professor.turmas.all()])
                        materias = ', '.join([materia.nome_materia for materia in professor.materia_lecionada.all()])
                        # Formate a resposta com os dados do professor
                        res = (
                            f" - Nome do Professor: {professor.nome}\n"
                            f" - Curso Lecionado: {cursos}\n"
                            f" - Turmas: {turmas}\n"
                            f" - Materias Lecionadas:  {materias}\n"
                            f" - Formação:  {professor.formacao}\n"
                            f" - Email para contato:  {professor.email}"                            
                        )
                    except Professor.DoesNotExist:
                        # Sugere professores com nomes semelhantes
                        suggestions = suggest_professors(message.strip().lower())
                        if suggestions:
                            request.session['awaiting_professor_name'] = True
                            request.session.modified = True
                            cont = 1
                            res = f"Não encontrei o professor exato, mas encontrei os seguintes nomes semelhantes: {', '.join(suggestions)}."                          
                        else:
                            res = "Professor não encontrado. Por favor, verifique o nome e tente novamente."
                            cont = 0
                    # Reinicia o estado da sessão caso cont for igual a 0
                    if(cont == 0):
                        del request.session['awaiting_professor_name']
                        request.session.modified = True
                    
                    return JsonResponse({"response": res})
                # Verifica se o chatbot está aguardando a matéria
                elif request.session.get('awaiting_materia'):
                    materia_name = message.strip().title()
                    request.session['materia'] = materia_name
                    request.session['awaiting_turma'] = True
                    request.session.modified = True
                    return JsonResponse({"response": "Por favor, informe a turma da matéria."})
                # Verifica se o chatbot está aguardando a Turma
                elif request.session.get('awaiting_materia_selection'):
                    selected_materia = message.strip().title()
                    materias_disponiveis = request.session.get('materias_disponiveis', [])

                    if selected_materia in materias_disponiveis:
                        try:
                            # Busca o horário da aula para a matéria selecionada e a turma do aluno
                            horario = HorarioAula.objects.filter(turma=aluno.turma, materia__nome_materia=selected_materia).first()

                            if horario:
                                res = (
                                    f"A aula de {selected_materia} para a turma {aluno.turma} "
                                    f"Ocorre às {horario.horario_inicio} -{horario.horario_fim} "
                                )
                            else:
                                res = "Não encontrei o horário dessa aula. Verifique os dados e tente novamente."
                        except Materia.DoesNotExist:
                            res = "Matéria não encontrada. Verifique os dados e tente novamente."
                    else:
                        res = "Matéria selecionada inválida. Por favor, escolha uma das opções fornecidas."

                    # Limpa o estado da sessão após a seleção da matéria
                    del request.session['materias_disponiveis']
                    del request.session['awaiting_materia_selection']
                    request.session.modified = True
                    
                    return JsonResponse({"response": res})
                
                else:
                    # Processamento normal da mensagem
                    ints = predict_class(message, model)
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

                    # Verifica se a intent é 'horario_aula'
                    if ints and ints[0]['intent'] == 'horario_aula':
                        # Obtém todas as matérias associadas à turma do aluno
                        materias = Materia.objects.filter(turmas=aluno.turma)
                        if materias.exists():
                            # Cria uma lista de matérias disponíveis
                            materias_list = [materia.nome_materia for materia in materias]
                            materias_str = ', '.join(materias_list)
                            # Armazena as matérias disponíveis na sessão para futura seleção
                            request.session['materias_disponiveis'] = materias_list
                            request.session['awaiting_materia_selection'] = True
                            request.session.modified = True
                            
                            # Resposta com as matérias disponíveis para o aluno escolher
                            res = f"Por favor, informe a matéria. Suas matérias disponíveis são: {materias_str}."
                        else:
                            res = "Não encontrei matérias para a sua turma. Por favor, entre em contato com o suporte."

                        return JsonResponse({"response": res})

                    return JsonResponse({"response": res})
            
            return JsonResponse({"error": "Mensagem não encontrada"}, status=400)
        except Exception as e:
            # Opcional: Log do erro para depuração
            print(f"Erro no chat: {e}")
            return JsonResponse({"error": "Erro ao processar a mensagem"}, status=500)
    
    return JsonResponse({"error": "Método não permitido"}, status=405)
