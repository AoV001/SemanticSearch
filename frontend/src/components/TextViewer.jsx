export default function TextViewer({ text, resolvedText, highlightData, corefMap }) {
  if (!text) {
    return (
      <div className="h-full flex items-center justify-center text-sm" style={{color: '#64748b'}}>
        Select a file to view text
      </div>
    )
  }

  const normalize = (str) => str.replace(/\s+/g, ' ').trim()

  const getFontSize = (t) => {
    const words = t.trim().split(/\s+/).length
    if (words < 50) return 'text-2xl'
    if (words < 150) return 'text-lg'
    if (words < 400) return 'text-base'
    if (words < 800) return 'text-sm'
    return 'text-xs'
  }

  const fontSize = getFontSize(text)

  if (!highlightData) {
    return (
      <div className={`h-full overflow-y-auto ${fontSize} leading-relaxed whitespace-pre-wrap`}
        style={{color: '#e2e8f0'}}>
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
      <div className={`h-full overflow-y-auto ${fontSize} leading-relaxed whitespace-pre-wrap`}
        style={{color: '#e2e8f0'}}>
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
        return (
          <mark key={j} style={{
            background: 'rgba(244, 114, 182, 0.3)',
            borderRadius: '3px',
            color: '#e2e8f0'
          }}>
            {word}
          </mark>
        )
      }
      return word
    })
  }

  return (
    <div className={`h-full overflow-y-auto ${fontSize} leading-relaxed whitespace-pre-wrap`}
      style={{color: '#e2e8f0'}}>
      {origSents.map((sent, i) => (
        matchedIndices.includes(i)
          ? <span key={i} style={{background: 'rgba(45, 212, 191, 0.15)', borderRadius: '4px'}}>
              {highlightWords(sent)}{' '}
            </span>
          : <span key={i}>{sent} </span>
      ))}
    </div>
  )
}