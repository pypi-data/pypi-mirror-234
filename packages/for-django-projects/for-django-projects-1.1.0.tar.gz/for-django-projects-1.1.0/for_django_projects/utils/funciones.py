import json
from django.core import signing


def redirectAfterPostGet(request, campos_add={}):
    dict_url_vars = request.GET.get('dict_url_vars') or request.POST.get('dict_url_vars') or ""
    if dict_url_vars:
        try:
            dict_url_vars = json.loads(get_decrypt(dict_url_vars)[1]).get(request.path) or ""
        except Exception as ex:
            print(ex)
    salida = "?action=add&" if '_add' in request.POST else request.path + "?"
    if '_add' in request.POST:
        for k, v in campos_add.items():
            salida += "&{}={}".format(k, v)
    return salida + "{}".format(dict_url_vars)


def ip_client_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_encrypt(values):
    try:
        return True, signing.dumps(values, compress=True)
    except Exception as ex:
        return False, str(ex)


def get_decrypt(cyphertxt):
    try:
        return True, signing.loads(cyphertxt)
    except Exception as ex:
        return False, str(ex)