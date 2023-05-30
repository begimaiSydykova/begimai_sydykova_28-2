from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from users.forms import AuthForm, RegisterForm

# Create your views here.

def auth_view(request):
    if request.method == 'GET':
        context = {
            'form': AuthForm
        }

        return render(request, 'users/auth.html', context=context)
    
    if request.method == 'POST':
        data = request.POST
        form = AuthForm(data=data)

        if form.is_valid():
            ''' authenticate '''
            user = authenticate(username=form.cleaned_data.get('username'),
                                password=form.cleaned_data.get('password'))
            if user:
                '''authorization'''
                login(request, user)
                return redirect('/products/')
            else:
                form.add_error('username', 'try again :(')                        

        return render(request, 'users/auth.html', context={
            'form': form
        })
    
def register_view(request):
    if request.method == 'GET':
        context = {
            'form': RegisterForm
        }
        
        return render(request, 'users/register.html', context=context)
        
    if request.method == 'POST':
        data = request.POST
        form = RegisterForm(data=data)

        if form.is_valid():
            if form.cleaned_data.get('password') == form.cleaned_data.get('password'):
                ''' register '''
                user = User.objects.create_user(
                    username=form.cleaned_data.get('username'),
                    password=form.cleaned_data.get('password')
                )
            
            ''' authorization '''
            login(request, user)
            return redirect('/products/')

        return render(request, 'users/register.html', context={
            'form': form
        })
