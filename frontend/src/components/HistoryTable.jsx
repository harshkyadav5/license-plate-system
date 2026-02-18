export default function HistoryTable({ history, onDelete, search, setSearch  }) {
  const filteredHistory = history.filter((item) =>
    item.plate_text.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <section className="bg-white rounded-2xl shadow-sm p-6">
      <h2 className="text-lg font-medium mb-4">Detection History</h2>

      <input
        type="text"
        placeholder="Search plate..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="border rounded-xl px-3 py-2 mb-4 w-full"
      />

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-gray-500 border-b">
              <th className="py-2">Image</th>
              <th>Plate</th>
              <th>Confidence</th>
              <th>Date</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {filteredHistory.map((item, index) => (
              <tr
                key={item.id}
                id={index === 0 ? "latest-row" : ""}
                className={`border-b last:border-none ${
                  index === 0 ? "bg-green-50" : ""
                }`}
              >
                <td className="py-3">
                  <img
                    src={`http://127.0.0.1:8000${item.image_url}`}
                    className="h-12 w-20 object-cover rounded-lg border"
                  />
                </td>

                <td className="font-medium tracking-wider">
                  {item.plate_text}
                </td>

                <td>{(item.confidence * 100).toFixed(2)}%</td>

                <td className="text-gray-500">
                  {new Date(item.created_at).toLocaleString()}
                </td>

                <td>
                  <button
                    onClick={() => onDelete(item.id)}
                    className="text-red-500 text-xs hover:underline"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
