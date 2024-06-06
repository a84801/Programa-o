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

        # Formulário e o tamanho que irá ocupar
        self.login_layout = GridLayout(cols=2, size_hint=(None, None), width=1000, height=200)
        self.add_widget(self.login_layout)

        # Adiciona o formulário do Email
        self.login_layout.add_widget(Label(text='Email'))
        self.login_input = TextInput(multiline=False)
        self.login_layout.add_widget(self.login_input)

        # Adiciona o formulário da Password
        self.login_layout.add_widget(Label(text='Password'))
        self.password_input = TextInput(password=True, multiline=False)
        self.login_layout.add_widget(self.password_input)

        # Adiciona o botão de login na parte inferior do layout
        self.login_layout.add_widget(Label())  # Adiciona um espaço vazio na grid para alinhar o botão
        self.login_button = Button(text='Entrar')
        self.login_button.bind(on_press=self.verify_credentials)
        self.login_layout.add_widget(self.login_button)

    def verify_credentials(self, instance):
        login = self.login_input.text
        password = self.password_input.text

        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Users WHERE email=? AND password=?', (login, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            print("Sucesso a entrar.")
            self.manager.current = 'Main'
        else:
            print("Tente de novo.")

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        
        # Imagem principal que ocupa a página inteira
        self.image = Image(source='hamburgueria.jpg', allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
        self.add_widget(self.image)
        
        #
        button_layout = GridLayout(cols=2, size_hint=(None, None), width=1000, height=200)
        
        # Botões
        self.add_client_button = Button(text='Adicionar novo Cliente', size_hint=(1, None), height=100, background_color=(1, 1, 1, 1))
        self.add_encomenda_button = Button(text='Adicionar nova Encomenda', size_hint=(1, None), height=50, background_color=(0, 0, 0, 0))
        
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
        
        # Imagem principal que ocupa a página inteira
        self.image = Image(source='hamburgueria.jpg', allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
        self.add_widget(self.image)
        
        # Formulário e o tamanho que irá ocupar
        self.login_layout = GridLayout(cols=2, size_hint=(None, None), width=1000, height=200)
        self.add_widget(self.login_layout)
        
        self.login_layout.add_widget(Label(text='Nome completo'))
        self.client_name = TextInput(multiline=False)
        self.login_layout.add_widget(self.client_name)

        self.login_layout.add_widget(Label(text='Morada'))
        self.client_address = TextInput(multiline=False)
        self.login_layout.add_widget(self.client_address)

        self.login_layout.add_widget(Label(text='Número de telemóvel'))
        self.client_phone = TextInput(multiline=False)
        self.login_layout.add_widget(self.client_phone)

        self.add_client_button = Button(text='Adicionar Cliente')
        self.add_client_button.bind(on_press=self.add_client)
        self.login_layout.add_widget(self.add_client_button)
        
        self.delete_client_button = Button(text='Apagar Cliente')
        self.delete_client_button.bind(on_press=self.delete_client)
        self.login_layout.add_widget(self.delete_client_button)

        self.back_button = Button(text='Voltar para o Menu Principal', size_hint=(1, 1), width=200, height=50)
        self.back_button.bind(on_press=self.go_to_main_screen)
        self.login_layout.add_widget(self.back_button)

    def go_to_main_screen(self, instance):
        self.manager.current = 'Main'

    def add_client(self, instance):
        # Function to add a client to the database
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
        
        # Imagem principal que ocupa a página inteira
        self.image = Image(source='hamburgueria.jpg', allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
        self.add_widget(self.image)
        
        # Formulário e o tamanho que irá ocupar
        self.login_layout = GridLayout(cols=2, size_hint=(None, None), width=1000, height=200)
        self.add_widget(self.login_layout)
        
        # DropDown para escolher o cliente
        self.client_dropdown = DropDown()
        
        # Mapeie os nomes dos hambúrgueres para os caminhos das imagens correspondentes
        self.hamburguer_images = {
            'Hambúrguer Normal': 'hamburgueria.jpg'
            # Adicione mais hambúrgueres e seus caminhos de imagem conforme necessário
        }
        
        # Obtendo os nomes dos clientes da base de dados
        self.cursor.execute('SELECT nome FROM Clientes')
        clientes = self.cursor.fetchall()
        
        for cliente in clientes:
            btn = Button(text=cliente[0], size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.client_dropdown.select(btn.text))
            self.client_dropdown.add_widget(btn)
        
        self.client_select_button = Button(text='Selecionar Cliente')
        self.client_select_button.bind(on_release=self.client_dropdown.open)
        self.client_dropdown.bind(on_select=lambda instance, x: self.show_selected_client(x))
        
        self.login_layout.add_widget(Label(text='Clientes'))
        self.login_layout.add_widget(self.client_select_button)
        
        self.hamburguer_dropdown = DropDown()
        
        # Obtendo os nomes dos hambúrgueres e seus preços da base de dados
        self.cursor.execute('SELECT nome_hamburguer, preco FROM Hamburgueres')
        hamburguers = self.cursor.fetchall()
        
        self.hamburguer_prices = {}  # Dicionário para mapear o nome do hambúrguer para o seu preço
        for hamburguer in hamburguers:
            btn = Button(text=hamburguer[0], size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.hamburguer_dropdown.select(btn.text))
            self.hamburguer_dropdown.add_widget(btn)
            self.hamburguer_prices[hamburguer[0]] = hamburguer[1]  # Adiciona o preço ao dicionário
        
        self.hamburguer_select_button = Button(text='Selecionar Hambúrguer')
        self.hamburguer_select_button.bind(on_release=self.hamburguer_dropdown.open)
        self.hamburguer_dropdown.bind(on_select=lambda instance, x: self.show_selected_hamburguer(x))
        
        self.login_layout.add_widget(Label(text='Hambúrgueres'))
        self.login_layout.add_widget(self.hamburguer_select_button)
        
        # Campo de entrada de texto para a quantidade de hambúrgueres
        self.quantity_input = TextInput(multiline=False, input_type='number', input_filter='int')
        self.quantity_input.bind(text=self.calculate_total)  # Atualiza o total quando a quantidade muda
        self.login_layout.add_widget(Label(text='Quantidade de Hambúrgueres'))
        self.login_layout.add_widget(self.quantity_input)
        
        # Spinner para escolher o tamanho do hambúrguer
        self.size_spinner = Spinner(
            text='Escolha o Tamanho',
            values=('Pequeno', 'Médio', 'Grande'),
        )
        self.login_layout.add_widget(Label(text='Tamanho do Hambúrguer'))
        self.login_layout.add_widget(self.size_spinner)
        
        # Label para exibir o valor total
        self.total_label = Label(text='')
        self.login_layout.add_widget(Label(text='Valor Total'))
        self.login_layout.add_widget(self.total_label)
        
        # Labels para exibir o cliente e o hambúrguer selecionados
        self.selected_client_label = Label(text='')
        self.login_layout.add_widget(self.selected_client_label)
        
        self.selected_hamburguer_label = Label(text='')
        self.login_layout.add_widget(self.selected_hamburguer_label)
        
        self.back_button = Button(text='Voltar para o Menu Principal')
        self.back_button.bind(on_press=self.go_to_main_screen)
        self.login_layout.add_widget(self.back_button)
        
        # Adiciona o widget de imagem do hambúrguer selecionado
        self.selected_hamburguer_image = Image(size_hint=(None, None), width=200, height=200)
        self.add_widget(self.selected_hamburguer_image)

    def go_to_main_screen(self, instance):
        self.manager.current = 'Main'
        
    def show_selected_client(self, client_name):
        self.client_select_button.text = client_name
    
    def show_selected_hamburguer(self, hamburguer_name):
        self.hamburguer_select_button.text = hamburguer_name
        self.calculate_total()  # Atualiza o total quando o hambúrguer muda
        self.update_hamburguer_image(hamburguer_name)  # Atualiza a imagem do hambúrguer
    
    def calculate_total(self, *args):
        # Calcula o valor total com base no preço do hambúrguer selecionado e na quantidade
        hamburguer_name = self.hamburguer_select_button.text
        quantity = int(self.quantity_input.text) if self.quantity_input.text else 0
        price_per_burger = self.hamburguer_prices.get(hamburguer_name, 0)
        total = quantity * price_per_burger
        self.total_label.text = f'R${total:.2f}'  # Exibe o total na label
    
    def update_hamburguer_image(self, hamburguer_name):
        # Atualiza a imagem do hambúrguer selecionado
        image_path = self.hamburguer_images.get(hamburguer_name, '')
        self.selected_hamburguer_image.source = image_path
        self.selected_hamburguer_image.reload()  # Recarrega a imagem para garantir que a nova imagem seja exibida

class First(ScreenManager):
    pass
    
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
    