"""
Serviços unificados: Banco de dados e Autenticação
"""
import os
import re
import hashlib
import streamlit as st
from datetime import datetime
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_ANON_KEY, TABELA_USUARIOS, SESSION_TIMEOUT

# ================= DATABASE =================

def conectar_supabase() -> Client:
    """Cria conexão com Supabase"""
    url = st.secrets.get("SUPABASE_URL") or SUPABASE_URL
    key = st.secrets.get("SUPABASE_ANON_KEY") or SUPABASE_ANON_KEY
    
    if not url or not key:
        st.error("⚠️ Configure SUPABASE_URL e SUPABASE_ANON_KEY")
        st.stop()
    
    return create_client(url, key)


def executar(query):
    """Executa query e retorna dados ou None em caso de erro"""
    try:
        resp = query.execute()
        return getattr(resp, "data", resp)
    except Exception as e:
        st.error(f"❌ Erro Supabase: {e}")
        return None


def init_db():
    """Verifica conexão com banco de dados"""
    sb = conectar_supabase()
    try:
        sb.table("usuarios").select("id").limit(1).execute()
        return True, "Conexão OK"
    except Exception:
        try:
            with open("schema.sql", "r", encoding="utf-8") as f:
                return False, f.read()
        except:
            return False, "Erro ao ler schema.sql"


# ================= AUTH =================

def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()


def email_valido(email: str) -> bool:
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email.strip()))


def validar_senha(senha: str) -> tuple[bool, str]:
    if not senha: return False, "Senha vazia"
    return True, "✅"


def registrar_usuario(nome: str, email: str, senha: str) -> tuple[bool, str]:
    sb = conectar_supabase()
    
    if not nome or not email or not senha: return False, "Preencha tudo"
    if not email_valido(email): return False, "Email inválido"
    
    valido, msg = validar_senha(senha)
    if not valido: return False, msg
    
    users = executar(sb.table(TABELA_USUARIOS).select("*").eq("email", email))
    if users: return False, "Email já registrado"
    
    novo = {
        "nome": nome, "email": email,
        "senha_hash": hash_senha(senha),
        "criado_em": datetime.now().isoformat()
    }
    
    if executar(sb.table(TABELA_USUARIOS).insert(novo)):
        return True, "✅ Sucesso!"
    return False, "Erro ao registrar"


def autenticar_usuario(email: str, senha: str) -> tuple[bool, dict | None]:
    sb = conectar_supabase()
    if not email or not senha: return False, None
    
    users = executar(sb.table(TABELA_USUARIOS).select("*").eq("email", email))
    if not users: return False, None
    
    user = users[0]
    if user.get("senha_hash") == hash_senha(senha):
        return True, user
    return False, None


def iniciar_sessao(usuario: dict):
    st.session_state.update({
        "logged_in": True, "usuario": usuario,
        "login_time": datetime.now(),
        "usuario_id": usuario.get("id"),
        "usuario_email": usuario.get("email"),
        "usuario_nome": usuario.get("nome")
    })


def encerrar_sessao():
    keys = ["logged_in", "usuario", "login_time", "usuario_id", "usuario_email", "usuario_nome"]
    for k in keys:
        if k in st.session_state: del st.session_state[k]


def verificar_sessao() -> bool:
    if not st.session_state.get("logged_in"): return False
    
    if (datetime.now() - st.session_state.get("login_time", datetime.now())).total_seconds() > SESSION_TIMEOUT:
        encerrar_sessao()
        st.warning("⏰ Sessão expirada")
        return False
        
    st.session_state.login_time = datetime.now()
    return True


# ================= PRODUTOS =================

@st.cache_data(ttl=60, show_spinner=False)
def listar_produtos():
    """Lista produtos com Cache (Memoization)"""
    sb = conectar_supabase()
    return executar(sb.table("produtos").select("*").order("descricao")) or []


def criar_produto(descricao: str, qtde: int, valor: float):
    sb = conectar_supabase()
    novo = {"descricao": descricao, "qtde_estoque": qtde, "valor": valor}
    return executar(sb.table("produtos").insert(novo))


def atualizar_produto(id_prod: str, dados: dict):
    sb = conectar_supabase()
    return executar(sb.table("produtos").update(dados).eq("id", id_prod))


def deletar_produto(id_prod: str):
    sb = conectar_supabase()
    return executar(sb.table("produtos").delete().eq("id", id_prod))


# ================= CARRINHO =================

def listar_carrinho(cliente_id: str):
    sb = conectar_supabase()
    # Query Otimizada: Busca carrinho E dados do produto em 1 request (Join)
    # Algoritmo: Eager Loading para evitar N+1
    res = executar(
        sb.table("carrinho")
        .select("*, produtos(*)")
        .eq("cliente_id", cliente_id)
    )
    
    carrinho_detalhado = []
    if res:
        for item in res:
            # Supabase retorna o join aninhado em 'produtos'
            prod = item.get("produtos")
            if prod:
                # Flattening dos dados para a view
                item["produto_nome"] = prod["descricao"]
                item["produto_valor_unit"] = prod["valor"]
                carrinho_detalhado.append(item)
            
    return carrinho_detalhado


def adicionar_carrinho(cliente_id: str, produto_id: str, qtde: int, valor_unit: float):
    sb = conectar_supabase()
    total = qtde * valor_unit
    novo = {
        "cliente_id": cliente_id,
        "produto_id": produto_id,
        "qtde": qtde,
        "valor_total": total
    }
    return executar(sb.table("carrinho").insert(novo))


def remover_carrinho(item_id: str) -> bool:
    return executar(
        conectar_supabase().table("carrinho").delete().eq("id", item_id)
    )

# ==============================================================================
# PERFIL DO USUÁRIO
# ==============================================================================

def buscar_perfil(user_id: str) -> dict:
    """Busca dados do perfil do usuário"""
    res = executar(
        conectar_supabase()
        .table(TABELA_USUARIOS)
        .select("*")
        .eq("id", user_id)
        .single()
    )
    return res if res else {}

def atualizar_perfil(user_id: str, nome: str, email: str, cidade: str, rua: str, numero: str, telefone: str) -> tuple[bool, str]:
    """Atualiza dados do perfil"""
    data = {
        "nome": nome,
        "email": email,
        "cidade": cidade,
        "rua": rua,
        "numero": numero,
        "telefone": telefone
    }
    res = executar(
        conectar_supabase()
        .table(TABELA_USUARIOS)
        .update(data)
        .eq("id", user_id)
    )
    if res:
        # Atualiza sessão se for o próprio usuário
        if st.session_state.usuario_id == user_id:
            st.session_state.usuario_nome = nome
            st.session_state.usuario_email = email
        return True, "Perfil atualizado!"
    return False, "Erro ao atualizar."

def limpar_dados_antigos():
    """Remove produtos indesejados (ex: Geladeira)"""
    sb = conectar_supabase()
    # Remove Geladeira se existir
    executar(sb.table("produtos").delete().ilike("descricao", "%Geladeira%"))
