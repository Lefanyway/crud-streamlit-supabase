"""
Configurações da aplicação
"""
import streamlit as st

# Configuração do Streamlit
PAGE_CONFIG = {
    "page_title": "CRUD + Login",
    "layout": "centered",
    "initial_sidebar_state": "collapsed"
}

# Supabase
# Acessando segredos do .streamlit/secrets.toml
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_ANON_KEY = st.secrets["SUPABASE_ANON_KEY"]
except FileNotFoundError:
    # Fallback para desenvolvimento local sem secrets.toml (opcional)
    import os
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# Tabelas
TABELA_USUARIOS = "usuarios"
TABELA_CLIENTES = "clientes"

# Sessão
SESSION_TIMEOUT = 3600  # 1 hora em segundos