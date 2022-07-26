from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.contrib.auth import authenticate
from django.urls import reverse
from rest_framework import status


class AuthenticationUserTestCase(APITestCase):
    
    def setUp(self):
        self.list_url = reverse('programas-list')
        self.user = User.objects.create_user('leonardo', password='123456')

    
    def test_autenticacao_user_com_credenciais_corretas(self):
        """Teste que verifica a autenticação de um user com credenciais corretas"""
        user = authenticate(username='leonardo', password='123456')
        self.assertTrue((user is not None) and user.is_authenticated)


    def test_requisicao_get_nao_autorizada(self):
        """Teste que verifica uma requisição sem autenticar"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_autenticacao_user_com_usuario_incorreto(self):
        """Teste que verifica a autenticação de um user incorreto"""
        user = authenticate(username='leonardoA', password='123456')
        self.assertFalse((user is not None) and user.is_authenticated)

    def test_autenticacao_user_com_senha_incorreta(self):
        """Teste que verifica a autenticação de um user com senha incorreta"""
        user = authenticate(username='leonardo', password='0123456')
        self.assertFalse((user is not None) and user.is_authenticated)        

    def test_requisicao_get_com_usuario_autenticado(self):
        """Teste que verifica uma requisição GET de user autenticado"""
        self.client.force_authenticate(self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)