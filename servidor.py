from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

base_de_dados = "hamburgueria.db"

# Função que faz a conexão à base de dados
def db_connection():
    return sqlite3.connect(base_de_dados)

# Serve para obter todos os dados na tabela "Clientes"
@app.route('/clientes', methods=['GET'])
def get_cliente():
    conn = db_connection()
    cliente = conn.execute('SELECT * FROM Clientes').fetchall()
    conn.close()
    return jsonify([{'id_cliente': row[0], 'nome': row[1], 'morada': row[2], 'telefone': row[3]} for row in cliente])

# Serve para adicionar dados na tabela "Clientes"
@app.route('/clientes', methods=['POST'])
def add_cliente():
    new_cliente = request.json
    conn = db_connection()
    conn.execute('INSERT INTO Clientes (nome, morada, telefone) VALUES (?, ?, ?)',
                 (new_cliente['nome'], new_cliente['morada'], new_cliente['telefone']))
    conn.commit()
    conn.close()
    return 'Novo cliente adicionado com sucesso.', 201

# Serve para atualizar dados na tabela de dados "Clientes"
@app.route('/clientes/<int:id>', methods=['PUT'])
def update_cliente(id):
    updated_cliente = request.json
    conn = db_connection()
    conn.execute('UPDATE Clientes SET nome=?, morada=?, telefone=? WHERE id_cliente=?',
                 (updated_cliente['nome'], updated_cliente['morada'], updated_cliente['telefone'], id))
    conn.commit()
    conn.close()
    return 'Cliente atualizado com sucesso.'

# Serve para excluir dados na tabela de dados "Clientes"
@app.route('/clientes/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    conn = db_connection()
    conn.execute('DELETE FROM Clientes WHERE id_cliente=?', (id,))
    conn.commit()
    conn.close()
    return 'Cliente excluído com sucesso.'

# Serve para obter todos os dados na tabela "Users"
@app.route('/users', methods=['GET'])
def get_user():
    conn = db_connection()
    user = conn.execute('SELECT * FROM Users').fetchall()
    conn.close()
    return jsonify([{'email': row[0], 'password': row[1]} for row in user])

# Serve para adicionar dados na tabela "Users"
@app.route('/users', methods=['POST'])
def add_user():
    new_user = request.json
    conn = db_connection()
    conn.execute('INSERT INTO Users (email, password) VALUES (?, ?)',
                 (new_user['email'], new_user['password']))
    conn.commit()
    conn.close()
    return 'Novo user adicionado com sucesso.', 201

# Serve para atualizar dados na tabela de dados "Users"
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    updated_user = request.json
    conn = db_connection()
    conn.execute('UPDATE Users SET email=?, password=? WHERE id=?',
                 (updated_user['email'], updated_user['password'], id))
    conn.commit()
    conn.close()
    return 'User atualizado com sucesso.'

# Serve para excluir dados na tabela de dados "Users"
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    conn = db_connection()
    conn.execute('DELETE FROM Users WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return 'User excluído com sucesso.'