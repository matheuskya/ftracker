from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from main.forms import LoginForm, CadastroForm, GastoForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from main.models import Gasto
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        gastos = list(Gasto.objects.values())
        return Response(gastos)


def home(request):
    return HttpResponse('funciona')


def login(request):
    form = LoginForm()
    if(request.method == "POST"):
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
    context = {
        'form': form,
    }
    return render(request, 'main/login.html', context)


def cadastro(request):
    form = CadastroForm()
    if (request.method == 'POST'):
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {
        'form': form
    }
    return render(request, 'main/cadastro.html', context)


@login_required(login_url='login')
def dashboard(request):
    gastos_list = Gasto.objects.all()
    valortotal = 0
    for gasto in gastos_list:
        valortotal = gasto.valor + valortotal
    context = {
        'gastos': gastos_list,
        'valortotal': valortotal
    }
    return render(request, 'main/dashboard.html', context)


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')


@login_required(login_url='login')
def gasto(request):
    if (request.method == 'POST'):
        form = GastoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = GastoForm()
        context = {
            'form': form
        }
        return render(request, 'main/gasto.html', context)


@login_required(login_url='login')
def deletar(request, gasto_id):
    gasto = Gasto.objects.get(pk=gasto_id)
    context = {
        "gasto": gasto
    }
    return render(request, 'main/deletar.html', context)


@login_required(login_url='login')
def deletar_post(request, gasto_id):
    Gasto.objects.get(id=gasto_id).delete()
    return redirect('dashboard')


@login_required(login_url='login')
def editar(request, gasto_id):
    gasto = get_object_or_404(Gasto, pk=gasto_id)
    form = GastoForm(instance=gasto)
    context = {
        'gasto': gasto,
        'form': form,
    }
    if (request.method == 'POST'):
        form = GastoForm(request.POST, instance=gasto)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    return render(request, 'main/editar.html', context)


# @login_required(login_url='login')
# def editar_post(request, gasto_id):
#     gasto = get_object_or_404(Gasto, pk=gasto_id)
#     if (request.method == 'POST'):
#         novo_gasto =
#     return redirect('dashboard')