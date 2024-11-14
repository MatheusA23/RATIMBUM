from app import db
from flask_login import UserMixin
from app import login_manager

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))  # Carrega o usuário pelo ID

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'

    id_usuario = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(60), nullable=False)
    telefone = db.Column(db.String(15))
    cpf = db.Column(db.String(11), unique=True)
    endereco = db.Column(db.String(200))

    reservas = db.relationship('Reserva', backref='usuario', lazy=True)

    def get_id(self):
        return str(self.id_usuario)

class Quarto(db.Model):
    __tablename__ = 'quarto'
    id_quarto = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.Enum('INDIVIDUAL', 'DUPLO', 'SUITE', name="tipo_quarto"), nullable=False)
    status = db.Column(db.Enum('DESOCUPADO', 'RESERVADO', name="status_quarto"), nullable=False)

class Reserva(db.Model):
    __tablename__ = 'reserva'
    id_reserva = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    id_quarto = db.Column(db.Integer, db.ForeignKey('quarto.id_quarto'), nullable=False)
    data_entrada = db.Column(db.DateTime, nullable=False)
    data_saida = db.Column(db.DateTime, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    status_pagamento = db.Column(db.Boolean, default=False)
