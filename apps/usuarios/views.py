from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.views import View
from django.contrib.auth.models import User
from .forms import LoginForm,CadastroForm
from django.urls import reverse_lazy
from .forms import SenhaEmailResetForm,SenhaResetConfirmForm,RecaptchaForm
from django.contrib.auth.views import PasswordResetView,PasswordResetConfirmView

# Create your views here.
class LoginView(View):
    template_name = 'login.html'
    
    def setup(self,*args,**kwargs):
        super().setup(*args,**kwargs)

        self.contexto = {'form':LoginForm(data=self.request.POST or None),
                         'recaptcha':RecaptchaForm(self.request.POST or None),
                        }
        self.login = self.contexto['form']

    def post(self,*args,**kwargs):
        form = self.contexto['recaptcha']
        if not form.is_valid():
            print('nao valido')
            self.contexto['error'] = 'Desculpe Mr. Robot, ocorreu um erro.'
            return render(self.request,self.template_name,self.contexto)
        
        if self.login.is_valid():
            user = self.request.POST.get('usuario')
            password = self.request.POST.get('password')
            usuario = authenticate(self.request,username=user,password=password)

        if usuario is not None:
            login(self.request,usuario)
            return redirect('home')
        self.contexto['error'] = 'Usuario ou Senha invalida'
        return render(self.request,self.template_name,self.contexto)
   
    def get(self,*args):
        if self.request.user.is_authenticated:
            return redirect('home')
        return render(self.request,self.template_name,self.contexto)

class CadastroView(View):
    template_name = 'cadastro.html'

    def setup(self,*args,**kwargs):
        super().setup(*args,**kwargs)

        self.contexto = {'form':CadastroForm(data=self.request.POST or None),
                        'recaptcha':RecaptchaForm(self.request.POST or None),
                        }
        self.cadastro = self.contexto['form']

    def post(self,*args,**kwargs):
        form = self.contexto['recaptcha']
        if not form.is_valid():
            print('nao valido')
            self.contexto['error'] = 'Desculpe Mr. Robot, ocorreu um erro.'
            return render(self.request,self.template_name,self.contexto)
        if self.cadastro.is_valid():
            user = self.cadastro.cleaned_data.get('username')
            password = self.cadastro.cleaned_data.get('password')
            first_name = self.cadastro.cleaned_data.get('first_name')
            last_name = self.cadastro.cleaned_data.get('last_name')
            email = self.cadastro.cleaned_data.get('email')

            usuario = User.objects.create_user(
                username=user,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            ) 
            usuario.save()   
            return redirect('login')
        return render(self.request,self.template_name,self.contexto)
        

    def get(self,*args):
        if self.request.user.is_authenticated:
            return redirect('home')
        return render (self.request,self.template_name,self.contexto)

def logoutview(request):
    logout(request)
    return redirect('home')


class RecuperarSenhaView(PasswordResetView):
    template_name = 'senha_reset_form.html'
    form_class = SenhaEmailResetForm
    email_template_name = 'senha_reset_email.html'
    success_url = reverse_lazy('recuperar_senha_enviado')

def recuperarsenha_enviado(request):
    return render(request,'senha_reset_enviada.html')

class RecuperarSenhaConfirmView(PasswordResetConfirmView):
    template_name='senha_reset_confirma.html'
    form_class = SenhaResetConfirmForm
    success_url = reverse_lazy('password_reset_complete')

def recuperarsenhaconfirm_completo(request):
    return render(request,'senha_reset_completo.html')