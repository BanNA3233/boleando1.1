from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, date
from sqlalchemy import Date
import asaas
import json

app = Flask(__name__)
app.secret_key = 'Ban'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:eeFA3bCGg3Bg-feAc-cAhGE3bhdCBHdF@roundhouse.proxy.rlwy.net:20270/railway' 

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Pontos(db.Model):
    __tablename__ = 'pontos'
    id = db.Column (db.Integer, primary_key=True)
    id_pay = db.Column (db.String(80), unique=True, nullable=False)
    id_assas = db.Column (db.String(80), nullable=False)
    id_jogador = db.Column (db.String(80), nullable=False)
    pontos = db.Column (db.String(80), nullable=False)
    data_compra = db.Column (db.DateTime)
    status = db.Column (db.String(80), nullable=True)
    link = db.Column (db.String(80))

class Users(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    id_assas = db.Column (db.String(80), unique=True, nullable=False)
    nome = db.Column (db.String(80), unique=True, nullable=False)
    cpf = db.Column (db.String(80), unique=True, nullable=False)
    email = db.Column (db.String(80), unique=True, nullable=False)
    endereco = db.Column (db.String(80), nullable=False) 
    senha = db.Column(db.String(4096), nullable=False)
    pontos = db.Column (db.Float(), nullable=False)
    
class Criarjogos (db.Model):
    id_jogo = db.Column (db.Integer, primary_key=True)
    id_criador = db.Column (db.String(80), nullable=False)
    nome_jogo = db.Column (db.String(80), nullable=False)
    banner_jogo = db.Column (db.String(80), nullable=False)
    resultado_jogo = db.Column (db.String(80), nullable=True)
    data_criacao = db.Column (db.DateTime)
    data_jogo = db.Column(Date, default=date.today)
    caminho_banner = db.Column (db.String(80), nullable=False)
    time1 = db.Column (db.String(80), nullable=False)
    time2 = db.Column (db.String(80), nullable=False)
    valor_acumulado = db.Column (db.Float(80), nullable=False)
    status = db.Column (db.String(80), nullable=False)
    
class Jogadar (db.Model):
    id_jogada = db.Column (db.Integer, primary_key=True)
    id_jogador = db.Column (db.String(80))
    id_jogo = db.Column (db.String(80))
    resultado = db.Column (db.String(80), nullable=False)
    valor = db.Column (db.String(80), nullable=False)
    data_jogada = db.Column(Date, default=date.today)
    
    

with app.app_context():
    db.create_all()






@app.route('/')
def index():
    if 'id' in session:
        user_id = session['id']
        jogos = Criarjogos.query.filter_by(status="rodando")
        usuario = Users.query.get(user_id)
        
        if usuario:
        
            return render_template('index.html', usuario=usuario, jogos=jogos)
    return redirect(url_for('login'))
    

@app.route('/registro', methods=['GET', 'POST'])
def registro():
        
        
    if request.method =='POST':
        username = request.form['nome']
        cpf = request.form['cpf']
        email = request.form['email']
        endereco = request.form['endereco']
        senha = request.form['senha']
        
        existing_user = Users.query.filter_by(email=email).first()
        if existing_user:
            return 'esse email ja esta cadastrado'
        
        existing_cpf = Users.query.filter_by(cpf=cpf).first()
        if existing_cpf:
            return 'esse cpf ja esta cadastrado'

        cliente_id = {
            "name": username,
            "email": email,
            "cpf": cpf
        }

        clienteassas = asaas.criarcliente(cliente_id=cliente_id)
        
        new_user = Users(id_assas=clienteassas ,nome=username, cpf=cpf, email=email, endereco=endereco, senha=senha, pontos=0)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))
    
    return render_template('registro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cpf_or_email = request.form['cpf']
        senha = request.form['senha']
        
        usuario = Users.query.filter((Users.email == cpf_or_email) | (Users.cpf == cpf_or_email)).first()

        # Verifique a senha usando custom_app_context.verify
        if usuario and senha == usuario.senha:
            session['id'] = usuario.id
            flash('Login Bem Sucedido', 'success')
            return redirect(url_for('perfil'))
        flash('Login ou senha incorretos, tente novamente.', 'danger')
        
    return render_template('login.html')

@app.route('/perfil', methods=['GET'])
def perfil():
    if 'id' in session:
        user_id = session['id']
        
        usuario = Users.query.get(user_id)
        
        if usuario:
            return render_template('perfil.html', usuario=usuario)
    
    flash('Faça login para acessar o perfil', 'info')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/editarPerfil', methods=['GET', 'POST'])
def editarPerfil():
    if 'id' in session:
        user_id = session['id']
        usuario = Users.query.get(user_id)
        
        
        if request.method == 'POST':
            usuario.nome = request.form['nome']
            usuario.cpf = request.form['cpf']
            usuario.email = request.form['email']
            usuario.endereco = request.form['endereco']
            
            if 'foto_perfil' in request.files:
                foto_perfil = request.files['foto_perfil']
            if foto_perfil.filename != '':
                # Salve a foto no servidor e atualize o caminho no banco de dados
                # Certifique-se de definir um caminho de destino adequado para salvar a foto
                caminho_salvar = "./static/"+str(user_id)+".jpg"
                foto_perfil.save(caminho_salvar)
                usuario.foto_perfil = caminho_salvar
                
            nova_senha = request.form['senha']
            if nova_senha:
                senhahash = generate_password_hash(nova_senha)
                usuario.senha = senhahash
                
            db.session.commit()
            return redirect(url_for('perfil'))
        return render_template('editarPerfil.html', usuario=usuario)
    
    
@app.route('/comprarpontos', methods=['GET', 'POST'])
def comprarPontos():
    if 'id' in session:
            user_id = session['id']
            usuario = Users.query.get(user_id)
            pontos = ''
            usuario.id = user_id
            if request.method == 'POST':
            
                pontos = request.form['qPontos']

                pontos = request.form['qPontos']
                data_compra = datetime.utcnow()
                
                cliente_id = {
                    "id": usuario.id_assas,
                    "valor": pontos,
                }

                

                pix = asaas.criarpix(cliente_id=cliente_id)
                print(pix[1])
                pay = str(pix[1])
                linkp = pix[0]
                by_history = Pontos(id_pay=pay ,id_assas=usuario.id_assas, id_jogador=user_id, pontos=pontos, data_compra=data_compra, status="pendente", link=linkp)
                db.session.add(by_history)
                
                db.session.commit()

                cliente_id = {
                    "id": usuario.id_assas,
                    "valor": pontos,
                }

                


                if pix[0]:
                    return redirect(pix[0])
                else:
                    return "algo deu errado tente novamente mais tarde"

    return render_template('comprarPontos.html', usuario=usuario)


@app.route("/webhook", methods=["POST","GET"])
def requests():
    if "id" in session:
        user_id = session["id"]
        usuario = Users.query.filter_by(id=user_id).first()
        extrato = Pontos.query.filter_by(id_jogador=user_id, status="pendente").all()
        print(extrato)
        for extratos in extrato:
            result = asaas.payment(id_pay=extratos.id_pay)

            if result == "RECEIVED":
                extratos.status = "pago"
                compra = Pontos.query.filter_by(id_pay=extratos.id_pay).first()
                usuario.pontos = float(usuario.pontos) + float(compra.pontos)
            if result == "PENDING":
                    extratos.status = "pendente"

            db.session.commit()
        return redirect(url_for("historico_compra"))

        


@app.route('/historicocompra')
def historico_compra():
    
    if 'id' in session:
    # Suponha que você tenha uma maneira de identificar o usuário logado (por exemplo, por meio de session['id'])
        user_id = session['id']
        usuario = Users.query.get(user_id)

        # Consulta o banco de dados para recuperar o histórico de compra do usuário
        historico_compra = Pontos.query.filter_by(id_jogador=user_id).all()

        return render_template('order_hystory.html', historico_compra=historico_compra, usuario=usuario)
    return redirect(url_for('login'))

@app.route('/historicojg')
def historico_jogos():
    
    if 'id' in session:
    # Suponha que você tenha uma maneira de identificar o usuário logado (por exemplo, por meio de session['id'])
        user_id = session['id']
        usuario = Users.query.get(user_id)

        # Consulta o banco de dados para recuperar o histórico de compra do usuário
        historico_jg = Criarjogos.query.filter_by(id_criador=user_id).all()

        return render_template('jogos_criados.html', historico_jg=historico_jg, usuario=usuario)
    return redirect(url_for('login'))

@app.route('/historicoap')
def historico_apostas():
    
    if 'id' in session:
    # Suponha que você tenha uma maneira de identificar o usuário logado (por exemplo, por meio de session['id'])
        user_id = session['id']
        usuario = Users.query.get(user_id)

        # Consulta o banco de dados para recuperar o histórico de compra do usuário
        historico_jg = Criarjogos.query.filter_by(id_criador=user_id).all()
        apostas = Jogadar.query.filter_by(id_jogador=user_id).all()

        return render_template('minhas_apostas.html', historico_jg=historico_jg, usuario=usuario, apostas=apostas)
    return redirect(url_for('login'))

@app.route('/criarjogo', methods=['POST', 'GET'])
def criar_jogos():
    if 'id' in session:
        user_id = session['id']
        usuario = Users.query.filter_by(id=user_id).first()
        if usuario.pontos == float(0.0):
            return redirect(url_for('comprarPontos'))
        else:
            if request.method == 'POST':
                print("post")
                nomeJogo = request.form.get('nomeJogo')
                data_jogo = request.form.get('dataJogo')
                time1 = request.form.get('time1')
                time2 = request.form.get('time2')
                if 'bannerJogo' in request.files:
                    bannerJogo = request.files['bannerJogo']
                    if bannerJogo.filename != '':
                        data_criacao = datetime.utcnow() 
                    # Salve a foto no servidor e atualize o caminho no banco de dados
                    # Certifique-se de definir um caminho de destino adequado para salvar a foto
                        caminho_salvar = "./static/"+str(user_id)+str(nomeJogo)+data_jogo+".jpg"
                        bannerJogo.save(caminho_salvar)
                        Criarjogos.banner_jogo = caminho_salvar
                        caminho_banner = str(user_id) + str(nomeJogo) + data_jogo + ".jpg"
                        
                        usuario.pontos -= float(2.0)
                        valor_somar = float(2)
                        
                        
                    
                    reg_jogo = Criarjogos(id_criador=user_id, nome_jogo=nomeJogo, banner_jogo=caminho_salvar, data_criacao=data_criacao, data_jogo=data_jogo, caminho_banner=caminho_banner, time1=time1, time2=time2, valor_acumulado=valor_somar, status="rodando")
                    
                    db.session.add(reg_jogo)
                    db.session.commit()
                    
                        
                    
                    return redirect(url_for('perfil'))     
    else:
        return redirect(url_for('login'))
    return render_template('criar_jogos.html', usuario=usuario)
    
    



@app.route('/jogo/<int:id_jogo>')
def jogo(id_jogo):
    
    # Use o id_jogo para recuperar informações sobre o jogo do banco de dados
    jogo = Criarjogos.query.get(id_jogo)

    if jogo.status == "fechado":
        return "jogo já foi encerrado"
    else:
        if 'id' in session:
            user_id = session['id']
            usuario = Users.query.filter_by(id=user_id).first()
            if user_id == jogo.id_criador:
                return render_template('pagina_jogo_criador.html', jogo=jogo, usuario=usuario)
            else:
                if jogo is None:
                    # Trate o caso em que o jogo não existe
                    return "Jogo não encontrado", 404

                # Renderize uma página HTML com informações sobre o jogo
                return render_template('pagina_jogo.html', jogo=jogo, usuario=usuario)


@app.route('/jogar', methods=['GET', 'POST'])
def jogar():
    if 'id' in session:
        user_id = session['id']
        usuario = Users.query.get(user_id)
        
        if request.method == 'POST':
            valor = request.form['valor']
            data_jogada = datetime.utcnow() 
            time1 = request.form['time1']
            time2 = request.form['time2']
            id_jogo = request.form['id_jogo']
            jogo = Criarjogos.query.get(id_jogo)
            
            resultado = str(time1) + 'X' + str(time2)
            
            reg_jogada = Jogadar(id_jogador=user_id, id_jogo=id_jogo, resultado=resultado, valor=valor, data_jogada=data_jogada)
            if int(user_id) == int(jogo.id_criador):
                return 'não e permitido apostar no proprio jogo'
            else:
            
                if int(usuario.pontos) < int(valor):
                    return redirect(url_for('comprarpontos'))
                else:
                    usuario.pontos = float(usuario.pontos) - float(valor)
                    jogo.valor_acumulado += float(valor)
                    
                    db.session.add(reg_jogada)
                    db.session.commit()
                    return redirect(url_for('perfil'))
                
@app.route('/definirResultado', methods=['POST'])
def definirResultado():
    id_jogo = request.form['id_jogo']
    time1 = request.form['time1']
    time2 = request.form['time2']
    jogo = Criarjogos.query.get(id_jogo)
    
    if jogo is None:
        return jsonify({'message': 'Jogo não encontrado'}), 404

    resultado = str(time1) + 'X' + str(time2)
    
    jogo.resultado_jogo = resultado
    
    db.session.commit()
    
    if jogo.resultado_jogo:
        apostas_vencedoras = Jogadar.query.filter_by(id_jogo=id_jogo, resultado=resultado).all()
        valor = jogo.valor_acumulado
        
        valor_criador = 0.10 * valor
        valor_adm = 0.10 * valor
        valor_restante = valor - valor_criador - valor_adm
        
        if apostas_vencedoras:
            valor_p_ganhador = valor_restante / len(apostas_vencedoras)
            
            for aposta in apostas_vencedoras:
                usuario_ganhador = aposta.id_jogador
                carteira_jogador = Users.query.filter_by(id=usuario_ganhador).first()
                carteira_jogador.pontos += valor_p_ganhador
        else:
            criador_jogo = jogo.id_criador
            carteira_criador = Users.query.get(criador_jogo)
            carteira_criador.pontos += valor_restante * 0.9
            
            taxa_nv = valor_restante * 0.10
        
            adm = Users.query.get(0)  # Substitua 4 pelo ID do usuário administrador
            adm.pontos += valor_adm + taxa_nv
            
        criador_jogo = jogo.id_criador
        carteira_criador = Users.query.get(criador_jogo)
        carteira_criador.pontos += valor_criador
        
        adm = Users.query.get(0)  # Substitua 4 pelo ID do usuário administrador
        adm.pontos += valor_adm
        
        jogo.valor_acumulado = float(0.0)
        jogo.status = "fechado"
        
        db.session.commit()
        
        return redirect(url_for('perfil'))
    
        
    return redirect(url_for('perfil'))


@app.route("/tutorial", methods=["GET"])
def tutorial():
    return render_template("tutorial.html")

    
    
                   

                
                
            
        
        
    
   
            
    


if __name__ == '__main__':
    app.run(debug=True)
    