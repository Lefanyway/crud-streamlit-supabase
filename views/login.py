"""
Página de Login
"""
import streamlit as st
from services import (
    registrar_usuario, autenticar_usuario, iniciar_sessao,
    validar_senha, email_valido
)


def pagina_login():
    """Interface de login"""
    st.title("🔐 Login")
    
    tab1, tab2 = st.tabs(["Login", "Registrar"])
    
    # =============== TAB LOGIN ===============
    with tab1:
        st.markdown("### Fazer Login")
        
        with st.form("form_login", clear_on_submit=True):
            email = st.text_input("Email", placeholder="seu@email.com")
            senha = st.text_input("Senha", type="password", placeholder="Sua senha")
            botao_login = st.form_submit_button("Entrar", use_container_width=True)
        
        if botao_login:
            if not email or not senha:
                st.error("❌ Preencha email e senha")
            else:
                autenticado, usuario = autenticar_usuario(email, senha)
                
                if autenticado and usuario:
                    iniciar_sessao(usuario)
                    st.success(f"✅ Bem-vindo, {usuario['nome']}!")
                    st.rerun()
                else:
                    st.error("❌ Email ou senha incorretos")
    
    # =============== TAB REGISTRAR ===============
    with tab2:
        st.markdown("### Criar Nova Conta")
        
        with st.form("form_registro", clear_on_submit=True):
            nome = st.text_input("Nome completo", placeholder="Seu nome")
            email_reg = st.text_input("Email", placeholder="seu@email.com", key="email_registro")
            
            # Validação em tempo real da senha (Removido requisitos)
            senha_reg = st.text_input(
                "Senha",
                type="password",
                placeholder="Crie uma senha",
                key="senha_registro"
            )
            confirma_senha = st.text_input(
                "Confirme a senha",
                type="password",
                placeholder="Repita a senha",
                key="confirma_senha"
            )
            
            botao_registrar = st.form_submit_button("Criar Conta", use_container_width=True)
        
        if botao_registrar:
            # Validações
            if not nome or not email_reg or not senha_reg or not confirma_senha:
                st.error("❌ Preencha todos os campos")
            elif not email_valido(email_reg):
                st.error("❌ Email inválido")
            elif senha_reg != confirma_senha:
                st.error("❌ As senhas não coincidem")
            else:
                sucesso, mensagem = registrar_usuario(nome, email_reg, senha_reg)
                
                if sucesso:
                    st.success(mensagem)
                    st.info("Agora você pode fazer login com suas credenciais!")
                else:
                    st.error(f"❌ {mensagem}")


if __name__ == "__main__":
    pagina_login()
