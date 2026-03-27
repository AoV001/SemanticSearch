import { useState } from 'react'
import ResultModal from './ResultModal'

export default function ResultCard({ result, onHover }) {
  const [modalOpen, setModalOpen] = useState(false)
  const { question, results } = result

  if (!results.length) {
    return (
      <div className="rounded-xl p-5" style={{background: '#222536', border: '1px solid #2a2d3a'}}>
        <p className="text-sm" style={{color: '#64748b'}}>Q: {question}</p>
        <p className="text-sm mt-1" style={{color: '#64748b'}}>No answer found.</p>
      </div>
    )
  }

  const top = results[0]

  return (
    <>
      {modalOpen && <ResultModal result={result} onClose={() => setModalOpen(false)} />}

      <div
        className="rounded-xl p-5 space-y-3 cursor-default transition"
        style={{background: '#222536', border: '1px solid #2a2d3a'}}
        onMouseEnter={() => onHover({ answer: top.answer, context: top.context })}
        onMouseLeave={() => onHover(null)}
      >
        <p className="text-xs" style={{color: '#64748b'}}>Q: {question}</p>
        <p className="text-2xl font-bold" style={{color: '#2dd4bf'}}>{top.answer}</p>
        <p className="text-xs" style={{color: '#64748b'}}>
          Confidence: {Math.round(top.confidence * 100)}%
        </p>

        <button
          onClick={() => setModalOpen(true)}
          className="text-xs px-3 py-1 rounded-lg transition"
          style={{border: '1px solid #2a2d3a', color: '#64748b'}}
          onMouseEnter={e => e.currentTarget.style.color = '#2dd4bf'}
          onMouseLeave={e => e.currentTarget.style.color = '#64748b'}
        >
          View details →
        </button>
      </div>
    </>
  )
}