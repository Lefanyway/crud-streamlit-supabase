"""
Página de Perfil do Usuário
"""
import streamlit as st
from services import (
    buscar_perfil, atualizar_perfil, verificar_sessao
)

def pagina_perfil():
    if not verificar_sessao():
        st.warning("⚠️ Faça login.")
        st.stop()
        
    st.title("👤 Meu Perfil")
    
    user_id = st.session_state.usuario_id
    dados = buscar_perfil(user_id)
    
    if not dados:
        st.error("Erro ao carregar perfil.")
        return
        
    with st.form("update_profile"):
        st.subheader("Dados Pessoais")
        
        col1, col2 = st.columns(2)
        nome = col1.text_input("Nome Completo", value=dados.get("nome", ""))
        email = col2.text_input("Email", value=dados.get("email", ""))
        
        st.subheader("Endereço e Contato")
        col3, col4 = st.columns([3, 1])
        cidade = col3.text_input("Cidade", value=dados.get("cidade", "") or "")
        numero = col4.text_input("Número", value=dados.get("numero", "") or "")
        
        rua = st.text_input("Rua / Avenida", value=dados.get("rua", "") or "")
        telefone = st.text_input("Telefone / WhatsApp", value=dados.get("telefone", "") or "")
        
        if st.form_submit_button("💾 Salvar Alterações"):
            ok, msg = atualizar_perfil(user_id, nome, email, cidade, rua, numero, telefone)
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)
