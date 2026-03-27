export default function ResultCard({ result, onHover }) {
  const { question, results } = result

  if (!results.length) {
    return (
      <div className="bg-white rounded-xl border border-gray-200 p-5">
        <p className="text-sm text-gray-500">Q: {question}</p>
        <p className="text-sm text-gray-400 mt-1">No answer found.</p>
      </div>
    )
  }

  const top = results[0]

  return (
    <div
      className="bg-white rounded-xl border border-gray-200 p-5 space-y-3 cursor-default"
      onMouseEnter={() => onHover({ answer: top.answer, context: top.context })}
      onMouseLeave={() => onHover(null)}
    >
      <p className="text-sm text-gray-500">Q: {question}</p>
      <p className="text-2xl font-bold text-blue-700">{top.answer}</p>
      <p className="text-xs text-gray-400">
        Confidence: {Math.round(top.confidence * 100)}%
      </p>

      <details>
        <summary className="text-xs text-gray-400 cursor-pointer hover:text-gray-600">
          Show evidence
        </summary>
        <ul className="mt-2 space-y-1">
          {top.evidence.map((e, i) => (
            <li key={i} className="text-xs text-gray-600 bg-gray-50 px-3 py-1 rounded-lg">
              • {e}
            </li>
          ))}
        </ul>
      </details>

      <details>
        <summary className="text-xs text-gray-400 cursor-pointer hover:text-gray-600">
          Show context
        </summary>
        <p className="mt-2 text-sm text-gray-600 bg-gray-50 p-3 rounded-lg leading-relaxed">
          {top.context}
        </p>
      </details>
    </div>
  )
}