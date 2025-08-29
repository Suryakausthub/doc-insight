import { useEffect, useState } from "react";
import { fetchHistory, fetchInsights } from "../api";
import InsightCard from "../components/InsightCard";
import HistoryList from "../components/HistoryList";

export default function HistoryPage() {
  const [items, setItems] = useState<any[]>([]);
  const [selected, setSelected] = useState<any>(null);

  useEffect(() => { fetchHistory().then(setItems); }, []);

  async function open(id: string) {
    const res = await fetchInsights(id);
    setSelected(res);
  }

  return (
    <div style={{display:"grid", gridTemplateColumns:"1fr 2fr", gap:16}}>
      <div>
        <h2>History</h2>
        <HistoryList items={items} onPick={open}/>
      </div>
      <div>
        {selected ? <InsightCard insight={selected}/> : <p>Select an item to view details.</p>}
      </div>
    </div>
  );
}
