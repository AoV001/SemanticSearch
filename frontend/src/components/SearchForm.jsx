import { useState } from 'react'

export default function SearchForm({ selectedFile, onSearch, loading }) {
  const [questions, setQuestions] = useState([''])

  const addQuestion = () => setQuestions([...questions, ''])

  const updateQuestion = (index, value) => {
    const updated = [...questions]
    updated[index] = value
    setQuestions(updated)
  }

  const removeQuestion = (index) => setQuestions(questions.filter((_, i) => i !== index))
  const clearAll = () => setQuestions([''])

  const handleSubmit = () => {
    const filtered = questions.filter(q => q.trim())
    if (!filtered.length || !selectedFile) return
    onSearch(filtered)
  }

  return (
    <div className="rounded-xl p-4 space-y-3"
      style={{background: '#222536', border: '1px solid #2a2d3a'}}>

      <div className="flex items-center justify-between">
        <h2 className="text-sm font-semibold" style={{color: '#e2e8f0'}}>Ask questions</h2>
        {questions.some(q => q.trim()) && (
          <button onClick={clearAll} className="text-xs" style={{color: '#f472b6'}}>
            Clear all
          </button>
        )}
      </div>

      {!selectedFile && (
        <p className="text-xs" style={{color: '#f472b6'}}>Select a file first</p>
      )}

      <div className="space-y-2">
        {questions.map((q, i) => (
          <div key={i} className="flex gap-2">
            <input
              type="text"
              value={q}
              onChange={(e) => updateQuestion(i, e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSubmit()}
              placeholder={`Question ${i + 1}`}
              className="flex-1 rounded-lg px-3 py-2 text-sm focus:outline-none"
              style={{background: '#1a1d27', border: '1px solid #2a2d3a', color: '#e2e8f0'}}
            />
            {questions.length > 1 && (
              <button onClick={() => removeQuestion(i)} style={{color: '#f472b6'}}>✕</button>
            )}
          </div>
        ))}
      </div>

      <div className="flex gap-2 items-center">
        <button onClick={addQuestion} className="text-xs" style={{color: '#2dd4bf'}}>
          + Add question
        </button>
        <button
          onClick={handleSubmit}
          disabled={!selectedFile || loading}
          className="ml-auto px-4 py-1.5 rounded-lg text-sm font-medium disabled:opacity-40 transition"
          style={{background: '#2dd4bf', color: '#0f1117'}}
        >
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>
    </div>
  )
}