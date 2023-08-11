from django.urls import path
from .views import LoginView,logoutview,CadastroView,RecuperarSenhaView,recuperarsenha_enviado,RecuperarSenhaConfirmView,recuperarsenhaconfirm_completo

urlpatterns = [
    path('',LoginView.as_view(),name='login'),
    path('logout/',logoutview,name='logout'),
    path('cadastrar/',CadastroView.as_view(),name='cadastro'),

    path('recuperar_senha/', RecuperarSenhaView.as_view(), name="reset_password"),
    path('recuperar_enviado/', recuperarsenha_enviado, name="recuperar_senha_enviado"),
    path('recuperar/<uidb64>/<token>', RecuperarSenhaConfirmView.as_view(), name="password_reset_confirm"),
    path('recuperar_bem_sucedido/', recuperarsenhaconfirm_completo,name="password_reset_complete"),

]
