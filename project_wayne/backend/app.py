from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager


app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'chave-teste-wayne-2024'
app.config['JWT_SECRET_KEY'] = 'jwt-chave-teste-wayne'  # usada para gerar tokens JWT

CORS(app)
jwt = JWTManager(app)

from api.auth import auth_bp
from api.access import acesso_bp
from api.dashboard import dashboard_bp  

app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(acesso_bp, url_prefix='/api')
app.register_blueprint(dashboard_bp, url_prefix='/api') 

@app.route('/')
def inicio():
    return jsonify({
        'mensagem': '✅ Sistema Wayne Industries - BACKEND FUNCIONANDO!',
        'status': 'operacional'
    }), 200

@app.route('/api/teste')
def teste():
    return jsonify({
        'mensagem': '🧩 API testada com sucesso!',
        'versao': '1.0',
        'autor': 'Wayne Enterprises Dev Team'
    }), 200

if __name__ == '__main__':
    print("🚀 Iniciando servidor Wayne Industries...")
    print("📍 Acesse: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
