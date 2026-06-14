from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from logging.handlers import SysLogHandler
import logging
import os

app = Flask(__name__)

# Diretório onde está o __init__.py
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = os.getenv(
    'SECRET_KEY',
    'dev-secret-key-change-me'
)

# Caminho absoluto para o banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'site.db')

# Configurações de segurança dos cookies
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'danger'

bcrypt = Bcrypt(app)

# =====================================================
# CONFIGURAÇÃO DE LOGS (SYSLOG + ARQUIVO)
# =====================================================

logger = logging.getLogger("taskmanager")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s %(name)s %(levelname)s: %(message)s'
)

file_handler = logging.FileHandler('taskmanager.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)

try:
    syslog_handler = SysLogHandler(address='/dev/log')
    syslog_handler.setLevel(logging.INFO)
    syslog_handler.setFormatter(formatter)

    if not any(isinstance(h, SysLogHandler) for h in logger.handlers):
        logger.addHandler(syslog_handler)

    logger.info("Syslog inicializado com sucesso")

except Exception as e:
    logger.warning(f"Nao foi possivel conectar ao Syslog: {e}")

logger.info("Aplicacao iniciada")


# =====================================================
# CABEÇALHOS DE SEGURANÇA HTTP
# =====================================================

@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = (
        'geolocation=(), microphone=(), camera=()'
    )
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
    response.headers['Cross-Origin-Resource-Policy'] = 'same-origin'
    response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'

    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self'; "
        "img-src 'self' data:; "
        "font-src 'self'; "
        "frame-ancestors 'self'; "
        "base-uri 'self'; "
        "form-action 'self'"
    )

    return response


# Always put Routes at end
from todo_project import routes