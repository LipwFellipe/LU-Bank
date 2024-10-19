import customtkinter as ctk
import pyodbc
from PIL import Image
from decimal import Decimal

conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server}; Server=LIPWNOTEBOOK\\SQLEXPRESS;Database=Banco_NuLipw;Trusted_Connection=yes;TrustServerCertificate=yes;')
print("Conexão bem sucedida")
cursor = conn.cursor()

def configurar_label(erro, widget, label, mensagem, cor_texto, cor_borda):
    label.configure(text=mensagem, text_color=cor_texto)
    widget.configure(border_color=cor_borda, placeholder_text=mensagem if erro else "", text_color=cor_texto)

def validar_cpf(cpf):
    return len(cpf) == 11 and cpf.isdigit()

def inserir_usuario(Inome, Isenha, Icpf):
    criar = f"""INSERT INTO usuario(nome, senha, cpf) VALUES('{Inome}', '{Isenha}', '{Icpf}')"""
    cursor.execute(criar)
    cursor.commit()
    id = cursor.execute(f"SELECT id FROM usuario WHERE cpf = '{Icpf}'").fetchone()
    cursor.execute(f"""INSERT INTO banco VALUES(0.00, '{id[0]}')""")
    cursor.commit()

def INSERT(cad_nome, cadas_cpf, cad_senha, cad_senha1, silvia_label):
    try:
        Inome = cad_nome.get()
        Icpf = cadas_cpf.get()
        Isenha = cad_senha.get()
        Isenha1 = cad_senha1.get()

        NomeCpf = cursor.execute("SELECT nome, cpf FROM usuario").fetchall()
        nomes, cpfs = zip(*NomeCpf)

        if Inome in nomes:
            configurar_label(True, cad_nome, silvia_label, "Nome já cadastrado!", "#fc1406", "#fc1406")
        else:
            configurar_label(False, cad_nome, silvia_label, "", "#000000", "#000000")

        if Isenha != Isenha1:
            configurar_label(True, cad_senha, silvia_label, "Senhas não coincidem!", "#fc1406", "#fc1406")
            configurar_label(True, cad_senha1, silvia_label, "", "#fc1406", "#fc1406")
        else:
            configurar_label(False, cad_senha, silvia_label, "", "#000000", "#000000")
            configurar_label(False, cad_senha1, silvia_label, "", "#000000", "#000000")

        if Icpf in cpfs:
            configurar_label(True, cadas_cpf, silvia_label, "CPF já cadastrado!", "#fc1406", "#fc1406")
        elif not validar_cpf(Icpf):
            configurar_label(True, cadas_cpf, silvia_label, "CPF inválido!", "#fc1406", "#fc1406")
        else:
            configurar_label(False, cadas_cpf, silvia_label, "", "#000000", "#000000")

        if all([Isenha == Isenha1, Inome, validar_cpf(Icpf), Icpf not in cpfs, Inome not in nomes]):
            inserir_usuario(Inome, Isenha, Icpf)
            configurar_label(False, cad_nome, silvia_label, "Usuário criado com sucesso!", "#117f09", "#117f09")
            configurar_label(False, cad_senha, silvia_label, "", "#117f09", "#117f09")
            configurar_label(False, cad_senha1, silvia_label, "", "#117f09", "#117f09")
            configurar_label(False, cadas_cpf, silvia_label, "", "#117f09", "#117f09")

    except Exception as e:
        print(f"Erro: {e}")
        configurar_label(True, cad_nome, silvia_label, "Erro no cadastro", "#fc1406", "#fc1406")
        configurar_label(True, cad_senha, silvia_label, "ERRO", "#fc1406", "#fc1406")
        configurar_label(True, cad_senha1, silvia_label, "ERRO", "#fc1406", "#fc1406")
        configurar_label(True, cadas_cpf, silvia_label, "ERRO", "#fc1406", "#fc1406")

def cadastro():
    # Remove os widgets da primeira página
    for widget in root_tk.winfo_children():
        widget.grid_forget()

    # Titulos
    nome_label = ctk.CTkLabel(root_tk, text="Cadastre-se", text_color="#FFFFFF", font=("Helvetica", 30, "bold"))
    nome_label.grid(row=0, column=0, padx=20, pady=45, columnspan=2)
    silvia_label = ctk.CTkLabel(root_tk, text="", text_color="#FFFFFF", font=("Helvetica", 20))
    silvia_label.grid(row=1, column=0, padx=20, pady=(5, 0), sticky="w", columnspan=2)

    # Entrada Nome
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
    # Função entrar é auto explicativa
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
    for widget in root_tk.winfo_children():
        widget.destroy()
    root_tk.configure(fg_color="#2d0b44")

    my_image = ctk.CTkImage(dark_image=Image.open('Lu.png'), size=(75, 75))
    image_label = ctk.CTkLabel(root_tk, image=my_image, text="")
    image_label.place(x=30, y=25)

    titulo_label = ctk.CTkLabel(root_tk, text="Entrar", text_color="#FFFFFF", font=("Helvetica", 30, "bold"))
    titulo_label.grid(row=0, column=0, padx=20, pady=45, columnspan=2)

    enter_cpf = ctk.CTkEntry(root_tk, fg_color="#FFFFFF", border_color="#000000", placeholder_text="Digite seu CPF...", placeholder_text_color="#000000")
    enter_cpf.grid(row=1, column=0, padx=20, pady=20, sticky="ew", columnspan=2)
    root_tk.grid_columnconfigure(0, weight=1)

    enter_senha = ctk.CTkEntry(root_tk, fg_color="#FFFFFF", border_color="#000000", placeholder_text="Digite sua senha...", placeholder_text_color="#000000")
    enter_senha.grid(row=2, column=0, padx=20, pady=20, sticky="ew", columnspan=2)

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

    frame_emcima = ctk.CTkFrame(root_tk, width=400, height=200, fg_color="white")
    frame_emcima.pack(side="top", fill="both", expand=True)
    frame_embaixo = ctk.CTkFrame(root_tk, width=400, height=50, fg_color="#2d0b44")
    frame_embaixo.pack(side="bottom", fill="x")
    frame_emcima.grid_columnconfigure(0, weight=1)
    frame_emcima.grid_columnconfigure(1, weight=1)
    frame_emcima.grid_rowconfigure(0, weight=1)
    frame_emcima.grid_rowconfigure(1, weight=1)

    root_tk.Extrato_Label = ctk.CTkLabel(frame_emcima, text="Extrato", text_color="#000000", font=("Helvetica", 30, "bold"))
    root_tk.Extrato_Label.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="n")

    pega_nome = cursor.execute(f"SELECT nome FROM usuario WHERE cpf = '{Ecpf}'").fetchone()
    root_tk.Nom_Label = ctk.CTkLabel(frame_emcima, text=f"{pega_nome[0]}, seu saldo é:", text_color="#000000", font=("Helvetica", 20, "bold"))
    root_tk.Nom_Label.grid(row=1, column=0, columnspan=2, padx=20, pady=31, sticky="n")

    # Consulta no banco de dados 
    sald = cursor.execute(f"SELECT banco.saldo FROM banco JOIN usuario ON banco.id_usuario = usuario.id WHERE usuario.cpf = '{Ecpf}';").fetchone()
    Saldo = ctk.CTkLabel(frame_emcima, text=f"R${sald[0]}", text_color="#000000", font=("Helvetica", 50, "bold"))
    Saldo.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    # Configurar o layout do frame de baixo (para os botões)
    frame_embaixo.grid_columnconfigure((0, 1, 2), weight=1)

    botao_D = ctk.CTkButton(frame_embaixo, text="Depósito", width=50, command=lambda: Deposito(Ecpf), fg_color="#5C0178", hover_color="#700192")
    botao_D.grid(row=0, column=0, padx=10, pady=70)
    botao_P = ctk.CTkButton(frame_embaixo, text="Pix", width=50, command=lambda: Pix(Ecpf), fg_color="#5C0178", hover_color="#700192")
    botao_P.grid(row=0, column=1, padx=10, pady=70)
    botao_S = ctk.CTkButton(frame_embaixo, text="Sacar", width=50, command=lambda: Saque(Ecpf), fg_color="#5C0178", hover_color="#700192")
    botao_S.grid(row=0, column=2, padx=10, pady=70)

def Pix(Ecpf):
    for widget in root_tk.winfo_children():
        widget.destroy()
    root_tk.configure(fg_color="#FFFFFF")
    
    frame_emcima = ctk.CTkFrame(root_tk, width=400, height=200, fg_color="white")
    frame_emcima.pack(side="top", fill="both", expand=True)

    frame_embaixo = ctk.CTkFrame(root_tk, width=400, height=50, fg_color="#2d0b44")
    frame_embaixo.pack(side="bottom", fill="x")

    frame_emcima.grid_columnconfigure(0, weight=1)
    frame_emcima.grid_columnconfigure(1, weight=1)
    frame_emcima.grid_columnconfigure(2, weight=1)
    frame_emcima.grid_rowconfigure(0, weight=1)
    frame_emcima.grid_rowconfigure(1, weight=1)
    frame_emcima.grid_rowconfigure(3, weight=1)

    root_tk.pix_Label = ctk.CTkLabel(frame_emcima, text="Transferencia/Pix", text_color="#000000", font=("Helvetica", 30, "bold"))
    root_tk.pix_Label.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="n")

    sil_Label = ctk.CTkLabel(frame_emcima, text="", text_color="#000000", font=("Helvetica", 20, "bold"))
    sil_Label.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="n")

    #Consultas para pegar o nome da pessoa
    nomin = cursor.execute(f"SELECT nome FROM usuario WHERE cpf = '{Ecpf}'").fetchone()
    cursor.execute(f"SELECT nome FROM usuario WHERE nome <> '{nomin[0]}';")
    choice = [row[0] for row in cursor.fetchall()]

    # Variável para armazenar a seleção
    selected_name = ctk.StringVar(value=choice[0] if choice else "")  # valor padrão

    pix_nome = ctk.CTkOptionMenu(frame_emcima, variable=selected_name, dropdown_hover_color="#2d0b44", dropdown_text_color="#FFFFFF", values=choice, fg_color="#5C0178", dropdown_fg_color="#700192", text_color="#FFFFFF", button_color="#2d0b44")
    pix_nome.grid(row=2, column=0, padx=10, pady=10, sticky="nesw")
    
    quantia = ctk.CTkEntry(frame_emcima, fg_color="#FFFFFF", border_color="#000000", placeholder_text="EX: 10.75", placeholder_text_color="#000000")
    quantia.grid(row=2, column=1, padx=10, pady=10, sticky="nesw", columnspan=2)
    
    Faz_pix = ctk.CTkButton(frame_emcima, text="Fazer Pix", width=50, command=lambda: Fazer_pix(selected_name.get(), quantia, Ecpf, sil_Label), fg_color="#5C0178", hover_color="#2d0b44")
    Faz_pix.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=3)

    frame_embaixo.grid_columnconfigure((0, 1, 2), weight=1)

    botao_E = ctk.CTkButton(frame_embaixo, text="Extrato", width=50, command=lambda: Extrato(Ecpf), fg_color="#5C0178", hover_color="#700192")
    botao_E.grid(row=0, column=0, padx=10, pady=70)

    botao_D = ctk.CTkButton(frame_embaixo, text="Deposito", width=50, command=lambda: Deposito(Ecpf), fg_color="#5C0178", hover_color="#700192")
    botao_D.grid(row=0, column=1, padx=10, pady=70)

    botao_S = ctk.CTkButton(frame_embaixo, text="Sacar", width=50, command=lambda: Saque(Ecpf), fg_color="#5C0178", hover_color="#700192")
    botao_S.grid(row=0, column=2, padx=10, pady=70)

def Fazer_pix(selected_user, quantia, Ecpf, sil_Label):
    try:
        maisdindin = Decimal(quantia.get())
        # Dinheiro do Usuario e da Pessoa beneficiaria
        id_U = cursor.execute(f"SELECT id FROM usuario WHERE cpf = '{Ecpf}';").fetchone()
        id_P = cursor.execute(f"SELECT id FROM usuario WHERE nome = '{selected_user}';").fetchone()
        dindinUsu = cursor.execute(f"SELECT saldo FROM banco WHERE id_usuario = '{id_U[0]}';").fetchone()
        dindinPes = cursor.execute(f"SELECT saldo FROM banco WHERE id_usuario = '{id_P[0]}';").fetchone()
        if dindinUsu[0] >= maisdindin:
            cursor.execute(f"UPDATE banco SET saldo = {dindinPes[0]} + {maisdindin} FROM banco WHERE id_usuario = {id_P[0]};")
            cursor.execute(f"UPDATE banco SET saldo = {dindinUsu[0]} - {maisdindin} FROM banco WHERE id_usuario = {id_U[0]};")
            cursor.commit()
            sil_Label.configure(text=f"Pix realizado para {selected_user}", text_color="#117f09")
            quantia.configure(border_color="#117f09")
        elif dindinUsu[0] < maisdindin:
            sil_Label.configure(text="Dinheiro insuficiente para Pix", text_color="#fc1406")
            quantia.configure(border_color="#fc1406")
        elif maisdindin == "":
            sil_Label.configure(text="Digite no campo abaixo", text_color="#fc1406")
            quantia.configure(border_color="#fc1406")
    except:
        sil_Label.configure(text="Digite apenas numeros", text_color="#fc1406")
        quantia.configure(border_color="#fc1406")

def Saque(Ecpf):
    for widget in root_tk.winfo_children():
        widget.destroy()
    root_tk.configure(fg_color="#FFFFFF")
    frame_emcima = ctk.CTkFrame(root_tk, width=400, height=200, fg_color="white")
    frame_emcima.pack(side="top", fill="both", expand=True)
    frame_embaixo = ctk.CTkFrame(root_tk, width=400, height=50, fg_color="#2d0b44")
    frame_embaixo.pack(side="bottom", fill="x")

    # Layout Frames
    frame_emcima.grid_columnconfigure(0, weight=1)
    frame_emcima.grid_columnconfigure(1, weight=1)
    frame_emcima.grid_rowconfigure(0, weight=1)
    frame_emcima.grid_rowconfigure(1, weight=1)
    frame_embaixo.grid_columnconfigure((0, 1, 2), weight=1)

    root_tk.Extrato_Label = ctk.CTkLabel(frame_emcima, text="Sacar", text_color="#000000", font=("Helvetica", 30, "bold"))
    root_tk.Extrato_Label.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="n")

    silvia = ctk.CTkLabel(frame_emcima, text="Digite um valor para Saque", text_color="#000000", font=("Helvetica", 20, "bold"))
    silvia.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="nesw")
    Sacar_entry = ctk.CTkEntry(frame_emcima, fg_color="#FFFFFF", border_color="#000000", placeholder_text="EX: 12.50", placeholder_text_color="#000000")
    Sacar_entry.grid(row=2, column=0, padx=10, pady=10, sticky="nesw")
    botao_saq = ctk.CTkButton(frame_emcima, text="Sacar", width=50, command=lambda: Sacar(Sacar_entry, Ecpf, silvia), fg_color="#5C0178", hover_color="#68102F")
    botao_saq.grid(row=2, column=1, padx=10, pady=30)

    # Botões
    botao_E = ctk.CTkButton(frame_embaixo, text="Extrato", width=50, command=lambda: Extrato(Ecpf), fg_color="#5C0178", hover_color="#700192")
    botao_E.grid(row=0, column=0, padx=10, pady=70)
    botao_P = ctk.CTkButton(frame_embaixo, text="Pix", width=50, command=lambda: Pix(Ecpf), fg_color="#5C0178", hover_color="#700192")
    botao_P.grid(row=0, column=1, padx=10, pady=70)
    botao_D = ctk.CTkButton(frame_embaixo, text="Depositar", width=50, command=lambda: Deposito(Ecpf), fg_color="#5C0178", hover_color="#700192")
    botao_D.grid(row=0, column=2, padx=10, pady=70)

def Sacar(Sacar_entry, Ecpf, silvia):
    try:
        saq = Decimal(Sacar_entry.get())
        idesaldo = cursor.execute(f"SELECT banco.id_usuario, banco.saldo FROM banco JOIN usuario ON banco.id_usuario = usuario.id WHERE usuario.cpf = '{Ecpf}';").fetchone()
        if saq <= idesaldo[1]:
            cursor.execute(f"UPDATE banco SET saldo={idesaldo[1] - saq} WHERE id_usuario = '{idesaldo[0]}';")
            cursor.commit()
            silvia.configure(text=f"Saque efetuado com sucesso", text_color="#117f09")
            Sacar_entry.configure(border_color="#117f09", placeholder_text="", placeholder_text_color="#117f09")
            Sacar_entry.delete(0, "end")
        elif saq > idesaldo[1]:
            Sacar_entry.configure(border_color="#fc1406", placeholder_text="Voce não tem dinheiro para sacar...", text_color="#fc1406", placeholder_text_color="#fc1406")
            silvia.configure(text=f"Voce não tem R${saq} para sacar...", text_color="#fc1406")
            Sacar_entry.delete(0, "end")
        elif saq < 0:
            Sacar_entry.configure(border_color="#fc1406", placeholder_text="Voce não tem dinheiro para sacar...", text_color="#fc1406", placeholder_text_color="#fc1406")
            silvia.configure(text=f"Voce não tem R${saq} para sacar...", text_color="#fc1406")
            Sacar_entry.delete(0, "end")
    except:
        silvia.configure(text="Digite apenas numeros...", text_color="#fc1406")
        Sacar_entry.configure(border_color="#fc1406")

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
    root_tk.Deposito_Label = ctk.CTkLabel(frame_emcima, text="Depositar", text_color="#000000", font=("Helvetica", 30, "bold"))
    root_tk.Deposito_Label.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="n")

    Silvya_Label = ctk.CTkLabel(frame_emcima, text="Digite um valor para deposito", text_color="#000000", font=("Helvetica", 20, "bold"))
    Silvya_Label.grid(row=1, column=0, columnspan=2, padx=20, pady=31, sticky="n")

    # Adicionar o saldo no canto superior direito do frame de cima
    deposit_entry = ctk.CTkEntry(frame_emcima, fg_color="#FFFFFF", border_color="#000000", placeholder_text="EX: 10.50", placeholder_text_color="#000000")
    deposit_entry.grid(row=2, column=0, padx=10, pady=10, sticky="nesw")
    botao_dep = ctk.CTkButton(frame_emcima, text="Depósitar", width=50, command=lambda: depositar(deposit_entry, Ecpf, Silvya_Label), fg_color="#5C0178", hover_color="#700192")
    botao_dep.grid(row=2, column=1, padx=10, pady=30)

    # Configurar o layout do frame de baixo (para os botões)
    frame_embaixo.grid_columnconfigure((0, 1, 2), weight=1)

    # Adicionar os botões no frame de baixo
    botao_E = ctk.CTkButton(frame_embaixo, text="Extrato", width=50, command=lambda: Extrato(Ecpf), fg_color="#5C0178", hover_color="#700192")
    botao_E.grid(row=0, column=0, padx=10, pady=70)

    botao_P = ctk.CTkButton(frame_embaixo, text="Pix", width=50, command=lambda: Pix(Ecpf), fg_color="#5C0178", hover_color="#700192")
    botao_P.grid(row=0, column=1, padx=10, pady=70)

    botao_S = ctk.CTkButton(frame_embaixo, text="Sacar", width=50, command=lambda: Saque(Ecpf), fg_color="#5C0178", hover_color="#700192")
    botao_S.grid(row=0, column=2, padx=10, pady=70)

def depositar(deposit_entry, Ecpf, Silvya_Label):
    try:
        depo = Decimal(deposit_entry.get())
        idesaldo = cursor.execute(f"SELECT banco.id_usuario, banco.saldo FROM banco JOIN usuario ON banco.id_usuario = usuario.id WHERE usuario.cpf = '{Ecpf}';").fetchone()
        if depo + idesaldo[1] >= 100000000:
            Silvya_Label.configure(text=f"O Limite de dinheiro é 100000000", text_color="#fc1406")
            deposit_entry.configure(border_color="#fc1406", placeholder_text="", placeholder_text_color="#fc1406")
            deposit_entry.delete(0, "end")    
        elif depo <= 0:
            Silvya_Label.configure(text=f"Digite um numero positivo", text_color="#fc1406")
            deposit_entry.configure(border_color="#fc1406", placeholder_text="", placeholder_text_color="#fc1406")
            deposit_entry.delete(0, "end")    
        elif depo >= 1:
            cursor.execute(f"UPDATE banco SET saldo={depo + idesaldo[1]} WHERE id_usuario = '{idesaldo[0]}';")
            cursor.commit()
            Silvya_Label.configure(text=f"Deposito Efetuado com Sucesso", text_color="#117f09")
            deposit_entry.configure(border_color="#117f09", placeholder_text="", placeholder_text_color="#117f09")
            deposit_entry.delete(0, "end")
        
    except:
        Silvya_Label.configure(text="Digite numeros sem letras ou virgulas", text_color="#fc1406")
        deposit_entry.configure(border_color="#fc1406")
        deposit_entry.delete(0, "end")

# Cria a janela principal
root_tk = ctk.CTk()
ctk.set_appearance_mode("light")
root_tk.geometry("400x400")
root_tk.title("Lu Bank")
root_tk.configure(fg_color="#2d0b44")
interface()

root_tk.mainloop()
