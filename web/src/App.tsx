import { useState } from "react";
import UploadPage from "./pages/Upload";
import HistoryPage from "./pages/History";

export default function App() {
  const [tab, setTab] = useState<"upload"|"history">("upload");

  return (
    <div style={{maxWidth:900, margin:"32px auto", padding:"0 16px"}}>
      <header style={{display:"flex", gap:8, marginBottom:16}}>
        <button onClick={()=>setTab("upload")}>Upload</button>
        <button onClick={()=>setTab("history")}>History</button>
      </header>
      {tab === "upload" ? <UploadPage/> : <HistoryPage/>}
    </div>
  );
}
