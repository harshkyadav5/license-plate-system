import { useState, useEffect } from "react";
import UploadBox from "./components/UploadBox";
import ResultCard from "./components/ResultCard";
import HistoryTable from "./components/HistoryTable";

export default function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (!selected)
      return;

    if (preview)
      URL.revokeObjectURL(preview);

    const url = URL.createObjectURL(selected);
    setFile(selected);
    setPreview(url);
    setResult(null);
  };

  const fetchHistory = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/logs");
      const data = await res.json();
      setHistory(data);
    } catch (err) {
      console.error("Failed to load history");
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select an image");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      const response = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok)
        throw new Error("Failed to process image");

      const data = await response.json();
      setResult(data);
      await fetchHistory();
    } catch (error) {
      alert(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      {/* Header */}
      <header className="fixed top-4 left-1/2 -translate-x-1/2 z-50 w-[95%] max-w-6xl">
        <div className="backdrop-blur-md bg-white/80 border border-gray-200 rounded-3xl shadow-sm">
          <div className="px-6 py-3 flex items-center justify-between">
            <h1 className="text-lg font-semibold tracking-tight">
              License Plate System
            </h1>
            <span className="text-sm text-gray-600">AI Detection & OCR</span>
          </div>
        </div>
      </header>

      {/* Main */}
      <main className="max-w-6xl mx-auto px-6 pt-32 pb-10 space-y-10">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
          <UploadBox
            preview={preview}
            loading={loading}
            onFileChange={handleFileChange}
            onUpload={handleUpload}
          />

          <ResultCard result={result} />
        </div>

        <HistoryTable history={history} />
      </main>

      {/* Footer */}
      <footer className="text-center text-xs text-gray-400 py-6">
        © {new Date().getFullYear()} License Plate Recognition System
      </footer>
    </div>
  );
}