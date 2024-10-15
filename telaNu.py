import customtkinter as ctk
import pyodbc
conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server}; Server=LIPWNOTEBOOK\\SQLEXPRESS;Database=Banco_NuLipw;Trusted_Connection=yes;TrustServerCertificate=yes;')
print("Conexão bem sucedida")
cursor = conn.cursor()

def INSERT(cad_nome, cad_email, cad_senha, cad_senha1):
    Inome = cad_nome.get()
    Imail = cad_email.get()
    Isenha = cad_senha.get()
    Isenha1 = cad_senha1.get()
    if not '@' in Imail:
        print("\033[91mDigite um E-mail válido\033[m")
    elif Isenha1 != Isenha:
        print("\033[91mSuas senhas não coincidem!\033[m")
    elif Isenha == Isenha1:
        criar = f"""INSERT INTO usuario(nome, email, senha) VALUES('{Inome}', '{Imail}', '{Isenha}')"""
        cursor.execute(criar)
        cursor.commit()
    print("Usuario criado com sucesso!")

def cadastro():
    # Remove os widgets da primeira página
    for widget in root_tk.winfo_children():
        widget.grid_forget()

    # Nova "página"
    titulo_label = ctk.CTkLabel(root_tk, text="Cadastre-se", text_color="#FFFFFF", font=("Helvetica", 30, "bold"))
    titulo_label.grid(row=0, column=0, padx=20, pady=45, columnspan=2)

    cad_nome = ctk.CTkEntry(root_tk, fg_color="#FFFFFF", border_color="#000000", placeholder_text="Digite seu Nome...", placeholder_text_color="#000000")
    cad_nome.grid(row=1, column=0, padx=20, pady=20, sticky="ew", columnspan=2)
    root_tk.grid_columnconfigure(0, weight=1)

    cad_email = ctk.CTkEntry(root_tk, fg_color="#FFFFFF", border_color="#000000", placeholder_text="Digite seu E-Mail...", placeholder_text_color="#000000")
    cad_email.grid(row=2, column=0, padx=20, pady=20, sticky="ew", columnspan=2)
    root_tk.grid_columnconfigure(0, weight=1)

    cad_senha = ctk.CTkEntry(root_tk, fg_color="#FFFFFF", border_color="#000000", placeholder_text="Digite sua senha...", placeholder_text_color="#000000")
    cad_senha.grid(row=3, column=0, sticky="w", padx=20, pady=20)
    cad_senha1 = ctk.CTkEntry(root_tk, fg_color="#FFFFFF", border_color="#000000", placeholder_text="Confirme sua senha...", placeholder_text_color="#000000")
    cad_senha1.grid(row=3, column=1, sticky="nsew", padx=20, pady=20)

    # Adiciona um botão para voltar à página anterior
    botao_voltar = ctk.CTkButton(root_tk, text="Voltar", fg_color="#000000", hover_color="#250438", command=interface)
    botao_voltar.grid(row=4, column=0, padx=20, pady=20, sticky="w")

    # Botão cadastrar com lambda para passar 'cad_nome'
    botao_cad = ctk.CTkButton(root_tk, text="Cadastrar", fg_color="#000000", hover_color="#250438", command=lambda: INSERT(cad_nome, cad_email, cad_senha, cad_senha1))
    botao_cad.grid(row=4, column=1, padx=20, pady=20)

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

    enter_nome = ctk.CTkEntry(root_tk, fg_color="#FFFFFF", border_color="#000000", placeholder_text="Digite seu nome...", placeholder_text_color="#000000")
    enter_nome.grid(row=1, column=0, padx=20, pady=20, sticky="ew", columnspan=2)
    root_tk.grid_columnconfigure(0, weight=1)

    enter_senha = ctk.CTkEntry(root_tk, fg_color="#FFFFFF", border_color="#000000", placeholder_text="Digite sua senha...", placeholder_text_color="#000000")
    enter_senha.grid(row=2, column=0, padx=20, pady=20, sticky="ew", columnspan=2)

    # Botão para entrar
    button2 = ctk.CTkButton(root_tk, text="Entrar", fg_color="#000000", hover_color="#250438", command=cadastro)
    button2.grid(row=3, column=0, padx=20, pady=10, columnspan=2)

    # Texto informativo abaixo do botão
    texto_clicavel = ctk.CTkLabel(root_tk, text="Clique aqui para abrir uma nova página", text_color="#FFFFFF", font=("Helvetica", 12, "underline"))
    texto_clicavel.grid(row=4, column=0, padx=20, pady=20, columnspan=2)
    texto_clicavel.bind("<Button-1>", lambda e: cadastro())  # Torna o texto clicável

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
