-- Habilite extensão para gerar UUID (normalmente já está disponível no Supabase)
create extension if not exists "pgcrypto";

-- Tabela de exemplo
create table if not exists public.clientes (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  nome text not null check (char_length(nome) <= 120),
  email text not null unique,
  ativo boolean not null default true,
  notas text
);

-- RLS
alter table public.clientes enable row level security;

-- AVISO: políticas amplas para prototipagem. Restrinja em produção.
drop policy if exists "p_select_all" on public.clientes;
drop policy if exists "p_insert_all" on public.clientes;
drop policy if exists "p_update_all" on public.clientes;
drop policy if exists "p_delete_all" on public.clientes;

create policy "p_select_all" on public.clientes for select using (true);
create policy "p_insert_all" on public.clientes for insert with check (true);
create policy "p_update_all" on public.clientes for update using (true) with check (true);
create policy "p_delete_all" on public.clientes for delete using (true);
