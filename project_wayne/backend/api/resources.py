from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

recursos_bp = Blueprint('recursos', __name__)

# Base de dados temporária para recursos
recursos_db = {
    'equipamentos': [
        {
            'id': 1,
            'nome': 'Terminal Batcomputer',
            'tipo': 'computador',
            'localizacao': 'caverna-morcego',
            'status': 'operacional',
            'ultima_manutencao': '2024-01-15',
            'responsavel': 'Bruce Wayne'
        },
        {
            'id': 2,
            'nome': 'Sistema de Câmeras de Segurança',
            'tipo': 'vigilancia',
            'localizacao': 'edificio-principal',
            'status': 'operacional',
            'ultima_manutencao': '2024-01-10',
            'responsavel': 'Lucius Fox'
        },
        {
            'id': 3,
            'nome': 'Scanner Biométrico - Entrada Principal',
            'tipo': 'controle_acesso',
            'localizacao': 'entrada-principal',
            'status': 'operacional',
            'ultima_manutencao': '2024-01-08',
            'responsavel': 'James Gordon'
        }
    ],
    'veiculos': [
        {
            'id': 1,
            'nome': 'Batmóvel',
            'tipo': 'tatico',
            'status': 'disponivel',
            'localizacao': 'garagem-caverna-morcego',
            'combustivel': '98%',
            'ultima_inspecao': '2024-01-12'
        },
        {
            'id': 2,
            'nome': 'Limousine Wayne Enterprises',
            'tipo': 'executivo',
            'status': 'em-uso',
            'localizacao': 'centro-cidade',
            'combustivel': '45%',
            'ultima_inspecao': '2024-01-14'
        }
    ],
    'dispositivos_seguranca': [
        {
            'id': 1,
            'nome': 'Sistema de Grade Laser',
            'tipo': 'detecao_intrusao',
            'status': 'manutencao',
            'localizacao': 'ala-secreta',
            'ultima_verificacao': '2024-01-05'
        },
        {
            'id': 2,
            'nome': 'Sensores de Movimento',
            'tipo': 'detecao_movimento',
            'status': 'operacional',
            'localizacao': 'corredor-a',
            'ultima_verificacao': '2024-01-03'
        }
    ]
}

@recursos_bp.route('/inventario', methods=['GET'])
@jwt_required()
def obter_inventario():
    usuario_atual = get_jwt_identity()
    
    return jsonify({
        'equipamentos': recursos_db['equipamentos'],
        'veiculos': recursos_db['veiculos'],
        'dispositivos_seguranca': recursos_db['dispositivos_seguranca'],
        'total_itens': len(recursos_db['equipamentos']) + len(recursos_db['veiculos']) + len(recursos_db['dispositivos_seguranca'])
    })

@recursos_bp.route('/equipamentos', methods=['POST'])
@jwt_required()
def adicionar_equipamento():
    usuario_atual = get_jwt_identity()
    
    # Verificar permissões
    if usuario_atual['funcao'] not in ['administrador', 'admin_seguranca']:
        return jsonify({'erro': 'Permissão negada'}), 403
    
    dados = request.get_json()
    
    novo_equipamento = {
        'id': len(recursos_db['equipamentos']) + 1,
        'nome': dados.get('nome'),
        'tipo': dados.get('tipo'),
        'localizacao': dados.get('localizacao'),
        'status': dados.get('status', 'operacional'),
        'ultima_manutencao': dados.get('ultima_manutencao'),
        'responsavel': usuario_atual['nome_completo']
    }
    
    recursos_db['equipamentos'].append(novo_equipamento)
    
    return jsonify({
        'mensagem': 'Equipamento adicionado com sucesso',
        'equipamento': novo_equipamento
    }), 201

@recursos_bp.route('/equipamentos/<int:equipamento_id>', methods=['PUT'])
@jwt_required()
def atualizar_equipamento(equipamento_id):
    usuario_atual = get_jwt_identity()
    
    if usuario_atual['funcao'] not in ['administrador', 'admin_seguranca', 'gerente']:
        return jsonify({'erro': 'Permissão negada'}), 403
    
    dados = request.get_json()
    
    for equipamento in recursos_db['equipamentos']:
        if equipamento['id'] == equipamento_id:
            equipamento.update({
                'nome': dados.get('nome', equipamento['nome']),
                'tipo': dados.get('tipo', equipamento['tipo']),
                'localizacao': dados.get('localizacao', equipamento['localizacao']),
                'status': dados.get('status', equipamento['status']),
                'ultima_manutencao': dados.get('ultima_manutencao', equipamento['ultima_manutencao'])
            })
            
            return jsonify({
                'mensagem': 'Equipamento atualizado com sucesso',
                'equipamento': equipamento
            })
    
    return jsonify({'erro': 'Equipamento não encontrado'}), 404

@recursos_bp.route('/status', methods=['GET'])
@jwt_required()
def obter_status_recursos():
    usuario_atual = get_jwt_identity()
    
    total_equipamentos = len(recursos_db['equipamentos'])
    equipamentos_operacionais = len([e for e in recursos_db['equipamentos'] if e['status'] == 'operacional'])
    
    total_veiculos = len(recursos_db['veiculos'])
    veiculos_disponiveis = len([v for v in recursos_db['veiculos'] if v['status'] == 'disponivel'])
    
    total_dispositivos = len(recursos_db['dispositivos_seguranca'])
    dispositivos_operacionais = len([d for d in recursos_db['dispositivos_seguranca'] if d['status'] == 'operacional'])
    
    return jsonify({
        'metricas_equipamentos': {
            'total': total_equipamentos,
            'operacionais': equipamentos_operacionais,
            'em_manutencao': total_equipamentos - equipamentos_operacionais
        },
        'metricas_veiculos': {
            'total': total_veiculos,
            'disponiveis': veiculos_disponiveis,
            'em_uso': total_veiculos - veiculos_disponiveis
        },
        'metricas_dispositivos': {
            'total': total_dispositivos,
            'operacionais': dispositivos_operacionais,
            'em_manutencao': total_dispositivos - dispositivos_operacionais
        }
    })

