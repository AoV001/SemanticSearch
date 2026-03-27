export default function TextViewer({ text, resolvedText, highlightData }) {
  if (!text) {
    return (
      <div className="h-full flex items-center justify-center text-gray-300 text-sm">
        Select a file to view text
      </div>
    )
  }

  const normalize = (str) => str.replace(/\s+/g, ' ').trim()

  if (!highlightData) {
    return (
      <div className="h-full overflow-y-auto text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">
        {text}
      </div>
    )
  }

  const { answer, context } = highlightData
  const base = resolvedText || text

  const origSents = normalize(text).split(/(?<=[.!?])\s+/)
  const resolvedSents = normalize(base).split(/(?<=[.!?])\s+/)
  const normalizedContext = normalize(context)

  const matchedIndices = resolvedSents.reduce((acc, sent, i) => {
    if (normalizedContext.includes(normalize(sent))) acc.push(i)
    return acc
  }, [])

  if (!matchedIndices.length) {
    return (
      <div className="h-full overflow-y-auto text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">
        {text}
      </div>
    )
  }

  return (
    <div className="h-full overflow-y-auto text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">
      {origSents.map((sent, i) => (
        matchedIndices.includes(i)
          ? <mark key={i} className="bg-yellow-200 rounded px-0.5">{sent} </mark>
          : <span key={i}>{sent} </span>
      ))}
    </div>
  )
}