# -*- coding: utf-8 -*-
from crypt import crypt
import cgi


def processar(user, domain, senha_atual, senha_nova):
    nome_arquivo = '../etc/' + domain + '/shadow'

    if not usuario_valido(nome_arquivo, user):
        return 'E-mail inválido'

    hash_arquivo = get_hash_senha_arquivo(nome_arquivo, user)

    salt = get_salt(nome_arquivo, user)
    hash_senha_atual = crypt(senha_atual, salt)
    hash_senha_nova = crypt(senha_nova, salt)

    if hash_senha_atual != hash_arquivo:
        return 'Senha atual inválida'

    texto_novo_arquivo = inserir_hash_senha_nova(nome_arquivo, user, hash_senha_nova)
    gravar_alteracoes(nome_arquivo, texto_novo_arquivo)

    return 'Senha alterada com sucesso!'


def usuario_valido(nome_arquivo, user):
    arquivo = open(nome_arquivo, 'r')
    texto_arquivo = arquivo.read()
    arquivo.close()

    texto_arquivo = texto_arquivo.split('\n')

    resul = False
    for linha in texto_arquivo:
        campos = linha.split(':')

        resul = campos[0] == user
        if resul:
            break

    return resul


def get_hash_senha_arquivo(nome_arquivo, user):
    arquivo = open(nome_arquivo, 'r')
    texto_arquivo = arquivo.read()
    arquivo.close()

    texto_arquivo = texto_arquivo.split('\n')

    hash_senha = ''
    for linha in texto_arquivo:
        campos = linha.split(':')

        if campos[0] == user:
            hash_senha = campos[1]
            break

    return hash_senha


def get_salt(nome_arquivo, user):
    arquivo = open(nome_arquivo, 'r')
    texto_arquivo = arquivo.read()
    arquivo.close()

    texto_arquivo = texto_arquivo.split('\n')

    salt = ''
    for linha in texto_arquivo:
        campos = linha.split(':')

        if campos[0] == user:
            partes = campos[1].split('$')
            salt = '$' + partes[1] + '$' + partes[2] + '$'
            break

    return salt


def inserir_hash_senha_nova(nome_arquivo, user, hash_senha_nova):
    arquivo = open(nome_arquivo, 'r')
    texto_arquivo = arquivo.read()
    arquivo.close()

    texto_arquivo = texto_arquivo.split('\n')

    for i in range(len(texto_arquivo)):
        linha_atual = texto_arquivo[i]
        campos = linha_atual.split(':')
        if campos[0] == user:
            nova_linha = ''
            for j in range(len(campos)):
                if nova_linha != '':
                    nova_linha += ':'
                if j == 1:
                    nova_linha += hash_senha_nova
                else:
                    nova_linha += campos[j]

            texto_arquivo.remove(linha_atual)
            texto_arquivo.insert(i, nova_linha)
            break
    return texto_arquivo


def gravar_alteracoes(nome_arquivo, texto_arquivo_novo):
    texto = ''
    for i in texto_arquivo_novo:
        texto += i + '\n'

    arquivo = open(nome_arquivo, 'w')
    arquivo.write(texto)
    arquivo.close()

# O PROGRAMA COMEÇA AQUI
if __name__ == "__main__":

    print 'Content-Type: text/html\n\n'

    email = ''
    senha_atual = ''
    senha_nova = ''

    parametros = cgi.FieldStorage()
    for parametro in parametros.keys():
        if parametro == 'email':
            email = parametros[parametro].value
        if parametro == 'senhaatual':
            senha_atual = parametros[parametro].value
        if parametro == 'senhanova':
            senha_nova = parametros[parametro].value

    if (email == '') or (not ('@' in email)) or (senha_atual == '') or (senha_nova == ''):
        print 'Parametros invalidos'
        exit()

    usuario = email.split('@')[0]
    dominio = email.split('@')[1]

    result = processar(usuario, dominio, senha_atual, senha_nova)

    print result
