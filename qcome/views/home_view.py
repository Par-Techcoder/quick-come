from django.views import View
from django.shortcuts import render, redirect
from ..decorators import auth_required, role_required
from ..constants import Role


@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
class HomeView(View):
    def get(self, request):
        return render(request, 'enduser/home/index.html')



    
class ChangeMyThemeView(View):
    def post(self, request):
        return
        
