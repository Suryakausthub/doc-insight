export default function InsightCard({ insight }: { insight: any }) {
  return (
    <div style={{border:"1px solid #444", padding:16, borderRadius:8, marginTop:16}}>
      <h3>{insight.filename}</h3>
      <p><b>Type:</b> {insight.summary_type}</p>
      {insight.summary && (
        <>
          <b>AI Summary:</b>
          <pre style={{whiteSpace:"pre-wrap"}}>{insight.summary}</pre>
        </>
      )}
      {insight.top_words && (
        <>
          <b>Top Words (fallback):</b>
          <ul>
            {insight.top_words.map(([w, c]: [string, number]) => (
              <li key={w}>{w} — {c}</li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}
