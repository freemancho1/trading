from django.shortcuts import render
from django.views.generic import *

from common.utils.auth.authentication import Authentication as certificate


def starting_point(request):
    return render(request, 'common/start.html', certificate.get_login_info(request))


class Login(FormView):
    template_name = 'common/login.html'




def main(request):
    pass
