# Design System — Football Collection Builder

## Conceito visual

Baseado em um museu esportivo moderno, o design system busca transmitir uma aparência elegante, sóbria e profissional. A intenção é oferecer uma interface administrativa moderna com forte presença visual sem perder a discrição e a legibilidade.

## Paleta de cores

- **Fundo principal:** #050918 (azul-marinho quase preto)
- **Fundo secundário:** #121d33 (azul-grafite)
- **Superfícies:** #1d2a47 (grafite azulado)
- **Cartões:** #24355e (azul-grafite claro)
- **Bordas:** #3a4d78 (cinza azulado discreto)
- **Texto principal:** #f8f7f4 (branco suave)
- **Texto secundário:** #c4cad8 (cinza claro)
- **Texto discreto:** #7d89a2 (cinza médio)
- **Destaque principal:** #d4af37 (dourado)
- **Sucesso:** #44b883 (verde)
- **Alerta:** #f3c241 (amarelo)
- **Erro:** #ef5c63 (vermelho)
- **Informação:** #4d8bf5 (azul)

## Significado dos tokens

- **Fundo principal:** base escura que dá profundidade e contraste à interface.
- **Fundo secundário:** área de apoio para seções menos destacadas.
- **Superfícies:** planos de conteúdo com presença sólida e elegante.
- **Cartões:** áreas de destaque com leve separação em relação ao fundo.
- **Bordas:** linhas sutis que definem limites sem chamar atenção excessiva.
- **Texto principal:** legibilidade em temas escuros.
- **Texto secundário:** usado em descrições e informações de apoio.
- **Texto discreto:** para notas menores e metadados.
- **Destaque principal:** elemento de identidade e ação principal.
- **Sucesso / Alerta / Erro / Informação:** estados claros e acessíveis para feedback.

## Tipografia

- Pilha de fontes do sistema: `system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`
- Peso médio para títulos e textos importantes.
- Tamanho fluido para títulos e conteúdo responsivo.

## Espaçamentos

- `--space-xxs`: 0.25rem
- `--space-xs`: 0.5rem
- `--space-sm`: 0.75rem
- `--space-md`: 1rem
- `--space-lg`: 1.5rem
- `--space-xl`: 2rem
- `--space-2xl`: 3rem

## Bordas

- `--radius-sm`: 0.5rem
- `--radius-md`: 0.75rem
- `--radius-lg`: 1rem
- Bordas arredondadas suaves para reforçar a leitura e reduzir rigidez.

## Sombras

- **Soft:** 0 14px 40px rgba(0, 0, 0, 0.18)
- **Elevated:** 0 26px 60px rgba(0, 0, 0, 0.24)
- Sombras são usadas com moderação, criando profundidade discreta em elementos destacados.

## Estados de interação

- Hover: leve elevação e contraste maior em botões.
- Focus: outline visível em elementos interativos e campos de formulário, garantindo navegação por teclado.
- Ativo: transições suaves e respostas táteis discretas.

## Acessibilidade

- Contraste suficiente entre texto e fundo escuro.
- Labels associados a inputs para navegação assistiva.
- Focus visível em botões e campos de texto.
- Uso de semântica HTML para estrutura.
- Navegação por teclado preservada.

## Responsividade

- Layout baseado em grades flexíveis.
- Colunas que se reúnem em uma única coluna em larguras menores.
- Tipografia ajustada para leitura em telas pequenas.

## Regras de uso futuro

- Não espalhar valores de cor arbitrários: utilizar tokens definidos.
- Evitar fontes externas e manter a pilha de fontes do sistema.
- Não usar sombreado excessivo; aplicar apenas quando necessário para hierarquia.
- Priorizar componentes acessíveis e com foco claro.
- O tema inicial é escuro e deve ser mantido até que um tema alternativo seja solicitado.
