export default function LogViewer({ content, findings }) {
  if (!content) return null;

  const lines = content.split('\n');
  const findingsMap = {};
  for (const f of findings) {
    if (!findingsMap[f.line]) findingsMap[f.line] = [];
    findingsMap[f.line].push(f);
  }

  const getLineClass = (lineFindings) => {
    if (!lineFindings) return 'log-line';
    const risks = lineFindings.map((f) => f.risk);
    if (risks.includes('critical')) return 'log-line flagged-critical';
    if (risks.includes('high')) return 'log-line flagged';
    if (risks.includes('medium')) return 'log-line flagged-medium';
    return 'log-line flagged-low';
  };

  return (
    <div className="log-viewer-wrapper">
      <div className="crosshair-corners"></div>
      <div className="log-scroll-area">
        {lines.map((line, idx) => {
          const lineNum = idx + 1;
          const lineFindings = findingsMap[lineNum];
          return (
            <div key={idx} className={getLineClass(lineFindings)}>
              <span className="line-number">{String(lineNum).padStart(4, '0')}</span>
              <span className="line-content">{line || ' '}</span>
              <div className="line-badges">
                {lineFindings &&
                  lineFindings.map((f, i) => (
                    <span key={i} className={`line-badge badge ${f.risk}`}>
                      [{f.type}]
                    </span>
                  ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
