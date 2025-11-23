-- Habilite extensão para gerar UUID
create extension if not exists "pgcrypto";

-- Tabela de usuários (CLIENTES)
create table if not exists public.usuarios (
  id uuid primary key default gen_random_uuid(),
  nome text not null,
  email text not null unique,
  senha_hash text not null,
  endereco text,
  cidade text,
  rua text,
  numero text,
  telefone text,
  criado_em timestamptz not null default now()
);

-- Tabela de PRODUTOS
create table if not exists public.produtos (
  id uuid primary key default gen_random_uuid(),
  descricao text not null,
  qtde_estoque integer not null default 0,
  valor decimal(10,2) not null default 0.00,
  criado_em timestamptz not null default now()
);

-- Tabela de CARRINHO (Relacionamento N)
create table if not exists public.carrinho (
  id uuid primary key default gen_random_uuid(),
  cliente_id uuid references public.usuarios(id) on delete cascade,
  produto_id uuid references public.produtos(id) on delete cascade,
  qtde integer not null default 1,
  valor_total decimal(10,2) not null default 0.00,
  criado_em timestamptz not null default now()
);

-- RLS (Row Level Security)
alter table public.usuarios enable row level security;
alter table public.produtos enable row level security;
alter table public.carrinho enable row level security;

-- Políticas simplificadas (Permitir tudo para demonstração)
create policy "Public Access Users" on public.usuarios for all using (true);
create policy "Public Access Products" on public.produtos for all using (true);
create policy "Public Access Cart" on public.carrinho for all using (true);

-- Índices de Performance (Algoritmos: B-Tree)
-- Otimiza busca por email no login (O(log N))
create index if not exists idx_usuarios_email on public.usuarios(email);
-- Otimiza busca de carrinho por cliente (O(log N))
create index if not exists idx_carrinho_cliente on public.carrinho(cliente_id);
-- Otimiza ordenação/busca de produtos
create index if not exists idx_produtos_descricao on public.produtos(descricao);
