import { useState } from 'react'

export default function SearchForm({ selectedFile, onSearch, loading }) {
  const [questions, setQuestions] = useState([''])

  const addQuestion = () => setQuestions([...questions, ''])

  const updateQuestion = (index, value) => {
    const updated = [...questions]
    updated[index] = value
    setQuestions(updated)
  }

  const removeQuestion = (index) => {
    setQuestions(questions.filter((_, i) => i !== index))
  }

  const clearAll = () => setQuestions([''])

  const handleSubmit = () => {
    const filtered = questions.filter(q => q.trim())
    if (!filtered.length || !selectedFile) return
    onSearch(filtered)
  }

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-4 space-y-3">
      <div className="flex items-center justify-between">
        <h2 className="text-sm font-semibold text-gray-700">Ask questions</h2>
        {questions.some(q => q.trim()) && (
          <button
            onClick={clearAll}
            className="text-xs text-red-400 hover:text-red-600"
          >
            Clear all
          </button>
        )}
      </div>

      {!selectedFile && (
        <p className="text-xs text-amber-500">Select a file first</p>
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
              className="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-400"
            />
            {questions.length > 1 && (
              <button
                onClick={() => removeQuestion(i)}
                className="text-red-400 hover:text-red-600 px-2"
              >
                ✕
              </button>
            )}
          </div>
        ))}
      </div>

      <div className="flex gap-2">
        <button
          onClick={addQuestion}
          className="text-xs text-blue-500 hover:text-blue-700"
        >
          + Add question
        </button>
        <button
          onClick={handleSubmit}
          disabled={!selectedFile || loading}
          className="ml-auto bg-blue-600 text-white px-4 py-1.5 rounded-lg text-sm hover:bg-blue-700 disabled:opacity-50 transition"
        >
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>
    </div>
  )
}