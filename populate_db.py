from app import create_app, db
from app.models import Usuario, Quarto
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    user = Usuario(
        nome="Cliente Teste",
        email="cliente@teste.com",
        senha=generate_password_hash("senhateste"),
        telefone="123456789",
        cpf="12345678901",
        endereco="Rua de Teste, 123"
    )
    db.session.add(user)

    for i in range(1, 51):
        quarto = Quarto(
            tipo='INDIVIDUAL' if i % 3 == 0 else 'DUPLO' if i % 3 == 1 else 'SUITE',
            status='DESOCUPADO'
        )
        db.session.add(quarto)

    db.session.commit()

    print("Banco de dados populado com sucesso!")
