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


## GitHub Repository

This project is maintained in a dedicated GitHub repository:

- GitHub account: `jddosorio`
- Repository: `valora-financial`
- Local project: `~/Projects/valora`
- Main branch: `main`

The repository was created directly in the GitHub account `jddosorio` as a new **Private** repository, without initializing it with a README, `.gitignore`, or license.

The local VALORA project was then connected to the new repository:

```bash
cd ~/Projects/valora

git remote add origin https://github.com/jddosorio/valora-financial.git
```

Verify the remote repository before making the first push:

```bash
git remote -v
```

Expected result:

```text
origin  https://github.com/jddosorio/valora-financial.git (fetch)
origin  https://github.com/jddosorio/valora-financial.git (push)
```

This verification is important to ensure that the VALORA project is not accidentally pushed to another repository.

### First commit

```bash
git status
git add .
git status

git commit -m "Initial VALORA financial portal"
git push -u origin main
```

### Normal update procedure

For subsequent changes:

```bash
cd ~/Projects/valora

git status
git add .
git status
git commit -m "Describe the changes"
git push origin main
```

Always review `git status` before committing.

### Files that must never be committed

The `.gitignore` file must include:

```gitignore
.venv/
.streamlit/secrets.toml
.env
.vscode/
__pycache__/
*.pyc
.DS_Store
```

In particular, `.streamlit/secrets.toml` contains the Supabase configuration used by the application and must never be stored in GitHub.