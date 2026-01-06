import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { User, MessageSquare, Search, Activity, FileText, Copy, Check, ChevronLeft, ChevronRight } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

// Bypass ngrok browser warning
axios.defaults.headers.common['ngrok-skip-browser-warning'] = 'true';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

function App() {
  const [patients, setPatients] = useState([]);
  const [selectedBcNo, setSelectedBcNo] = useState(null);
  const [summary, setSummary] = useState('');
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [copied, setCopied] = useState(false);
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);

  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      axios.get(`${API_BASE}/patients?search=${searchTerm}`)
        .then(res => setPatients(res.data))
        .catch(err => console.error(err));
    }, 500);

    return () => clearTimeout(delayDebounceFn);
  }, [searchTerm]);

  const handlePatientSelect = (bcno) => {
    setSelectedBcNo(bcno);
    setSummary('Generating summary...');
    setAnswer('');
    axios.get(`${API_BASE}/summary/${bcno}`)
      .then(res => setSummary(res.data.summary))
      .catch(err => setSummary('Error generating summary or patient data missing.'));
  };

  const handleAsk = () => {
    if (!question || !selectedBcNo) return;
    setLoading(true);
    axios.post(`${API_BASE}/ask`, { bcno: selectedBcNo, question })
      .then(res => {
        setAnswer(res.data.answer);
        setLoading(false);
      })
      .catch(err => {
        setAnswer('Error getting answer.');
        setLoading(false);
      });
  };

  const filteredPatients = patients;

  const handleCopy = () => {
    if (!summary || summary === 'Generating summary...') return;
    navigator.clipboard.writeText(summary);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div style={{ display: 'flex', width: '100%', height: '100vh', overflow: 'hidden' }}>
      {/* Sidebar */}
      <div className={`sidebar ${isSidebarCollapsed ? 'collapsed' : ''}`}>
        <div style={{ padding: '20px', borderBottom: '1px solid var(--glass-border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          {!isSidebarCollapsed && <h2 style={{ fontSize: '1.2rem', margin: 0 }}>BrCa AI Portal</h2>}
          <button
            onClick={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
            className="collapse-toggle"
            title={isSidebarCollapsed ? "Expand Sidebar" : "Collapse Sidebar"}
          >
            {isSidebarCollapsed ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
          </button>
        </div>
        {!isSidebarCollapsed && (
          <>
            <div style={{ padding: '16px' }}>
              <div style={{ position: 'relative' }}>
                <Search size={18} style={{ position: 'absolute', left: '10px', top: '10px', color: 'var(--text-secondary)' }} />
                <input
                  type="text"
                  placeholder="Search patients..."
                  className="chat-input"
                  style={{ paddingLeft: '36px' }}
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
            </div>
            <div style={{ flex: 1, overflowY: 'auto' }}>
              {filteredPatients.map(p => (
                <div
                  key={p.BCNo}
                  className={`patient-list-item ${selectedBcNo === p.BCNo ? 'selected' : ''}`}
                  onClick={() => handlePatientSelect(p.BCNo)}
                >
                  <div style={{ fontWeight: 600 }}>{p.PatientName}</div>
                  <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>ID: {p.BCNo} • Age: {p.Age}</div>
                </div>
              ))}
            </div>
          </>
        )}
      </div>

      {/* Main Content */}
      <div className="main-content">
        <AnimatePresence mode='wait'>
          {selectedBcNo ? (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              key={selectedBcNo}
              style={{ width: '100%' }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                <div>
                  <h1 style={{ margin: 0 }}>{patients.find(p => p.BCNo === selectedBcNo)?.PatientName}</h1>
                  <p style={{ color: 'var(--text-secondary)' }}>Case Analysis & Q&A</p>
                </div>
                <div style={{ display: 'flex', gap: '12px' }}>
                  <div className="glass-card" style={{ padding: '8px 16px', margin: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <Activity size={16} color="var(--accent-color)" />
                    <span>Stage: {patients.find(p => p.BCNo === selectedBcNo)?.Stage || 'N/A'}</span>
                  </div>
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1fr) minmax(0, 1fr)', gap: '24px' }}>
                {/* AI Summary */}
                <div className="glass-card">
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <FileText size={20} color="var(--accent-color)" />
                      <h3 style={{ margin: 0 }}>AI Case Summary</h3>
                    </div>
                    {summary && summary !== 'Generating summary...' && (
                      <button
                        className="copy-btn"
                        onClick={handleCopy}
                        title="Copy to clipboard"
                      >
                        {copied ? <Check size={16} color="#4caf50" /> : <Copy size={16} />}
                        <span style={{ fontSize: '0.8rem', marginLeft: '4px' }}>{copied ? 'Copied' : 'Copy'}</span>
                      </button>
                    )}
                  </div>
                  <div className="markdown-content">
                    <ReactMarkdown>{summary}</ReactMarkdown>
                  </div>
                </div>

                {/* AI Q&A */}
                <div className="glass-card">
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
                    <MessageSquare size={20} color="var(--accent-color)" />
                    <h3 style={{ margin: 0 }}>Ask Patient Data</h3>
                  </div>
                  <div style={{ marginBottom: '16px' }}>
                    <input
                      type="text"
                      placeholder="e.g., What was the tumor size?"
                      className="chat-input"
                      value={question}
                      onChange={(e) => setQuestion(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && handleAsk()}
                    />
                  </div>
                  <button className="btn-primary" onClick={handleAsk} disabled={loading}>
                    {loading ? 'Thinking...' : 'Analyze'}
                  </button>
                  {answer && (
                    <motion.div
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      style={{ marginTop: '20px', padding: '16px', background: 'rgba(124, 77, 255, 0.05)', borderRadius: '8px', borderLeft: '3px solid var(--accent-color)' }}
                    >
                      <div style={{ fontWeight: 600, marginBottom: '8px' }}>AI Answer:</div>
                      <div style={{ color: 'var(--text-secondary)', lineHeight: '1.5' }}>
                        <ReactMarkdown>{answer}</ReactMarkdown>
                      </div>
                    </motion.div>
                  )}
                </div>
              </div>
            </motion.div>
          ) : (
            <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-secondary)' }}>
              <div style={{ textAlign: 'center' }}>
                <User size={48} style={{ marginBottom: '16px', opacity: 0.3 }} />
                <p>Select a patient to see AI-powered summaries and ask questions.</p>
              </div>
            </div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

export default App;
