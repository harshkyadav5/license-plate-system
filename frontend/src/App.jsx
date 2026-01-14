import { useState } from "react";

const dummyHistory = [
  {
    id: 1,
    image_url: "/media/sample1.jpg",
    plate_text: "DL8CAF5031",
    confidence: 0.94,
    created_at: "2025-01-12 14:32",
  },
  {
    id: 2,
    image_url: "/media/sample2.jpg",
    plate_text: "MH12AB1234",
    confidence: 0.89,
    created_at: "2025-01-11 10:18",
  },
];

export default function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history] = useState(dummyHistory);

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (!selected)
      return;

    setFile(selected);
    setPreview(URL.createObjectURL(selected));
    setResult(null);
  };

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
        {/* Upload + Result */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
          <div className="bg-white rounded-2xl shadow-sm p-6">
            <h2 className="text-lg font-medium mb-2">Upload Image</h2>
            <p className="text-sm text-gray-500 mb-4">
              Upload a vehicle image to detect and recognize the license plate.
            </p>

            <label className="flex flex-col items-center justify-center border-2 border-dashed rounded-xl p-6 cursor-pointer hover:border-gray-400 transition">
              <input
                type="file"
                accept="image/*"
                onChange={handleFileChange}
                className="hidden"
              />
              <span className="text-sm text-gray-500">
                Click to upload or drag & drop
              </span>
            </label>

            {preview && (
              <img
                src={preview}
                alt="preview"
                className="w-full h-48 object-contain rounded-lg mt-4 bg-gray-100"
              />
            )}

            <button
              onClick={handleUpload}
              disabled={loading}
              className="mt-4 w-full bg-black text-white py-2.5 rounded-xl hover:opacity-90 disabled:opacity-50 transition"
            >
              {loading ? "Processing..." : "Detect License Plate"}
            </button>
          </div>

          <div className="bg-white rounded-2xl shadow-sm p-6">
            <h2 className="text-lg font-medium mb-2">Result</h2>
            <p className="text-sm text-gray-500 mb-4">
              Recognition output will appear here.
            </p>

            {!result && (
              <div className="text-gray-400 text-sm flex items-center justify-center h-40 border rounded-xl">
                No result yet
              </div>
            )}

            {result && (
              <div className="space-y-3">
                <div className="p-4 rounded-xl bg-gray-100">
                  <p className="text-sm text-gray-500">Detected Plate</p>
                  <p className="text-xl font-semibold tracking-wider">
                    {result.text}
                  </p>
                </div>

                <div className="p-4 rounded-xl bg-gray-100">
                  <p className="text-sm text-gray-500">Confidence</p>
                  <p className="text-lg font-medium">
                    {(result.confidence * 100).toFixed(2)}%
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* History Section */}
        <section className="bg-white rounded-2xl shadow-sm p-6">
          <h2 className="text-lg font-medium mb-4">Detection History</h2>

          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-gray-500 border-b">
                  <th className="py-2">Plate</th>
                  <th>Confidence</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {history.map((item) => (
                  <tr
                    key={item.id}
                    className="border-b last:border-none"
                  >
                    <td className="py-3 font-medium tracking-wider">
                      {item.plate_text}
                    </td>
                    <td>{(item.confidence * 100).toFixed(2)}%</td>
                    <td className="text-gray-500">{item.created_at}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="text-center text-xs text-gray-400 py-6">
        © {new Date().getFullYear()} License Plate Recognition System
      </footer>
    </div>
  );
}