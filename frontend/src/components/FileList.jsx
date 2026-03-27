import { useState } from 'react'
import { deleteFile, deleteAllFiles } from '../api/client'
import HistoryOverlay from './HistoryOverlay'

export default function FileList({ files, selectedFile, onSelect, onDelete, onDeleteAll }) {
  const [confirmDelete, setConfirmDelete] = useState(null)
  const [historyFile, setHistoryFile] = useState(null)
  const [confirmDeleteAll, setConfirmDeleteAll] = useState(false)

  const handleConfirmDelete = async () => {
    try {
      await deleteFile(confirmDelete)
      onDelete(confirmDelete)
    } catch (e) {
      console.error(e)
    } finally {
      setConfirmDelete(null)
    }
  }

  const handleDeleteAll = async () => {
    try {
      await deleteAllFiles()
      onDeleteAll()
    } catch (e) {
      console.error(e)
    } finally {
      setConfirmDeleteAll(false)
    }
  }

  if (files.length === 0) {
    return <p className="text-gray-400 text-sm text-center py-4">No files uploaded yet</p>
  }

  return (
    <>
      {historyFile && (
        <HistoryOverlay
          filename={historyFile}
          onClose={() => setHistoryFile(null)}
        />
      )}

      {confirmDelete && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-6 shadow-xl max-w-sm w-full mx-4">
            <h3 className="font-semibold text-gray-800 mb-2">Delete file?</h3>
            <p className="text-sm text-red-500 mb-5">
              This will permanently delete the file and its search history.
            </p>
            <div className="flex gap-3 justify-end">
              <button onClick={() => setConfirmDelete(null)}
                className="px-4 py-2 text-sm rounded-lg border border-gray-300 hover:bg-gray-50">
                Cancel
              </button>
              <button onClick={handleConfirmDelete}
                className="px-4 py-2 text-sm rounded-lg bg-red-500 text-white hover:bg-red-600">
                Delete
              </button>
            </div>
          </div>
        </div>
      )}

      {confirmDeleteAll && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-6 shadow-xl max-w-sm w-full mx-4">
            <h3 className="font-semibold text-gray-800 mb-2">Delete all files?</h3>
            <p className="text-sm text-red-500 mb-5">
              This will permanently delete all files and their search history.
            </p>
            <div className="flex gap-3 justify-end">
              <button onClick={() => setConfirmDeleteAll(false)}
                className="px-4 py-2 text-sm rounded-lg border border-gray-300 hover:bg-gray-50">
                Cancel
              </button>
              <button onClick={handleDeleteAll}
                className="px-4 py-2 text-sm rounded-lg bg-red-500 text-white hover:bg-red-600">
                Delete all
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Кнопка Delete all */}
      <div className="flex justify-end mb-2">
        <button
          onClick={() => setConfirmDeleteAll(true)}
          className="text-xs text-red-400 hover:text-red-600"
        >
          Delete all
        </button>
      </div>

      <ul className="space-y-2">
        {files.map((file) => (
          <li key={file}
            className={`rounded-xl border transition
              ${selectedFile === file ? 'border-blue-300 bg-blue-50' : 'border-gray-200 bg-white'}`}
          >
            <div className="flex items-center gap-2 px-3 py-2">
              <span className="text-base">{file.endsWith('.pdf') ? '📄' : '📝'}</span>
              <span className="text-sm text-gray-700 truncate flex-1">{file}</span>
            </div>
            <div className="flex gap-1 px-3 pb-2">
              <button onClick={() => onSelect(file)}
                className="text-xs text-blue-500 hover:text-blue-700 px-2 py-1 rounded hover:bg-blue-50">
                Search
              </button>
              <button onClick={() => setHistoryFile(file)}
                className="text-xs text-gray-500 hover:text-gray-700 px-2 py-1 rounded hover:bg-gray-100">
                History
              </button>
              <button onClick={() => setConfirmDelete(file)}
                className="text-xs text-red-400 hover:text-red-600 px-2 py-1 rounded hover:bg-red-50 ml-auto">
                ✕ Delete
              </button>
            </div>
          </li>
        ))}
      </ul>
    </>
  )
}