# ET-031 — Checklist de produção para ET-032

## Gate pré-deploy

- [ ] Seis informações do ambiente recebidas e registradas.
- [ ] Repositório/artefato de release isolado do root Git `C:\`.
- [ ] Espaço livre suficiente para release, backup, rollback, venv e logs.
- [ ] Site atual e configuração do web server inventariados e copiados para rollback.
- [ ] Novo snapshot pós-ET-029G criado com data, bytes, SHA-256 e integrity checks.
- [ ] Build final gerado sem URL `127.0.0.1:8000` embutida.
- [ ] Título, idioma e meta description mínimos definidos.
- [ ] Backend testado em venv limpo, sem `--reload`, sob supervisor.
- [ ] DB em storage persistente, com ACL para usuário do serviço e sem sobrescrita por release.
- [ ] 15.592 mídias copiadas/montadas; workspace configurado; zero ausente.
- [ ] `/api` em reverse proxy e porta 8000 não exposta publicamente.
- [ ] Endpoints administrativos/métodos mutáveis negados ou autenticados.
- [ ] CORS compatível com same-origin ou domínio HTTPS exato.
- [ ] Fallback SPA configurado depois das regras de arquivo e `/api`.
- [ ] Logs/stdout capturados com rotação e retenção.
- [ ] HTTPS e redirect 80→443 validados.

## Smoke pré e pós-cutover

- [ ] `/site`
- [ ] `/site/paises`
- [ ] `/site/equipes`
- [ ] `/site/colecoes`
- [ ] `/site/ultimas`
- [ ] `/site/chicao`
- [ ] Refresh direto de uma equipe, coleção e item.
- [ ] Busca exata e busca genérica.
- [ ] Três MP4 de Chicão.
- [ ] `/api/health`, catálogo público e uma mídia real.
- [ ] Zero 404/5xx novo nos logs; certificado e hostname corretos.

## Gate de rollback

- [ ] Web root/config anterior pronto para restauração atômica.
- [ ] Processo novo pode ser parado sem afetar o anterior.
- [ ] Banco anterior e novo permanecem separados e preservados.
- [ ] Critérios e responsável por rollback definidos antes do cutover.
- [ ] Após sucesso, manter rollback até concluir homologação visual pós-publicação.

