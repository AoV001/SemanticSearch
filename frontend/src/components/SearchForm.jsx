import { useState } from 'react'

export default function SearchForm({ selectedFile, onSearch, loading }) {
  const [input, setInput] = useState('')
  const [collapsed, setCollapsed] = useState(false)

  const parseQuestions = (text) =>
    text.split(/\n|;/).map(q => q.trim()).filter(q => q.length > 0)

  const handleSubmit = () => {
    const questions = parseQuestions(input)
    if (!questions.length || !selectedFile) return
    onSearch(questions)
    setCollapsed(true)
  }

  const questionCount = parseQuestions(input).length

  return (
    <div className="rounded-xl overflow-hidden"
      style={{background: '#222536', border: '1px solid #2a2d3a'}}>

      {/* Header — всегда виден */}
      <div className="flex items-center justify-between px-4 py-3">
        <div className="flex items-center gap-2">
          <h2 className="text-sm font-semibold" style={{color: '#e2e8f0'}}>Ask questions</h2>
          {collapsed && questionCount > 0 && (
            <span className="text-xs px-2 py-0.5 rounded-full"
              style={{background: 'rgba(45,212,191,0.1)', color: '#2dd4bf'}}>
              {questionCount} question{questionCount > 1 ? 's' : ''}
            </span>
          )}
        </div>
        <div className="flex items-center gap-2">
          {!selectedFile && (
            <p className="text-xs" style={{color: '#f472b6'}}>Select a file first</p>
          )}
          <button
            onClick={() => setCollapsed(!collapsed)}
            className="text-xs px-2 py-1 rounded transition"
            style={{color: '#64748b'}}
          >
            {collapsed ? '▼ expand' : '▲ collapse'}
          </button>
        </div>
      </div>

      {/* Тело — сворачивается */}
      {!collapsed && (
        <div className="px-4 pb-4 space-y-3" style={{borderTop: '1px solid #2a2d3a'}}>
          <p className="text-xs pt-3" style={{color: '#64748b'}}>
            One question per line, or separate with semicolons
          </p>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && e.ctrlKey) handleSubmit()
            }}
            placeholder={"Who kicked the ball?\nWhy did the girl run?\nWhat happened after?"}
            rows={4}
            className="w-full rounded-lg px-3 py-2 text-sm focus:outline-none resize-none"
            style={{
              background: '#1a1d27',
              border: '1px solid #2a2d3a',
              color: '#e2e8f0',
            }}
          />
          <div className="flex items-center justify-between">
            {input.trim() && (
              <button onClick={() => setInput('')} className="text-xs" style={{color: '#f472b6'}}>
                Clear
              </button>
            )}
            <button
              onClick={handleSubmit}
              disabled={!selectedFile || loading || !input.trim()}
              className="ml-auto px-4 py-1.5 rounded-lg text-sm font-medium disabled:opacity-40 transition"
              style={{background: '#2dd4bf', color: '#0f1117'}}
            >
              {loading ? 'Searching...' : `Search${questionCount > 1 ? ` (${questionCount})` : ''}`}
            </button>
          </div>
          <p className="text-xs" style={{color: '#2a2d3a'}}>Ctrl+Enter to search</p>
        </div>
      )}

      {/* Быстрый поиск когда свёрнуто */}
      {collapsed && (
        <div className="px-4 pb-3 flex gap-2" style={{borderTop: '1px solid #2a2d3a'}}>
          <button
            onClick={() => { setCollapsed(false) }}
            className="text-xs mt-3" style={{color: '#64748b'}}
          >
            Edit questions
          </button>
          <button
            onClick={handleSubmit}
            disabled={!selectedFile || loading || !input.trim()}
            className="ml-auto mt-3 px-3 py-1 rounded-lg text-xs font-medium disabled:opacity-40"
            style={{background: '#2dd4bf', color: '#0f1117'}}
          >
            {loading ? '...' : 'Re-run'}
          </button>
        </div>
      )}
    </div>
  )
}