import { useState } from 'react'
import { uploadFile, uploadText } from '../api/client'

export default function FileUpload({ onUploadSuccess }) {
  const [mode, setMode] = useState('file')
  const [dragging, setDragging] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [pasteText, setPasteText] = useState('')
  const [pasteName, setPasteName] = useState('')

  const MAX_TEXT = 5000
  const MAX_FILE_MB = 5

  const handleFile = async (file) => {
    if (!file) return
    if (file.size > MAX_FILE_MB * 1024 * 1024) {
      return setError(`File too large. Maximum size is ${MAX_FILE_MB}MB`)
  }
    setError(null)
    setLoading(true)
    try {
      const result = await uploadFile(file)
      onUploadSuccess(result)
    } catch (e) {
      setError('Only .txt and .pdf files are allowed.')
    } finally {
      setLoading(false)
    }
  }

  const handlePaste = async () => {
    if (!pasteText.trim()) return setError('Text cannot be empty')
    if (!pasteName.trim()) return setError('Please enter a filename')
    setError(null)
    setLoading(true)
    try {
      const result = await uploadText(pasteName.trim(), pasteText.trim())
      onUploadSuccess(result)
      setPasteText('')
      setPasteName('')
    } catch (e) {
      setError('Could not save text. Try a different filename.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-3">
      {/* Переключатель */}
      <div className="flex rounded-lg overflow-hidden text-xs" style={{border: '1px solid #2a2d3a'}}>
        <button
          onClick={() => setMode('file')}
          className="flex-1 py-1.5 transition"
          style={mode === 'file'
            ? {background: '#2dd4bf', color: '#0f1117'}
            : {background: '#1a1d27', color: '#64748b'}}
        >
          Upload file
        </button>
        <button
          onClick={() => setMode('text')}
          className="flex-1 py-1.5 transition"
          style={mode === 'text'
            ? {background: '#2dd4bf', color: '#0f1117'}
            : {background: '#1a1d27', color: '#64748b'}}
        >
          Paste text
        </button>
      </div>

      {mode === 'file' ? (
        <div
          onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
          onDragLeave={() => setDragging(false)}
          onDrop={(e) => { e.preventDefault(); setDragging(false); handleFile(e.dataTransfer.files[0]) }}
          className="rounded-xl p-6 text-center transition-all"
          style={{
            border: dragging ? '2px dashed #2dd4bf' : '2px dashed #2a2d3a',
            background: dragging ? 'rgba(45,212,191,0.05)' : '#0f1117'
          }}
        >
          <p className="text-xs mb-2" style={{color: '#64748b'}}>Drag & drop or</p>
          <label className="cursor-pointer px-3 py-1.5 rounded-lg text-xs font-medium transition"
            style={{background: '#2dd4bf', color: '#0f1117'}}>
            Browse
            <input type="file" accept=".txt,.pdf" className="hidden"
              onChange={(e) => handleFile(e.target.files[0])} />
          </label>
        </div>
      ) : (
        <div className="space-y-2">
          <input
            type="text"
            value={pasteName}
            onChange={(e) => setPasteName(e.target.value)}
            placeholder="Filename (e.g. my-text)"
            className="w-full rounded-lg px-3 py-1.5 text-xs focus:outline-none"
            style={{background: '#0f1117', border: '1px solid #2a2d3a', color: '#e2e8f0'}}
          />
         <textarea
            value={pasteText}
            onChange={(e) => {
                if (e.target.value.length <= MAX_TEXT) setPasteText(e.target.value)
            }}
            placeholder="Paste your text here..."
            rows={5}
            className="w-full rounded-lg px-3 py-2 text-xs focus:outline-none resize-none"
            style={{background: '#0f1117', border: '1px solid #2a2d3a', color: '#e2e8f0'}}
        />
// Счётчик под textarea:
        <p className="text-xs text-right" style={{color: pasteText.length > MAX_TEXT * 0.9 ? '#f472b6' : '#64748b'}}>
            {pasteText.length}/{MAX_TEXT}
        </p>
          <button
            onClick={handlePaste}
            disabled={loading}
            className="w-full py-1.5 rounded-lg text-xs font-medium disabled:opacity-50 transition"
            style={{background: '#2dd4bf', color: '#0f1117'}}
          >
            {loading ? 'Saving...' : 'Save & open'}
          </button>
        </div>
      )}

      {error && <p className="text-xs" style={{color: '#f472b6'}}>{error}</p>}
      {loading && mode === 'file' && <p className="text-xs text-center" style={{color: '#2dd4bf'}}>Uploading...</p>}
    </div>
  )
}