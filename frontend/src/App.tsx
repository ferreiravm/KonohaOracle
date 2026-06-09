import { Dispatch, FormEvent, SetStateAction, useMemo, useState } from "react";
import { Check, Database, LoaderCircle, RefreshCw, Search, Send, X } from "lucide-react";

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
  erroaplicacao?: string | null;
  criadoem: string;
};

type ApplyPreview = {
  curation_id: number;
  status: string;
  entity: string;
  query: string;
  operations: Record<string, unknown>[];
  resolved_fields: Record<string, unknown>;
  critical_missing: string[];
  warnings: string[];
  next_required_action: string;
};

type ReferenceOption = {
  id: number | string;
  label: string;
};

type ReferenceOptions = {
  tipos_personagem: ReferenceOption[];
  arcos: ReferenceOption[];
  estados: ReferenceOption[];
  sexos: ReferenceOption[];
  clas: ReferenceOption[];
  vilas: ReferenceOption[];
  ocupacoes: ReferenceOption[];
};

const apiUrl = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const configuredAdminToken = import.meta.env.VITE_ADMIN_TOKEN ?? "";

function App() {
  const [activeView, setActiveView] = useState<"chat" | "admin">("chat");
  const [adminSection, setAdminSection] = useState<"curation" | "characters">("curation");
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
  const [applyPreview, setApplyPreview] = useState<ApplyPreview | null>(null);
  const [referenceOptions, setReferenceOptions] = useState<ReferenceOptions | null>(null);
  const [applyOverrides, setApplyOverrides] = useState<Record<string, string>>({});
  const [curationFilter, setCurationFilter] = useState<"todos" | "Aprovado" | "Rejeitado" | "Aplicado" | "Erro">("todos");
  const [curationStatus, setCurationStatus] = useState("");
  const [isCurating, setIsCurating] = useState(false);
  const [characterSearch, setCharacterSearch] = useState("");
  const [characterResults, setCharacterResults] = useState<Record<string, unknown>[]>([]);
  const [selectedCharacter, setSelectedCharacter] = useState<Record<string, unknown> | null>(null);
  const [characterForm, setCharacterForm] = useState<Record<string, string>>({});

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
      setApplyPreview(null);
    } catch (requestError) {
      setCurationStatus(requestError instanceof Error ? requestError.message : "Erro inesperado.");
    }
  }

  async function loadApplyPreview() {
    if (!selectedCuration) {
      return;
    }

    setCurationStatus("");
    setIsCurating(true);

    try {
      const response = await fetch(`${apiUrl}/admin/curation/${selectedCuration.idcuradoria}/preview-apply`, {
        method: "POST",
        headers: buildAdminHeaders(adminToken),
        body: JSON.stringify({ overrides: normalizeOverrides(applyOverrides) }),
      });

      if (!response.ok) {
        const payload = await response.json().catch(() => null);
        throw new Error(payload?.detail ?? "Nao foi possivel gerar o preview de aplicacao.");
      }

      setApplyPreview((await response.json()) as ApplyPreview);
      await loadReferenceOptions();
    } catch (requestError) {
      setCurationStatus(requestError instanceof Error ? requestError.message : "Erro inesperado.");
    } finally {
      setIsCurating(false);
    }
  }

  async function applyToDatabase() {
    if (!selectedCuration || !applyPreview || applyPreview.status !== "ready") {
      return;
    }

    setCurationStatus("");
    setIsCurating(true);

    try {
      const response = await fetch(`${apiUrl}/admin/curation/${selectedCuration.idcuradoria}/apply`, {
        method: "POST",
        headers: buildAdminHeaders(adminToken),
        body: JSON.stringify({ overrides: normalizeOverrides(applyOverrides) }),
      });

      if (!response.ok) {
        const payload = await response.json().catch(() => null);
        throw new Error(payload?.detail ?? "Nao foi possivel aplicar a curadoria.");
      }

      const payload = (await response.json()) as { idpersonagem: number; status: string };
      setCurationStatus(`Curadoria aplicada. Personagem criado com ID ${payload.idpersonagem}.`);
      await loadCurationItems();
    } catch (requestError) {
      setCurationStatus(requestError instanceof Error ? requestError.message : "Erro inesperado.");
    } finally {
      setIsCurating(false);
    }
  }

  async function loadReferenceOptions() {
    if (referenceOptions) {
      return;
    }

    const response = await fetch(`${apiUrl}/admin/reference-options`, {
      headers: buildAdminHeaders(adminToken),
    });

    if (!response.ok) {
      return;
    }

    setReferenceOptions((await response.json()) as ReferenceOptions);
  }

  async function searchCharacters(event?: FormEvent<HTMLFormElement>) {
    event?.preventDefault();
    setCurationStatus("");

    try {
      const params = new URLSearchParams({ q: characterSearch, limit: "30" });
      const response = await fetch(`${apiUrl}/admin/personagens?${params.toString()}`, {
        headers: buildAdminHeaders(adminToken),
      });

      if (!response.ok) {
        const payload = await response.json().catch(() => null);
        throw new Error(payload?.detail ?? "Nao foi possivel buscar personagens.");
      }

      setCharacterResults((await response.json()) as Record<string, unknown>[]);
    } catch (requestError) {
      setCurationStatus(requestError instanceof Error ? requestError.message : "Erro inesperado.");
    }
  }

  async function loadCharacter(personagemId: number) {
    setCurationStatus("");

    try {
      await loadReferenceOptions();
      const response = await fetch(`${apiUrl}/admin/personagens/${personagemId}`, {
        headers: buildAdminHeaders(adminToken),
      });

      if (!response.ok) {
        const payload = await response.json().catch(() => null);
        throw new Error(payload?.detail ?? "Nao foi possivel carregar personagem.");
      }

      const payload = (await response.json()) as Record<string, unknown>;
      setSelectedCharacter(payload);
      setCharacterForm(recordToStringForm(payload));
    } catch (requestError) {
      setCurationStatus(requestError instanceof Error ? requestError.message : "Erro inesperado.");
    }
  }

  async function saveCharacter() {
    if (!selectedCharacter) {
      return;
    }

    setCurationStatus("");
    setIsCurating(true);

    try {
      const personagemId = Number(selectedCharacter.idpersonagem);
      const response = await fetch(`${apiUrl}/admin/personagens/${personagemId}`, {
        method: "PUT",
        headers: buildAdminHeaders(adminToken),
        body: JSON.stringify({ data: normalizeOverrides(characterForm) }),
      });

      if (!response.ok) {
        const payload = await response.json().catch(() => null);
        throw new Error(payload?.detail ?? "Nao foi possivel salvar personagem.");
      }

      const payload = (await response.json()) as Record<string, unknown>;
      setSelectedCharacter(payload);
      setCharacterForm(recordToStringForm(payload));
      setCurationStatus("Personagem atualizado.");
      await searchCharacters();
    } catch (requestError) {
      setCurationStatus(requestError instanceof Error ? requestError.message : "Erro inesperado.");
    } finally {
      setIsCurating(false);
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

          <div className="admin-subnav">
            <button className={adminSection === "curation" ? "active" : ""} onClick={() => setAdminSection("curation")} type="button">
              Curadoria
            </button>
            <button className={adminSection === "characters" ? "active" : ""} onClick={() => setAdminSection("characters")} type="button">
              Personagens
            </button>
          </div>

          {adminSection === "curation" ? (
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
                    <option value="Aplicado">Aplicados</option>
                    <option value="Erro">Com erro</option>
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
                      onClick={() => {
                        setSelectedCuration(item);
                        setApplyPreview(null);
                        setApplyOverrides({});
                      }}
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
                  <div className="detail-header">
                    <div>
                      <h3>{selectedCuration.consulta}</h3>
                      <p>
                        {selectedCuration.status} em {new Date(selectedCuration.criadoem).toLocaleString("pt-BR")}
                      </p>
                    </div>
                    <button disabled={isCurating || !canPreviewApply(selectedCuration)} onClick={loadApplyPreview} type="button">
                      <Database size={16} />
                      <span>{normalizeText(selectedCuration.status) === "erro" ? "Corrigir aplicacao" : "Preview aplicar"}</span>
                    </button>
                  </div>

                  {selectedCuration.erroaplicacao ? (
                    <div className="preview-block warning">
                      <strong>Erro anterior</strong>
                      <p>{selectedCuration.erroaplicacao}</p>
                    </div>
                  ) : null}

                  {applyPreview ? (
                    <div className="apply-preview">
                      <h4>{applyPreview.next_required_action}</h4>
                      {applyPreview.critical_missing.length > 0 ? (
                        <div className="preview-block warning">
                          <strong>Campos criticos pendentes</strong>
                          <ul>
                            {applyPreview.critical_missing.map((field) => (
                              <li key={field}>{field}</li>
                            ))}
                          </ul>
                        </div>
                      ) : null}

                      <div className="completion-form">
                        <h4>Revisar personagem</h4>
                        <PersonagemEditor
                          applyOverrides={applyOverrides}
                          preview={applyPreview}
                          referenceOptions={referenceOptions}
                          setApplyOverrides={setApplyOverrides}
                        />
                        <div className="completion-actions">
                          <button disabled={isCurating} onClick={loadApplyPreview} type="button">
                            <Database size={16} />
                            <span>Atualizar preview</span>
                          </button>
                          <button
                            className="apply-final"
                            disabled={isCurating || applyPreview.status !== "ready"}
                            onClick={applyToDatabase}
                            type="button"
                          >
                            <Check size={16} />
                            <span>Aplicar ao banco</span>
                          </button>
                        </div>
                      </div>

                      {applyPreview.warnings.length > 0 ? (
                        <div className="preview-block">
                          <strong>Avisos</strong>
                          <ul>
                            {applyPreview.warnings.map((warning) => (
                              <li key={warning}>{warning}</li>
                            ))}
                          </ul>
                        </div>
                      ) : null}

                      <pre>{JSON.stringify(applyPreview, null, 2)}</pre>
                    </div>
                  ) : (
                    <pre>{JSON.stringify(selectedCuration.proposta, null, 2)}</pre>
                  )}
                </div>
              ) : null}
            </section>
          </div>
          ) : (
            <section className="admin-grid characters-admin">
              <form className="admin-panel" onSubmit={searchCharacters}>
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
                  Buscar personagem
                  <input
                    placeholder="Ex: Naruto"
                    value={characterSearch}
                    onChange={(event) => setCharacterSearch(event.target.value)}
                  />
                </label>
                <button className="primary-action" type="submit">
                  <Search size={18} />
                  <span>Buscar</span>
                </button>
                {curationStatus ? <p className="admin-status">{curationStatus}</p> : null}
              </form>

              <div className="review-panel character-results">
                {characterResults.length === 0 ? (
                  <div className="empty-state admin-empty">
                    <h2>Nenhum personagem carregado</h2>
                    <p>Busque por nome ou sobrenome para editar um registro existente.</p>
                  </div>
                ) : (
                  characterResults.map((character) => (
                    <button
                      className={`curation-row ${selectedCharacter?.idpersonagem === character.idpersonagem ? "selected" : ""}`}
                      key={String(character.idpersonagem)}
                      onClick={() => loadCharacter(Number(character.idpersonagem))}
                      type="button"
                    >
                      <span className="status-badge aprovado">{String(character.estado ?? "")}</span>
                      <strong>{`${character.nome ?? ""} ${character.sobrenome ?? ""}`}</strong>
                      <small>#{String(character.idpersonagem)}</small>
                    </button>
                  ))
                )}
              </div>

              {selectedCharacter ? (
                <section className="curation-list character-editor-panel">
                  <div className="list-header">
                    <h2>{`${selectedCharacter.nome ?? ""} ${selectedCharacter.sobrenome ?? ""}`}</h2>
                    <button className="save-character" disabled={isCurating} onClick={saveCharacter} type="button">
                      <Check size={16} />
                      <span>Salvar alteracoes</span>
                    </button>
                  </div>
                  <div className="completion-form">
                    <PersonagemEditor
                      applyOverrides={characterForm}
                      preview={buildEditorPreview(characterForm)}
                      referenceOptions={referenceOptions}
                      setApplyOverrides={setCharacterForm}
                    />
                  </div>
                </section>
              ) : null}
            </section>
          )}
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

function canPreviewApply(curation: CurationItem) {
  const entity = normalizeText(curation.entidade);
  const status = normalizeText(curation.status);

  return entity === "personagem" && ["aprovado", "erro"].includes(status);
}

function normalizeText(value: unknown) {
  return String(value ?? "")
    .trim()
    .toLowerCase();
}

type PersonagemEditorProps = {
  applyOverrides: Record<string, string>;
  preview: ApplyPreview;
  referenceOptions: ReferenceOptions | null;
  setApplyOverrides: Dispatch<SetStateAction<Record<string, string>>>;
};

const PERSONAGEM_FIELDS = [
  { key: "nome", label: "Nome", type: "text" },
  { key: "sobrenome", label: "Sobrenome", type: "text" },
  { key: "idtipopersonagem", label: "Tipo de personagem", type: "select", optionKey: "tipos_personagem" },
  { key: "idcla", label: "Cla", type: "select", optionKey: "clas" },
  { key: "idarcoaparicao", label: "Arco de aparicao", type: "select", optionKey: "arcos" },
  { key: "idarcomorte", label: "Arco de morte", type: "select", optionKey: "arcos" },
  { key: "idocupacaoclassico", label: "Ocupacao classico", type: "select", optionKey: "ocupacoes" },
  { key: "idocupacaoshippuden", label: "Ocupacao Shippuden", type: "select", optionKey: "ocupacoes" },
  { key: "idvila", label: "Vila", type: "select", optionKey: "vilas" },
  { key: "sexo", label: "Sexo", type: "select", optionKey: "sexos" },
  { key: "estado", label: "Estado", type: "select", optionKey: "estados" },
  { key: "idadeclasico", label: "Idade classico", type: "number" },
  { key: "idadeshippuden", label: "Idade Shippuden", type: "number" },
  { key: "datanascimento", label: "Data de nascimento", type: "date" },
  { key: "alturaclassico", label: "Altura classico", type: "number" },
  { key: "alturashippuden", label: "Altura Shippuden", type: "number" },
  { key: "corcabelo", label: "Cor do cabelo", type: "text" },
  { key: "corolhos", label: "Cor dos olhos", type: "text" },
  { key: "corpele", label: "Cor da pele", type: "text" },
  { key: "missoescompletas", label: "Missoes completas", type: "number" },
  { key: "descricao", label: "Descricao", type: "textarea" },
  { key: "historiapersonagem", label: "Historia", type: "textarea" },
  { key: "descricaoroupaclassico", label: "Roupa classico", type: "textarea" },
  { key: "descricaoroupashippuden", label: "Roupa Shippuden", type: "textarea" },
] as const;

function PersonagemEditor({ applyOverrides, preview, referenceOptions, setApplyOverrides }: PersonagemEditorProps) {
  function getFieldValue(key: string) {
    if (applyOverrides[key] !== undefined) {
      return applyOverrides[key];
    }

    const value = preview.resolved_fields[key];
    return value === null || value === undefined ? "" : String(value);
  }

  function updateField(key: string, value: string) {
    setApplyOverrides((current) => ({ ...current, [key]: value }));
  }

  return (
    <div className="personagem-editor">
      {PERSONAGEM_FIELDS.map((field) => {
        const isCritical = preview.critical_missing.includes(field.key);

        if (field.type === "select") {
          const options = referenceOptions?.[field.optionKey as keyof ReferenceOptions] ?? [];
          return (
            <label className={isCritical ? "critical-field" : ""} key={field.key}>
              {field.label}
              <select value={getFieldValue(field.key)} onChange={(event) => updateField(field.key, event.target.value)}>
                <option value="">Nao informado</option>
                {options.map((option) => (
                  <option key={option.id} value={option.id}>
                    {option.label}
                  </option>
                ))}
              </select>
            </label>
          );
        }

        if (field.type === "textarea") {
          return (
            <label className={isCritical ? "critical-field" : ""} key={field.key}>
              {field.label}
              <textarea rows={4} value={getFieldValue(field.key)} onChange={(event) => updateField(field.key, event.target.value)} />
            </label>
          );
        }

        return (
          <label className={isCritical ? "critical-field" : ""} key={field.key}>
            {field.label}
            <input
              step={field.key.startsWith("altura") ? "0.01" : undefined}
              type={field.type}
              value={getFieldValue(field.key)}
              onChange={(event) => updateField(field.key, event.target.value)}
            />
          </label>
        );
      })}
    </div>
  );
}

function normalizeOverrides(overrides: Record<string, string>) {
  return Object.fromEntries(
    Object.entries(overrides)
      .filter(([, value]) => value !== "")
      .map(([key, value]) => {
        const numericValue = Number(value);
        return [key, Number.isNaN(numericValue) ? value : numericValue];
      }),
  );
}

function recordToStringForm(record: Record<string, unknown>) {
  return Object.fromEntries(
    Object.entries(record).map(([key, value]) => [key.toLowerCase(), value === null || value === undefined ? "" : String(value)]),
  );
}

function buildEditorPreview(form: Record<string, string>): ApplyPreview {
  return {
    curation_id: 0,
    status: "ready",
    entity: "personagem",
    query: "",
    operations: [],
    resolved_fields: form,
    critical_missing: [],
    warnings: [],
    next_required_action: "",
  };
}

export default App;
