export default function InsightsPanel({ data }) {
  if (!data) return null;
  const { summary, insights, findings, risk_score, risk_level, action } = data;

  const riskCounts = { critical: 0, high: 0, medium: 0, low: 0 };
  for (const f of findings) {
    if (riskCounts[f.risk] !== undefined) riskCounts[f.risk]++;
  }

  return (
    <div className="panel insights-panel">
      <div className="crosshair-corners"></div>
      <div className="panel-header">
        <span>[ TELEMETRY ]</span>
        <span className="deco">ANALYSIS_COMPLETE</span>
      </div>

      <div className="panel-body">
        <div className="summary-grid">
          <div className={`stat-box risk-${risk_level}`}>
            <div className="stat-val">{risk_score}</div>
            <div className="stat-lbl">THREAT_LVL</div>
          </div>
          <div className={`stat-box risk-${risk_level}`}>
            <div className="stat-val">{risk_level.toUpperCase()}</div>
            <div className="stat-lbl">PROGNOSIS</div>
          </div>
        </div>

        <div className="insight-text">
          {summary.toUpperCase()}
        </div>

        {findings.length > 0 && (
          <div style={{ marginBottom: 20 }}>
            <div className="micro-data" style={{ marginBottom: 8 }}>VULNERABILITY_MATRIX:</div>
            <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
              {Object.entries(riskCounts).map(([level, count]) =>
                count > 0 ? (
                  <span key={level} className={`badge ${level}`}>
                    {level.toUpperCase()}: {String(count).padStart(2, '0')}
                  </span>
                ) : null
              )}
            </div>
          </div>
        )}

        <div className="micro-data" style={{ marginBottom: 8 }}>PROTOCOL_ACTION:</div>
        <div>
          <span className={`action-badge ${action}`}>
            ► {action}
          </span>
        </div>

        <div className="micro-data" style={{ marginBottom: 8 }}>REMEDIATION_LOG:</div>
        <ul className="insight-list">
          {insights.map((insight, idx) => (
            <li key={idx} className="insight-item">
              <span className="insight-icon deco">◂</span>
              {insight.toUpperCase()}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
