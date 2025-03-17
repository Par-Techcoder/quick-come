from django.http import JsonResponse
from django.views import View
from qcome.services import user_service, admin_service
from django.shortcuts import redirect, render
import os
import hashlib
from quickcome import settings
from ..constants.error_message import ErrorMessage
from ..constants.success_message import SuccessMessage
from ..package.response import success_response,error_response
from django.contrib import messages  # For user feedback
import datetime
from qcome.constants.default_values import Gender

class ManageUsersListView(View):
    def get(self, request):
        users = user_service.get_all_user()
        admin_data = user_service.get_user(request.user.id)
        for user in users:
            if user.gender:
                user.gender = Gender(user.gender).name.capitalize()  # e.g., "Male"
            else:
                user.gender = "Not provided"
                            
        return render(request, 'adminuser/user/user_list.html',{'users':users, 'admin': admin_data})
    

class ManageUsersCreateView(View):
    def get(self, request):
        admin_data = user_service.get_user(request.user.id)
        return render(request, 'adminuser/user/create_user.html', {'admin': admin_data})
    
    def post(self, request):
        print(request.POST)
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender') or None
        
        # Profile photo handling
        profile_photo = request.FILES.get('profile_photo')
        profile_photo_path = ''

        if profile_photo:
            profile_photo_img_dir = os.path.join(settings.BASE_DIR, 'static', 'all-Pictures', 'profile-images')
            if not os.path.exists(profile_photo_img_dir):
                os.makedirs(profile_photo_img_dir)

            md5_hash = hashlib.md5()
            for chunk in profile_photo.chunks():
                md5_hash.update(chunk)
            file_hash = md5_hash.hexdigest()

            _, ext = os.path.splitext(profile_photo.name)
            new_file_name = f"{file_hash}{ext}"
            file_path = os.path.join(profile_photo_img_dir, new_file_name)

            if not os.path.exists(file_path):
                profile_photo.seek(0)
                with open(file_path, 'wb+') as destination:
                    for chunk in profile_photo.chunks():
                        destination.write(chunk)

            profile_photo_path = f'/static/all-Pictures/profile-images/{new_file_name}'
        
        user_service.user_create(first_name, middle_name, last_name, dob, email, phone, gender, profile_photo_path)

        return redirect('manage_users')


class ManageUserUpdateView(View):
    def get(self , request, user_id):
        user = user_service.get_user(user_id)
        admin_data = user_service.get_user(request.user.id)
        return render(request, 'adminuser/user/update_user.html', {'user':user, 'admin': admin_data})
    
    def post(self, request, user_id):
            user = user_service.get_user(user_id)
            # Fetch form data and strip whitespace
            first_name = request.POST.get('first_name').strip() or user.first_name
            middle_name = request.POST.get('middle_name').strip() or user.middle_name
            last_name = request.POST.get('last_name').strip() or user.last_name
            email = request.POST.get('email').strip() or user.email
            phone = request.POST.get('phone').strip() or user.phone
            gender_str = request.POST.get('gender')
            dob_str = request.POST.get('dob') or user.dob

            gender = user.gender
            if gender_str:
                gender = int(gender_str)
                    
            if dob_str:
                try:
                    dob = datetime.datetime.strptime(dob_str, '%Y-%m-%d').date()
                except ValueError:
                    messages.error(request, ErrorMessage.E00002.value)
                    return redirect('myadmin_profile')

            # Profile photo handling
            profile_photo = request.FILES.get('profile_photo')
            profile_photo_path = user.profile_photo_url

            if profile_photo:
                profile_photo_img_dir = os.path.join(settings.BASE_DIR, 'static', 'all-Pictures', 'profile-images')
                if not os.path.exists(profile_photo_img_dir):
                    os.makedirs(profile_photo_img_dir)

                md5_hash = hashlib.md5()
                for chunk in profile_photo.chunks():
                    md5_hash.update(chunk)
                file_hash = md5_hash.hexdigest()

                _, ext = os.path.splitext(profile_photo.name)
                new_file_name = f"{file_hash}{ext}"
                file_path = os.path.join(profile_photo_img_dir, new_file_name)

                if not os.path.exists(file_path):
                    profile_photo.seek(0)
                    with open(file_path, 'wb+') as destination:
                        for chunk in profile_photo.chunks():
                            destination.write(chunk)

                profile_photo_path = f'/static/all-Pictures/profile-images/{new_file_name}'

            
            admin_service.admin_profile_update(
                user, first_name, middle_name, last_name, email, phone, gender, dob, profile_photo_path
            )

            messages.success(request, SuccessMessage.S00002.value)
            return redirect('manage_users')
    

class ManageUserToggleView(View):
    def post(self, request, user_id):
        # Toggle the user's status using the service function.
        user = user_service.toggle_user_status(user_id)
        if user is None:
            return JsonResponse(error_response(ErrorMessage.E00012.value))
        # Return the updated status in JSON format.
        return JsonResponse(success_response(SuccessMessage.S00005.value))

    
