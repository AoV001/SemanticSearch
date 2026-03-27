import { useState, useEffect } from 'react'
import FileUpload from '../components/FileUpload'
import FileList from '../components/FileList'
import SearchForm from '../components/SearchForm'
import ResultCard from '../components/ResultCard'
import TextViewer from '../components/TextViewer'
import { getFiles, searchFile, getFileText } from '../api/client'

export default function Home() {
  const [files, setFiles] = useState([])
  const [selectedFile, setSelectedFile] = useState(null)
  const [fileText, setFileText] = useState(null)
  const [resolvedText, setResolvedText] = useState(null)
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [highlightContext, setHighlightContext] = useState(null)

  useEffect(() => {
    getFiles().then(data => setFiles(data.files))
  }, [])

  const handleSelect = async (filename) => {
    setSelectedFile(filename)
    setResults([])
    setHighlightContext(null)
    try {
      const data = await getFileText(filename)
      setFileText(data.text)
    } catch (e) {
      setFileText(null)
    }
  }

  const handleUploadSuccess = (result) => {
    setFiles(prev => [...prev, result.filename])
    handleSelect(result.filename)
  }

  const handleDelete = (filename) => {
    setFiles(prev => prev.filter(f => f !== filename))
    if (selectedFile === filename) {
      setSelectedFile(null)
      setFileText(null)
      setResults([])
    }
  }

const handleSearch = async (questions) => {
    setLoading(true)
    setResults([])
    setHighlightContext(null)
    try {
      const data = await searchFile(selectedFile, questions)
      setResults(data.results)
      setResolvedText(data.resolved_text)
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      <header className="bg-white border-b border-gray-200 px-6 py-3 shrink-0">
        <div className="flex items-center gap-3">
            <img src="/favicon.png" alt="logo" className="w-8 h-8" />
            <h1 className="text-lg font-bold text-gray-800">Semantic Search</h1>
        </div>
      </header>

      {/* 2:5:3 через grid */}
      <div className="flex-1 overflow-hidden grid grid-cols-10">

        {/* Левая — 2/10 */}
        <div className="col-span-2 border-r border-gray-200 bg-white flex flex-col overflow-hidden">
          <div className="p-3 border-b border-gray-100 shrink-0">
            <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Files</p>
            {/* Загрузка здесь только если файл уже выбран */}
            {selectedFile && (
              <FileUpload onUploadSuccess={handleUploadSuccess} />
            )}
          </div>
          <div className="flex-1 overflow-y-auto p-3">
            <FileList
              files={files}
              selectedFile={selectedFile}
              onSelect={handleSelect}
              onDelete={handleDelete}
            />
          </div>
        </div>

        {/* Центр — 5/10 */}
        <div className="col-span-5 border-r border-gray-200 bg-white flex flex-col overflow-hidden">
          {!selectedFile ? (
            /* Стартовый экран — загрузка по центру */
            <div className="flex-1 flex flex-col items-center justify-center p-12">
              <p className="text-2xl font-bold text-gray-700 mb-2">Welcome</p>
              <p className="text-sm text-gray-400 mb-8">Upload a file to get started</p>
              <div className="w-full max-w-sm">
                <FileUpload onUploadSuccess={handleUploadSuccess} />
              </div>
              {files.length > 0 && (
                <p className="text-xs text-gray-400 mt-6">
                  Or select an existing file from the left panel
                </p>
              )}
            </div>
          ) : (
            <>
              <div className="px-4 py-2 border-b border-gray-100 shrink-0">
                <p className="text-xs text-gray-400 truncate">{selectedFile}</p>
              </div>
              <div className="flex-1 overflow-hidden p-4">
                <TextViewer
                  text={fileText}
                  highlightContext={highlightContext}
                />
              </div>
            </>
          )}
        </div>

        {/* Правая — 3/10 */}
        <div className="col-span-3 bg-gray-50 flex flex-col overflow-hidden">
          <div className="p-4 border-b border-gray-200 bg-white shrink-0">
            <SearchForm
              selectedFile={selectedFile}
              onSearch={handleSearch}
              loading={loading}
            />
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {results.length === 0 && (
              <p className="text-xs text-gray-400 text-center pt-8">
                Results will appear here
              </p>
            )}
            {results.map((result, i) => (
              <ResultCard
                key={i}
                result={result}
                onHover={setHighlightContext}
              />
            ))}
          </div>
        </div>

      </div>
    </div>
  )
}