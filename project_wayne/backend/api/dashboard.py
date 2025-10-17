from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
import random

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/metricas', methods=['GET'])
@jwt_required()
def obter_metricas_dashboard():
    usuario_atual = get_jwt_identity()  # ✅ CORRIGIDO
    
    # Métricas de segurança
    metricas_seguranca = {
        'tentativas_acesso_total': 1560,
        'acessos_bem_sucedidos': 1520,
        'tentativas_falhas': 40,
        'incidentes_seguranca': 3,
        'tempo_operacional_sistema': '99.9%',
        'alertas_ativos': 2
    }
    
    # Métricas de recursos
    metricas_recursos = {
        'total_equipamentos': 47,
        'equipamentos_operacionais': 44,
        'equipamentos_manutencao': 3,
        'veiculos_disponiveis': 6,
        'dispositivos_seguranca_online': 31,
        'taxa_utilizacao_recursos': '87%'
    }
    
    # Dados para gráficos
    tendencias_acesso = []
    datas = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7, 0, -1)]
    for data in datas:
        tendencias_acesso.append({
            'data': data,
            'acessos': random.randint(130, 180),
            'incidentes': random.randint(0, 2)
        })
    
    # Status de equipamentos
    status_equipamentos = [
        {'status': 'Operacional', 'quantidade': 44, 'cor': '#10B981'},
        {'status': 'Em Manutencao', 'quantidade': 3, 'cor': '#F59E0B'},
        {'status': 'Offline', 'quantidade': 0, 'cor': '#EF4444'}
    ]
    
    # Atividades recentes
    atividades_recentes = [
        {
            'usuario': 'Bruce Wayne',
            'acao': 'Acesso à Caverna do Morcego',
            'data_hora': '2024-01-15 20:15:00',
            'localizacao': 'caverna-morcego',
            'tipo': 'acesso'
        },
        {
            'usuario': 'Lucius Fox',
            'acao': 'Atualização de sistema de segurança',
            'data_hora': '2024-01-15 18:30:00',
            'localizacao': 'laboratorio-pd',
            'tipo': 'manutencao'
        }
    ]
    
    return jsonify({
        'metricas_seguranca': metricas_seguranca,
        'metricas_recursos': metricas_recursos,
        'tendencias_acesso': tendencias_acesso,
        'status_equipamentos': status_equipamentos,
        'atividades_recentes': atividades_recentes,
        'ultima_atualizacao': datetime.now().isoformat()
    })