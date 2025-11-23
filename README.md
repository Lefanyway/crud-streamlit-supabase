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

## 👤 Uso da Aplicação

### Registro
1. Clique em **"Registrar"** na aba de login
2. Preencha:
   - Nome completo
   - Email válido
   - Senha (mínimo 6 caracteres, 1 maiúscula, 1 número)
3. Clique em **"Criar Conta"**

### Login
1. Digite seu email e senha
2. Clique em **"Entrar"**

### Gerenciar Clientes
Após autenticado, você pode:
- **Consultar** - Pesquisar clientes por nome ou email
- **Adicionar** - Criar novo cliente
- **Editar** - Atualizar informações
- **Excluir** - Remover cliente (requer confirmação)

## 🔒 Segurança

- ✅ Senhas com hash SHA256
- ✅ Validação de email
- ✅ Força de senha obrigatória
- ✅ Sessões com expiração (1 hora)
- ✅ RLS (Row Level Security) no Supabase

⚠️ **Importante para Produção:**
- Altere as políticas RLS do `schema.sql`
- Use Supabase Row Level Security corretamente
- Implemente autenticação mais robusta (OAuth, JWT)
- Use HTTPS em produção

## 📦 Dependências

- **streamlit** - Framework web
- **supabase** - Cliente Python para Supabase
- **pandas** - Manipulação de dados
- **python-dotenv** - Gerenciamento de variáveis
- **bcrypt** - Hash de senhas
