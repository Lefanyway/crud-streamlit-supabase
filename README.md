# 🔐 CRUD Supabase + Streamlit com Login

### 1. Clonar repositório
```bash
git clone https://github.com/seu-usuario/crud-streamlit-supabase.git
cd crud-streamlit-supabase
```

### 2. Criar e ativar ambiente virtual

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar Supabase

#### Opção A: Usando arquivo `.env`
Crie um arquivo `.env` na raiz do projeto:
```
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_ANON_KEY=sua-chave-anonima
```

#### Opção B: Usando `st.secrets` (Streamlit Cloud)
Crie `.streamlit/secrets.toml`:
```toml
SUPABASE_URL = "https://seu-projeto.supabase.co"
SUPABASE_ANON_KEY = "sua-chave-anonima"
```

### 5. Criar tabelas no Supabase

1. Abra o [Supabase Dashboard](https://app.supabase.com)
2. Vá para **SQL Editor**
3. Crie uma nova query
4. Cole o conteúdo de `schema.sql`
5. Execute a query

### 6. Executar aplicação
```bash
streamlit run app.py
```

A aplicação será aberta em `http://localhost:8501`