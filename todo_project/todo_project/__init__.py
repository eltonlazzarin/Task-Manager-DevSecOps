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

# Log em arquivo (facilita testes e evidências)
file_handler = logging.FileHandler('taskmanager.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Syslog Linux / WSL
try:
    syslog_handler = SysLogHandler(address='/dev/log')
    syslog_handler.setLevel(logging.INFO)
    syslog_handler.setFormatter(formatter)
    logger.addHandler(syslog_handler)

    logger.info("Syslog inicializado com sucesso")

except Exception as e:
    logger.warning(f"Nao foi possivel conectar ao Syslog: {e}")

logger.info("Aplicacao iniciada")

# Always put Routes at end
from todo_project import routes