# VALORA

Plataforma de información e ingeniería financiera para empresas.

## Objetivo

VALORA integra información contable, tributaria y financiera para
transformarla en reportes, indicadores y herramientas de apoyo a la
gestión empresarial.

## Arquitectura inicial

```text
SII
 │
 │ RCV Compras / Ventas
 ▼
Importador VALORA
 │
 ▼
Supabase / PostgreSQL
 │
 ├── Empresas
 ├── Usuarios autorizados
 ├── Compras
 └── Ventas
 │
 ▼
Streamlit
 │
 ▼
Portal Financiero VALORA