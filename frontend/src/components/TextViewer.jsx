export default function TextViewer({ text, highlightContext }) {
  if (!text) {
    return (
      <div className="h-full flex items-center justify-center text-gray-300 text-sm">
        Select a file to view text
      </div>
    )
  }

  if (!highlightContext) {
    return (
      <div className="h-full overflow-y-auto text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">
        {text}
      </div>
    )
  }


  const idx = text.indexOf(highlightContext)
  if (idx === -1) {
    return (
      <div className="h-full overflow-y-auto text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">
        {text}
      </div>
    )
  }

  const before = text.slice(0, idx)
  const match = text.slice(idx, idx + highlightContext.length)
  const after = text.slice(idx + highlightContext.length)

  return (
    <div className="h-full overflow-y-auto text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">
      {before}
      <mark className="bg-yellow-200 rounded px-0.5">{match}</mark>
      {after}
    </div>
  )
}