import { useState, useEffect } from 'react'
import { deleteFile, getFileHistory } from '../api/client'

export default function FileList({ files, selectedFile, onSelect, onDelete }) {
  const [expanded, setExpanded] = useState(null)
  const [histories, setHistories] = useState({})
  const [confirmDelete, setConfirmDelete] = useState(null)

  useEffect(() => {
    if (expanded) {
      getFileHistory(expanded).then(data =>
        setHistories(prev => ({ ...prev, [expanded]: data.history }))
      )
    }
  }, [expanded])

  const handleExpand = (filename) => {
    setExpanded(expanded === filename ? null : filename)
  }

  const handleDeleteClick = (filename, e) => {
    e.stopPropagation()
    setConfirmDelete(filename)
  }

  const handleConfirmDelete = async () => {
    try {
      await deleteFile(confirmDelete)
      onDelete(confirmDelete)
      if (expanded === confirmDelete) setExpanded(null)
    } catch (e) {
      console.error(e)
    } finally {
      setConfirmDelete(null)
    }
  }

  if (files.length === 0) {
    return <p className="text-gray-400 text-sm text-center py-4">No files uploaded yet</p>
  }

  return (
    <div className="space-y-2">
      {/* Диалог подтверждения удаления */}
      {confirmDelete && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-6 shadow-xl max-w-sm w-full mx-4">
            <h3 className="font-semibold text-gray-800 mb-2">Delete file?</h3>
            <p className="text-sm text-gray-500 mb-1">
              <span className="font-medium text-gray-700">{confirmDelete}</span>
            </p>
            <p className="text-sm text-red-500 mb-5">
              This will permanently delete the file and its search history.
            </p>
            <div className="flex gap-3 justify-end">
              <button
                onClick={() => setConfirmDelete(null)}
                className="px-4 py-2 text-sm rounded-lg border border-gray-300 hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                onClick={handleConfirmDelete}
                className="px-4 py-2 text-sm rounded-lg bg-red-500 text-white hover:bg-red-600"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}

      {files.map((file) => (
        <div key={file} className="border border-gray-200 rounded-xl overflow-hidden">
          {/* Заголовок файла */}
          <div
            onClick={() => handleExpand(file)}
            className={`flex items-center justify-between px-4 py-3 cursor-pointer transition
              ${selectedFile === file ? 'bg-blue-50' : 'bg-white hover:bg-gray-50'}`}
          >
            <div className="flex items-center gap-2 min-w-0">
              <span className="text-gray-400 text-xs">
                {file.endsWith('.pdf') ? '📄' : '📝'}
              </span>
              <span className="text-sm text-gray-700 truncate">{file}</span>
            </div>
            <div className="flex items-center gap-2 shrink-0 ml-2">
              <button
                onClick={(e) => { e.stopPropagation(); onSelect(file) }}
                className="text-xs text-blue-500 hover:text-blue-700 px-2 py-1 rounded hover:bg-blue-50"
              >
                Search
              </button>
              <button
                onClick={(e) => handleDeleteClick(file, e)}
                className="text-xs text-red-400 hover:text-red-600 px-2 py-1 rounded hover:bg-red-50"
              >
                ✕
              </button>
              <span className="text-gray-300 text-xs">
                {expanded === file ? '▲' : '▼'}
              </span>
            </div>
          </div>

          {/* Раскрывающаяся история */}
          {expanded === file && (
            <div className="border-t border-gray-100 bg-gray-50 px-4 py-3">
              <p className="text-xs font-semibold text-gray-500 mb-2">Search history</p>
              {!histories[file] ? (
                <p className="text-xs text-gray-400">Loading...</p>
              ) : histories[file].length === 0 ? (
                <p className="text-xs text-gray-400">No searches yet</p>
              ) : (
                <ul className="space-y-2">
                  {histories[file].map((item) => (
                    <li key={item.id} className="text-xs bg-white rounded-lg px-3 py-2 border border-gray-100">
                      <p className="text-gray-600 font-medium">{item.question}</p>
                      <p className="text-blue-600 mt-0.5">{item.answer}</p>
                      <p className="text-gray-300 mt-0.5">
                        {Math.round(item.confidence * 100)}% · {new Date(item.created_at).toLocaleDateString()}
                      </p>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          )}
        </div>
      ))}
    </div>
  )
}