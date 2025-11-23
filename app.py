"""
Aplicação Principal - CRUD com Sistema de Login
"""
import streamlit as st
from config import PAGE_CONFIG
from services import verificar_sessao, encerrar_sessao, init_db
from views import login, perfil, produtos, carrinho


# Configurar página
st.set_page_config(**PAGE_CONFIG)


# Verificar banco de dados
db_ok, msg = init_db()
if not db_ok:
    st.error("⚠️ As tabelas do banco de dados não foram encontradas.")
    st.info("Por favor, execute o SQL abaixo no Editor SQL do Supabase:")
    st.code(msg, language="sql")
    st.stop()

# Limpeza de dados antigos (Geladeira)
try:
    from services import limpar_dados_antigos
    limpar_dados_antigos()
except:
    pass

# Inicializar estado de sessão
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.usuario = None


def main():
    """Função principal da aplicação"""
    
    # Verifica se usuário está logado
    if verificar_sessao():
        # =============== USUÁRIO LOGADO ===============
        
        # Sidebar
        with st.sidebar:
            st.markdown("---")
            st.markdown(f"👤 **{st.session_state.usuario_nome}**")
            st.caption(st.session_state.usuario_email)
            st.markdown("---")
            
            pagina = st.radio(
                "📌 Navegação",
                ["👤 Meu Perfil", "📦 Produtos", "🛒 Carrinho"]
            )
            
            if st.button("🚪 Sair", use_container_width=True):
                encerrar_sessao()
                st.rerun()
        
        # Páginas
        if pagina == "👤 Meu Perfil":
            perfil.pagina_perfil()
            
        elif pagina == "📦 Produtos":
            produtos.pagina_produtos()
            
        elif pagina == "🛒 Carrinho":
            carrinho.pagina_carrinho()
    
    else:
        # =============== USUÁRIO NÃO LOGADO ===============
        login.pagina_login()


if __name__ == "__main__":
    main()
