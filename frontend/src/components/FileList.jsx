import { useState } from 'react'
import { deleteFile, deleteAllFiles } from '../api/client'
import HistoryOverlay from './HistoryOverlay'

/**
 * FileList component for displaying uploaded files with actions.
 *
 * Props:
 * - files: Array of filenames (strings) to display.
 * - selectedFile: Currently selected file for highlighting.
 * - onSelect: Callback when "Search" button is clicked for a file. Receives filename.
 * - onDelete: Callback when a single file is deleted. Receives filename.
 * - onDeleteAll: Callback when all files are deleted.
 *
 * Features:
 * - Shows file list with icons (PDF or TXT).
 * - Buttons for "Search", "History", and "Delete" per file.
 * - Delete confirmation dialogs for single and all files.
 * - Integrates with HistoryOverlay component for viewing search history.
 * - Handles core actions via API client functions (deleteFile, deleteAllFiles).
 */

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

  const Dialog = ({ title, message, onConfirm, onCancel }) => (
    <div className="fixed inset-0 flex items-center justify-center z-50" style={{background: 'rgba(0,0,0,0.6)'}}>
      <div className="rounded-xl p-6 shadow-xl max-w-sm w-full mx-4" style={{background: '#1a1d27', border: '1px solid #2a2d3a'}}>
        <h3 className="font-semibold mb-2" style={{color: '#e2e8f0'}}>{title}</h3>
        <p className="text-sm mb-5" style={{color: '#f472b6'}}>{message}</p>
        <div className="flex gap-3 justify-end">
          <button onClick={onCancel}
            className="px-4 py-2 text-sm rounded-lg"
            style={{border: '1px solid #2a2d3a', color: '#e2e8f0'}}>
            Cancel
          </button>
          <button onClick={onConfirm}
            className="px-4 py-2 text-sm rounded-lg font-medium"
            style={{background: '#f472b6', color: '#0f1117'}}>
            Delete
          </button>
        </div>
      </div>
    </div>
  )

  if (files.length === 0) {
    return <p className="text-sm text-center py-4" style={{color: '#64748b'}}>No files uploaded yet</p>
  }

  return (
    <>
      {historyFile && <HistoryOverlay filename={historyFile} onClose={() => setHistoryFile(null)} />}

      {confirmDelete && (
        <Dialog
          title="Delete file?"
          message="This will permanently delete the file and its search history."
          onConfirm={handleConfirmDelete}
          onCancel={() => setConfirmDelete(null)}
        />
      )}

      {confirmDeleteAll && (
        <Dialog
          title="Delete all files?"
          message="This will permanently delete all files and their search history."
          onConfirm={handleDeleteAll}
          onCancel={() => setConfirmDeleteAll(false)}
        />
      )}

      <div className="flex justify-end mb-2">
        <button onClick={() => setConfirmDeleteAll(true)} className="text-xs" style={{color: '#f472b6'}}>
          Delete all
        </button>
      </div>

      <ul className="space-y-2">
        {files.map((file) => (
          <li key={file} className="rounded-xl transition"
            style={{
              background: selectedFile === file ? '#222536' : '#1a1d27',
              border: selectedFile === file ? '1px solid #2dd4bf' : '1px solid #2a2d3a'
            }}>
            <div className="flex items-center gap-2 px-3 py-2">
              <span>{file.endsWith('.pdf') ? '📄' : '📝'}</span>
              <span className="text-sm truncate flex-1" style={{color: '#e2e8f0'}}>{file}</span>
            </div>
            <div className="flex gap-1 px-3 pb-2">
              <button onClick={() => onSelect(file)} className="text-xs px-2 py-1 rounded" style={{color: '#2dd4bf'}}>
                Search
              </button>
              <button onClick={() => setHistoryFile(file)} className="text-xs px-2 py-1 rounded" style={{color: '#64748b'}}>
                History
              </button>
              <button onClick={() => setConfirmDelete(file)} className="text-xs px-2 py-1 rounded ml-auto" style={{color: '#f472b6'}}>
                ✕ Delete
              </button>
            </div>
          </li>
        ))}
      </ul>
    </>
  )
}