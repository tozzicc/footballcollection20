# Football Collection 2.0 — Sprint 0

Ferramenta inicial de engenharia do acervo. Ela lê o CSV de inventário e gera um catálogo preliminar **sem renomear, mover ou apagar qualquer arquivo**.

## Pré-requisitos

- Windows 10/11
- Python 3.11 ou superior

## Execução

No PowerShell, dentro desta pasta:

```powershell
python .\src\analyze_inventory.py "C:\caminho\inventario-footballcollection.csv" --output .\output
```

## Arquivos gerados

- `summary.json`: totais por tipo, extensão e seção.
- `catalog.preview.json`: catálogo preliminar País → Equipe → Pasta → Imagens.
- `collection-images.csv`: imagens candidatas ao novo site.
- `ignored-files.csv`: arquivos técnicos ignorados, com o motivo.
- `inventory.normalized.json`: inventário integral normalizado.

## Regra de segurança

A ferramenta opera somente em leitura sobre o CSV. O acervo original não é alterado.

## Limite desta primeira versão

Ela interpreta a estrutura observada como:

```text
camisas/<pais>/<equipe-ou-selecao>/<pasta-da-colecao>/<imagem>
```

Os nomes como `01_13`, `02_17` e semelhantes ainda são tratados como pastas da coleção, não como anos. A próxima etapa do Sprint 0 será extrair metadados dos HTMLs antigos para descobrir o significado correto dessas pastas.
