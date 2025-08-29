import axios from "axios";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
});

export async function uploadResume(file: File) {
  const fd = new FormData();
  fd.append("file", file);
  const { data } = await api.post("/upload-resume", fd);
  return data;
}

export async function fetchHistory() {
  const { data } = await api.get("/history");
  return data;
}

export async function fetchInsights(id: string) {
  const { data } = await api.get("/insights", { params: { id } });
  return data;
}
