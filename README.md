# CRUD Supabase + Streamlit

## Rodando local
1. `python -m venv .venv && source .venv/bin/activate` (Windows: `.\.venv\Scripts\activate`)
2. `pip install -r requirements.txt`
3. Crie `.env` com `SUPABASE_URL` e `SUPABASE_ANON_KEY` (ou use `st.secrets`).
4. Crie a tabela: cole `schema.sql` no SQL do Supabase.
5. `streamlit run app.py`

## Segurança
As políticas RLS no `schema.sql` são abertas para prototipagem. Em produção, restrinja conforme sua regra de negócio.
