import os
import re
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client, Client

# ---------------- CONFIG ----------------
st.set_page_config(page_title="CRUD Supabase", layout="centered")
st.title("📋 Gerenciador de Clientes")

load_dotenv()

def conectar_supabase() -> Client:
    url = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
    key = st.secrets.get("SUPABASE_ANON_KEY") or os.getenv("SUPABASE_ANON_KEY")
    if not url or not key:
        st.error("⚠️ Configure SUPABASE_URL e SUPABASE_ANON_KEY em secrets.toml ou .env")
        st.stop()
    return create_client(url, key)

sb = conectar_supabase()
TABELA = "clientes"

def executar(query):
    try:
        resp = query.execute()
        return getattr(resp, "data", resp)
    except Exception as e:
        st.error(f"Erro Supabase: {e}")
        return None

def email_valido(email: str) -> bool:
    """Valida formato básico de e-mail."""
    padrao = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(padrao, email.strip()))

# ---------------- CONSULTAR ----------------
st.markdown("### 🔍 Consultar clientes")
busca = st.text_input("Pesquisar por nome ou email", placeholder="Ex: Maria, João@gmail.com")
dados = executar(sb.table(TABELA).select("*").order("created_at", desc=True)) or []

if busca:
    dados = [d for d in dados if busca.lower() in str(d.get("nome", "")).lower() or busca.lower() in str(d.get("email", "")).lower()]

df = pd.DataFrame(dados)
if not df.empty:
    st.dataframe(df[["id", "nome", "email", "ativo"]], use_container_width=True, hide_index=True)
else:
    st.info("Nenhum cliente encontrado.")

st.divider()

# ---------------- ADICIONAR ----------------
st.markdown("### ➕ Adicionar novo cliente")
nome, email, ativo, notas = "", "", True, ""

with st.form("form_add", clear_on_submit=True):
    nome = st.text_input("Nome completo")
    email = st.text_input("Email")
    ativo = st.checkbox("Ativo", True)
    notas = st.text_area("Notas", placeholder="Observações opcionais")
    salvar = st.form_submit_button("Salvar")

if salvar:
    if not nome or not email:
        st.warning("Preencha nome e email.")
    elif not email_valido(email):
        st.error("❌ E-mail inválido. Verifique o formato (ex: usuario@dominio.com).")
    else:
        novo = {"nome": nome, "email": email, "ativo": ativo, "notas": notas or None}
        res = executar(sb.table(TABELA).insert(novo))
        if res:
            st.success("✅ Cliente adicionado!")
            st.rerun()
        else:
            st.error("Erro ao adicionar cliente.")

st.divider()

# ---------------- EDITAR / EXCLUIR ----------------
st.markdown("### ✏️ Editar ou excluir cliente")
id_cliente = st.text_input("Digite o ID do cliente para editar ou excluir")
acao = st.radio("Ação", ["Editar", "Excluir"], horizontal=True)

if id_cliente:
    registro = executar(sb.table(TABELA).select("*").eq("id", id_cliente))
    registro = registro[0] if registro else None

    if not registro:
        st.warning("ID não encontrado.")
    elif acao == "Editar":
        with st.form("form_edit"):
            nome_e = st.text_input("Nome", registro["nome"])
            email_e = st.text_input("Email", registro["email"])
            ativo_e = st.checkbox("Ativo", registro["ativo"])
            notas_e = st.text_area("Notas", registro.get("notas", "") or "")
            salvar_edicao = st.form_submit_button("Salvar alterações")
        if salvar_edicao:
            if not nome_e or not email_e:
                st.warning("Preencha nome e email.")
            elif not email_valido(email_e):
                st.error("❌ E-mail inválido. Verifique o formato.")
            else:
                update = {"nome": nome_e, "email": email_e, "ativo": ativo_e, "notas": notas_e}
                ok = executar(sb.table(TABELA).update(update).eq("id", id_cliente))
                if ok:
                    st.success("✅ Dados atualizados!")
                    st.rerun()
                else:
                    st.error("Erro ao atualizar registro.")
    elif acao == "Excluir":
        confirmar = st.checkbox("Confirmar exclusão permanente")
        if confirmar and st.button("Excluir agora"):
            executar(sb.table(TABELA).delete().eq("id", id_cliente))
            st.success("🗑️ Cliente excluído com sucesso.")
            st.rerun()
