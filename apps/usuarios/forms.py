from typing import Any, Dict
from django import forms
from django.contrib.auth.models import User
import re
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm

class LoginForm(forms.Form):
    usuario = forms.CharField(
        max_length=150,
        required=True,
        label="Usuario",
        widget=forms.TextInput(
            attrs={'placeholder':"Usuario",'class':'form__input__area'})
        )
    password = forms.CharField(
        max_length=150,
        required=True,
        label="Senha",
        widget=forms.PasswordInput(
            attrs={'placeholder':"Senha",'class':'form__input__area'})
        )

class CadastroForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password')

    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder':"Usuario",'class':'form__input__area'})
        ) 
    
    first_name = forms.CharField(
        max_length=150,
        required=True,
        label='Nome',
        widget=forms.TextInput(
            attrs={'placeholder':"Nome",'class':'form__input__area'})
        )  

    last_name = forms.CharField(
        max_length=150,
        required=True,
        label='Sobrenome',
        widget=forms.TextInput(
            attrs={'placeholder':"Sobrenome",'class':'form__input__area'})
        )  

    email = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.EmailInput(
            attrs={'placeholder':"Email",'class':'form__input__area'})
        )  
    
    password = forms.CharField(
        max_length=150,
        required=True,
        label='Senha',
        widget=forms.PasswordInput(
            attrs={'placeholder':"Senha",'class':'form__input__area'})
        )
    def clean(self) -> Dict[str, Any]:
        cleaned = self.cleaned_data
        validation_error_msg = {}
        
        username_data = cleaned.get('username')
        username_lower = username_data.lower()
        cleaned['username'] = username_lower
        
        first_name_data = cleaned.get('first_name').lower().title()
        cleaned['firstname'] = first_name_data

        last_name_data = cleaned.get('first_name').lower().title()
        cleaned['last_name'] = last_name_data

        email_data = cleaned.get('email').lower()
        cleaned['email'] = email_data

        senha_data = cleaned.get('password')
        cleaned['password'] = senha_data

        if username_data:
            if re.search(r'[^a-zA-Z0-9\s]', username_data):
                validation_error_msg['username'] = 'Nao e possivel utiliza careteristicos "especiais"'
        
        if first_name_data:
            if re.search(r'[^a-zA-Z0-9\s]', first_name_data):
                validation_error_msg['first_name'] = 'Nao e possivel utiliza careteristicos "especiais"'
        
        if last_name_data:
            if re.search(r'[^a-zA-Z0-9\s]', last_name_data):
                validation_error_msg['last_name'] = 'Nao e possivel utiliza careteristicos "especiais"'
                   
        if senha_data :
            if len(senha_data) < 5:
                validation_error_msg['password'] = 'Senha muito curta, precisa ter mais de "5 digitos".'

        if email_data:
            email_user = User.objects.filter(email=email_data).exists()
            if email_user:
                validation_error_msg['email'] = 'Email Já utilizado'
        if username_data:
            username_user = User.objects.filter(username=username_data).exists()
            if username_user:
                validation_error_msg['username'] = 'Usuario Cadastrado'
        if validation_error_msg:
            raise(forms.ValidationError(validation_error_msg))

        return cleaned
    

class SenhaResetConfirmForm(SetPasswordForm):

    new_password1 = forms.CharField(        
        label='Senha Nova',
        max_length=100,
        widget=forms.PasswordInput(
            attrs={"class":"form__input__area",
            "phaceholder":"Senha Nova",
            'type':'password'}
        )
    )

    new_password2 = forms.CharField(        
        label='Repetir Senha',
        max_length=100,
        widget=forms.PasswordInput(
            attrs={"class":"form__input__area",
            "phaceholder":"Digite Novamente",
            'type':'password'}
        )
    )


    field_order = ["old_password", "new_password1", "new_password2"]

class SenhaEmailResetForm(PasswordResetForm):

    email = forms.EmailField(        
        label='Email',
        max_length=254,
        required=True,
        widget=forms.EmailInput(
            attrs={"class":"form__input__area",
            "phaceholder":"Senha",
            'type':'email'}
        )
    )

    class Meta:
        model = User
        fields = ('email')

class AlterarSenhaForm(SenhaResetConfirmForm):

    old_password = forms.CharField(        
        label='Senha Antiga',
        max_length=100,
        widget=forms.PasswordInput(
            attrs={"class":"form__input__area",
            "phaceholder":"Senha",
            'type':'password'}
        )
    )

    class Meta:
        model = User
        fields = ('old_password','new_password1','new_password2')