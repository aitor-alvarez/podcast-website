from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from forms import SignUpForm
import random
import string


def request_user(request):
	letters = string.ascii_lowercase
	passw = ''.join(random.choice(letters) for i in range(10))
	if (request.method == 'POST') and request.user.is_anonymous == True:
		form = SignUpForm(request.POST)
		if form.is_valid():
			if User.objects.filter(username=form.cleaned_data['email']).exists():
				return render(request, 'podcast_user/details.html',
				              {'message': 'The email is currently in use. Please provide another email address.'})
			else:
				try:
					email = form.cleaned_data['email']
					data = form.save(commit=False)
					data.username = email
					data.password = make_password(passw)
					data.save()
					return render(request, 'podcast_user/details.html', {'user': email, 'passw': passw})

				except:
					HttpResponse('The email is currently in use. Please provide another email address.')
	else:
		form = SignUpForm()
	return render(request, 'podcast_user/signup.html', {'form': form})
