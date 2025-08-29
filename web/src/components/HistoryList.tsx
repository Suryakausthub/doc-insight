export default function HistoryList({ items, onPick }:{
  items: any[], onPick: (id:string)=>void
}) {
  if (!items?.length) return <p>No uploads yet.</p>;
  return (
    <ul>
      {items.map(it => (
        <li key={it.id}>
          <button onClick={() => onPick(it.id)}>
            {it.filename} • {new Date(it.uploaded_at).toLocaleString()} • {it.summary_type}
          </button>
        </li>
      ))}
    </ul>
  );
}
