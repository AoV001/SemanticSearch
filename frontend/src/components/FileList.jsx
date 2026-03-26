import { deleteFile } from '../api/client'

export default function FileList({ files, selectedFile, onSelect, onDelete }) {
  const handleDelete = async (filename, e) => {
    e.stopPropagation()
    try {
      await deleteFile(filename)
      onDelete(filename)
    } catch (e) {
      console.error(e)
    }
  }

  if (files.length === 0) {
    return <p className="text-gray-400 text-sm text-center py-4">No files uploaded yet</p>
  }

  return (
    <ul className="space-y-2">
      {files.map((file) => (
        <li
          key={file}
          onClick={() => onSelect(file)}
          className={`flex items-center justify-between px-4 py-2 rounded-lg cursor-pointer transition
            ${selectedFile === file ? 'bg-blue-100 border border-blue-400' : 'bg-white border border-gray-200 hover:bg-gray-50'}`}
        >
          <span className="text-sm text-gray-700 truncate">{file}</span>
          <button
            onClick={(e) => handleDelete(file, e)}
            className="ml-2 text-red-400 hover:text-red-600 text-xs shrink-0"
          >
            ✕
          </button>
        </li>
      ))}
    </ul>
  )
}