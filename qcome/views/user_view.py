from django.views import View
from qcome.services import user_service
from django.shortcuts import render,redirect
from ..decorators import auth_required, role_required
from ..constants import Role
from ..services import get_user_details,update_user_details


@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
class EnduserProfileView(View):
    def get(self, request):
        user_id=request.user.id
        user_details=user_service.get_user_details(user_id)
        return render(request,'enduser/Profile/user_profile.html',{'user':user_details})
    

class EnduserProfileCreate(View):
    def get(self, request):
        return
    




class EnduserProfileUpdate(View):
    def get(self, request, user_id):
        user_details = get_user_details(user_id)
        context = {'user_details': user_details}
        return render(request, 'enduser/profile/user_profile_update.html', context)

    def post(self, request, user_id):
        user = get_user_details(user_id)
        if user:
            update_user_details(user, request.POST, request.FILES)
            return redirect('user_profile')  
        return redirect('user_profile')  



class EnduserProfileDelete(View):
    def get(self, request, user_id):
        user_del = get_user_details(user_id)
        context = {'user_del': user_del}
        return render(request, 'enduser/profile/user_profile_delete.html', context)

    def post(self, request, user_id):
        user = get_user_details(user_id)
        if user:
            user.delete()
            return redirect('user_profile')  
        return redirect('user_profile')
  
    
#user_profile_update.html