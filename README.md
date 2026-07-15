# Football Collection Builder

## Descrição

Football Collection Builder é uma aplicação para construir e gerenciar coleções de futebol. O projeto permite aos usuários organizar, catalogar e exportar suas coleções de cards, figurinhas e outros itens relacionados ao futebol.

## Status das ETs

- ET-001: concluída
- ET-002: concluída
- ET-003: concluída
- ET-004: concluída
- ET-005: concluída
- ET-006: concluída
- ET-007A: concluída
- ET-007B: concluída

## Atualização recente

O frontend agora inclui um layout base com AppShell, navegação real via React Router, páginas base para as principais seções e o módulo Workspace com persistência local usando `localStorage`.

## Objetivo

Criar uma plataforma web completa que facilite a gestão de coleções de futebol com recursos de:
- Catalogação de itens
- Organização por coleções
- Importação e exportação de dados
- Interface intuitiva e responsiva

## Estrutura do Projeto

```
football-collection-builder/
├── frontend/          # Aplicação frontend (React)
├── backend/           # API backend (Node.js/Express)
├── database/          # Scripts e arquivos de banco de dados
├── docs/              # Documentação do projeto
├── exports/           # Arquivos exportados pelos usuários
├── logs/              # Logs de aplicação
├── tests/             # Testes automatizados
├── README.md          # Este arquivo
└── .gitignore         # Arquivos a serem ignorados pelo Git
```

## Backend

Para executar o backend:

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Para executar os testes do backend:

```bash
cd backend
.\.venv\Scripts\Activate.ps1
pytest
```

## Frontend

Para executar o frontend:

```bash
cd frontend
npm install
npm run dev
```

## Documentação do Design System

Veja também: `docs/design-system.md`

## Próximos Passos

- [ ] Criar esquema de banco de dados
- [ ] Implementar API RESTful
- [ ] Desenvolver UI/UX

## Licença

(A ser definida)

## Autor

Football Collection Builder Team
