import { FormEvent, useMemo, useState } from "react";
import { Check, LoaderCircle, RefreshCw, Search, Send, X } from "lucide-react";

type ChatMessage = {
  id: number;
  role: "user" | "oracle";
  content: string;
};

type ChatResponse = {
  answer: string;
  sql: string;
  rows: Record<string, unknown>[];
};

type EntityType = "personagem" | "jutsu" | "arco" | "vila" | "cla" | "grupo" | "ferramenta";

type CurationResult = {
  entity: string;
  query: string;
  sources: Record<string, unknown>[];
  proposal: Record<string, unknown>;
};

type CurationItem = {
  idcuradoria: number;
  entidade: string;
  consulta: string;
  status: string;
  proposta: Record<string, unknown>;
  fontes: Record<string, unknown>[];
  observacao?: string | null;
  criadoem: string;
};

const apiUrl = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const configuredAdminToken = import.meta.env.VITE_ADMIN_TOKEN ?? "";

function App() {
  const [activeView, setActiveView] = useState<"chat" | "admin">("chat");
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const [adminToken, setAdminToken] = useState(configuredAdminToken);
  const [entity, setEntity] = useState<EntityType>("personagem");
  const [curationQuery, setCurationQuery] = useState("");
  const [curationNotes, setCurationNotes] = useState("");
  const [curationResult, setCurationResult] = useState<CurationResult | null>(null);
  const [curationItems, setCurationItems] = useState<CurationItem[]>([]);
  const [selectedCuration, setSelectedCuration] = useState<CurationItem | null>(null);
  const [curationFilter, setCurationFilter] = useState<"todos" | "Aprovado" | "Rejeitado">("todos");
  const [curationStatus, setCurationStatus] = useState("");
  const [isCurating, setIsCurating] = useState(false);

  const canSubmit = useMemo(() => question.trim().length >= 2 && !isLoading, [question, isLoading]);
  const canCurate = useMemo(() => curationQuery.trim().length >= 2 && !isCurating, [curationQuery, isCurating]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const cleanQuestion = question.trim();

    if (!cleanQuestion) {
      return;
    }

    setMessages((current) => [...current, { id: Date.now(), role: "user", content: cleanQuestion }]);
    setQuestion("");
    setError("");
    setIsLoading(true);

    try {
      const response = await fetch(`${apiUrl}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: cleanQuestion }),
      });

      if (!response.ok) {
        const payload = await response.json().catch(() => null);
        throw new Error(payload?.detail ?? "Nao foi possivel consultar o Konoha Oracle.");
      }

      const payload = (await response.json()) as ChatResponse;
      setMessages((current) => [
        ...current,
        {
          id: Date.now() + 1,
          role: "oracle",
          content: payload.answer,
        },
      ]);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Erro inesperado.");
    } finally {
      setIsLoading(false);
    }
  }

  async function handleCuration(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setCurationStatus("");
    setCurationResult(null);
    setIsCurating(true);

    try {
      const response = await fetch(`${apiUrl}/admin/curation/propose`, {
        method: "POST",
        headers: buildAdminHeaders(adminToken),
        body: JSON.stringify({
          entity,
          query: curationQuery.trim(),
          notes: curationNotes.trim(),
        }),
      });

      if (!response.ok) {
        const payload = await response.json().catch(() => null);
        throw new Error(payload?.detail ?? "Nao foi possivel gerar a proposta.");
      }

      setCurationResult((await response.json()) as CurationResult);
    } catch (requestError) {
      setCurationStatus(requestError instanceof Error ? requestError.message : "Erro inesperado.");
    } finally {
      setIsCurating(false);
    }
  }

  async function handleDecision(status: "Aprovado" | "Rejeitado") {
    if (!curationResult) {
      return;
    }

    setCurationStatus("");
    setIsCurating(true);

    try {
      const response = await fetch(`${apiUrl}/admin/curation/decision`, {
        method: "POST",
        headers: buildAdminHeaders(adminToken),
        body: JSON.stringify({
          entity: curationResult.entity,
          query: curationResult.query,
          status,
          proposal: curationResult.proposal,
          sources: curationResult.sources,
          note: curationNotes.trim() || null,
        }),
      });

      if (!response.ok) {
        const payload = await response.json().catch(() => null);
        throw new Error(payload?.detail ?? "Nao foi possivel salvar a decisao.");
      }

      const payload = (await response.json()) as { id: number; status: string };
      setCurationStatus(`Curadoria ${payload.status.toLowerCase()} registrada com ID ${payload.id}.`);
      await loadCurationItems();
    } catch (requestError) {
      setCurationStatus(requestError instanceof Error ? requestError.message : "Erro inesperado.");
    } finally {
      setIsCurating(false);
    }
  }

  async function loadCurationItems() {
    setCurationStatus("");

    try {
      const params = new URLSearchParams({ limit: "30" });
      if (curationFilter !== "todos") {
        params.set("status", curationFilter);
      }

      const response = await fetch(`${apiUrl}/admin/curation/items?${params.toString()}`, {
        headers: buildAdminHeaders(adminToken),
      });

      if (!response.ok) {
        const payload = await response.json().catch(() => null);
        throw new Error(payload?.detail ?? "Nao foi possivel carregar curadorias.");
      }

      setCurationItems((await response.json()) as CurationItem[]);
    } catch (requestError) {
      setCurationStatus(requestError instanceof Error ? requestError.message : "Erro inesperado.");
    }
  }

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <img className="brand-logo" src="/naruto_logo.png" alt="Konoha Oracle" />
        <nav className="nav-tabs" aria-label="Navegacao principal">
          <button className={activeView === "chat" ? "active" : ""} onClick={() => setActiveView("chat")} type="button">
            Chat
          </button>
          <button className={activeView === "admin" ? "active" : ""} onClick={() => setActiveView("admin")} type="button">
            Admin
          </button>
        </nav>
        <div className="status-panel">
          <span className="status-dot" />
          <span>API: {apiUrl}</span>
        </div>
      </aside>

      {activeView === "chat" ? (
        <section className="chat-area" aria-label="Chat Konoha Oracle">
          <header className="chat-header">
            <div>
              <p className="eyebrow">Konoha Oracle</p>
              <h1>Consulte o banco de dados de Naruto</h1>
            </div>
          </header>

          <div className="messages" aria-live="polite">
            {messages.length === 0 ? (
              <div className="empty-state">
                <h2>Digite uma pergunta para comecar</h2>
                <p>Exemplos: quais personagens usam fogo? quais jutsus o Naruto conhece?</p>
              </div>
            ) : (
              messages.map((message) => (
                <article className={`message ${message.role}`} key={message.id}>
                  <p>{message.content}</p>
                </article>
              ))
            )}

            {isLoading ? (
              <div className="message oracle loading">
                <LoaderCircle aria-hidden="true" className="spin" size={18} />
                <span>Consultando...</span>
              </div>
            ) : null}
          </div>

          {error ? <p className="error-message">{error}</p> : null}

          <form className="composer" onSubmit={handleSubmit}>
            <input
              aria-label="Pergunta"
              placeholder="Pergunte sobre personagens, jutsus, arcos ou vilas"
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
            />
            <button aria-label="Enviar pergunta" disabled={!canSubmit} title="Enviar pergunta" type="submit">
              <Send size={20} />
            </button>
          </form>
        </section>
      ) : (
        <section className="admin-area" aria-label="Curadoria de dados">
          <header className="chat-header">
            <div>
              <p className="eyebrow">Curadoria</p>
              <h1>Pesquisar e revisar novas informacoes</h1>
            </div>
          </header>

          <div className="admin-grid">
            <form className="admin-panel" onSubmit={handleCuration}>
              <label>
                Token admin
                <input
                  autoComplete="off"
                  placeholder="X-Admin-Token"
                  type="password"
                  value={adminToken}
                  onChange={(event) => setAdminToken(event.target.value)}
                />
              </label>

              <label>
                Tipo
                <select value={entity} onChange={(event) => setEntity(event.target.value as EntityType)}>
                  <option value="personagem">Personagem</option>
                  <option value="jutsu">Jutsu</option>
                  <option value="arco">Arco</option>
                  <option value="vila">Vila</option>
                  <option value="cla">Cla</option>
                  <option value="grupo">Grupo</option>
                  <option value="ferramenta">Ferramenta</option>
                </select>
              </label>

              <label>
                Busca publica
                <input
                  placeholder="Ex: Kisame Hoshigaki"
                  value={curationQuery}
                  onChange={(event) => setCurationQuery(event.target.value)}
                />
              </label>

              <label>
                Observacoes
                <textarea
                  placeholder="Opcional: foco da pesquisa, duvidas ou contexto adicional"
                  rows={5}
                  value={curationNotes}
                  onChange={(event) => setCurationNotes(event.target.value)}
                />
              </label>

              <button className="primary-action" disabled={!canCurate} type="submit">
                {isCurating ? <LoaderCircle className="spin" size={18} /> : <Search size={18} />}
                <span>Analisar</span>
              </button>

              {curationStatus ? <p className="admin-status">{curationStatus}</p> : null}
            </form>

            <div className="review-panel">
              {curationResult ? (
                <>
                  <div className="review-actions">
                    <button className="approve" disabled={isCurating} onClick={() => handleDecision("Aprovado")} type="button">
                      <Check size={18} />
                      <span>Aprovar</span>
                    </button>
                    <button className="reject" disabled={isCurating} onClick={() => handleDecision("Rejeitado")} type="button">
                      <X size={18} />
                      <span>Rejeitar</span>
                    </button>
                  </div>

                  <section className="proposal-section">
                    <h2>Proposta estruturada</h2>
                    <pre>{JSON.stringify(curationResult.proposal, null, 2)}</pre>
                  </section>

                  <section className="proposal-section">
                    <h2>Fontes publicas</h2>
                    <pre>{JSON.stringify(curationResult.sources, null, 2)}</pre>
                  </section>
                </>
              ) : (
                <div className="empty-state admin-empty">
                  <h2>Nenhuma proposta gerada</h2>
                  <p>Pesquise uma entidade para receber uma proposta estruturada antes de aprovar a curadoria.</p>
                </div>
              )}
            </div>

            <section className="curation-list">
              <div className="list-header">
                <h2>Fila de curadoria</h2>
                <div className="list-controls">
                  <select value={curationFilter} onChange={(event) => setCurationFilter(event.target.value as typeof curationFilter)}>
                    <option value="todos">Todos</option>
                    <option value="Aprovado">Aprovados</option>
                    <option value="Rejeitado">Rejeitados</option>
                  </select>
                  <button onClick={loadCurationItems} type="button">
                    <RefreshCw size={16} />
                    <span>Atualizar</span>
                  </button>
                </div>
              </div>

              <div className="curation-items">
                {curationItems.length === 0 ? (
                  <p className="muted-text">Nenhuma curadoria carregada.</p>
                ) : (
                  curationItems.map((item) => (
                    <button
                      className={`curation-row ${selectedCuration?.idcuradoria === item.idcuradoria ? "selected" : ""}`}
                      key={item.idcuradoria}
                      onClick={() => setSelectedCuration(item)}
                      type="button"
                    >
                      <span className={`status-badge ${item.status.toLowerCase()}`}>{item.status}</span>
                      <strong>{item.consulta}</strong>
                      <small>{item.entidade} #{item.idcuradoria}</small>
                    </button>
                  ))
                )}
              </div>

              {selectedCuration ? (
                <div className="curation-detail">
                  <h3>{selectedCuration.consulta}</h3>
                  <p>
                    {selectedCuration.status} em {new Date(selectedCuration.criadoem).toLocaleString("pt-BR")}
                  </p>
                  <pre>{JSON.stringify(selectedCuration.proposta, null, 2)}</pre>
                </div>
              ) : null}
            </section>
          </div>
        </section>
      )}
    </main>
  );
}

function buildAdminHeaders(adminToken: string) {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };

  if (adminToken.trim()) {
    headers["X-Admin-Token"] = adminToken.trim();
  }

  return headers;
}

export default App;
