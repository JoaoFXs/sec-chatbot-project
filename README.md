# Projeto Chatbot
## Desenvolvimento de Chatbot para aprimorar o atendimento nas instituições de ensino superior: Uma abordagem para melhoria da experiência do usuário.

Este projeto é um aplicativo web desenvolvido com Django que permite o desenvolvimento de um chatbot para aprimorar o atendimento aos alunos em instituições de ensino superior, com foco na melhoria da experiência do usuário. O projeto envolve a escolha da linguagem de programação adequada, a avaliação de diferentes modelos de chatbots e a implementação de recursos de processamento de linguagem natural e aprendizado de máquina para permitir que o chatbot compreenda e responda eficazmente a uma diversidade de perguntas dos alunos. Espera-se que o chatbot automatize tarefas comuns, alivie a sobrecarga das secretarias e proporcione um serviço mais ágil e personalizado aos alunos, melhorando a sua satisfação e retenção nas instituições de ensino superior.

## Configuração do Ambiente de Desenvolvimento

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/projeto-django-chatbot.git
   cd projeto-django-chatbot

2. **Crie um ambiente virtual:**

```
 python -m venv venv
 ```
3. **Ative o ambiente virtual**
 - ###### No Windows:
    
    ```
    venv\Scripts\activate
    ```
    
     - ###### No macOS/Linux:
    
    ```
    source venv/bin/activate
    ```
4. **Instale as dependências:**

```
 pip install -r requirements.txt
 ```

5. **Configure o banco de dados:**

```
python manage.py migrate
```

6. **Crie um superusuário:**

```
python manage.py createsuperuser
```


### Rodando o Projeto

1. **Inicie o servidor de desenvolvimento:**

```
python manage.py runserver
```

2. **Acesse o aplicativo no navegador:**

```
http://127.0.0.1:8000/
```


#### O arquivo views contém as views para autenticação de usuários e a página inicial do aplicativo.

def user_login(request):

    
    View para realizar o login do usuário.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.

    Returns:
        HttpResponse: Redireciona para a página inicial se o login for bem-sucedido,
                      caso contrário, renderiza a página de login com o formulário.
   

def home(request):

 
    View para renderizar a página inicial do usuário logado.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.

    Returns:
        HttpResponse: Renderiza a página inicial com as informações do aluno.
  

  ## Funcionalidades de Autenticação e Sessão

Este projeto inclui um conjunto de funções para gerenciar autenticação e sessões de usuários em um aplicativo Django.

### Principais Funções

- **Autenticação**:
  - `authenticate(request=None, **credentials)`: Autentica um usuário com as credenciais fornecidas.
  - `aauthenticate(request=None, **credentials)`: Versão assíncrona de `authenticate`.

- **Gerenciamento de Sessão**:
  - `login(request, user, backend=None)`: Realiza o login de um usuário e persiste a sessão.
  - `alogin(request, user, backend=None)`: Versão assíncrona de `login`.
  - `logout(request)`: Realiza o logout de um usuário e limpa a sessão.
  - `alogout(request)`: Versão assíncrona de `logout`.

- **Utilitários de Usuário**:
  - `get_user_model()`: Retorna o modelo de usuário ativo no projeto.
  - `get_user(request)`: Retorna a instância do usuário associada à sessão da requisição.
  - `aget_user(request)`: Versão assíncrona de `get_user`.

- **Outras Funções**:
  - `get_permission_codename(action, opts)`: Retorna o codinome da permissão para uma ação específica.
  - `update_session_auth_hash(request, user)`: Atualiza o hash de autenticação da sessão após uma mudança de senha.
  - `aupdate_session_auth_hash(request, user)`: Versão assíncrona de `update_session_auth_hash`.

### Exemplo de Uso

Para autenticar um usuário:
```python
from myapp.auth import authenticate

user = authenticate(request, username='john', password='secret')
if user is not None:
    # Credenciais válidas
    login(request, user)
else:
    # Credenciais inválidas
    pass