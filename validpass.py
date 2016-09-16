#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path
from crypt import crypt
import cgi
import shadowhandler as shadow


def validate_password(user, domain, password):
    path_shadow_file = os.path.expanduser('~/etc/' + domain + '/shadow')

    if not shadow.valid_user(path_shadow_file, user):
        # E-mail invalido
        return '1'

    hash_file = shadow.get_hash_password(path_shadow_file, user)

    salt = shadow.get_salt(path_shadow_file, user)
    hash_password = crypt(password, salt)

    if hash_password == hash_file:
        # Senha valida
        return '99'
    else:
        # Senha invalida
        return '1'


# O PROGRAMA COMECA AQUI
if __name__ == "__main__":

    print "Content-Type: text/html\n\n"

    email = ''
    password = ''

    parameters = cgi.FieldStorage()
    for parameter in parameters.keys():
        if parameter == 'email':
            email = parameters[parameter].value
        if parameter == 'senha':
            password = parameters[parameter].value

    if (email == '') or (not ('@' in email)) or (password == ''):
        print 'parametros invalidos'
        exit()

    user = email.split('@')[0]
    domain = email.split('@')[1]

    result = validate_password(user, domain, password)

    print "-[" + result + "]-"
