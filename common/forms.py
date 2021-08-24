from django import forms

from django.contrib.auth.hashers import make_password, check_password

from common.utils.logs import Logger as log
from common.utils.validator import *
from common.wrapper import UserWrapper as cuw


class LoginForm(forms.Form):
    username = forms.CharField(label='ID', help_text=sys_message['input_id'])
    password = forms.CharField(label='Password', strip=False, widget=forms.PasswordInput(),
                               help_text=sys_message['input_password'])

    class Meta:
        fields = ['username', 'password']

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        try:
            act_user = cuw.get_active_user(username)
            if not check_password(password, act_user.password):
                self.add_error('password',
                               forms.ValidationError(sys_error_message['password_mistype_err']))
        except Exception as e:
            log.error(e)
            self.add_error('username',
                           forms.ValidationError(sys_error_message['username_not_found_err']))