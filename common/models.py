from django.db import models


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