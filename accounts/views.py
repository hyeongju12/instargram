from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
	LoginView, LogoutView, logout_then_login, PasswordChangeView as AuthPasswordChangeView
)
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from .forms import SignupForm, ProfileForm, PasswordChangeForm
from django.contrib import messages as msgs
from django.core.mail import send_mail
from .models import User
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

class PasswordChangeView(LoginRequiredMixin,AuthPasswordChangeView):
	success_url = reverse_lazy("password_change")
	template_name = 'accounts/password_change_form.html'
	form_class = PasswordChangeForm

	def form_valid(self, form):
		msgs.success(self.request, '암호를 변경했습니다.')
		return super().form_valid(form)

password_change = PasswordChangeView.as_view()

@login_required
def user_follow(request, username):
	follow_user = get_object_or_404(User, username=username, is_active=True)
	# request.user = > follow_user를 팔로우 하려고 합니다.
	request.user.following_set.add(follow_user)
	follow_user.follower_set.add(request.user)
	msgs.success(request, f"{follow_user}님을 팔로우 했습니다.")
	redirect_url = request.META.get('HTTP_REFERER', 'root')
	return redirect(redirect_url)

@login_required
def user_unfollow(request, username):
	unfollow_user = get_object_or_404(User, username=username, is_active=True)
	request.user.following_set.remove(unfollow_user)
	unfollow_user.follower_set.remove(request.user)
	msgs.success(request, f"{unfollow_user}님을 언팔로우 했습니다.")
	redirect_url = request.META.get('HTTP_REFERER', 'root')
	return redirect(redirect_url)
