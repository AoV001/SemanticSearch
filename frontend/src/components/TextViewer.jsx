export default function TextViewer({ text, resolvedText, highlightData, corefMap }) {
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
  const normalizedAnswer = normalize(answer).toLowerCase()

  const matchedIndices = resolvedSents.reduce((acc, sent, i) => {
    const sentInContext = normalizedContext.includes(normalize(sent))
    const resolvedHasAnswer = normalize(sent).toLowerCase().includes(normalizedAnswer)
    const origHasAnswer = normalize(origSents[i] || '').toLowerCase().includes(normalizedAnswer)
    if (sentInContext && (resolvedHasAnswer || origHasAnswer)) acc.push(i)
    return acc
  }, [])

  if (!matchedIndices.length) {
    return (
      <div className="h-full overflow-y-auto text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">
        {text}
      </div>
    )
  }

  const answerLower = answer.toLowerCase()
  const relatedWords = new Set([
    answerLower,
    ...(corefMap?.[answer] || []),
    ...(corefMap?.[answerLower] || [])
  ])

  const highlightWords = (sent) => {
    const parts = sent.split(/(\s+|(?=[.,!?;:])|(?<=[.,!?;:]))/)
    return parts.map((word, j) => {
      const wordLower = word.toLowerCase().replace(/[.,!?;:]/g, '')
      if (wordLower && relatedWords.has(wordLower)) {
        return <mark key={j} className="bg-blue-300 rounded px-0.5 font-medium">{word}</mark>
      }
      return word
    })
  }

  const getFontSize = (text) => {
  const words = text.trim().split(/\s+/).length
  if (words < 50) return 'text-2xl'
  if (words < 150) return 'text-lg'
  if (words < 400) return 'text-base'
  if (words < 800) return 'text-sm'
  return 'text-xs'
}
  const fontSize = getFontSize(text)

  return (
    <div className={`h-full overflow-y-auto ${fontSize} text-gray-700 leading-relaxed whitespace-pre-wrap`}>
      {origSents.map((sent, i) => (
        matchedIndices.includes(i)
          ? <span key={i} className="bg-yellow-100 rounded">
              {highlightWords(sent)}{' '}
            </span>
          : <span key={i}>{sent} </span>
      ))}
    </div>
  )
}