export default function TextViewer({ text, resolvedText, highlightContext }) {
  if (!text) {
    return (
      <div className="h-full flex items-center justify-center text-gray-300 text-sm">
        Select a file to view text
      </div>
    )
  }

  const normalize = (str) => str.replace(/\s+/g, ' ').trim()
  const searchBase = resolvedText || text
  const normalizedBase = normalize(searchBase)
  const normalizedContext = highlightContext ? normalize(highlightContext) : null
  const idx = normalizedContext ? normalizedBase.indexOf(normalizedContext) : -1

  if (!normalizedContext || idx === -1) {
    return (
      <div className="h-full overflow-y-auto text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">
        {text}
      </div>
    )
  }

  // Находим примерную позицию в оригинальном тексте по соотношению
  const ratio = idx / normalizedBase.length
  const normalizedOrig = normalize(text)
  const approxIdx = Math.floor(ratio * normalizedOrig.length)

  // Ищем ближайшее совпадение первых слов контекста
  const firstWords = normalizedContext.split(' ').slice(0, 4).join(' ')
  const origIdx = normalizedOrig.indexOf(firstWords)

  if (origIdx === -1) {
    return (
      <div className="h-full overflow-y-auto text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">
        {text}
      </div>
    )
  }

  // Находим конец подсветки по количеству слов
  const contextWordCount = normalizedContext.split(' ').length
  const origWords = normalizedOrig.split(' ')
  const startWordIdx = normalizedOrig.slice(0, origIdx).split(' ').length
  const endWordIdx = startWordIdx + contextWordCount
  const endIdx = origWords.slice(0, endWordIdx).join(' ').length

  const before = text.slice(0, origIdx)
  const match = text.slice(origIdx, origIdx + (endIdx - origIdx))
  const after = text.slice(origIdx + (endIdx - origIdx))

  return (
    <div className="h-full overflow-y-auto text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">
      {before}
      <mark className="bg-yellow-200 rounded px-0.5">{match}</mark>
      {after}
    </div>
  )
}