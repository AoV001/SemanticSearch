import { useEffect, useState } from 'react'
import { getFileHistory } from '../api/client'

export default function HistoryOverlay({ filename, onClose }) {
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getFileHistory(filename)
      .then(data => setHistory(data.history))
      .finally(() => setLoading(false))
  }, [filename])

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center"
      style={{background: 'rgba(0,0,0,0.7)'}}>
      <div className="rounded-2xl shadow-2xl w-full max-w-2xl mx-4 max-h-[80vh] flex flex-col"
        style={{background: '#1a1d27', border: '1px solid #2a2d3a'}}>

        <div className="flex items-center justify-between px-6 py-4"
          style={{borderBottom: '1px solid #2a2d3a'}}>
          <div>
            <h2 className="font-semibold" style={{color: '#e2e8f0'}}>Search History</h2>
            <p className="text-xs mt-0.5" style={{color: '#64748b'}}>{filename}</p>
          </div>
          <button onClick={onClose} className="text-xl transition"
            style={{color: '#64748b'}}>
            ✕
          </button>
        </div>

        <div className="overflow-y-auto px-6 py-4 space-y-3">
          {loading ? (
            <p className="text-sm text-center py-8" style={{color: '#64748b'}}>Loading...</p>
          ) : history.length === 0 ? (
            <p className="text-sm text-center py-8" style={{color: '#64748b'}}>No searches yet for this file</p>
          ) : (
            history.map((item) => (
              <div key={item.id} className="rounded-xl px-4 py-3"
                style={{background: '#222536', border: '1px solid #2a2d3a'}}>
                <p className="text-sm" style={{color: '#64748b'}}>{item.question}</p>
                <p className="text-lg font-bold mt-1" style={{color: '#2dd4bf'}}>{item.answer}</p>
                <p className="text-xs mt-1" style={{color: '#2a2d3a'}}>
                  {Math.round(item.confidence * 100)}% confidence ·{' '}
                  {new Date(item.created_at).toLocaleString()}
                </p>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}