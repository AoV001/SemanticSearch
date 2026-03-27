export default function ResultCard({ result, onHover }) {
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

      <details>
        <summary className="text-xs cursor-pointer" style={{color: '#64748b'}}>
          Show evidence
        </summary>
        <ul className="mt-2 space-y-1">
          {top.evidence.map((e, i) => (
            <li key={i} className="text-xs px-3 py-1 rounded-lg" style={{color: '#e2e8f0', background: '#1a1d27'}}>
              • {e}
            </li>
          ))}
        </ul>
      </details>

      <details>
        <summary className="text-xs cursor-pointer" style={{color: '#64748b'}}>
          Show context
        </summary>
        <p className="mt-2 text-sm p-3 rounded-lg leading-relaxed" style={{color: '#e2e8f0', background: '#1a1d27'}}>
          {top.context}
        </p>
      </details>
    </div>
  )
}