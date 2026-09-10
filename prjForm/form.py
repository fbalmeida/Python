import os
import json
import re
import customtkinter as ctk
from tkinter import messagebox

DATA_FILE = "data.json"

def toggle_document_fields():
    selecao = type_var.get()
    
    # Limpa o campo atual para não misturar dados
    entry_doc.delete(0, ctk.END)
    
    if selecao == "Física":
        label_doc.configure(text="CPF:")
        entry_doc.configure(placeholder_text="000.000.000-00")
    else:
        label_doc.configure(text="CNPJ:")
        entry_doc.configure(placeholder_text="00.000.000/0001-00")


def validate_and_save():
    """Valida as entradas e salva no arquivo JSON."""
    name = entry_name.get().strip()
    email = entry_email.get().strip()
    birth_date = entry_date.get().strip()
    gender = combo_gender.get()
    person_type = type_var.get()
    document = entry_doc.get().strip()
    
    # Verifica e-mail está vazio
    if not email:
        messagebox.showerror("Erro de Validação", "O campo de E-mail não pode ficar vazio!")
        return

    # Validação sintaxe de e-mail
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        messagebox.showerror("Erro de Validação", "Por favor, insira um e-mail válido.")
        return

    # Verifica data (DD/MM/YYYY = 10 caracteres)
    if len(birth_date) < 10:
        messagebox.showerror("Erro de Validação", "Por favor, insira uma data de nascimento completa (DD/MM/YYYY).")
        return

    # Verifica documento se é CPF Ou CNPJ e valida
    if not document:
        doc_nome = "CPF" if person_type == "Física" else "CNPJ"
        messagebox.showerror("Erro de Validação", f"O campo de {doc_nome} não pode ficar vazio!")
        return

    # Salvar dados
    data = {
        "name": name,
        "email": email,
        "birth_date": birth_date,
        "gender": gender,
        "person_type": person_type,
        "document": document
    }
    
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        messagebox.showinfo("Sucesso", "Dados validados e salvos com sucesso!")
    except Exception as e:
        messagebox.showerror("Error", f"Não foi possível salvar o arquivo: {e}")

def load_data():
    """LEr JSON local e valores default"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                entry_name.insert(0, data.get("name", ""))
                entry_email.insert(0, data.get("email", ""))
                entry_date.insert(0, data.get("birth_date", ""))
                combo_gender.set(data.get("gender", "M"))
                type_var.set(data.get("person_type", "Física"))
                #toggle_document_fields()
                entry_doc.insert(0, data.get("document", ""))
        except Exception as e:
            print(f"Erro ao carregar dados salvos: {e}")

def format_date_mask(event):
    """Máscara DD/MM/YYYY."""
    # Ignora as teclas Backspace e Delete para permitir correções do usuário
    if event.keysym in ("Backspace", "Delete"):
        return

    text = entry_date.get()
    text_clean = "".join(filter(str.isdigit, text)) # Mantém apenas números
    
    formatted = ""
    if len(text_clean) > 0:
        formatted += text_clean[:2]  # DD
    if len(text_clean) > 2:
        formatted += "/" + text_clean[2:4]  # MM
    if len(text_clean) > 4:
        formatted += "/" + text_clean[4:8]  # YYYY

    # Atualiza o campo de texto dinamicamente
    entry_date.delete(0, ctk.END)
    entry_date.insert(0, formatted)

def confirm_exit():
    """Confirmação Sair"""
    resposta = messagebox.askyesno("Confirmar Saída", "Deseja realmente sair sem salvar as alterações recentes?")
    if resposta: # Se clicar em 'Sim' (True)
        root.destroy()

# Configuração da Interface
ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue") 

root = ctk.CTk()
root.title("Cadastro de Pessoa")
root.geometry("350x650")

# Campo Nome
ctk.CTkLabel(root, text="Nome:").pack(pady=(15, 2))
entry_name = ctk.CTkEntry(root, placeholder_text="Digite seu nome", width=200)
entry_name.pack(pady=5)

# Campo E-mail
ctk.CTkLabel(root, text="E-mail:").pack(pady=(10, 2))
entry_email = ctk.CTkEntry(root, placeholder_text="Digite seu e-mail", width=200)
entry_email.pack(pady=5)

# Campo Data de Nascimento (com Máscara)
ctk.CTkLabel(root, text="Data de Nascimento (DD/MM/YYYY):").pack(pady=(10, 2))
entry_date = ctk.CTkEntry(root, placeholder_text="DD/MM/YYYY", width=80)
entry_date.pack(pady=5)
# Vincula o evento de soltar a tecla para disparar a máscara
entry_date.bind("<KeyRelease>", format_date_mask)

# Campo Gender
ctk.CTkLabel(root, text="Gênero:").pack(pady=(10, 2))
combo_gender = ctk.CTkComboBox(root, values=["M", "F"], width=80)
combo_gender.pack(pady=5)

#Campo Tipo Pessoa
ctk.CTkLabel(root, text="Tipo de Pessoa:").pack(pady=(10, 2))
type_var = ctk.StringVar(value="Física")

frame_radio = ctk.CTkFrame(root, fg_color="transparent")
frame_radio.pack(pady=5)

radio_fisica = ctk.CTkRadioButton(frame_radio, text="Física", variable=type_var, value="Física", command=toggle_document_fields)
radio_fisica.pack(side="left", padx=15)

radio_juridica = ctk.CTkRadioButton(frame_radio, text="Jurídica", variable=type_var, value="Jurídica", command=toggle_document_fields)
radio_juridica.pack(side="left", padx=15)

# CPF OU CNPJ
label_doc = ctk.CTkLabel(root, text="CPF:")
label_doc.pack(pady=(10, 2))
entry_doc = ctk.CTkEntry(root, placeholder_text="000.000.000-00", width=260)
entry_doc.pack(pady=5)


# --- BUTTONS CONTAINER ---
frame_botoes = ctk.CTkFrame(root, fg_color="transparent")
frame_botoes.pack(pady=30)
# Botão Salvar
submit_btn = ctk.CTkButton(frame_botoes, text="Salvar", command=validate_and_save, width=110)
submit_btn.pack(side="left", padx=10)
# Botão Sair 
exit_btn = ctk.CTkButton(frame_botoes, text="Sair", command=confirm_exit, width=110, fg_color="#D32F2F", hover_color="#B71C1C")
exit_btn.pack(side="left", padx=10)

load_data()
root.mainloop()
