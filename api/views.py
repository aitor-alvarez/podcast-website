from django.views.decorators.csrf import csrf_exempt
from podcast.views import api_search
from .models import *
import random, hashlib, datetime
from django.http import JsonResponse


@csrf_exempt
def verify_device(config, ip):
	if ExternalDevice.objects.filter(ipaddress=ip, key=config['key']).exists():
		obj = ExternalDevice.objects.get(ipaddress=config['ip'], key=config['key'])
		s = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz!.#') for i in range(59))
		try:
			hash = hashlib.sha256(s.encode('utf-8'))
			Token.objects.create(device=obj, token=hash.hexdigest(), valid_until=datetime.datetime.now(tz=datetime.timezone.utc)+datetime.timedelta(days=2))
			return {'message': 'OK', 'token': s}
		except Exception as e:
			print(e)
			return {'message': 'KO'}
	else:
		return {'message': 'KO'}

@csrf_exempt
def token_is_valid(token):
	hash = hashlib.sha256(token.encode('utf-8'))
	try:
		tk = Token.objects.get(token=hash.hexdigest())
		if tk.valid_until > datetime.datetime.now(tz=datetime.timezone.utc):
			return True
		else:
			return False
	except:
		return False


@csrf_exempt
def authenticate_request(params, ip):
	token = params.get('token', '')
	if not token_is_valid(token):
		valid_device = verify_device(params, ip)
		if 'token' in valid_device:
			valid_device['message'] = 'RENEWED'
			token = valid_device['token']
		else:
			return {'message': 'Your device is not allowed to perform this action'}
	return {'message': 'OK', 'token': token}


@csrf_exempt
def search_podcasts(request):
	try:
		ip = get_client_ip(request)
		auth = authenticate_request(request.POST, ip)
		if 'token' in auth:
			search_results = api_search(request.POST['q'], request.POST['language'])
			return JsonResponse(search_results)
		else:
			return JsonResponse(auth)
	except Exception as e:
		return JsonResponse({"message": "The following error has happened: "+ e})


def get_client_ip(request):
	user_ip = request.META.get('HTTP_X_FORWARDED_FOR')
	if user_ip:
		ip = user_ip.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip