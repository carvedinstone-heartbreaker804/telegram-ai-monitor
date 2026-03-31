export default function FilterBar({ activeFilter, setFilter }) {
  const filters = ["All", "Spam", "Important", "Question", "Normal"];

  return (
    <div className="filter-bar">
      {filters.map((filter) => (
        <button
          key={filter}
          className={`filter-chip ${activeFilter === filter ? "active" : ""}`}
          onClick={() => setFilter(filter)}
        >
          {filter}
        </button>
      ))}
    </div>
  );
}