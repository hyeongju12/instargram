from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib import messages as msgs

# Create your views here.
def signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			user = form.save()
			msgs.success(request, "Sign up Completed!")
			next_url= request.GET.get('next', '/') # pattern name 사용가능
			return redirect(next_url)
	else:
		form = SignupForm
	return render(request, 'accounts/signup_form.html', {
		'form' : form
	})