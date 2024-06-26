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

# Serve para obter todos os dados na tabela de dados "Ingredientes"
@app.route('/ingredientes', methods=['GET'])
def get_ingrediente():
    conn = db_connection()
    ingrediente = conn.execute('SELECT * FROM Ingredientes').fetchall()
    conn.close()
    return jsonify([{'id_ingrediente': row[0], 'nome_ingrediente': row[1]} for row in ingrediente])

# Serve para adicionar dados na tabela de dados "Ingredientes"
@app.route('/ingredientes', methods=['POST'])
def add_ingrediente():
    new_ingrediente = request.json
    conn = db_connection()
    conn.execute('INSERT INTO Ingredientes (nome_ingrediente) VALUES (?)',
                 (new_ingrediente['nome_ingrediente'],))
    conn.commit()
    conn.close()
    return 'Novo(s) ingrediente(s) adicionado(s) com sucesso.', 201

# Serve para atualizar dados na tabela de dados "Ingredientes"
@app.route('/ingredientes/<int:id>', methods=['PUT'])
def update_ingrediente(id):
    updated_ingrediente = request.json
    conn = db_connection()
    conn.execute('UPDATE Ingredientes SET nome_ingrediente=? WHERE id_ingrediente=?',
                 (updated_ingrediente['nome_ingrediente'], id))
    conn.commit()
    conn.close()
    return 'Ingrediente(s) atualizado(s) com sucesso.'

# Serve para excluir dados na tabela de dados "Ingredientes"
@app.route('/ingredientes/<int:id>', methods=['DELETE'])
def delete_ingrediente(id):
    conn = db_connection()
    conn.execute('DELETE FROM Ingredientes WHERE id_ingrediente=?', (id,))
    conn.commit()
    conn.close()
    return 'Ingrediente(s) excluído(s) com sucesso.'

# Serve para obter todos os dados da tabela de dados "Hamburgueres"
@app.route('/hamburgueres', methods=['GET'])
def get_hamburguer():
    conn = db_connection()
    hamburguer = conn.execute('SELECT * FROM Hamburgueres').fetchall()
    conn.close()
    return jsonify([{'nome_hamburguer': row[0], 'preco': row[1]} for row in hamburguer])

# Serve para adicionar dados na tabela de dados "Hamburgueres"
@app.route('/hamburgueres', methods=['POST'])
def add_hamburguer():
    new_hamburguer = request.json
    conn = db_connection()
    conn.execute('INSERT INTO Hamburgueres (nome_hamburguer, preco) VALUES (?, ?)',
                 (new_hamburguer['nome_hamburguer'], new_hamburguer['preco']))
    conn.commit()
    conn.close()
    return 'Novo Hamburguer adicionado com sucesso.', 201

# Serve para atualizar dados na tabela de dados "Hamburgueres"
@app.route('/hamburgueres/<int:id>', methods=['PUT'])
def update_hamburguer(id):
    updated_hamburguer = request.json
    conn = db_connection()
    conn.execute('UPDATE Hamburgueres SET nome_hamburguer=?, preco=? WHERE id=?',
                 (updated_hamburguer['nome_hamburguer'], updated_hamburguer['preco'], id))
    conn.commit()
    conn.close()
    return 'Hamburguer atualizado com sucesso.'

# Serve para excluir dados na tabela de dados "Hamburgueres"
@app.route('/hamburgueres/<int:id>', methods=['DELETE'])
def delete_hamburguer(id):
    conn = db_connection()
    conn.execute('DELETE FROM Hamburgueres WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return 'Hamburguer excluído com sucesso.'

# Serve para obter todos os dados da tabela de dados "Hamburguer_Ingredientes"
@app.route('/hamburguer/ingredientes', methods=['GET'])
def get_hamburguer_ingrediente():
    conn = db_connection()
    hamburguer_ingrediente = conn.execute('SELECT * FROM Hamburguer_Ingredientes').fetchall()
    conn.close()
    return jsonify([{'nome_hamburguer': row[0], 'id_ingrediente': row[1]} for row in hamburguer_ingrediente])

# Serve para adicionar dados na tabela de dados "Hamburguer_Ingredientes"
@app.route('/hamburguer/ingredientes', methods=['POST'])
def add_hamburguer_ingrediente():
    new_hamburguer_ingrediente = request.json
    conn = db_connection()
    conn.execute('INSERT INTO Hamburguer_Ingredientes (nome_hamburguer, id_ingrediente) VALUES (?, ?)',
                 (new_hamburguer_ingrediente['nome_hamburguer'], new_hamburguer_ingrediente['id_ingrediente']))
    conn.commit()
    conn.close()
    return 'Novo hamburguer e os respetivos ingredientes adicionados com sucesso.', 201

# Serve para atualizar dados na tabela de dados "Hamburguer_Ingredientes"
@app.route('/hamburguer/ingredientes/<int:id>', methods=['PUT'])
def update_hamburguer_ingrediente(id):
    updated_hamburguer_ingrediente = request.json
    conn = db_connection()
    conn.execute('UPDATE Hamburguer_Ingredientes SET nome_hamburguer=?, id_ingrediente=? WHERE id=?',
                 (updated_hamburguer_ingrediente['nome_hamburguer'], updated_hamburguer_ingrediente['id_ingrediente'], id))
    conn.commit()
    conn.close()
    return 'Hamburguer e os respetivos ingredientes atualizados com sucesso.'

# Serve para excluir dados na tabela de dados "Hamburguer_Ingredientes"
@app.route('/hamburguer/ingredientes/<int:id>', methods=['DELETE'])
def delete_hamburguer_ingrediente(id):
    conn = db_connection()
    conn.execute('DELETE FROM Hamburguer_Ingredientes WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return 'Hamburguer e os respetivos ingredientes excluídos com sucesso.'

# Serve para obter todos os dados da tabela de dados "Pedidos"
@app.route('/pedidos', methods=['GET'])
def get_pedido():
    conn = db_connection()
    pedido = conn.execute('SELECT * FROM Pedidos').fetchall()
    conn.close()
    return jsonify([{'id_pedido': row[0], 'id_cliente': row[1], 'nome_hamburguer': row[2],
                     'quantidade': row[3], 'tamanho': row[4], 'data_hora': row[5], 'valor_total': row[6]} for row in pedido])

# Serve para adicionar dados na tabela de dados "Pedidos"
@app.route('/pedidos', methods=['POST'])
def add_pedido():
    new_pedido = request.json
    conn = db_connection()
    conn.execute('INSERT INTO Pedidos (id_cliente, nome_hamburguer, quantidade, tamanho, data_hora, valor_total) VALUES (?, ?, ?, ?, ?, ?)',
                 (new_pedido['id_cliente'], new_pedido['nome_hamburguer'], new_pedido['quantidade'],
                  new_pedido['tamanho'], new_pedido['data_hora'], new_pedido['valor_total']))
    conn.commit()
    conn.close()
    return 'Novo Pedido adicionado com sucesso.', 201

# Serve para atualizar dados na tabela de dados "Pedidos"
@app.route('/pedidos/<int:id>', methods=['PUT'])
def update_pedido(id):
    updated_pedido = request.json
    conn = db_connection()
    conn.execute('UPDATE Pedidos SET id_cliente=?, nome_hamburguer=?, quantidade=?, tamanho=?, data_hora=?, valor_total=? WHERE id_pedido=?',
                 (updated_pedido['id_cliente'], updated_pedido['nome_hamburguer'],
                  updated_pedido['quantidade'], updated_pedido['tamanho'], updated_pedido['data_hora'],
                  updated_pedido['valor_total'], id))
    conn.commit()
    conn.close()
    return 'Pedido atualizado com sucesso.'

# Serve para excluir dados na tabela de dados "Pedidos"
@app.route('/pedidos/<int:id>', methods=['DELETE'])
def delete_pedido(id):
    conn = db_connection()
    conn.execute('DELETE FROM Pedidos WHERE id_pedido=?', (id,))
    conn.commit()
    conn.close()
    return 'Pedido excluído com sucesso.'

if __name__ == '__main__':
    app.run(debug=True)
