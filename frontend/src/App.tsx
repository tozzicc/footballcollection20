import './App.css'

function App() {
  return (
    <div className="app-shell">
      <header className="hero-panel">
        <p className="eyebrow">Design System — Sprint 1</p>
        <h1>Football Collection Builder</h1>
        <p className="hero-text">
          Uma fundação visual sóbria e profissional inspirada em um museu esportivo
          moderno, com foco em elegância, imagem forte e administração de coleções.
        </p>
      </header>

      <main className="demo-layout">
        <section className="panel preview-panel">
          <h2>Paleta de cores</h2>
          <p className="panel-description">
            Tokens principais usados no design system para o tema escuro e profissional.
          </p>
          <div className="colors-grid">
            <article className="color-token bg-primary">
              <span>Fundo primário</span>
              <strong>#050918</strong>
            </article>
            <article className="color-token bg-secondary">
              <span>Fundo secundário</span>
              <strong>#121d33</strong>
            </article>
            <article className="color-token bg-surface">
              <span>Superfície</span>
              <strong>#1d2a47</strong>
            </article>
            <article className="color-token bg-card">
              <span>Cartão</span>
              <strong>#24355e</strong>
            </article>
            <article className="color-token bg-border">
              <span>Borda</span>
              <strong>#3a4d78</strong>
            </article>
            <article className="color-token bg-accent">
              <span>Destaque</span>
              <strong>#d4af37</strong>
            </article>
          </div>
        </section>

        <section className="panel example-panel">
          <div className="example-group">
            <h2>Componentes</h2>
            <div className="button-row">
              <button className="btn btn-primary">Botão primário</button>
              <button className="btn btn-secondary">Botão secundário</button>
              <button className="btn btn-danger">Botão de perigo</button>
            </div>
          </div>

          <div className="example-group">
            <h3>Cartão</h3>
            <article className="card-surface">
              <h4>Cartão de exemplo</h4>
              <p>
                Este cartão demonstra a superfície de conteúdo com borda suave,
                sombra discreta e tipografia legível.
              </p>
            </article>
          </div>

          <div className="example-group">
            <h3>Badges</h3>
            <div className="badge-row">
              <span className="badge badge-success">Sucesso</span>
              <span className="badge badge-warning">Alerta</span>
              <span className="badge badge-error">Erro</span>
            </div>
          </div>

          <div className="example-group form-group">
            <h3>Campo de texto</h3>
            <label className="field-label" htmlFor="demo-input">
              Buscar coleção
            </label>
            <input
              id="demo-input"
              type="text"
              className="text-field"
              placeholder="Digite um termo..."
            />
          </div>
        </section>
      </main>
    </div>
  )
}

export default App
