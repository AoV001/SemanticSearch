export default function ResultCard({ result }) {
  const { question, results } = result

  if (!results.length) {
    return (
      <div className="bg-white rounded-xl border border-gray-200 p-5">
        <p className="text-sm font-medium text-gray-600">Q: {question}</p>
        <p className="text-sm text-gray-400 mt-1">No answer found.</p>
      </div>
    )
  }

  const top = results[0]

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5 space-y-3">
      <p className="text-sm font-medium text-gray-500">Q: {question}</p>
      <p className="text-xl font-bold text-blue-700">
        {top.answer}
      </p>
      <p className="text-xs text-gray-400">
        Confidence: {Math.round(top.confidence * 100)}%
      </p>

      {top.evidence.length > 0 && (
        <div>
          <p className="text-xs font-semibold text-gray-500 mb-1">Evidence:</p>
          <ul className="space-y-1">
            {top.evidence.map((e, i) => (
              <li key={i} className="text-xs text-gray-600 bg-gray-50 px-3 py-1 rounded-lg">
                • {e}
              </li>
            ))}
          </ul>
        </div>
      )}

      <details className="text-xs text-gray-400">
        <summary className="cursor-pointer hover:text-gray-600">Context</summary>
        <p className="mt-1 bg-gray-50 p-2 rounded">{top.context}</p>
      </details>
    </div>
  )
}