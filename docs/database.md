# VALORA — Modelo de Base de Datos

## Plataforma

- PostgreSQL
- Supabase
- Proyecto: `financiera`
- Autenticación: Supabase Auth

## Principio de diseño

VALORA utiliza una base de datos multiempresa.

Los usuarios son autenticados mediante Supabase Auth y posteriormente
VALORA determina a qué empresas puede acceder cada usuario.

La contraseña nunca se almacena en las tablas de VALORA.

## Modelo inicial

```text
Supabase Auth
   auth.users
       │
       │ user_id
       ▼
user_companies
       │
       │ company_id
       ▼
   companies
       │
       ├── ACME SpA
       ├── Empresa B
       └── Empresa C