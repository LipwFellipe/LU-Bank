# NU Bank | LU Bank
Projeto utilizando SQL SERVER como banco de dados, Python na versão 3.9 e a biblioteca CustomTKinter

O intuito do projeto foi melhorar meus conhecimentos em cima do SQL SERVER e fazer uma integração utilizando PYTHON. Minha ideia foi criar um plagio do NU Bank, mas de uma forma mais simples. 

## Restaurando o banco de dados:

1. Tenha o SSMS(SQL SERVER MANAGEMENT STUDIO) instalado na maquina e restaure o backup do arquivo DB_bank.bak :

https://github.com/user-attachments/assets/0a2b4fc7-27d4-44b2-b31d-03631bba02c9

2. Certifique-se de ter o Python instalado na versão 3.9 ou acima. Verifique digitando no terminal:

```bash
python --version
```
3. Instale os requirements.txt executando o seguinte comando no terminal:

```bash
pip install -r requirements.txt
```


## Executando o Programa:

1. Com codigo em mãos, na linha 6, altere o codigo com as suas especificações de DRIVER e SERVER com seu HOSTNAME:
```bash
pyodbc.connect('DRIVER=digite seu driver; Server=HOSTNAME;Database=DB_bank;Trusted_Connection=yes;TrustServerCertificate=yes;')
```
2. No terminal da sua ID, execute o seguinte comando para rodar o codigo:
```bash
python Bank_LU.py 
```
3. E por fim, Cadastre-se e se divirta realizando pix para outras contas bancárias!!

<img src="https://media.tenor.com/1MfQk9vFF7MAAAAM/anime-bye-bye-maki.gif">
