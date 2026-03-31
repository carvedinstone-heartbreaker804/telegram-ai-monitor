const statLabels = {
  total: "Total Messages",
  spam: "Spam",
  important: "Important",
  question: "Questions",
  normal: "Normal",
};

export default function StatsCards({ stats }) {
  if (!stats) {
    return (
      <div className="stats-grid">
        {[1, 2, 3, 4, 5].map((item) => (
          <div key={item} className="stat-card skeleton-card" />
        ))}
      </div>
    );
  }

  return (
    <div className="stats-grid">
      {Object.entries(statLabels).map(([key, label]) => (
        <div key={key} className={`stat-card stat-${key}`}>
          <span className="stat-label">{label}</span>
          <div className="stat-value">{stats[key] ?? 0}</div>
        </div>
      ))}
    </div>
  );
}