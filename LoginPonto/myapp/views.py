from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Pessoa, Endereco, Registro
from django.http import HttpResponseForbidden

def check_ip(request):
  client_ip = request.META.get('REMOTE_ADDR')
  return HttpResponse(f'Seu endereço IP é: {client_ip}')

def registro_atual_view(request):
  username = request.user.username
  pessoa = request.user.pessoa
  registros = Registro.objects.all()[::-1]
  if request.method == 'GET':
    return render(
        request, 'registro_atual.html', {
            'username': username,
            'authenticated': True,
            'registros': registros,
            'pessoa': pessoa,
        })
  else:
    return HttpResponseBadRequest()


def home_view(request):
  if request.user.is_authenticated:
    username = request.user.username
    return render(request, 'home.html', {
        'username': username,
        'authenticated': True
    })
  else:
    return render(request, 'home.html', {
        'username': None,
        'authenticated': False
    })


@login_required(login_url='/login')
def logout_view(request):
  logout(request)
  return render(request, 'home.html')


def login_view(request):
  if request.method == 'GET':
    return render(request, 'login.html', {'incorrect_login': False})
  elif request.method == 'POST':
    username = request.POST['username']
    password = request.POST['senha']
    user = authenticate(username=username, password=password)
    if user is not None:
      login(request, user)
      return redirect('/registro')
    else:
      return render(request, 'login.html', {'incorrect_login': True})
  else:
    return HttpResponseBadRequest()


def cadastro_view(request):
  if request.method == 'GET':
    if request.user.is_authenticated:
      return render(request, 'cadastro.html', {
          'username': request.user.username,
          'authenticated': True
      })
    else:
      return render(request, 'cadastro.html')
  elif request.method == 'POST':
    # Criar e salvar um objeto Enderecos
    endereco = request.POST['endereco']
    numero = request.POST['numero']
    complemento = request.POST['complemento']
    bairro = request.POST['bairro']
    cidade = request.POST['cidade']
    estado = request.POST['estado']
    cep = request.POST['cep']
    pais = request.POST['pais']
    enderecos = Endereco.objects.create(endereco=endereco,
                                        numero=numero,
                                        complemento=complemento,
                                        bairro=bairro,
                                        cidade=cidade,
                                        estado=estado,
                                        cep=cep,
                                        pais=pais)

    # Criar e salvar um objeto User
    username = request.POST['cpf']
    email = request.POST['email']
    password = request.POST['senha']
    user = User.objects.create_user(username=username,
                                    email=email,
                                    password=password)

    # Criar e salvar um objeto Pessoas associado ao objeto Enderecos e User
    nome = request.POST['nome']
    cpf = request.POST['cpf']
    telefone = request.POST['telefone']
    nascimento = request.POST['nascimento']
    mae = request.POST['mae']
    pai = request.POST['pai']
    pessoas = Pessoa.objects.create(nome=nome,
                                    cpf=cpf,
                                    telefone=telefone,
                                    nascimento=nascimento,
                                    mae=mae,
                                    pai=pai,
                                    enderecos=enderecos,
                                    usuario=user)
    pessoas.save()
    return redirect('/registro')
  else:
    return HttpResponseBadRequest()


@login_required(login_url='/login')
def registro_view(request):
    username = request.user.username
    pessoa = Pessoa.objects.get(cpf=username)
    ip_cliente = request.META.get('REMOTE_ADDR')

    # Verifica se o IP do cliente está na lista permitida
    if ip_cliente not in ['172.31.196.74']:
        return HttpResponseForbidden("Acesso negado.")
    else:
        if request.method == 'GET':
            if request.user.is_authenticated:
                return render(
                    request, 'registro.html', {
                        'username': username,
                        'authenticated': True,
                        'pessoa': pessoa,
                    })
            else:
                return render(request, 'cadastro.html')

        elif request.method == 'POST':
            if 'entrada' in request.POST:
                # Cria um registro de entrada para a pessoa
                Registro.objects.create(pessoa=pessoa, entrada=True)
                return redirect('/registro_atual')
            elif 'saida' in request.POST:
                # Cria um registro de saída para a pessoa
                Registro.objects.create(pessoa=pessoa, entrada=False)
                return redirect('/registro_atual')
            else:
                return HttpResponseBadRequest("Pedido inválido.")

        else:
            return HttpResponseBadRequest("Método HTTP inválido.")  

@login_required(login_url='/login')
def registro_confirmado_view(request):
  username = request.user.username
  #pessoa = Pessoa.objects.get(cpf=username)
  pessoa = request.user.pessoa
  registros = Registro.objects.filter(pessoa=pessoa)
  if request.method == 'GET':
    return render(
        request, 'registro_confirmado.html', {
            'username': username,
            'authenticated': True,
            'registros': registros,
            'pessoa': pessoa,
        })
  else:
    return HttpResponseBadRequest()
