import { useState, useEffect } from 'react'
import FileUpload from '../components/FileUpload'
import FileList from '../components/FileList'
import SearchForm from '../components/SearchForm'
import ResultCard from '../components/ResultCard'
import { getFiles, searchFile } from '../api/client'

export default function Home() {
  const [files, setFiles] = useState([])
  const [selectedFile, setSelectedFile] = useState(null)
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    getFiles().then(data => setFiles(data.files))
  }, [])

  const handleUploadSuccess = (result) => {
    setFiles(prev => [...prev, result.filename])
    setSelectedFile(result.filename)
  }

  const handleDelete = (filename) => {
    setFiles(prev => prev.filter(f => f !== filename))
    if (selectedFile === filename) {
      setSelectedFile(null)
      setResults([])
    }
  }

  const handleSearch = async (questions) => {
    setLoading(true)
    setResults([])
    try {
      const data = await searchFile(selectedFile, questions)
      setResults(data)
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 space-y-6">
      <h1 className="text-3xl font-bold text-gray-800">Semantic Search</h1>

      <div className="grid grid-cols-3 gap-6">
        {/* Левая колонка — файлы */}
        <div className="space-y-4">
          <FileUpload onUploadSuccess={handleUploadSuccess} />
          <FileList
            files={files}
            selectedFile={selectedFile}
            onSelect={setSelectedFile}
            onDelete={handleDelete}
          />
        </div>

        {/* Правая колонка — поиск и результаты */}
        <div className="col-span-2 space-y-4">
          <SearchForm
            selectedFile={selectedFile}
            onSearch={handleSearch}
            loading={loading}
          />

          {selectedFile && (
            <p className="text-sm text-gray-500">
              Selected: <span className="font-medium text-blue-600">{selectedFile}</span>
            </p>
          )}

          {results.map((result, i) => (
            <ResultCard key={i} result={result} />
          ))}
        </div>
      </div>
    </div>
  )
}