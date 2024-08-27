from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Aluno
# Create your views here.
from .forms import AlunoAuthenticationForm

def user_llogin(request):
    if request.method == 'POST':
        ##form = AlunoAuthenticationForm(request, data=request.POST)
        form = AlunoAuthenticationForm(request.POST)
       
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AlunoAuthenticationForm()
    return render(request, 'sec_chatbot/pages/login.html', {'form': form})

@login_required
def home(request):
    try:
        aluno = Aluno.objects.get(ra=request.user.ra)
    except Aluno.DoesNotExist:
        aluno = None
    return render(request, 'sec_chatbot/pages/home.html', {'aluno': aluno})