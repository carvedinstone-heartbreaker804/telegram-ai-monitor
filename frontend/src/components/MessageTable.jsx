function getCategoryClass(category) {
  const normalized = (category || "").toLowerCase();

  if (normalized === "spam") return "badge-spam";
  if (normalized === "important") return "badge-important";
  if (normalized === "question") return "badge-question";
  return "badge-normal";
}

export default function MessageTable({ messages, loading }) {
  if (loading) {
    return <div className="empty-state">Loading messages...</div>;
  }

  if (!messages.length) {
    return <div className="empty-state">No messages found for this filter.</div>;
  }

  return (
    <div className="table-card">
      <table className="message-table">
        <thead>
          <tr>
            <th>Sender</th>
            <th>Message</th>
            <th>Category</th>
            <th>Confidence</th>
            <th>Reason</th>
            <th>Time</th>
          </tr>
        </thead>
        <tbody>
          {messages.map((message) => (
            <tr key={message.id}>
              <td>
                <div className="sender-cell">
                  <div className="sender-avatar">
                    {(message.sender_name || "?").charAt(0).toUpperCase()}
                  </div>
                  <span>{message.sender_name || "Unknown"}</span>
                </div>
              </td>
              <td className="message-text-cell">{message.message_text}</td>
              <td>
                <span className={`category-badge ${getCategoryClass(message.category)}`}>
                  {message.category}
                </span>
              </td>
              <td>
                {typeof message.confidence === "number"
                  ? `${Math.round(message.confidence * 100)}%`
                  : "—"}
              </td>
              <td className="reason-cell">{message.reason || "—"}</td>
              <td>{new Date(message.created_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}