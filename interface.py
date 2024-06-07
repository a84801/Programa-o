from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner
import sqlite3

base_de_dados = "hamburgueria.db"

# Função que faz a conexão à base de dados
def db_connection():
    return sqlite3.connect(base_de_dados)

class EmailScreen(Screen):
    def __init__(self, **kwargs):
        super(EmailScreen, self).__init__(**kwargs)

        # Imagem principal que ocupa a página inteira
        self.image = Image(source='hamburgueria.jpg', allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
        self.add_widget(self.image)

        # Layout do formulário de login com 2 colunas e um tamanho específico
        self.login_layout = GridLayout(cols=2, size_hint=(None, None), width=1000, height=200)
        self.add_widget(self.login_layout)

        # Adiciona o campo de Email no formulário
        self.login_layout.add_widget(Label(text='Email'))
        self.login_input = TextInput(multiline=False)
        self.login_layout.add_widget(self.login_input)

        # Adiciona o campo de Password no formulário
        self.login_layout.add_widget(Label(text='Password'))
        self.password_input = TextInput(password=True, multiline=False)
        self.login_layout.add_widget(self.password_input)

        # Adiciona o botão de login na parte inferior do layout
        self.login_layout.add_widget(Label())
        self.login_button = Button(text='Entrar')
        self.login_button.bind(on_press=self.verify_credentials)
        self.login_layout.add_widget(self.login_button)

    # Função para verificar as credenciais de login
    def verify_credentials(self, instance):
        login = self.login_input.text
        password = self.password_input.text

        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Users WHERE email=? AND password=?', (login, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            print("Sucesso a entrar no menu principal.")
            self.manager.current = 'Main'
        else:
            print("Um dos dois campos está incorreto! Tenta de novo!")

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        
        # Imagem principal que ocupa a página inteira
        self.image = Image(source='hamburgueria.jpg', allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
        self.add_widget(self.image)
        
        # Layout de grade para os botões com 2 colunas, tamanho especificado
        button_layout = GridLayout(cols=2, size_hint=(None, None), width=1000, height=200)
        
        # Botões
        self.add_client_button = Button(text='Adicionar novo Cliente', size_hint=(1, None), height=100, background_color=(144/255, 238/255, 144/255, 1))
        self.add_encomenda_button = Button(text='Adicionar nova Encomenda', size_hint=(1, None), height=100, background_color=(144/255, 238/255, 144/255, 1))
        
        # Adiciona-se a função dos botões (ao carregar)
        self.add_client_button.bind(on_press=self.go_to_client_screen)
        self.add_encomenda_button.bind(on_press=self.go_to_encomenda_screen)
        
        # Adiciona-se os botões à página
        button_layout.add_widget(self.add_client_button)
        button_layout.add_widget(self.add_encomenda_button)
        
        # Adicionando o layout dos botões à direita ao layout principal
        self.add_widget(button_layout)
        
    def go_to_client_screen(self, instance):
        self.manager.current = 'Clientes'
        
    def go_to_encomenda_screen(self, instance):
        self.manager.current = 'Pedidos'
    
class Cliente(Screen):
    def __init__(self, **kwargs):
        super(Cliente, self).__init__(**kwargs)
        self.conn = db_connection()
        self.cursor = self.conn.cursor()
        
        # Adiciona uma imagem de fundo que ocupa toda a tela
        self.image = Image(source='hamburgueria.jpg', allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
        self.add_widget(self.image)
        
        # Cria um layout em grade para o formulário de cliente
        self.login_layout = GridLayout(cols=2, size_hint=(None, None), width=1000, height=200)
        self.add_widget(self.login_layout)
        
        # Adiciona campos para inserir o nome completo do cliente
        self.login_layout.add_widget(Label(text='Nome completo'))
        self.client_name = TextInput(multiline=False)
        self.login_layout.add_widget(self.client_name)

        # Adiciona campos para inserir a morada do cliente
        self.login_layout.add_widget(Label(text='Morada'))
        self.client_address = TextInput(multiline=False)
        self.login_layout.add_widget(self.client_address)

        # Adiciona campos para inserir o número de telemóvel do cliente
        self.login_layout.add_widget(Label(text='Número de telemóvel'))
        self.client_phone = TextInput(multiline=False)
        self.login_layout.add_widget(self.client_phone)

        # Botão para adicionar um cliente à base de dados
        self.add_client_button = Button(text='Adicionar Cliente')
        self.add_client_button.bind(on_press=self.add_client)
        self.login_layout.add_widget(self.add_client_button)
        
        # Botão para apagar um cliente da base de dados
        self.delete_client_button = Button(text='Apagar Cliente')
        self.delete_client_button.bind(on_press=self.delete_client)
        self.login_layout.add_widget(self.delete_client_button)

        # Botão para voltar ao menu principal
        self.back_button = Button(text='Voltar para o Menu Principal', size_hint=(1, 1), width=200, height=50)
        self.back_button.bind(on_press=self.go_to_main_screen)
        self.login_layout.add_widget(self.back_button)

    # Método para voltar à página principal
    def go_to_main_screen(self, instance):
        self.manager.current = 'Main'

    # Método para adicionar um cliente à base de dados
    def add_client(self, instance):
        client_name = self.client_name.text
        client_address = self.client_address.text
        client_phone = self.client_phone.text

        if client_name and client_address and client_phone:
            self.cursor.execute('''
                INSERT INTO Clientes (nome, morada, telefone)
                VALUES (?, ?, ?)
            ''', (client_name, client_address, client_phone))
            self.conn.commit()
            print(f"Cliente adicionado: {client_name}, {client_address}, {client_phone}")
        else:
            print("Por favor, preencha todos os campos.")

    # Método para apagar um cliente da base de dados
    def delete_client(self, instance):
        client_name = self.client_name.text
        if client_name:
            self.cursor.execute('''
                DELETE FROM Clientes
                WHERE nome = ?
            ''', (client_name,))
            self.conn.commit()
            print(f"Cliente apagado: {client_name}")
        else:
            print("Por favor, forneça o nome do cliente a ser apagado.")
        
class Pedido(Screen):
    def __init__(self, **kwargs):
        super(Pedido, self).__init__(**kwargs)
        self.conn = db_connection()
        self.cursor = self.conn.cursor()
        
        # Adiciona uma imagem de fundo que ocupa a página toda
        self.image = Image(source='hamburgueria.jpg', allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
        self.add_widget(self.image)
        
        # Cria um layout em grade para o formulário dos pedidos
        self.login_layout = GridLayout(cols=2, size_hint=(None, None), width=1000, height=200)
        self.add_widget(self.login_layout)
        
        # Cria um dropdown para selecionar o cliente
        self.client_dropdown = DropDown()
        
        # Cada hambúrguer corresponde à sua imagem
        self.hamburguer_images = {
            'Hamburguer Normal': 'hamburguer1.jpg',
            'Hamburguer com Ovo Estrelado': 'hamburguer2.jpg',
        }
        
        # Executa uma consulta SQL para obter os nomes dos clientes
        self.cursor.execute('SELECT nome FROM Clientes')
        clientes = self.cursor.fetchall()
        
        # Adiciona cada cliente ao dropdown
        for cliente in clientes:
            btn = Button(text=cliente[0], size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.client_dropdown.select(btn.text))
            self.client_dropdown.add_widget(btn)
        
        # Botão para abrir o dropdown de seleção de cliente
        self.client_select_button = Button(text='Selecionar Cliente')
        self.client_select_button.bind(on_release=self.client_dropdown.open)
        self.client_dropdown.bind(on_select=lambda instance, x: self.show_selected_client(x))
        
        # Adiciona o dropdown de clientes ao layout
        self.login_layout.add_widget(Label(text='Clientes'))
        self.login_layout.add_widget(self.client_select_button)
        
        # Cria um dropdown para selecionar o hambúrguer
        self.hamburguer_dropdown = DropDown()
        
        # Executa uma consulta SQL para obter os nomes dos hambúrgueres e seus preços
        self.cursor.execute('SELECT nome_hamburguer, preco FROM Hamburgueres')
        hamburguers = self.cursor.fetchall()
        
        # Dicionário para escolher o nome do hambúrguer e o seu devido preço
        self.hamburguer_prices = {}
        for hamburguer in hamburguers:
            btn = Button(text=hamburguer[0], size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.hamburguer_dropdown.select(btn.text))
            self.hamburguer_dropdown.add_widget(btn)
            self.hamburguer_prices[hamburguer[0]] = hamburguer[1]
        
        # Botão para abrir o dropdown de seleção de hambúrguer
        self.hamburguer_select_button = Button(text='Selecionar Hambúrguer')
        self.hamburguer_select_button.bind(on_release=self.hamburguer_dropdown.open)
        self.hamburguer_dropdown.bind(on_select=lambda instance, x: self.show_selected_hamburguer(x))
        
        # Adiciona o dropdown de hambúrgueres ao layout
        self.login_layout.add_widget(Label(text='Hambúrgueres'))
        self.login_layout.add_widget(self.hamburguer_select_button)
        
        # Campo de entrada de texto para a quantidade de hambúrgueres
        self.quantity_input = TextInput(multiline=False, input_type='number', input_filter='int')
        self.quantity_input.bind(text=self.calculate_total)
        self.login_layout.add_widget(Label(text='Quantidade de Hambúrgueres'))
        self.login_layout.add_widget(self.quantity_input)
        
        # Spinner para escolher o tamanho do hambúrguer
        self.size_spinner = Spinner(
            text='Escolha o Tamanho',
            values=('Pequeno', 'Médio', 'Grande'),
        )
        
        self.login_layout.add_widget(Label(text='Tamanho do Hambúrguer'))
        self.login_layout.add_widget(self.size_spinner)
        
        # Label para exibir o valor total do pedido
        self.total_label = Label(text='')
        self.login_layout.add_widget(Label(text='Valor Total'))
        self.login_layout.add_widget(self.total_label)
        
        # Labels para exibir o cliente e o hambúrguer selecionados
        self.selected_client_label = Label(text='')
        self.login_layout.add_widget(self.selected_client_label)
        self.selected_hamburguer_label = Label(text='')
        self.login_layout.add_widget(self.selected_hamburguer_label)
        
        # Botão para voltar ao menu principal
        self.back_button = Button(text='Voltar para o Menu Principal')
        self.back_button.bind(on_press=self.go_to_main_screen)
        self.login_layout.add_widget(self.back_button)
        
        # Botão para enviar o pedido
        self.send_button = Button(text='Enviar Pedido')
        self.send_button.bind(on_press=self.send_order_to_database)
        self.login_layout.add_widget(self.send_button)
        
        # Adiciona o widget da imagem do hambúrguer selecionado
        self.selected_hamburguer_image = Image(size_hint=(None, None), width=200, height=200)
        self.selected_hamburguer_image.pos_hint = {'center_x': 0.5, 'y': 0.3}  # Posiciona o widget no centro horizontal e a 30% da altura da tela
        self.add_widget(self.selected_hamburguer_image)

    # Método para enviar o pedido para a base de dados
    def send_order_to_database(self, instance):
        self.calculate_total()
    
    # Método para voltar à página principal
    def go_to_main_screen(self, instance):
        self.manager.current = 'Main'
    
    # Método para exibir o cliente selecionado
    def show_selected_client(self, client_name):
        self.client_select_button.text = client_name
    
    # Método para exibir o hambúrguer selecionado e atualizar a imagem
    def show_selected_hamburguer(self, hamburguer_name):
        self.hamburguer_select_button.text = hamburguer_name
        self.calculate_total()
        self.update_hamburguer_image(hamburguer_name)
    
    # Método para calcular o valor total do pedido
    def calculate_total(self, *args):
        hamburguer_name = self.hamburguer_select_button.text
        quantity = int(self.quantity_input.text) if self.quantity_input.text else 0
        price_per_burger = self.hamburguer_prices.get(hamburguer_name, 0)
        total = quantity * price_per_burger
        self.total_label.text = f'{total:.2f}€'
        
        # Vai recuperar o id do cliente
        client_name = self.client_select_button.text
        self.cursor.execute("SELECT id_cliente FROM Clientes WHERE nome = ?", (client_name,))
        client_data = self.cursor.fetchone()
        if client_data is None:
            print("Cliente não encontrado.")
            return
        client_id = client_data[0]

        # Vai inserir o pedido na base de dados
        size = self.size_spinner.text
        if size not in ('Pequeno', 'Médio', 'Grande'):
            print("Tamanho inválido!")
            return
        self.cursor.execute("INSERT INTO Pedidos (id_cliente, nome_hamburguer, quantidade, tamanho, valor_total) VALUES (?, ?, ?, ?, ?)", 
                            (client_id, hamburguer_name, quantity, size, total))
        self.conn.commit()
    
    # Método para atualizar a imagem do hambúrguer selecionado
    def update_hamburguer_image(self, hamburguer_name):
        image_path = self.hamburguer_images.get(hamburguer_name, 'hamburguer1.jpg')
        image_path = self.hamburguer_images.get(hamburguer_name, 'hamburguer2.jpg')
        self.selected_hamburguer_image.source = image_path
        self.selected_hamburguer_image.reload()

# Classe que gerencia as páginas
class First(ScreenManager):
    pass

# Classe principal da aplicação
class Aplicação(App):
    def build(self):
        first = First()
        first.add_widget(EmailScreen(name='Email'))
        first.add_widget(MainScreen(name='Main'))
        first.add_widget(Cliente(name='Clientes'))
        first.add_widget(Pedido(name='Pedidos'))
        return first

if __name__ == '__main__':
    Aplicação().run()
    