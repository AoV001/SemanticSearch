import { useState } from 'react'
import { uploadFile, uploadText } from '../api/client'

export default function FileUpload({ onUploadSuccess }) {
  const [mode, setMode] = useState('file')  // 'file' | 'text'
  const [dragging, setDragging] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [pasteText, setPasteText] = useState('')
  const [pasteName, setPasteName] = useState('')

  const handleFile = async (file) => {
    if (!file) return
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
      <div className="flex rounded-lg border border-gray-200 overflow-hidden text-xs">
        <button
          onClick={() => setMode('file')}
          className={`flex-1 py-1.5 transition ${mode === 'file' ? 'bg-blue-600 text-white' : 'bg-white text-gray-500 hover:bg-gray-50'}`}
        >
          Upload file
        </button>
        <button
          onClick={() => setMode('text')}
          className={`flex-1 py-1.5 transition ${mode === 'text' ? 'bg-blue-600 text-white' : 'bg-white text-gray-500 hover:bg-gray-50'}`}
        >
          Paste text
        </button>
      </div>

      {mode === 'file' ? (
        <div
          onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
          onDragLeave={() => setDragging(false)}
          onDrop={(e) => { e.preventDefault(); setDragging(false); handleFile(e.dataTransfer.files[0]) }}
          className={`border-2 border-dashed rounded-xl p-6 text-center transition-colors
            ${dragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300 bg-white'}`}
        >
          <p className="text-gray-400 text-xs mb-2">Drag & drop or</p>
          <label className="cursor-pointer bg-blue-600 text-white px-3 py-1.5 rounded-lg text-xs hover:bg-blue-700 transition">
            Browse
            <input
              type="file"
              accept=".txt,.pdf"
              className="hidden"
              onChange={(e) => handleFile(e.target.files[0])}
            />
          </label>
        </div>
      ) : (
        <div className="space-y-2">
          <input
            type="text"
            value={pasteName}
            onChange={(e) => setPasteName(e.target.value)}
            placeholder="Filename (e.g. my-text)"
            className="w-full border border-gray-300 rounded-lg px-3 py-1.5 text-xs focus:outline-none focus:border-blue-400"
          />
          <textarea
            value={pasteText}
            onChange={(e) => setPasteText(e.target.value)}
            placeholder="Paste your text here..."
            rows={5}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-xs focus:outline-none focus:border-blue-400 resize-none"
          />
          <button
            onClick={handlePaste}
            disabled={loading}
            className="w-full bg-blue-600 text-white py-1.5 rounded-lg text-xs hover:bg-blue-700 disabled:opacity-50 transition"
          >
            {loading ? 'Saving...' : 'Save & open'}
          </button>
        </div>
      )}

      {error && <p className="text-red-500 text-xs">{error}</p>}
      {loading && mode === 'file' && <p className="text-blue-500 text-xs text-center">Uploading...</p>}
    </div>
  )
}