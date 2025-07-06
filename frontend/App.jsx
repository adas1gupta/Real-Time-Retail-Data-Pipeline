import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [sales, setSales] = useState([]);
  useEffect(() => {
    axios.get("http://localhost:8000/sales").then((res) => setSales(res.data));
  }, []);

  return (
    <main className="p-4 text-center">
      <h1 className="text-2xl font-bold mb-4">Top 10 Revenue by Country</h1>
      <table className="mx-auto">
        <thead>
          <tr><th>Country</th><th>Revenue (£)</th></tr>
        </thead>
        <tbody>
          {sales.map((row) => (
            <tr key={row.country}>
              <td>{row.country}</td>
              <td>{Number(row.revenue).toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
export default App;