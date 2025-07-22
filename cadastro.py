import sqlite3
import re  # Importa o módulo para trabalhar com expressões regulares

conn = sqlite3.connect("banco_dados.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL
)
""")
conn.commit()

def validar_email(email):
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(padrao, email) is not None

def adicionar_usuario():
    nome = input("Digite o nome do usuário: ")
    email = input("Digite o e-mail do usuário: ")

    if not validar_email(email):
        print("❌ Email inválido. Tente novamente.")
        return

    cursor.execute("INSERT INTO usuarios (nome, email) VALUES (?, ?)", (nome, email))
    conn.commit()
    print("✅ Usuário cadastrado com sucesso!")

def listar_usuarios():
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    if usuarios:
        print("\n--- Lista de Usuários ---")
        for usuario in usuarios:
            print(f"ID: {usuario[0]} | Nome: {usuario[1]} | E-mail: {usuario[2]}")
    else:
        print("Nenhum usuário encontrado.")

def buscar_usuario():
    nome_busca = input("Digite o nome a buscar: ")
    cursor.execute("SELECT * FROM usuarios WHERE nome LIKE ?", (f'%{nome_busca}%',))
    resultados = cursor.fetchall()
    if resultados:
        for usuario in resultados:
            print(f"ID: {usuario[0]} | Nome: {usuario[1]} | E-mail: {usuario[2]}")
    else:
        print("Nenhum usuário encontrado com esse nome.")

def editar_usuario():
    listar_usuarios()
    try:
        id_usuario = int(input("Digite o ID do usuário que deseja editar: "))
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id_usuario,))
        usuario = cursor.fetchone()
        if usuario:
            novo_nome = input(f"Digite o novo nome (ou enter para manter '{usuario[1]}'): ")
            novo_email = input(f"Digite o novo e-mail (ou enter para manter '{usuario[2]}'): ")

            if novo_nome.strip() == "":
                novo_nome = usuario[1]
            if novo_email.strip() == "":
                novo_email = usuario[2]
            else:
                if not validar_email(novo_email):
                    print("❌ Email inválido. Edição cancelada.")
                    return

            cursor.execute("UPDATE usuarios SET nome = ?, email = ? WHERE id = ?", (novo_nome, novo_email, id_usuario))
            conn.commit()
            print("✅ Usuário atualizado com sucesso!")
        else:
            print("Usuário não encontrado.")
    except ValueError:
        print("ID inválido.")

def excluir_usuario():
    listar_usuarios()
    try:
        id_usuario = int(input("Digite o ID do usuário que deseja excluir: "))
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id_usuario,))
        usuario = cursor.fetchone()
        if usuario:
            confirmar = input(f"Tem certeza que deseja excluir o usuário '{usuario[1]}'? (s/n): ").lower()
            if confirmar == 's':
                cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_usuario,))
                conn.commit()
                print("✅ Usuário excluído com sucesso!")
            else:
                print("Exclusão cancelada.")
        else:
            print("Usuário não encontrado.")
    except ValueError:
        print("ID inválido.")

def menu():
    while True:
        print("\n--- Menu ---")
        print("1. Adicionar Usuário")
        print("2. Listar Usuários")
        print("3. Buscar Usuário")
        print("4. Editar Usuário")
        print("5. Excluir Usuário")
        print("6. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            adicionar_usuario()
        elif opcao == '2':
            listar_usuarios()
        elif opcao == '3':
            buscar_usuario()
        elif opcao == '4':
            editar_usuario()
        elif opcao == '5':
            excluir_usuario()
        elif opcao == '6':
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

menu()
conn.close()
