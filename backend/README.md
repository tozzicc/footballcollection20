# Backend do Football Collection Builder

## Requisitos

- Python 3.10+
- venv

## Criação do ambiente virtual (Windows PowerShell)

```powershell
python -m venv .venv
```

## Ativar ambiente virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

## Instalar dependências

```powershell
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Executar o backend

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Executar testes

```powershell
pytest
```

## Documentação da API

A documentação interativa estará disponível em:

http://127.0.0.1:8000/docs
