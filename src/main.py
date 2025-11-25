import sqlite3
from flask import Flask, render_template, request, jsonify, g

app = Flask(__name__)
DATABASE = 'database.db'

# --- Configuração do Banco de Dados ---

def get_db():
    """Conecta-se ao banco de dados, criando um se não existir."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Fecha a conexão com o banco de dados ao final da requisição."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """Cria as tabelas e popula com dados iniciais."""
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        # Cria tabela de usuários (apenas para simulação)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
        ''')
        
        # Cria tabela de produtos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
        ''')
        
        # Limpa usuários antigos e insere dados de exemplo
        cursor.execute("DELETE FROM users")
        sample_users = [
            (1, 'aluno@teste.com', 'senha123')
        ]
        cursor.executemany("INSERT INTO users (id, email, password) VALUES (?, ?, ?)", sample_users)
        
        # Limpa produtos antigos e insere dados de exemplo
        cursor.execute("DELETE FROM products")
        sample_products = [
            ('Notebook Gamer', 5800.50),
            ('Mouse Óptico', 120.00),
            ('Teclado Mecânico', 350.75),
            ('Monitor 4K', 1800.00)
        ]
        cursor.executemany("INSERT INTO products (name, price) VALUES (?, ?)", sample_products)
        
        db.commit()
        print("Banco de dados 'database.db' inicializado com produtos e usuários.")

# --- Rotas da Aplicação ---

@app.route('/')
def index():
    """Serve a página de login (index.html)."""
    return render_template('index.html')

@app.route('/dashboard', methods=['POST'])
def dashboard():
    """
    Processa o formulário de login.
    """
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    # Validação simples (suficiente para o teste do Selenium)
    db = get_db()
    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM users WHERE email='{email}' AND password='{password}'")
    users = cursor.fetchall()
    print(users)
    
    if len(users) > 0:
        # Se o login for "bem-sucedido", busca os produtos
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        
        # Retorna a página do dashboard com os produtos
        return render_template('dashboard.html', products=products, name=name, userid=users[0][0])
    else:
        # Se falhar (campos vazios)
        return "Falha no login: campos obrigatórios não preenchidos.", 400

@app.route('/profile/<userid>')
def profile(userid):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM users WHERE id={userid}")
    user = cursor.fetchone()

    if user is not None:
        return render_template('profile.html', user=user)
    else:
        return "Nenhum usuário foi achado com esse ID"

# --- Rota da API (Alvo do JMeter) ---

@app.route('/api/products', methods=['GET'])
def api_products():
    """
    Endpoint de API que retorna a lista de produtos em formato JSON.
    Ideal para testes de carga com o JMeter.
    """
    db = get_db()
    # Usar Row Factory para facilitar a conversão para JSON
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute("SELECT id, name, price FROM products")
    products = cursor.fetchall()
    
    # Converte os resultados (Row) para uma lista de dicionários
    products_list = [dict(product) for product in products]
    
    return jsonify(products_list)

# --- Execução ---

if __name__ == '__main__':
    # Inicializa o banco de dados antes de rodar a app
    init_db()
    # Roda a aplicação Flask
    app.run(debug=True, port=5000)
