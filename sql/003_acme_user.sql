-- ============================================================
-- VALORA
-- Associate ACME demo user with ACME company
-- ============================================================

insert into public.user_companies (
    user_id,
    company_id,
    role
)
select
    u.id,
    c.id,
    'client'
from auth.users u
cross join public.companies c
where u.email = 'demo@acme.cl'
  and c.nombre_fantasia = 'ACME';