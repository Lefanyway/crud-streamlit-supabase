"""
Configurações da aplicação
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Configuração do Streamlit
PAGE_CONFIG = {
    "page_title": "CRUD + Login",
    "layout": "centered",
    "initial_sidebar_state": "collapsed"
}

# Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# Tabelas
TABELA_USUARIOS = "usuarios"
TABELA_CLIENTES = "clientes"

# Sessão
SESSION_TIMEOUT = 3600  # 1 hora em segundos