"""
Página do Carrinho de Compras
"""
import pandas as pd
import streamlit as st
from services import (
    listar_produtos, listar_carrinho, adicionar_carrinho, remover_carrinho,
    verificar_sessao
)

def pagina_carrinho():
    if not verificar_sessao():
        st.warning("⚠️ Faça login para acessar.")
        st.stop()
        
    st.title("🛒 Meu Carrinho")
    
    user_id = st.session_state.usuario_id
    
    # Adicionar Item
    st.subheader("Adicionar ao Carrinho")
    produtos = listar_produtos()
    
    if produtos:
        col1, col2, col3 = st.columns([3, 1, 1])
        prod_sel = col1.selectbox(
            "Produto",
            options=produtos,
            format_func=lambda x: f"{x['descricao']} (R$ {x['valor']})"
        )
        qtde = col2.number_input("Qtde", min_value=1, value=1)
        
        if col3.button("➕ Adicionar"):
            if adicionar_carrinho(user_id, prod_sel["id"], qtde, prod_sel["valor"]):
                st.success("Adicionado!")
                st.rerun()
            else:
                st.error("Erro ao adicionar.")
    else:
        st.info("Sem produtos disponíveis.")
        
    st.divider()
    
    # Listar Carrinho
    itens = listar_carrinho(user_id)
    
    if itens:
        total_geral = sum(i["valor_total"] for i in itens)
        
        st.markdown(f"### Total: R$ {total_geral:.2f}")
        
        for item in itens:
            with st.container(border=True):
                c1, c2, c3 = st.columns([3, 1, 1])
                c1.markdown(f"**{item.get('produto_nome', 'Produto')}**")
                c1.caption(f"Unit: R$ {item.get('produto_valor_unit', 0):.2f}")
                c2.markdown(f"{item['qtde']}x")
                c2.markdown(f"**R$ {item['valor_total']:.2f}**")
                
                if c3.button("🗑️", key=item["id"]):
                    remover_carrinho(item["id"])
                    st.rerun()
    else:
        st.info("Seu carrinho está vazio.")
