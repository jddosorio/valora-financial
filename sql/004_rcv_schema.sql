-- ============================================================
-- VALORA
-- SII Registro de Compras y Ventas (RCV)
-- ============================================================


-- ------------------------------------------------------------
-- RCV COMPRAS
-- ------------------------------------------------------------

create table public.rcv_compras (

    id bigint generated always as identity primary key,

    company_id uuid not null
        references public.companies(id)
        on delete cascade,

    periodo char(6) not null,

    tipo_documento integer not null,
    tipo_compra text,
    rut_proveedor text not null,
    razon_social text,
    folio bigint,
    fecha_documento date,

    monto_exento numeric(18,2) not null default 0,
    monto_neto numeric(18,2) not null default 0,
    iva_recuperable numeric(18,2) not null default 0,
    iva_no_recuperable numeric(18,2) not null default 0,
    monto_total numeric(18,2) not null default 0,

    created_at timestamptz not null default now(),

    constraint rcv_compras_periodo_check
        check (periodo ~ '^[0-9]{6}$')
);


-- ------------------------------------------------------------
-- RCV VENTAS
-- ------------------------------------------------------------

create table public.rcv_ventas (

    id bigint generated always as identity primary key,

    company_id uuid not null
        references public.companies(id)
        on delete cascade,

    periodo char(6) not null,

    tipo_documento integer not null,
    rut_cliente text,
    razon_social text,
    folio bigint,
    fecha_documento date,

    monto_exento numeric(18,2) not null default 0,
    monto_neto numeric(18,2) not null default 0,
    iva numeric(18,2) not null default 0,
    monto_total numeric(18,2) not null default 0,

    created_at timestamptz not null default now(),

    constraint rcv_ventas_periodo_check
        check (periodo ~ '^[0-9]{6}$')
);


-- ------------------------------------------------------------
-- Indexes
-- ------------------------------------------------------------

create index idx_rcv_compras_company_periodo
    on public.rcv_compras(company_id, periodo);

create index idx_rcv_ventas_company_periodo
    on public.rcv_ventas(company_id, periodo);

create index idx_rcv_compras_proveedor
    on public.rcv_compras(company_id, rut_proveedor);

create index idx_rcv_ventas_cliente
    on public.rcv_ventas(company_id, rut_cliente);


-- ------------------------------------------------------------
-- Row Level Security
-- ------------------------------------------------------------

alter table public.rcv_compras enable row level security;

alter table public.rcv_ventas enable row level security;