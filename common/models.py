from django.db import models
from django.urls import reverse

from common.utils.validator import *


class Code(models.Model):

    c_type              = models.CharField('CodeType', max_length=1, null=False)
    code                = models.CharField('Code', max_length=4, null=False, db_index=True)
    name                = models.CharField('CodeName', max_length=100, null=False)
    memo                = models.CharField('Description', max_length=999)

    class Meta:
        db_table        = 'trading_common_code'
        ordering        = ['c_type', 'code']

    def __init__(self, id, c_type, code, name, memo=None, *args, **kwargs):
        super(Code, self).__init__(*args, **kwargs)
        self.id         = id
        self.c_type     = c_type
        self.code       = code
        self.name       = name
        self.memo       = memo

    def __str__(self):
        return f'CODE(ID={self.id}, ' \
               f'C_TYPE={self.c_type}, CODE={self.code}, NAME={self.name}, ' \
               f'DESCRIPTION={self.memo})'


class User(models.Model):

    username            = models.CharField(max_length=150, unique=True,
                                           validators=username_validators)
    password            = models.CharField(max_length=128)
    email               = models.CharField(max_length=254, unique=True,
                                           validators=email_validators)
    first_name          = models.CharField(max_length=150, null=True)
    last_name           = models.CharField(max_length=150, null=True)
    is_staff            = models.BooleanField(default=False)
    is_superuser        = models.BooleanField(default=False)
    is_active           = models.BooleanField(default=True)
    gender              = models.SmallIntegerField(choices=GENDER_CHOICES, default=0)
    last_login          = models.DateTimeField(null=True)
    date_joined         = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table        = 'trading_common_user'
        ordering        = ['-id']

    def __init__(self, id,
                 username, password, email, first_name, last_name,
                 is_staff=None, is_superuser=None, is_active=None,
                 gender=0, last_login=None,
                 *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

        self.id         = id
        self.username   = username
        self.password   = password
        self.email      = email
        self.first_name = first_name
        self.last_name  = last_name
        self.is_staff   = is_staff
        self.is_superuser = is_superuser
        self.is_active  = is_active
        self.gender     = gender
        self.last_login = last_login

    def __str__(self):
        return f'USER(ID={self.id}, USERNAME={self.username})'

    def get_absolute_url(self):
        return reverse('common:user_detail', args=[self.id])