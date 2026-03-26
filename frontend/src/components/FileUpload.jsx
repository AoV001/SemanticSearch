import { useState } from 'react'
import { uploadFile } from '../api/client'

export default function FileUpload({ onUploadSuccess }) {
  const [dragging, setDragging] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleFile = async (file) => {
    if (!file) return
    setError(null)
    setLoading(true)
    try {
      const result = await uploadFile(file)
      onUploadSuccess(result)
    } catch (e) {
      setError('Upload failed. Only .txt and .pdf files are allowed.')
    } finally {
      setLoading(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDragging(false)
    handleFile(e.dataTransfer.files[0])
  }

  return (
    <div
      onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
      onDragLeave={() => setDragging(false)}
      onDrop={handleDrop}
      className={`border-2 border-dashed rounded-xl p-8 text-center transition-colors
        ${dragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300 bg-white'}`}
    >
      <p className="text-gray-500 mb-3">Drag & drop a file here, or</p>
      <label className="cursor-pointer bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition">
        Browse file
        <input
          type="file"
          accept=".txt,.pdf"
          className="hidden"
          onChange={(e) => handleFile(e.target.files[0])}
        />
      </label>
      {loading && <p className="mt-3 text-blue-500 text-sm">Uploading...</p>}
      {error && <p className="mt-3 text-red-500 text-sm">{error}</p>}
    </div>
  )
}