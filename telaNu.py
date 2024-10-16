import customtkinter as ctk
import pyodbc
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

def ENTRAR(enter_nome, enter_senha):
    try:
        Ecpf = enter_nome.get()
        Esenha = enter_senha.get()
        cursor.execute(f"SELECT senha FROM usuario WHERE cpf = '{Ecpf}'")
        resul = cursor.fetchone()
        if Esenha == resul[0]:
            banco()
    except:
        enter_nome.configure(border_color="#fc1406", placeholder_text="Digite um CPF valido...", text_color="#fc1406", placeholder_text_color="#fc1406")
        enter_senha.configure(border_color="#fc1406", placeholder_text="Digite uma senha valida...", text_color="#fc1406", placeholder_text_color="#fc1406")
            
def interface():
    # Limpa os widgets existentes (caso esteja voltando da nova página)
    for widget in root_tk.winfo_children():
        widget.grid_forget()

    from PIL import Image
    my_image = ctk.CTkImage(dark_image=Image.open('Lu.png'), size=(75, 75))
    image_label = ctk.CTkLabel(root_tk, image=my_image, text="")
    image_label.place(x=30, y=25)

    # Seção inicial (primeira "página")
    titulo_label = ctk.CTkLabel(root_tk, text="Entrar", text_color="#FFFFFF", font=("Helvetica", 30, "bold"))
    titulo_label.grid(row=0, column=0, padx=20, pady=45, columnspan=2)

    enter_nome = ctk.CTkEntry(root_tk, fg_color="#FFFFFF", border_color="#000000", placeholder_text="Digite seu CPF...", placeholder_text_color="#000000")
    enter_nome.grid(row=1, column=0, padx=20, pady=20, sticky="ew", columnspan=2)
    root_tk.grid_columnconfigure(0, weight=1)

    enter_senha = ctk.CTkEntry(root_tk, fg_color="#FFFFFF", border_color="#000000", placeholder_text="Digite sua senha...", placeholder_text_color="#000000")
    enter_senha.grid(row=2, column=0, padx=20, pady=20, sticky="ew", columnspan=2)

    # Botão para entrar
    button2 = ctk.CTkButton(root_tk, text="Entrar", fg_color="#000000", hover_color="#250438", command=lambda: ENTRAR(enter_nome, enter_senha))
    button2.grid(row=3, column=0, padx=20, pady=10, columnspan=2)

    # Texto informativo abaixo do botão
    texto_clicavel = ctk.CTkLabel(root_tk, text="Cadastre-se", text_color="#FFFFFF", font=("Helvetica", 12, "underline"))
    texto_clicavel.grid(row=4, column=0, padx=20, pady=20, columnspan=2)
    texto_clicavel.bind("<Button-1>", lambda e: cadastro())  # Torna o texto clicável

def banco():
    for widget in root_tk.winfo_children():
        widget.grid_forget()
        
    

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
