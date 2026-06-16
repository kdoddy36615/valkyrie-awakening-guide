import { useEffect, useState } from "react";

const ENDPOINT = "https://formsubmit.co/ajax/efficienttechllc@gmail.com";
const MAILTO = "mailto:efficienttechllc@gmail.com?subject=Awakening%20Valkyrie%20Guide%20—%20feedback";

type Status = "idle" | "sending" | "sent" | "error";

/**
 * Backend-less feedback form: POSTs to FormSubmit.co, which relays the message
 * by email (free, no account). Falls back to a mailto link if the relay fails.
 */
export default function FeedbackModal({ onClose }: { onClose: () => void }) {
  const [message, setMessage] = useState("");
  const [from, setFrom] = useState("");
  const [status, setStatus] = useState<Status>("idle");

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);

  async function send(e: React.FormEvent) {
    e.preventDefault();
    if (!message.trim()) return;
    setStatus("sending");
    try {
      const res = await fetch(ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({
          message,
          from: from || "(not given)",
          _subject: "Awakening Valkyrie Guide — feedback",
          _captcha: "false",
        }),
      });
      setStatus(res.ok ? "sent" : "error");
    } catch {
      setStatus("error");
    }
  }

  return (
    <div className="lightbox" onClick={onClose} role="dialog" aria-label="Feedback">
      <form className="feedback-form" onClick={(e) => e.stopPropagation()} onSubmit={send}>
        <h3>Feedback</h3>
        {status === "sent" ? (
          <p className="note">Sent — thanks!</p>
        ) : (
          <>
            <label>
              <span className="k">Message</span>
              <textarea
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                rows={5}
                autoFocus
                placeholder="Wrong number, missing combo, bad explanation…"
              />
            </label>
            <label>
              <span className="k">Contact (optional)</span>
              <input
                type="text"
                value={from}
                onChange={(e) => setFrom(e.target.value)}
                placeholder="Discord handle / email, if you want a reply"
              />
            </label>
            {status === "error" && (
              <p className="note">
                Couldn’t send. <a href={MAILTO}>Email instead</a>.
              </p>
            )}
            <div className="row">
              <button type="submit" className="primary" disabled={status === "sending" || !message.trim()}>
                {status === "sending" ? "Sending…" : "Send"}
              </button>
              <button type="button" onClick={onClose}>
                Close
              </button>
            </div>
          </>
        )}
      </form>
    </div>
  );
}
