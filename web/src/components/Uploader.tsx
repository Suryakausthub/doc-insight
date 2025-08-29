import { useState } from "react";
import { uploadResume } from "../api";

export default function Uploader({ onDone }: { onDone: (insight: any) => void }) {
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  return (
    <div>
      <input
        type="file"
        accept="application/pdf"
        onChange={async (e) => {
          const f = e.target.files?.[0];
          if (!f) return;
          setErr(null); setLoading(true);
          try {
            const res = await uploadResume(f);
            onDone(res);
          } catch (e: any) {
            setErr(e?.response?.data?.detail || "Upload failed");
          } finally {
            setLoading(false);
          }
        }}
      />
      {loading && <p>Processing…</p>}
      {err && <p style={{color:"tomato"}}>{err}</p>}
    </div>
  );
}
