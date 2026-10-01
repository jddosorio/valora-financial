-- ============================================================
-- VALORA
-- Initial Database Schema
-- PostgreSQL / Supabase
-- ============================================================


-- ------------------------------------------------------------
-- Extension
-- ------------------------------------------------------------

create extension if not exists pgcrypto;


-- ------------------------------------------------------------
-- Companies
-- ------------------------------------------------------------

create table public.companies (

    id uuid primary key default gen_random_uuid(),

    rut text not null unique,

    razon_social text not null,

    nombre_fantasia text,

    active boolean not null default true,

    created_at timestamptz not null default now()
);


-- ------------------------------------------------------------
-- User ↔ Company authorization
--
-- User authentication is managed by Supabase Auth.
-- Passwords are NOT stored in VALORA tables.
-- ------------------------------------------------------------

create table public.user_companies (

    user_id uuid not null
        references auth.users(id)
        on delete cascade,

    company_id uuid not null
        references public.companies(id)
        on delete cascade,

    role text not null default 'client',

    active boolean not null default true,

    created_at timestamptz not null default now(),

    primary key (user_id, company_id),

    constraint user_companies_role_check
        check (role in ('admin', 'client', 'accountant'))
);


-- ------------------------------------------------------------
-- Indexes
-- ------------------------------------------------------------

create index idx_user_companies_company
    on public.user_companies(company_id);


create index idx_user_companies_user
    on public.user_companies(user_id);


-- ------------------------------------------------------------
-- Row Level Security
-- ------------------------------------------------------------

alter table public.companies enable row level security;

alter table public.user_companies enable row level security;