export default function HistoryTable({ history }) {
  return (
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
              <tr key={item.id} className="border-b last:border-none">
                <td className="py-3 font-medium tracking-wider">
                  {item.actual_plate || item.predicted_plate}
                </td>
                <td>{(item.confidence * 100).toFixed(2)}%</td>
                <td className="text-gray-500">
                  {new Date(item.entry_time).toLocaleString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
