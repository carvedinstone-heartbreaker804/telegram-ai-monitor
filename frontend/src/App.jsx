import { useEffect, useState } from "react";
import API from "./api/client";
import StatsCards from "./components/StatsCards";
import FilterBar from "./components/FilterBar";
import MessageTable from "./components/MessageTable";

function App() {
  const [messages, setMessages] = useState([]);
  const [stats, setStats] = useState(null);
  const [filter, setFilter] = useState("All");
  const [loading, setLoading] = useState(false);

  const fetchMessages = async () => {
    try {
      setLoading(true);
      const res = await API.get("/messages", {
        params: {
          category: filter === "All" ? undefined : filter,
        },
      });
      setMessages(res.data);
    } catch (error) {
      console.error("Failed to fetch messages:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const res = await API.get("/stats");
      setStats(res.data);
    } catch (error) {
      console.error("Failed to fetch stats:", error);
    }
  };

  useEffect(() => {
    fetchMessages();
    fetchStats();
  }, [filter]);

  return (
    <div className="app-shell">
      <div className="dashboard-container">
        <div className="page-header">
          <div>
            <p className="eyebrow">AI Moderation Dashboard</p>
            <h1>Telegram AI Monitor</h1>
            <p className="subtitle">
              Track incoming Telegram messages, classify them with AI, and
              surface important signals.
            </p>
          </div>

          <button className="refresh-btn" onClick={fetchMessages}>
            Refresh
          </button>
        </div>

        <StatsCards stats={stats} />
        <FilterBar activeFilter={filter} setFilter={setFilter} />

        <div className="table-section">
          <div className="section-header">
            <div>
              <h2>Recent Messages</h2>
              <p>{loading ? "Loading messages..." : `${messages.length} messages shown`}</p>
            </div>
          </div>

          <MessageTable messages={messages} loading={loading} />
        </div>
      </div>
    </div>
  );
}

export default App;