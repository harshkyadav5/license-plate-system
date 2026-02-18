export default function ResultCard({ result }) {
  return (
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

          <button
            onClick={() => navigator.clipboard.writeText(result.text)}
            className="mt-2 text-sm text-blue-600 hover:underline"
          >
            Copy plate number
          </button>
        </div>
      )}
    </div>
  );
}
