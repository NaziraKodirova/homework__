from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.contrib import messages
from users.forms import LoginForm, CustomerUserForm, CustomerUserUpdateForm, ProfileForm, ProfileUpdateForm, \
    ChangePasswordForm
from users.models import CustomUser, Profile


class Login(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, 'register-login.html', {'login_form': login_form})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Tizimga muvaffaqqiyatli kirdingiz")
                return redirect('listing_app:home')
            else:
                messages.error(request, 'Bunday login yoki parol mavjud emas')
                return redirect('users:register')
        else:
            messages.error(request, 'Login yoki parolda xatolik mavjud')
            return redirect('users:register')


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('listing_app:home')


class Register(View):
    def get(self, request):
        register_form = CustomerUserForm()
        return render(request, 'register-login.html', {'register_form': register_form})

    def post(self, request):
        register_form = CustomerUserForm(request.POST)
        if register_form.is_valid():
            password = register_form.cleaned_data['password']
            confirm_password = register_form.cleaned_data['confirm_password']
            if password == confirm_password:
                user = register_form.save(commit=False)
                user.set_password(password)
                user.save()
                first_name = user.first_name
                last_name = user.last_name
                phone_number = user.phone_number
                email = user.email
                is_agent = user.is_agent
                telegram_username = user.telegram_username
                new_profile = Profile.objects.create(user=user, first_name=first_name, last_name=last_name,
                                                     phone_number=phone_number, email=email, is_agent=is_agent,
                                                     telegram_username=telegram_username)
                user.profile = new_profile
                user.save()
                messages.success(request, "Muvaffaqqiyatli ro'yxatdan o'tdingiz")
                return HttpResponseRedirect(reverse('listing_app:home'))
            else:
                register_form.add_error('confirm_password', "Parolni tasdiqlashda xatolik yuzaga keldi")
        else:
            messages.error(request, "M'alumotlarni kiritishda xatolik mavjud")
            return render(request, 'register-login.html', {'register_form': register_form})


class CustomUserUpdate(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        update_form = CustomerUserUpdateForm(instance=user)
        return render(request, 'update-user.html', {'update_form': update_form})

    def post(self, request):
        user = request.user
        profile = CustomUser.objects.filter(id=user.id).first()
        update_form = CustomerUserUpdateForm(request.POST, request.FILES, instance=profile)
        if update_form.is_valid():
            update_form.save()
            messages.success(request, "Ma'lumotlar yangilandi.")
            return redirect('listing_app:home')
        else:
            messages.error(request, "Ma'lumotlarni yangilashda xatolik yuzaga keldi. Qayta urinib ko'ring.")
            return render(request, 'update-user.html', {'update_form': update_form})


class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        profile_form = ProfileForm(instance=request.user.profile)
        username = request.user.username
        return render(request, 'update_profile.html', {'profile_form': profile_form, 'username': username})

    def post(self, request):
        profile = request.user.profile
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profilingiz ma'lumotlari yangilandi!")
            return redirect('listing_app:home')
        else:
            messages.error(request, "Ma'lumotlarni yangilashda xatolik yuzaga keldi. Qayta urinib ko'ring.")
        return render(request, 'update_profile.html', {'profile_form': profile_form})


class ChangePasswordView(LoginRequiredMixin, View):
    form_class = ChangePasswordForm
    template_name = 'change-password.html'

    def get(self, request):
        form = self.form_class()
        username = request.user.username
        return render(request, self.template_name, {'form': form, 'username': username})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password1']
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                messages.success(request, "Parolingiz muvaffaqiyatli o'zgartirildi!")
                update_session_auth_hash(request, user)
                return redirect('listing_app:home')
            else:
                form.add_error('old_password', "Eski parol noto'g'ri")
        return render(request, self.template_name, {'form': form})
