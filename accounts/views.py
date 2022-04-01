from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from .forms import SignupForm, ProfileForm
from django.contrib import messages as msgs
from django.core.mail import send_mail

# Create your views here.
login = LoginView.as_view(template_name="accounts/login_form.html")

def logout(request):
	msgs.success(request, 'Logout Completed!')
	return logout_then_login(request)

def signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			signed_user = form.save()
			auth_login(request, signed_user)
			msgs.success(request, "Sign up Completed!")
			signed_user.send_welcome_email() # FIXME : Celery로 처리하는것으로 추천
			next_url= request.GET.get('next', '/') # pattern name 사용가능
			return redirect(next_url)
	else:
		form = SignupForm
	return render(request, 'accounts/signup_form.html', {
		'form' : form
	})

@login_required
def profile_edit(request):
	if request.method == 'POST':
		form = ProfileForm(request.POST, request.FILES, instance=request.user)
		if form.is_valid():
			form.save()
			msgs.success(request, "프로필을 수정/저장했습니다.")
			return redirect('profile_edit')
	else:
		form = ProfileForm(instance=request.user) # 현재 user를 지정하지 않으면, ProfileForm을 만들게됨.
	return render(request, "accounts/profile_edit_form.html", {
		'form' : form
	})