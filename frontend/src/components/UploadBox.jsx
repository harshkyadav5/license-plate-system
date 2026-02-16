export default function UploadBox({ preview, loading, onFileChange, onUpload }) {
  return (
    <div className="bg-white rounded-2xl shadow-sm p-6">
      <h2 className="text-lg font-medium mb-2">Upload Image</h2>
      <p className="text-sm text-gray-500 mb-4">
        Upload a vehicle image to detect and recognize the license plate.
      </p>

      <label className="flex flex-col items-center justify-center border-2 border-dashed rounded-xl p-6 cursor-pointer hover:border-gray-400 transition">
        <input
          type="file"
          accept="image/*"
          onChange={onFileChange}
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
        onClick={onUpload}
        disabled={loading}
        className="mt-4 w-full bg-black text-white py-2.5 rounded-xl hover:opacity-90 disabled:opacity-50 transition"
      >
        {loading ? "Processing..." : "Detect License Plate"}
      </button>
    </div>
  );
}
