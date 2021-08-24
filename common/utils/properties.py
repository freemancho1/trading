GENDER_CHOICES = (
    (0, 'Not to disclose'),
    (1, 'Male'),
    (2, 'Female'),
)


sys_error_message = {
    'username_set_err'          : 'Username setting error.',
    'username_unique_err'       : 'A username with the same name already exists.',
    'username_not_found_err'    : 'Username does not exist.',
    'username_empty_err'        : 'Username is required.',
    'password_set_err'          : 'Password setting error.',
    'password_mistype_err'      : 'Entered the wrong password.',
    'password_mismatch_err'     : 'The two passwords do not match.',
    'password_empty_err'        : 'Password is required.',
    'curr_password_mistype_err' : 'Entered the wrong current password.',
    'email_set_err'             : 'Email setting error.',
    'email_unique_err'          : 'A email with the same name already exists.',
    'email_not_found_err'       : 'Email does not exist.',
    'email_empty_err'           : 'Email is required.',
    'superuser_staff_false_err' : 'Superuser must have is_staff=True.',
    'superuser_super_false_err' : 'Superuser must have is_superuser=True.',
    'gender_data_err'           : 'GENDER field can only use numbers 1, 2 and 3.'
}

sys_message = {
    'input_id'                  : 'Please enter your ID.',
    'input_password'            : 'Please enter your password.',
    'input_password_c'          : 'Please enter it again to confirm your password.',
    'input_curr_password'       : 'Please enter your current password',
    'input_new_password'        : 'Please enter your new password',
    'input_email'               : 'Please enter your E-mail.',
    'input_first_name'          : 'Please enter your first name',
    'input_last_name'           : 'Please enter your last name',
}


secret_str = {
    'sess_id'                   : 'XFDSAGADSR',
    'sess_username'             : 'AFBTYNRYTR',
    'sess_is_staff'             : 'DSAAEBGFGT',
}
SECRET_ID = secret_str['sess_id']
SECRET_USER = secret_str['sess_username']
SECRET_STF = secret_str['sess_is_staff']