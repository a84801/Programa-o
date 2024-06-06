import sqlite3

# Definição do SQL para criar as tabelas para a base de dados
sql = """
CREATE TABLE Clientes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    morada TEXT NOT NULL,
    telefone TEXT NOT NULL UNIQUE
);

CREATE TABLE Users (
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

CREATE TABLE Hamburgueres (
    nome_hamburguer TEXT PRIMARY KEY,
    preco REAL NOT NULL
);

CREATE TABLE Ingredientes (
    id_ingrediente INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_ingrediente TEXT NOT NULL
);

CREATE TABLE Hamburguer_Ingredientes (
    nome_hamburguer TEXT,
    id_ingrediente INTEGER,
    FOREIGN KEY (nome_hamburguer) REFERENCES Hamburgueres(nome_hamburguer) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (id_ingrediente) REFERENCES Ingredientes(id_ingrediente) ON UPDATE CASCADE ON DELETE CASCADE,
    UNIQUE (nome_hamburguer, id_ingrediente)
);

CREATE TABLE Pedidos (
    id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    nome_hamburguer TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    tamanho TEXT NOT NULL CHECK (tamanho IN ('Pequeno', 'Médio', 'Grande')),
    data_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    valor_total REAL NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (nome_hamburguer) REFERENCES Hamburgueres(nome_hamburguer) ON UPDATE CASCADE ON DELETE CASCADE
);
"""

# Criação das tabelas para a base de dados 
with sqlite3.connect("hamburgueria.db") as conn:
    cursor = conn.cursor()
    cursor.executescript(sql)
