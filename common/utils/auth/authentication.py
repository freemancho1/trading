from datetime import datetime

from common.wrapper import UserWrapper as cuw
from common.utils.properties import *


class Authentication:

    @staticmethod
    def is_login(request):
        return True if request.session.get(SECRET_ID, False) else False

    @staticmethod
    def get_login_info(request):
        login_info = {
            'id'      : request.session.get(SECRET_ID),
            'username': request.session.get(SECRET_USER),
            'is_staff': request.session.get(SECRET_STF),
            'is_login': Authentication.is_login(request)
        }
        return login_info

    @staticmethod
    def do_login(request, id):
        user = cuw.get(id)
        user.last_login = datetime.now()
        cuw.save(user)

        request.session[SECRET_ID] = id
        request.session[SECRET_USER] = user.username
        request.session[SECRET_STF] = user.is_staff

    @staticmethod
    def do_logout(request):
        request.session.pop(SECRET_ID)
        request.session.pop(SECRET_USER)
        request.session.pop(SECRET_STF)