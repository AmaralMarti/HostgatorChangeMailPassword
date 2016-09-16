#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path
from crypt import crypt
import cgi
import shadowhandler as shadow


def change_password(user, domain, old_password, new_password):
    path_shadow_file = os.path.expanduser('~/etc/' + domain + '/shadow')

    if not shadow.valid_user(path_shadow_file, user):
        # E-mail invalido
        return '1'

    hash_file = shadow.get_hash_password(path_shadow_file, user)

    salt = shadow.get_salt(path_shadow_file, user)
    hash_old_password = crypt(old_password, salt)
    hash_new_password = crypt(new_password, salt)

    if hash_old_password != hash_file:
        # Senha invalida
        return '1'

    new_content = shadow.change_hash(path_shadow_file, user, hash_new_password)
    shadow.write_file(path_shadow_file, new_content)

    return '99'


# O PROGRAMA COMECA AQUI
if __name__ == "__main__":

    print "Content-Type: text/html\n\n"

    email = ''
    old_password = ''
    new_password = ''

    parameters = cgi.FieldStorage()
    for parameter in parameters.keys():
        if parameter == 'email':
            email = parameters[parameter].value
        if parameter == 'senhaatual':
            old_password = parameters[parameter].value
        if parameter == 'senhanova':
            new_password = parameters[parameter].value

    if (email == '') or (not ('@' in email)) or (old_password == '') or (new_password == ''):
        print 'Parametros invalidos'
        exit()

    user = email.split('@')[0]
    domain = email.split('@')[1]

    result = change_password(user, domain, old_password, new_password)

    print "-[" + result + "]-"
