import { FormEvent, useMemo, useState } from "react";
import { LoaderCircle, Send } from "lucide-react";

type ChatMessage = {
  id: number;
  role: "user" | "oracle";
  content: string;
  sql?: string;
};

type ChatResponse = {
  answer: string;
  sql: string;
  rows: Record<string, unknown>[];
};

const apiUrl = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const canSubmit = useMemo(() => question.trim().length >= 2 && !isLoading, [question, isLoading]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const cleanQuestion = question.trim();

    if (!cleanQuestion) {
      return;
    }

    const userMessage: ChatMessage = {
      id: Date.now(),
      role: "user",
      content: cleanQuestion,
    };

    setMessages((current) => [...current, userMessage]);
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
          sql: payload.sql,
        },
      ]);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Erro inesperado.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <img className="brand-logo" src="/naruto_logo.png" alt="Konoha Oracle" />
        <div className="status-panel">
          <span className="status-dot" />
          <span>API: {apiUrl}</span>
        </div>
      </aside>

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
                {message.sql ? <code>{message.sql}</code> : null}
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
    </main>
  );
}

export default App;
