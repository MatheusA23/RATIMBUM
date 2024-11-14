from flask import Blueprint, request, redirect, url_for, flash, jsonify, render_template
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from app.models import Usuario, Quarto, Reserva
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/booking')
def booking():
    return render_template('booking.html')

@main.route('/mybooking')
def mybooking():
    return render_template('mybooking.html')

@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')

    user = Usuario.query.filter_by(email=email).first()
    if user and check_password_hash(user.senha, senha):
        login_user(user)
        return jsonify({"message": "Login realizado com sucesso!"}), 200
    else:
        return jsonify({"message": "Email ou senha inválidos!"}), 401

@main.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso!"}), 200

@main.route('/quartos-disponiveis', methods=['GET'])
def listar_quartos_disponiveis():
    quartos = Quarto.query.filter_by(status='DESOCUPADO').all()
    quartos_disponiveis = [{"id": q.id_quarto, "tipo": q.tipo, "status": q.status} for q in quartos]
    return jsonify(quartos_disponiveis), 200

@main.route('/reservar-quarto', methods=['POST'])
@login_required
def reservar_quarto():
    data = request.get_json()
    id_quarto = data.get('id_quarto')
    data_entrada = datetime.strptime(data.get('data_entrada'), '%Y-%m-%d')
    data_saida = datetime.strptime(data.get('data_saida'), '%Y-%m-%d')
    preco = data.get('preco', 0.0)

    quarto = Quarto.query.get(id_quarto)
    if quarto and quarto.status == 'DESOCUPADO':
        reserva = Reserva(
            id_usuario=current_user.id_usuario,
            id_quarto=id_quarto,
            data_entrada=data_entrada,
            data_saida=data_saida,
            preco=preco,
            status_pagamento=False
        )
        quarto.status = 'RESERVADO'
        db.session.add(reserva)
        db.session.commit()
        return jsonify({"message": "Quarto reservado com sucesso!"}), 201
    else:
        return jsonify({"message": "Quarto não disponível para reserva."}), 400


@main.route('/minhas-reservas', methods=['GET'])
@login_required
def minhas_reservas():
    reservas = Reserva.query.filter_by(id_usuario=current_user.id_usuario).all()
    reservas_info = []

    for reserva in reservas:
        quarto = Quarto.query.get(reserva.id_quarto)

        reservas_info.append({
            "id_reserva": reserva.id_reserva,
            "id_quarto": reserva.id_quarto,
            "tipo_quarto": quarto.tipo,
            "status_quarto": quarto.status,
            "data_entrada": reserva.data_entrada.strftime('%Y-%m-%d'),
            "data_saida": reserva.data_saida.strftime('%Y-%m-%d'),
            "preco": reserva.preco,
            "status_pagamento": reserva.status_pagamento
        })

    if reservas_info:
        return jsonify({"reservas": reservas_info}), 200
    else:
        return jsonify({"message": "Você não tem reservas no momento."}), 404

@main.route('/pagar-reserva/<int:id_reserva>', methods=['PUT'])
@login_required
def pagar_reserva(id_reserva):
    reserva = Reserva.query.get(id_reserva)
    if reserva and reserva.id_usuario == current_user.id_usuario:
        reserva.status_pagamento = True
        db.session.commit()
        return jsonify({"message": "Pagamento realizado com sucesso!"}), 200
    else:
        return jsonify({"message": "Reserva não encontrada ou acesso negado."}), 404

@main.route('/editar-reserva/<int:id_reserva>', methods=['PUT'])
@login_required
def editar_reserva(id_reserva):
    data = request.get_json()
    nova_data_entrada = datetime.strptime(data.get('data_entrada'), '%Y-%m-%d')
    nova_data_saida = datetime.strptime(data.get('data_saida'), '%Y-%m-%d')

    reserva = Reserva.query.get(id_reserva)
    if reserva and reserva.id_usuario == current_user.id_usuario:
        reserva.data_entrada = nova_data_entrada
        reserva.data_saida = nova_data_saida
        db.session.commit()
        return jsonify({"message": "Reserva atualizada com sucesso!"}), 200
    else:
        return jsonify({"message": "Reserva não encontrada ou acesso negado."}), 404

@main.route('/excluir-reserva/<int:id_reserva>', methods=['DELETE'])
@login_required
def excluir_reserva(id_reserva):
    reserva = Reserva.query.get(id_reserva)
    if reserva and reserva.id_usuario == current_user.id_usuario:
        quarto = Quarto.query.get(reserva.id_quarto)
        quarto.status = 'DESOCUPADO'
        db.session.delete(reserva)
        db.session.commit()
        return jsonify({"message": "Reserva excluída com sucesso!"}), 200
    else:
        return jsonify({"message": "Reserva não encontrada ou acesso negado."}), 404
