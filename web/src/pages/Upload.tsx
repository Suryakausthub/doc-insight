import { useState } from "react";
import Uploader from "../components/Uploader";
import InsightCard from "../components/InsightCard";

export default function UploadPage() {
  const [insight, setInsight] = useState<any>(null);

  return (
    <div>
      <h2>Upload Resume</h2>
      <Uploader onDone={setInsight} />
      {insight && <InsightCard insight={insight} />}
    </div>
  );
}
