export default function TextViewer({ text, highlightAnswer }) {
  if (!text) {
    return (
      <div className="h-full flex items-center justify-center text-gray-300 text-sm">
        Select a file to view text
      </div>
    )
  }

  const normalize = (str) => str.replace(/\s+/g, ' ').trim()
  const normalizedText = normalize(text)

  if (!highlightAnswer) {
    return (
      <div className="h-full overflow-y-auto text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">
        {text}
      </div>
    )
  }

  // Разбиваем на предложения и ищем то которое содержит answer
  const sentences = normalizedText.split(/(?<=[.!?])\s+/)
  const targetSent = sentences.find(s =>
    s.toLowerCase().includes(highlightAnswer.toLowerCase())
  )

  if (!targetSent) {
    return (
      <div className="h-full overflow-y-auto text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">
        {text}
      </div>
    )
  }

  const idx = normalizedText.indexOf(targetSent)
  const before = normalizedText.slice(0, idx)
  const after = normalizedText.slice(idx + targetSent.length)

  return (
    <div className="h-full overflow-y-auto text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">
      {before}
      <mark className="bg-yellow-200 rounded px-0.5">{targetSent}</mark>
      {after}
    </div>
  )
}