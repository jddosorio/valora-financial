-- ============================================================
-- VALORA
-- Row Level Security Policies
-- ============================================================

-- User can see only their own authorizations
create policy "Users can view own company authorizations"
on public.user_companies
for select
to authenticated
using (
    user_id = (select auth.uid())
);


-- User can see only authorized companies
create policy "Users can view authorized companies"
on public.companies
for select
to authenticated
using (
    exists (
        select 1
        from public.user_companies uc
        where uc.company_id = companies.id
          and uc.user_id = (select auth.uid())
          and uc.active = true
    )
);


-- User can see only purchases of authorized companies
create policy "Users can view authorized purchases"
on public.rcv_compras
for select
to authenticated
using (
    exists (
        select 1
        from public.user_companies uc
        where uc.company_id = rcv_compras.company_id
          and uc.user_id = (select auth.uid())
          and uc.active = true
    )
);


-- User can see only sales of authorized companies
create policy "Users can view authorized sales"
on public.rcv_ventas
for select
to authenticated
using (
    exists (
        select 1
        from public.user_companies uc
        where uc.company_id = rcv_ventas.company_id
          and uc.user_id = (select auth.uid())
          and uc.active = true
    )
);