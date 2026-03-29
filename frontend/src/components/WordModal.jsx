/**
 * WordModal component displays the dictionary definition of a selected word in a modal overlay.
 *
 * Props:
 * - word: string | null — the word to display
 * - definition: object | null — the dictionary definition object retrieved from the API
 * - loading: boolean — true while the definition is being fetched
 * - onClose: function — callback to close the modal
 *
 * Features:
 * - Dark-themed modal with rounded corners and scrollable content.
 * - Header displays the word with a close button.
 * - Shows a loading message while fetching definitions.
 * - Renders up to 3 definitions per meaning, including part of speech and example sentences.
 * - Clicking outside the modal closes it.
 */

export default function WordModal({ word, definition, loading, onClose }) {
  if (!word) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4"
      style={{background: 'rgba(0,0,0,0.7)'}}
      onClick={onClose}>
      <div className="rounded-2xl w-full max-w-md max-h-[70vh] flex flex-col overflow-hidden"
        style={{background: '#1a1d27', border: '1px solid #2a2d3a'}}
        onClick={e => e.stopPropagation()}>

        {/* Header */}
        <div className="flex items-center justify-between px-5 py-4 shrink-0"
          style={{borderBottom: '1px solid #2a2d3a'}}>
          <div>
            <p className="text-xl font-bold" style={{color: '#2dd4bf'}}>{word}</p>
          </div>
          <button onClick={onClose} style={{color: '#64748b'}}>✕</button>
        </div>

        <div className="overflow-y-auto px-5 py-4 space-y-4">
          {loading ? (
            <p className="text-sm text-center py-4" style={{color: '#64748b'}}>Looking up...</p>
          ) : !definition ? (
            <p className="text-sm text-center py-4" style={{color: '#64748b'}}>
              No definition found for "{word}"
            </p>
          ) : (
            definition.meanings?.map((meaning, i) => (
              <div key={i}>
                <p className="text-xs font-semibold uppercase tracking-wide mb-2"
                  style={{color: '#f472b6'}}>
                  {meaning.partOfSpeech}
                </p>
                <ul className="space-y-2">
                  {meaning.definitions?.slice(0, 3).map((def, j) => (
                    <li key={j} className="text-sm leading-relaxed"
                      style={{color: '#e2e8f0'}}>
                      {j + 1}. {def.definition}
                      {def.example && (
                        <p className="text-xs mt-1 italic" style={{color: '#64748b'}}>
                          "{def.example}"
                        </p>
                      )}
                    </li>
                  ))}
                </ul>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}