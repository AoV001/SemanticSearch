import { useState } from 'react'
import { getDefinition } from '../api/dictionary'
import WordModal from './WordModal'

/**
 * TextViewer component displays the content of a selected file as interactive text.
 *
 * Props:
 * - text: string — original text of the file
 * - resolvedText: string | null — optionally preprocessed or resolved text for coreference
 * - highlightData: { answer: string, context: string } | null — highlights relevant sentences containing the answer
 * - corefMap: object | null — maps answers to their coreferent words for highlighting
 *
 * Features:
 * - Dynamically adjusts font size based on text length.
 * - Renders all words as clickable spans; clicking fetches a dictionary definition.
 * - Uses WordModal to display definitions asynchronously from dictionary API.
 * - Highlights sentences and words related to a given answer when highlightData is provided.
 * - Coreferent words are highlighted along with the answer.
 * - Supports hover effects for clickable words and visually distinct highlights.
 * - Scrollable, responsive layout with dark-themed styling and proper spacing.
 */

export default function TextViewer({ text, resolvedText, highlightData, corefMap }) {
  const [wordModal, setWordModal] = useState(null)
  const [definition, setDefinition] = useState(null)
  const [defLoading, setDefLoading] = useState(false)

  const handleWordClick = async (word) => {
    const clean = word.replace(/[^a-zA-Z]/g, '')
    if (!clean) return
    setWordModal(clean)
    setDefinition(null)
    setDefLoading(true)
    const def = await getDefinition(clean)
    setDefinition(def)
    setDefLoading(false)
  }

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

  const renderClickable = (str) =>
    str.split(/(\s+)/).map((token, i) => {
      if (/^\s+$/.test(token)) return token
      const clean = token.replace(/[^a-zA-Z]/g, '')
      if (!clean) return token
      return (
        <span key={i}
          onClick={() => handleWordClick(token)}
          className="cursor-pointer rounded transition-colors"
          style={{}}
          onMouseEnter={e => e.currentTarget.style.color = '#2dd4bf'}
          onMouseLeave={e => e.currentTarget.style.color = ''}
        >
          {token}
        </span>
      )
    })

  if (!highlightData) {
    return (
      <>
        <WordModal
          word={wordModal}
          definition={definition}
          loading={defLoading}
          onClose={() => setWordModal(null)}
        />
        <div className={`h-full overflow-y-auto ${fontSize} leading-relaxed whitespace-pre-wrap`}
          style={{color: '#e2e8f0'}}>
          {renderClickable(text)}
        </div>
      </>
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
          <mark key={j}
            onClick={() => handleWordClick(word)}
            className="cursor-pointer"
            style={{background: 'rgba(244, 114, 182, 0.3)', borderRadius: '3px', color: '#e2e8f0'}}>
            {word}
          </mark>
        )
      }
      return (
        <span key={j}
          onClick={() => handleWordClick(word)}
          className="cursor-pointer rounded"
          onMouseEnter={e => e.currentTarget.style.color = '#2dd4bf'}
          onMouseLeave={e => e.currentTarget.style.color = ''}
        >
          {word}
        </span>
      )
    })
  }

  return (
    <>
      <WordModal
        word={wordModal}
        definition={definition}
        loading={defLoading}
        onClose={() => setWordModal(null)}
      />
      <div className={`h-full overflow-y-auto ${fontSize} leading-relaxed whitespace-pre-wrap`}
        style={{color: '#e2e8f0'}}>
        {origSents.map((sent, i) => (
          matchedIndices.includes(i)
            ? <span key={i} style={{background: 'rgba(45, 212, 191, 0.15)', borderRadius: '4px'}}>
                {highlightWords(sent)}{' '}
              </span>
            : <span key={i}>{renderClickable(sent)} </span>
        ))}
      </div>
    </>
  )
}