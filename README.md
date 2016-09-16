# Hostgator Change Mail Password

Esses scripts foram escritos para rodarem no plano de hospegagem compartilhada do Hostgator (que é o que eu uso), portanto eu só
testei seu funcionamento no Hostgator, mas dependendo do seu caso é possível adaptás-los à sua realidade.

Esse repositório é composto por 4 scripts:

* **getdomains.py:** retorna a lista de domínios que você têm hospedado
* **validpass.py:** valida a senha do e-mail informado
* **changepass.py:** altera a senha do e-mail informado
* **shadowhandler.py:** tem um conjunto de métodos que são usados pelos demais scripts (*mais pra frente eu explico*)

## Como usar

Eu chamo esses scripts através de **CGI** (se você não conhece basta ler esse [tutorial de CGI com Python]
(http://www.tutorialspoint.com/python/python_cgi_programming.htm) e [como ativar Python via CGI no Hostgator]
(http://support.hostgator.com/articles/specialized-help/technical/perl-and-python-scripts))

**Importante**: os parâmetros são passados para os scripts via POST

### getdomains.py 

Esse script retorna uma lista com todos os domínios hospedados.

```
Parâmetros: 
    Nenhum
  
Retorno:
    <dominio1>
    <dominio2>
    ...
    <dominioN>
     
    * Há uma quebra de linha entre os nomes dos domínios
     
```

### validpass.py 

Esse script valida se a senha informada é a senha correta para o e-mail informado

```
Parâmetros: 
    email    = o e-mail cuja senha será validada
    password = a senha a ser validada
  
Retorno:
    -[99]-   = sucesso (a senha está correta)
    -[1]-    = erro
     
```

### changepass.py 

Esse script altera a senha do e-mail informado

```
Parâmetros: 
    email    = o e-mail cuja senha será alterada
    oldpass  = a senha atual
    newpass  = a nova senha
  
Retorno:
    -[99]-   = (sucesso) a senha foi alterada
    -[1]-    = erro
     
```

## Como funciona?

Eu queria criar um formulário personalizado para fazer a troca de senha dos e-mail dos domínios que hospedo no Hostgator e 
dando uma olhada na estrutura de diretórios da hospegagem compartilhada que assino eu percebi que tenho acesso ao arquivo 
`shadow` de cada domínios através do caminho `~/etc/<dominio>/shadow`.

**Dica**: *Shadow é o arquivo que contém os usuários e suas senhas, essas últimas criptografadas, claro!*

Usando um exemplo onde você tenha uma hospedagem no Hostgator com os 3 domínio `abc.com.br`, `123.com.br`, e `xyz.com.br` a 
árvore de diretórios fica mais ou menos assim:

```
  ~ (home do seu usuário)
  |
  |--etc
      |
      |--abc.com.br
      |          |
      |          |--shadow
      |
      |--123.com.br
      |          |
      |          |--shadow
      |
      |--xyz.com.br
                 |
                 |--shadow      

```      

### Como eu listo os domínio?

Dentro do diretório `~/etc/` há um diretório para cada domínio que você tem hospedado, portanto a lista de domínios é a lista
de diretórios.

### Como eu verifico e altero as senhas?

Dentro do diretório de cada domínio existe um arquivo `shadow`, nesse arquivo estão cadastrados os usuários e suas senhas, o
que eu faço é abrir esse arquivo e ler as informações de lá. Com relação a criptografia, o Python tem um módulo que cuida disso
pra mim: `crypt`

Para entender como fazer a alteração propriamente dita no arquivo shadow leia o [post no meu site que explica tudo]
(http://marti.com.br/alterar-a-senha-de-usuarios-do-linux-com-python/).
