"""
Página de Produtos (Estilo E-commerce)
"""
import streamlit as st
from services import (
    listar_produtos, criar_produto, adicionar_carrinho, verificar_sessao
)

def garantir_produtos_demo():
    """Cria produtos de demonstração se não existirem"""
    produtos_demo = [
        {"descricao": "Videogame", "valor": 3500.00, "qtde": 50, "icon": "🎮"},
        {"descricao": "Televisão 4K", "valor": 2800.00, "qtde": 30, "icon": "📺"},
        {"descricao": "Computador Gamer", "valor": 5000.00, "qtde": 20, "icon": "🖥️"},
        {"descricao": "Macbook Pro", "valor": 12000.00, "qtde": 15, "icon": "💻"},
        {"descricao": "iPhone 15", "valor": 8000.00, "qtde": 40, "icon": "📱"},
    ]
    
    existentes = listar_produtos()
    descricoes_existentes = [p["descricao"] for p in existentes]
    
    for prod in produtos_demo:
        if prod["descricao"] not in descricoes_existentes:
            criar_produto(prod["descricao"], prod["qtde"], prod["valor"])

def pagina_produtos():
    if not verificar_sessao():
        st.warning("⚠️ Faça login.")
        st.stop()
        
    st.title("📦 Produtos Disponíveis")
    
    # Garantir que produtos existam
    garantir_produtos_demo()
    
    produtos = listar_produtos()
    
    # Mapeamento de ícones (simples, baseado no nome)
    icons = {
        "Videogame": "🎮",
        "Televisão": "📺",
        "Computador": "🖥️",
        "Macbook": "💻",
        "iPhone": "📱"
    }
    
    if not produtos:
        st.info("Nenhum produto encontrado.")
        return

    # Layout em Grid (3 colunas)
    cols = st.columns(3)
    
    for i, prod in enumerate(produtos):
        with cols[i % 3]:
            with st.container(border=True):
                # Tenta achar ícone ou usa padrão
                icon = next((v for k, v in icons.items() if k in prod["descricao"]), "📦")
                
                st.markdown(f"<h1 style='text-align: center;'>{icon}</h1>", unsafe_allow_html=True)
                st.markdown(f"### {prod['descricao']}")
                st.markdown(f"**R$ {prod['valor']:.2f}**")
                st.caption(f"Estoque: {prod['qtde_estoque']}")
                
                if st.button("Adicionar ao Carrinho", key=f"add_{prod['id']}", use_container_width=True):
                    if adicionar_carrinho(st.session_state.usuario_id, prod["id"], 1, prod["valor"]):
                        st.toast(f"{prod['descricao']} adicionado!", icon="🛒")
                    else:
                        st.error("Erro ao adicionar.")
