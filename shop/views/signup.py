from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from shop.models import Customer

class Consulta(View):
    def get(self, request):
        return redirect('ShopHome')
    def post(self, request):
        mensaj= request.POST['mensaj']
        print(mensaj)
        return redirect('ShopHome')

class Signup(View):
    def get(self, request):
        current_user = request.user
        if current_user.id:
            messages.success(request, 'Already logged in!!!')
            return redirect('ShopHome')
        return render(request, 'signup.html')

    def post(self, request):
        
        
        email = request.POST['email']
        fname = request.POST['fname']
        phone = request.POST['phone']
        ubicacion = request.POST['ubicacion']

        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        uname = email
        
        
        print(uname, fname, email, phone,ubicacion, pass1)


        values = {
            'email': email,
            'fname': fname,
            'phone': phone,
            'ubicacion':ubicacion,
        }

        # Form Validations
        if User.objects.filter(email=email):
            messages.success(request, "E-mail ya esta registrado!")
            return render(request, 'signup.html', values)



        if not fname:
            messages.warning(request,"Favor escribir tu usuario.")
            return render(request, 'signup.html', values)
        if len(pass1)<5:
            messages.warning(request, "Contraseña muy corta!")
            return render(request, 'signup.html', values)
        if pass1!=pass2:
            messages.warning(request, "Ambas contraseñas no son iguales!")
            return render(request, 'signup.html', values)

        new_user = User.objects.create_user(
            uname,
            email=email,
            password=pass1,
            first_name=fname.capitalize(),
            )
        new_user.save()

        customer = Customer(
            user=new_user,
            phone=phone,
            ubicacion=ubicacion,
        )
        customer.save()

        user = authenticate(request, username=email, password=pass1)
        if user is not None:
            login(request, user)

        messages.success(request, "Cuenta creada con exito!!!")
        return redirect('ShopHome')
        