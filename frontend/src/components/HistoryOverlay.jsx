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
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl mx-4 max-h-[80vh] flex flex-col">
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-100">
          <div>
            <h2 className="font-semibold text-gray-800">Search History</h2>
            <p className="text-xs text-gray-400 mt-0.5">{filename}</p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 text-xl"
          >
            ✕
          </button>
        </div>

        <div className="overflow-y-auto px-6 py-4 space-y-3">
          {loading ? (
            <p className="text-sm text-gray-400 text-center py-8">Loading...</p>
          ) : history.length === 0 ? (
            <p className="text-sm text-gray-400 text-center py-8">No searches yet for this file</p>
          ) : (
            history.map((item) => (
              <div key={item.id} className="border border-gray-100 rounded-xl px-4 py-3">
                <p className="text-sm text-gray-500">{item.question}</p>
                <p className="text-lg font-bold text-blue-600 mt-1">{item.answer}</p>
                <p className="text-xs text-gray-300 mt-1">
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