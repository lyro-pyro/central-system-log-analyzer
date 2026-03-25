import { useState } from 'react';

export default function IocPanel({ iocs }) {
  const [copied, setCopied] = useState(false);

  if (!iocs || Object.values(iocs).every((arr) => arr.length === 0)) {
    return null;
  }

  const handleCopy = () => {
    navigator.clipboard.writeText(JSON.stringify(iocs, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getTotal = () => {
    return Object.values(iocs).reduce((acc, arr) => acc + arr.length, 0);
  };

  return (
    <div className="panel insights-panel" style={{ marginTop: '24px', borderColor: 'var(--critical-red)' }}>
      <div className="crosshair-corners" style={{ borderColor: 'var(--critical-red)' }}></div>
      <div className="panel-header" style={{ borderBottomColor: 'rgba(255,51,51,0.3)' }}>
        <span style={{ color: 'var(--critical-red)' }}>[ THREAT_INTEL // IOC_REGISTRY ]</span>
        <span className="deco" style={{ color: 'var(--critical-red)' }}>COMPROMISE_INDICATORS</span>
      </div>

      <div className="panel-body">
        <div className="micro-data" style={{ marginBottom: 12 }}>TOTAL EXTRACTED IOCs: {getTotal()}</div>
        
        {iocs.ips?.length > 0 && (
          <div style={{ marginBottom: '16px' }}>
            <div className="micro-data" style={{ color: 'var(--text-secondary)' }}>MALICIOUS_IP_ADDRESSES</div>
            <div className="ioc-list">
              {iocs.ips.map((ip, i) => (
                <div key={i} className="ioc-item ip">{ip}</div>
              ))}
            </div>
          </div>
        )}

        {iocs.tokens?.length > 0 && (
          <div style={{ marginBottom: '16px' }}>
            <div className="micro-data" style={{ color: 'var(--text-secondary)' }}>EXPOSED_CREDENTIALS / TOKENS</div>
            <div className="ioc-list">
              {iocs.tokens.map((token, i) => (
                <div key={i} className="ioc-item token" style={{ fontFamily: 'monospace', fontSize: '0.8rem', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {token}
                </div>
              ))}
            </div>
          </div>
        )}

        {iocs.emails?.length > 0 && (
          <div style={{ marginBottom: '16px' }}>
            <div className="micro-data" style={{ color: 'var(--text-secondary)' }}>COMPROMISED_IDENTITIES</div>
            <div className="ioc-list">
              {iocs.emails.map((email, i) => (
                <div key={i} className="ioc-item email">{email}</div>
              ))}
            </div>
          </div>
        )}

        <button 
          onClick={handleCopy}
          className="analyze-btn" 
          style={{ width: '100%', height: '40px', marginTop: '12px', background: 'var(--accent-orange)', color: '#000', fontWeight: 'bold' }}
        >
          {copied ? '✓ IOCs COPIED DIRECT TO CLIPBOARD' : '📋 COPY IOCs FOR SIEM / FIREWALL EXPORT'}
        </button>
      </div>
    </div>
  );
}
