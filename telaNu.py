import customtkinter as ctk
import pyodbc
from PIL import Image
from decimal import Decimal

conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server}; Server=LIPWNOTEBOOK\\SQLEXPRESS;Database=Banco_NuLipw;Trusted_Connection=yes;TrustServerCertificate=yes;')
print("Conexão bem sucedida")
cursor = conn.cursor()

def INSERT(cad_nome, cadas_cpf, cad_senha, cad_senha1, silvia_label):
    try:
        Inome = cad_nome.get()
        Icpf = cadas_cpf.get()
        Isenha = cad_senha.get()
        Isenha1 = cad_senha1.get()
        if Isenha1 != Isenha or Isenha == '' or Isenha1 == '':
            silvia_label.configure(text="Suas senhas não coincidem!", text_color="#fc1406")
            cad_senha.configure(border_color="#fc1406", placeholder_text="Senha invalida...", text_color="#fc1406", placeholder_text_color="#fc1406")
            cad_senha1.configure(border_color="#fc1406", placeholder_text="Senha invalida...", text_color="#fc1406", placeholder_text_color="#fc1406")
        elif Isenha == Isenha1:
            cad_senha.configure(border_color="#000000", text_color="#000000")
            cad_senha1.configure(border_color="#000000",text_color="#000000")

        if len(Icpf) < 11 or len(Icpf) > 11 or ('abcdefghijklmnopqrstuvwxyz@!#$%¨&*()-_.,') in Icpf :
            silvia_label.configure(text="CPF deve conter 11 digitos e apenas numeros...", text_color="#fc1406", font=("Helvetica", 15))
            cadas_cpf.configure(border_color="#fc1406", placeholder_text="CPF invalido...", text_color="#fc1406", placeholder_text_color="#fc1406")

        elif len(Icpf) == 11 and ('abcdefghijklmnopqrstuvwxyz@!#$%¨&*()-_.,') not in Icpf :
            cadas_cpf.configure(border_color="#000000", text_color="#000000")

        if Inome == "":
            cad_nome.configure(border_color="#fc1406", placeholder_text="Nome invalido...", text_color="#fc1406", placeholder_text_color="#fc1406")
        
        elif Inome != "":
            cad_nome.configure(border_color="#000000",text_color="#000000")

        if Isenha == Isenha1 and Isenha != '' and Isenha1 != '' and Inome != '' and Icpf != '':
            criar = f"""INSERT INTO usuario(nome, senha, cpf) VALUES('{Inome}', '{Isenha}', '{Icpf}')"""
            cursor.execute(criar)
            cursor.commit()
            id = cursor.execute(f"SELECT id FROM usuario WHERE cpf = '{Icpf}'").fetchone()
            cursor.execute(f"""INSERT INTO banco VALUES(0.00, '{id[0]}')""")
            cursor.commit()
             
            silvia_label.configure(text="Usuario criado com sucesso!", text_color="#117f09")
            cad_nome.configure(border_color="#117f09", text_color="#117f09")
            cad_senha.configure(border_color="#117f09", text_color="#117f09")
            cad_senha1.configure(border_color="#117f09", text_color="#117f09")
            cadas_cpf.configure(border_color="#117f09", text_color="#117f09")
        
    except:
        silvia_label.configure(text="Oque vc fez?", text_color="#fc1406")
        cad_nome.configure(border_color="#fc1406", placeholder_text="ERRO", text_color="#fc1406", placeholder_text_color="#fc1406")
        cad_senha.configure(border_color="#fc1406", placeholder_text="ERRO", text_color="#fc1406", placeholder_text_color="#fc1406")
        cad_senha1.configure(border_color="#fc1406", placeholder_text="ERRO", text_color="#fc1406", placeholder_text_color="#fc1406")
        cadas_cpf.configure(border_color="#fc1406", placeholder_text="ERRO", text_color="#fc1406", placeholder_text_color="#fc1406")

def cadastro():
    # Remove os widgets da primeira página
    for widget in root_tk.winfo_children():
        widget.grid_forget()

    # Nova "página"
    nome_label = ctk.CTkLabel(root_tk, text="Cadastre-se", text_color="#FFFFFF", font=("Helvetica", 30, "bold"))
    nome_label.grid(row=0, column=0, padx=20, pady=45, columnspan=2)

    # Label pequena acima do nome
    silvia_label = ctk.CTkLabel(root_tk, text="", text_color="#FFFFFF", font=("Helvetica", 20))  # Pequena label
    silvia_label.grid(row=1, column=0, padx=20, pady=(5, 0), sticky="w", columnspan=2)

    cad_nome = ctk.CTkEntry(root_tk, fg_color="#FFFFFF", border_color="#000000", placeholder_text="Digite seu Nome...", placeholder_text_color="#000000")
    cad_nome.grid(row=2, column=0, padx=20, pady=10, sticky="ew", columnspan=2)
    root_tk.grid_columnconfigure(0, weight=1)

    # Entrada CPF
    cadas_cpf = ctk.CTkEntry(root_tk, fg_color="#FFFFFF", border_color="#000000", placeholder_text="Digite seu CPF...", placeholder_text_color="#000000")
    cadas_cpf.grid(row=3, column=0, padx=20, pady=20, sticky="ew", columnspan=2)
    root_tk.grid_columnconfigure(0, weight=1)

    # Entrada de senha
    cad_senha = ctk.CTkEntry(root_tk, fg_color="#FFFFFF", border_color="#000000", placeholder_text="Digite sua senha...", placeholder_text_color="#000000")
    cad_senha.grid(row=4, column=0, sticky="w", padx=20, pady=20)

    # Entrada para confirmar senha
    cad_senha1 = ctk.CTkEntry(root_tk, fg_color="#FFFFFF", border_color="#000000", placeholder_text="Confirme sua senha...", placeholder_text_color="#000000")
    cad_senha1.grid(row=4, column=1, sticky="nsew", padx=20, pady=20)

    # Botão voltar
    botao_voltar = ctk.CTkButton(root_tk, text="Voltar", fg_color="#000000", hover_color="#250438", command=interface)
    botao_voltar.grid(row=5, column=0, padx=20, pady=20, sticky="w")

    # Botão cadastrar
    botao_cad = ctk.CTkButton(root_tk, text="Cadastrar", fg_color="#000000", hover_color="#250438", command=lambda: INSERT(cad_nome, cadas_cpf, cad_senha, cad_senha1, silvia_label))
    botao_cad.grid(row=5, column=1, padx=20, pady=20)

def ENTRAR(enter_cpf, enter_senha):
    try:
        Ecpf = enter_cpf.get()
        Esenha = enter_senha.get()
        cursor.execute(f"SELECT senha FROM usuario WHERE cpf = '{Ecpf}'")
        resul = cursor.fetchone()
        if Esenha == resul[0]:
            Extrato(Ecpf)
    except:
        enter_cpf.configure(border_color="#fc1406", placeholder_text="Digite um CPF valido...", text_color="#fc1406", placeholder_text_color="#fc1406")
        enter_senha.configure(border_color="#fc1406", placeholder_text="Digite uma senha valida...", text_color="#fc1406", placeholder_text_color="#fc1406")
            
def interface():
    # Limpa os widgets existentes (caso esteja voltando da nova página)
    for widget in root_tk.winfo_children():
        widget.grid_forget()

    my_image = ctk.CTkImage(dark_image=Image.open('Lu.png'), size=(75, 75))
    image_label = ctk.CTkLabel(root_tk, image=my_image, text="")
    image_label.place(x=30, y=25)

    # Seção inicial (primeira "página")
    titulo_label = ctk.CTkLabel(root_tk, text="Entrar", text_color="#FFFFFF", font=("Helvetica", 30, "bold"))
    titulo_label.grid(row=0, column=0, padx=20, pady=45, columnspan=2)

    enter_cpf = ctk.CTkEntry(root_tk, fg_color="#FFFFFF", border_color="#000000", placeholder_text="Digite seu CPF...", placeholder_text_color="#000000")
    enter_cpf.grid(row=1, column=0, padx=20, pady=20, sticky="ew", columnspan=2)
    root_tk.grid_columnconfigure(0, weight=1)

    enter_senha = ctk.CTkEntry(root_tk, fg_color="#FFFFFF", border_color="#000000", placeholder_text="Digite sua senha...", placeholder_text_color="#000000")
    enter_senha.grid(row=2, column=0, padx=20, pady=20, sticky="ew", columnspan=2)

    # Botão para entrar
    button2 = ctk.CTkButton(root_tk, text="Entrar", fg_color="#000000", hover_color="#250438", command=lambda: ENTRAR(enter_cpf, enter_senha))
    button2.grid(row=3, column=0, padx=20, pady=10, columnspan=2)

    # Texto informativo abaixo do botão
    texto_clicavel = ctk.CTkLabel(root_tk, text="Cadastre-se", text_color="#FFFFFF", font=("Helvetica", 12, "underline"))
    texto_clicavel.grid(row=4, column=0, padx=20, pady=20, columnspan=2)
    texto_clicavel.bind("<Button-1>", lambda e: cadastro())  # Torna o texto clicável

def Extrato(Ecpf):
    for widget in root_tk.winfo_children():
        widget.destroy()
    root_tk.configure(fg_color="#FFFFFF")

    # Criar o frame de cima (fundo branco)
    frame_emcima = ctk.CTkFrame(root_tk, width=400, height=200, fg_color="white")
    frame_emcima.pack(side="top", fill="both", expand=True)

    # Criar o frame de baixo (cor #2d0b44)
    frame_embaixo = ctk.CTkFrame(root_tk, width=400, height=50, fg_color="#2d0b44")
    frame_embaixo.pack(side="bottom", fill="x")

    # Configurar o layout do frame de cima
    frame_emcima.grid_columnconfigure(0, weight=1)
    frame_emcima.grid_columnconfigure(1, weight=1)
    frame_emcima.grid_rowconfigure(0, weight=1)
    frame_emcima.grid_rowconfigure(1, weight=1)

    # Adicionar o Label "Extrato" no centro do frame de cima
    root_tk.Extrato_Label = ctk.CTkLabel(frame_emcima, text="Extrato", text_color="#000000", font=("Helvetica", 30, "bold"))
    root_tk.Extrato_Label.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="n")

    # Suponha que você já tenha a conexão e o cursor definidos corretamente
    sald = cursor.execute(f"SELECT banco.saldo FROM banco JOIN usuario ON banco.id_usuario = usuario.id WHERE usuario.cpf = '{Ecpf}';").fetchone()

    # Adicionar o saldo no canto superior direito do frame de cima
    Saldo = ctk.CTkLabel(frame_emcima, text=f"R${sald[0]}", text_color="#000000", font=("Helvetica", 20, "bold"))
    Saldo.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    # Configurar o layout do frame de baixo (para os botões)
    frame_embaixo.grid_columnconfigure((0, 1, 2), weight=1)

    # Adicionar os botões no frame de baixo
    botao_D = ctk.CTkButton(frame_embaixo, text="Depósito", width=50, command=lambda: Deposito(Ecpf))
    botao_D.grid(row=0, column=0, padx=10, pady=70)

    botao_P = ctk.CTkButton(frame_embaixo, text="Pix", width=50, command=lambda: Pix(Ecpf))
    botao_P.grid(row=0, column=1, padx=10, pady=70)

    botao_S = ctk.CTkButton(frame_embaixo, text="Sacar", width=50, command=lambda: Saque(Ecpf))
    botao_S.grid(row=0, column=2, padx=10, pady=70)

    # Adicionar a imagem (se necessário)
    my_image = ctk.CTkImage(dark_image=Image.open('Lu.png'), size=(75, 75))
    image_label = ctk.CTkLabel(root_tk, image=my_image, text="")
    image_label.place(x=30, y=25)

def Pix(Ecpf):
    for widget in root_tk.winfo_children():
        widget.destroy()
    root_tk.configure(fg_color="#FFFFFF")

    # Criar o frame de cima (fundo branco)
    frame_emcima = ctk.CTkFrame(root_tk, width=400, height=200, fg_color="white")
    frame_emcima.pack(side="top", fill="both", expand=True)

    # Criar o frame de baixo (cor #2d0b44)

    frame_embaixo = ctk.CTkFrame(root_tk, width=400, height=50, fg_color="#2d0b44")
    frame_embaixo.pack(side="bottom", fill="x")

    # Configurar o layout do frame de cima
    frame_emcima.grid_columnconfigure(0, weight=1)
    frame_emcima.grid_columnconfigure(1, weight=1)
    frame_emcima.grid_columnconfigure(2, weight=1)
    frame_emcima.grid_rowconfigure(0, weight=1)
    frame_emcima.grid_rowconfigure(1, weight=1)

    # Adicionar o Label "Extrato" no centro do frame de cima
    root_tk.Extrato_Label = ctk.CTkLabel(frame_emcima, text="Transferencia/Pix", text_color="#000000", font=("Helvetica", 30, "bold"))
    root_tk.Extrato_Label.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="n")

    # Adicionar o saldo no canto superior direito do frame de cima
    pix_cpf = ctk.CTkEntry(frame_emcima, fg_color="#FFFFFF", border_color="#000000", placeholder_text="CPF do Beneficiario...", placeholder_text_color="#000000")
    pix_cpf.grid(row=1, column=0, padx=10, pady=10, sticky="nesw")
    quantia = ctk.CTkEntry(frame_emcima, fg_color="#FFFFFF", border_color="#000000", placeholder_text="Valor do Pix...", placeholder_text_color="#000000")
    quantia.grid(row=1, column=1, padx=10, pady=10, sticky="nesw")
    Faz_pix = ctk.CTkButton(frame_emcima, text="Fazer Pix", width=50, command=lambda: Fazer_pix(pix_cpf, quantia))
    Faz_pix.grid(row=2, column=0, padx=10, pady=10, sticky="nesw")

    # Configurar o layout do frame de baixo (para os botões)
    frame_embaixo.grid_columnconfigure((0, 1, 2), weight=1)

    # Adicionar os botões no frame de baixo
    botao_D = ctk.CTkButton(frame_embaixo, text="Extrato", width=50, command=lambda: Extrato(Ecpf))
    botao_D.grid(row=0, column=0, padx=10, pady=70)

    botao_P = ctk.CTkButton(frame_embaixo, text="Pix", width=50, command=lambda: Extrato(Ecpf))
    botao_P.grid(row=0, column=1, padx=10, pady=70)

    botao_S = ctk.CTkButton(frame_embaixo, text="Sacar", width=50, command=lambda: Saque(Ecpf))
    botao_S.grid(row=0, column=2, padx=10, pady=70)

def Fazer_pix(pix_cpf, quantia):
    pass

def Saque(Ecpf):
    for widget in root_tk.winfo_children():
        widget.destroy()
    root_tk.configure(fg_color="#FFFFFF")

    # Criar o frame de cima (fundo branco)
    frame_emcima = ctk.CTkFrame(root_tk, width=400, height=200, fg_color="white")
    frame_emcima.pack(side="top", fill="both", expand=True)

    # Criar o frame de baixo (cor #2d0b44)
    frame_embaixo = ctk.CTkFrame(root_tk, width=400, height=50, fg_color="#2d0b44")
    frame_embaixo.pack(side="bottom", fill="x")

    # Configurar o layout do frame de cima
    frame_emcima.grid_columnconfigure(0, weight=1)
    frame_emcima.grid_columnconfigure(1, weight=1)
    frame_emcima.grid_rowconfigure(0, weight=1)
    frame_emcima.grid_rowconfigure(1, weight=1)

    # Adicionar o Label "Extrato" no centro do frame de cima
    root_tk.Extrato_Label = ctk.CTkLabel(frame_emcima, text="Sacar", text_color="#000000", font=("Helvetica", 30, "bold"))
    root_tk.Extrato_Label.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="n")

    # Adicionar o saldo no canto superior direito do frame de cima
    Sacar_entry = ctk.CTkEntry(frame_emcima, fg_color="#FFFFFF", border_color="#000000", placeholder_text="Valor do saque", placeholder_text_color="#000000")
    Sacar_entry.grid(row=1, column=1, padx=10, pady=10, sticky="nesw")
    botao_saq = ctk.CTkButton(frame_emcima, text="Sacar", width=50, command=lambda: Sacar(Sacar_entry, Ecpf))
    botao_saq.grid(row=1, column=0, padx=10, pady=70)

    # Configurar o layout do frame de baixo (para os botões)
    frame_embaixo.grid_columnconfigure((0, 1, 2), weight=1)

    # Adicionar os botões no frame de baixo
    botao_D = ctk.CTkButton(frame_embaixo, text="Extrato", width=50, command=lambda: Extrato(Ecpf))
    botao_D.grid(row=0, column=0, padx=10, pady=70)

    botao_P = ctk.CTkButton(frame_embaixo, text="Pix", width=50, command=lambda: Pix(Ecpf))
    botao_P.grid(row=0, column=1, padx=10, pady=70)

    botao_S = ctk.CTkButton(frame_embaixo, text="Depositar", width=50, command=lambda: Deposito(Ecpf))
    botao_S.grid(row=0, column=2, padx=10, pady=70)

def Sacar(Sacar_entry, Ecpf):
    saq = Decimal(Sacar_entry.get())
    idesaldo = cursor.execute(f"SELECT banco.id_usuario, banco.saldo FROM banco JOIN usuario ON banco.id_usuario = usuario.id WHERE usuario.cpf = '{Ecpf}';").fetchone()
    if saq <= idesaldo[1]:
        cursor.execute(f"UPDATE banco SET saldo={idesaldo[1] - saq} WHERE id_usuario = '{idesaldo[0]}';")
        cursor.commit()
        print('Foi, eu acho')

    elif saq > idesaldo[1]:
        print('NOAAOOOOOOOOOOOOeu acho')

def Deposito(Ecpf):
    for widget in root_tk.winfo_children():
        widget.destroy()
    root_tk.configure(fg_color="#FFFFFF")

    # Criar o frame de cima (fundo branco)
    frame_emcima = ctk.CTkFrame(root_tk, width=400, height=200, fg_color="white")
    frame_emcima.pack(side="top", fill="both", expand=True)

    # Criar o frame de baixo (cor #2d0b44)
    frame_embaixo = ctk.CTkFrame(root_tk, width=400, height=150, fg_color="#2d0b44")
    frame_embaixo.pack(side="bottom", fill="both", expand=True)

    # Configurar o layout do frame de cima
    frame_emcima.grid_columnconfigure(0, weight=1)
    frame_emcima.grid_columnconfigure(1, weight=1)
    frame_emcima.grid_rowconfigure(0, weight=1)
    frame_emcima.grid_rowconfigure(1, weight=1)

    # Adicionar o Label "Extrato" no centro do frame de cima
    root_tk.Extrato_Label = ctk.CTkLabel(frame_emcima, text="Depositar", text_color="#000000", font=("Helvetica", 30, "bold"))
    root_tk.Extrato_Label.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="n")

    # Adicionar o saldo no canto superior direito do frame de cima
    deposit_entry = ctk.CTkEntry(frame_emcima, fg_color="#FFFFFF", border_color="#000000", placeholder_text="Valor do Depósito", placeholder_text_color="#000000")
    deposit_entry.grid(row=1, column=1, padx=10, pady=10, sticky="nesw")
    botao_dep = ctk.CTkButton(frame_emcima, text="Depósitar", width=50, command=lambda: depositar(deposit_entry, Ecpf))
    botao_dep.grid(row=1, column=0, padx=10, pady=70)

    # Configurar o layout do frame de baixo (para os botões)
    frame_embaixo.grid_columnconfigure((0, 1, 2), weight=1)

    # Adicionar os botões no frame de baixo
    botao_D = ctk.CTkButton(frame_embaixo, text="Extrato", width=50, command=lambda: Extrato(Ecpf))
    botao_D.grid(row=0, column=0, padx=10, pady=70)

    botao_P = ctk.CTkButton(frame_embaixo, text="Pix", width=50, command=lambda: Pix(Ecpf))
    botao_P.grid(row=0, column=1, padx=10, pady=70)

    botao_S = ctk.CTkButton(frame_embaixo, text="Sacar", width=50, command=lambda: Saque(Ecpf))
    botao_S.grid(row=0, column=2, padx=10, pady=70)

    # Adicionar a imagem (se necessário)
    my_image = ctk.CTkImage(dark_image=Image.open('Lu.png'), size=(75, 75))
    image_label = ctk.CTkLabel(root_tk, image=my_image, text="")
    image_label.place(x=30, y=25)

def depositar(deposit_entry, Ecpf):
    depo = Decimal(deposit_entry.get())
    print(Ecpf)
    idesaldo = cursor.execute(f"SELECT banco.id_usuario, banco.saldo FROM banco JOIN usuario ON banco.id_usuario = usuario.id WHERE usuario.cpf = '{Ecpf}';").fetchone()
    cursor.execute(f"UPDATE banco SET saldo={depo + idesaldo[1]} WHERE id_usuario = '{idesaldo[0]}';")
    cursor.commit()
    print('Foi, eu acho')



# Cria a janela principal
root_tk = ctk.CTk()
ctk.set_appearance_mode("light")
root_tk.geometry("400x400")
root_tk.title("Lu Bank")

# Define a cor de fundo da janela
root_tk.configure(fg_color="#2d0b44")  # Cor de fundo

# Inicia a interface principal
interface()

root_tk.mainloop()
