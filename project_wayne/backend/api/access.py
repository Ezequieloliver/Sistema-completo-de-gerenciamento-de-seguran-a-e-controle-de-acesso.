from flask import Blueprint, jsonify, request  
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

acesso_bp = Blueprint('acesso', __name__)


areas_restritas = {
    'caverna-morcego': ['administrador', 'admin_seguranca'],
    'laboratorio-pd': ['administrador', 'admin_seguranca', 'gerente'],
    'arsenal': ['administrador', 'admin_seguranca'],
    'sala-servidores': ['administrador', 'admin_seguranca', 'gerente'],
    'andar-executivo': ['administrador', 'gerente'],
    'escritorio-geral': ['administrador', 'admin_seguranca', 'gerente', 'funcionario']
}

registro_acessos = []


@acesso_bp.route('/areas', methods=['GET'])
@jwt_required()
def obter_areas_acessiveis():
    usuario_atual = get_jwt_identity()
    funcao_usuario = usuario_atual.get('funcao', 'desconhecida')

    areas_acessiveis = []
    for area, funcoes_permitidas in areas_restritas.items():
        areas_acessiveis.append({
            'id_area': area,
            'nome_area': area.replace('-', ' ').title(),
            'nivel_acesso': 'permitido' if funcao_usuario in funcoes_permitidas else 'negado'
        })

    return jsonify({
        'usuario': usuario_atual.get('nome_completo', 'Usuário desconhecido'),
        'funcao': funcao_usuario,
        'areas_acessiveis': areas_acessiveis
    }), 200



@acesso_bp.route('/verificar-acesso/<id_area>', methods=['GET'])
@jwt_required()
def verificar_acesso(id_area):
    usuario_atual = get_jwt_identity()
    funcao_usuario = usuario_atual.get('funcao', 'desconhecida')

    if id_area not in areas_restritas:
        return jsonify({'erro': 'Área não encontrada'}), 404

    if funcao_usuario in areas_restritas[id_area]:
        registro = {
            'usuario': usuario_atual.get('nome_completo', 'Desconhecido'),
            'area': id_area,
            'acesso': 'permitido',
            'data_hora': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        registro_acessos.append(registro)

        return jsonify({
            'mensagem': f"Acesso PERMITIDO à área '{id_area}'.",
            'usuario': registro['usuario'],
            'data_hora': registro['data_hora']
        }), 200

    # Caso contrário:
    registro = {
        'usuario': usuario_atual.get('nome_completo', 'Desconhecido'),
        'area': id_area,
        'acesso': 'negado',
        'motivo': 'Nível de autorização insuficiente',
        'data_hora': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    registro_acessos.append(registro)

    return jsonify({
        'mensagem': f"Acesso NEGADO à área '{id_area}'.",
        'motivo': registro['motivo']
    }), 403


@acesso_bp.route('/registros', methods=['GET'])
@jwt_required()
def obter_registros_acesso():
    usuario_atual = get_jwt_identity()
    funcao_usuario = usuario_atual.get('funcao', 'desconhecida')

    if funcao_usuario not in ['administrador', 'admin_seguranca']:
        return jsonify({'erro': 'Permissão negada. Apenas administradores podem visualizar os registros.'}), 403

    return jsonify({
        'total_registros': len(registro_acessos),
        'registros': registro_acessos[-50:]  # Últimos 50 registros
    }), 200


@acesso_bp.route('/admin/recursos', methods=['GET'])
@jwt_required()
def listar_recursos():
    usuario_atual = get_jwt_identity()
    funcao_usuario = usuario_atual.get('funcao', 'desconhecida')

    if funcao_usuario not in ['administrador', 'admin_seguranca']:
        return jsonify({'erro': 'Acesso negado. Apenas administradores.'}), 403

    recursos = []
    for area_id, funcoes in areas_restritas.items():
        recursos.append({
            'id': area_id,
            'nome': area_id.replace('-', ' ').title(),
            'funcoes_permitidas': funcoes,
            'nivel_acesso': ' | '.join(funcoes)
        })
    
    return jsonify({'recursos': recursos}), 200

@acesso_bp.route('/admin/recursos', methods=['POST'])
@jwt_required()
def adicionar_recurso():
    usuario_atual = get_jwt_identity()
    funcao_usuario = usuario_atual.get('funcao', 'desconhecida')

    if funcao_usuario not in ['administrador', 'admin_seguranca']:
        return jsonify({'erro': 'Acesso negado. Apenas administradores.'}), 403

    dados = request.get_json()
    
    if not dados or 'id' not in dados or 'funcoes_permitidas' not in dados:
        return jsonify({'erro': 'Dados incompletos. Forneça id e funcoes_permitidas.'}), 400

    novo_id = dados['id'].lower().replace(' ', '-')
    funcoes_permitidas = dados['funcoes_permitidas']

    if novo_id in areas_restritas:
        return jsonify({'erro': 'Recurso já existe.'}), 400

    areas_restritas[novo_id] = funcoes_permitidas

    return jsonify({
        'mensagem': 'Recurso adicionado com sucesso!',
        'recurso': {
            'id': novo_id,
            'nome': novo_id.replace('-', ' ').title(),
            'funcoes_permitidas': funcoes_permitidas
        }
    }), 201

@acesso_bp.route('/admin/recursos/<recurso_id>', methods=['PUT'])
@jwt_required()
def atualizar_recurso(recurso_id):
    usuario_atual = get_jwt_identity()
    funcao_usuario = usuario_atual.get('funcao', 'desconhecida')

    if funcao_usuario not in ['administrador', 'admin_seguranca']:
        return jsonify({'erro': 'Acesso negado. Apenas administradores.'}), 403

    if recurso_id not in areas_restritas:
        return jsonify({'erro': 'Recurso não encontrado.'}), 404

    dados = request.get_json()
    
    if not dados or 'funcoes_permitidas' not in dados:
        return jsonify({'erro': 'Forneça funcoes_permitidas.'}), 400

    areas_restritas[recurso_id] = dados['funcoes_permitidas']

    return jsonify({
        'mensagem': 'Recurso atualizado com sucesso!',
        'recurso': {
            'id': recurso_id,
            'nome': recurso_id.replace('-', ' ').title(),
            'funcoes_permitidas': dados['funcoes_permitidas']
        }
    }), 200

@acesso_bp.route('/admin/recursos/<recurso_id>', methods=['DELETE'])
@jwt_required()
def remover_recurso(recurso_id):
    usuario_atual = get_jwt_identity()
    funcao_usuario = usuario_atual.get('funcao', 'desconhecida')

    if funcao_usuario not in ['administrador', 'admin_seguranca']:
        return jsonify({'erro': 'Acesso negado. Apenas administradores.'}), 403

    if recurso_id not in areas_restritas:
        return jsonify({'erro': 'Recurso não encontrado.'}), 404

    recurso_removido = areas_restritas.pop(recurso_id)

    return jsonify({
        'mensagem': 'Recurso removido com sucesso!',
        'recurso_removido': {
            'id': recurso_id,
            'nome': recurso_id.replace('-', ' ').title(),
            'funcoes_permitidas': recurso_removido
        }
    }), 200
