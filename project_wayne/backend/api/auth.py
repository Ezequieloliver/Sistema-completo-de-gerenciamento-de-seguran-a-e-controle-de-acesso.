from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import datetime

auth_bp = Blueprint('auth', __name__)

# 🔹 Usuários do sistema Wayne Industries
usuarios = {
    "bruce": {
        "senha": "batman123",  
        "nome_completo": "Bruce Wayne",
        "funcao": "administrador"
    },
    "lucius": {
        "senha": "techmaster", 
        "nome_completo": "Lucius Fox",
        "funcao": "gerente"
    },
    "alfred": {
        "senha": "mayordomo",  
        "nome_completo": "Alfred Pennyworth", 
        "funcao": "admin_seguranca"
    },
    "selina": {  
        "senha": "gato123",
        "nome_completo": "Selina Kyle",
        "funcao": "funcionaria"
    }
}

# 🔹 Rota de login
@auth_bp.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    usuario = dados.get("username")
    senha = dados.get("password")

    if usuario in usuarios and usuarios[usuario]["senha"] == senha:
        usuario_info = usuarios[usuario]

        # Gerar token JWT
        token = create_access_token(
            identity={
                "username": usuario,
                "nome_completo": usuario_info["nome_completo"],
                "funcao": usuario_info["funcao"]
            },
            expires_delta=datetime.timedelta(hours=3)
        )

        return jsonify({
            "mensagem": f"Bem-vindo(a), {usuario_info['nome_completo']}!",
            "token": token,
            "funcao": usuario_info["funcao"]
        }), 200

    return jsonify({"erro": "Usuário ou senha incorretos!"}), 401
