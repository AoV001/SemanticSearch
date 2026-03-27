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
  const [highlightData, setHighlightData] = useState(null)
  const [corefMap, setCorefMap] = useState({})

  useEffect(() => {
    getFiles().then(data => setFiles(data.files))
  }, [])

  const handleSelect = async (filename) => {
    setSelectedFile(filename)
    setResults([])
    setHighlightData(null)
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
    setHighlightData(null)
    try {
      const data = await searchFile(selectedFile, questions)
      setResults(data.results)
      setResolvedText(data.resolved_text)
      setCorefMap(data.coref_map || {})
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="h-screen flex flex-col" style={{background: '#0f1117'}}>
      <header style={{background: '#1a1d27', borderBottom: '1px solid #2a2d3a'}} className="px-6 py-3 shrink-0">
        <div className="flex items-center gap-3">
          <h1 className="text-lg font-bold" style={{color: '#2dd4bf'}}>Semantic Search</h1>
        </div>
      </header>

      <div className="flex-1 overflow-hidden grid grid-cols-10">

        {/* Левая — 2/10 */}
        <div className="col-span-2 flex flex-col overflow-hidden" style={{background: '#1a1d27', borderRight: '1px solid #2a2d3a'}}>
          <div className="p-3 shrink-0" style={{borderBottom: '1px solid #2a2d3a'}}>
            <p className="text-xs font-semibold uppercase tracking-wide mb-2" style={{color: '#64748b'}}>Files</p>
            {selectedFile && <FileUpload onUploadSuccess={handleUploadSuccess} />}
          </div>
          <div className="flex-1 overflow-y-auto p-3">
            <FileList
              files={files}
              selectedFile={selectedFile}
              onSelect={handleSelect}
              onDelete={handleDelete}
              onDeleteAll={() => {
                setFiles([])
                setSelectedFile(null)
                setFileText(null)
                setResults([])
              }}
            />
          </div>
        </div>

        {/* Центр — 5/10 */}
        <div className="col-span-5 flex flex-col overflow-hidden" style={{background: '#13151f', borderRight: '1px solid #2a2d3a'}}>
          {!selectedFile ? (
            <div className="flex-1 flex flex-col items-center justify-center p-12">
              <p className="text-2xl font-bold mb-2" style={{color: '#e2e8f0'}}>Welcome</p>
              <p className="text-sm mb-8" style={{color: '#64748b'}}>Upload a file to get started</p>
              <div className="w-full max-w-sm">
                <FileUpload onUploadSuccess={handleUploadSuccess} />
              </div>
              {files.length > 0 && (
                <p className="text-xs mt-6" style={{color: '#64748b'}}>
                  Or select an existing file from the left panel
                </p>
              )}
            </div>
          ) : (
            <>
              <div className="px-4 py-2 shrink-0" style={{borderBottom: '1px solid #2a2d3a'}}>
                <p className="text-xs truncate" style={{color: '#64748b'}}>{selectedFile}</p>
              </div>
              <div className="flex-1 overflow-hidden p-4">
                <TextViewer
                  text={fileText}
                  resolvedText={resolvedText}
                  highlightData={highlightData}
                  corefMap={corefMap}
                />
              </div>
            </>
          )}
        </div>

        {/* Правая — 3/10 */}
        <div className="col-span-3 flex flex-col overflow-hidden" style={{background: '#1a1d27'}}>
          <div className="p-4 shrink-0" style={{borderBottom: '1px solid #2a2d3a'}}>
            <SearchForm
              selectedFile={selectedFile}
              onSearch={handleSearch}
              loading={loading}
            />
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {results.length === 0 && (
              <p className="text-xs text-center pt-8" style={{color: '#64748b'}}>
                Results will appear here
              </p>
            )}
            {results.map((result, i) => (
              <ResultCard
                key={i}
                result={result}
                onHover={setHighlightData}
              />
            ))}
          </div>
        </div>

      </div>
    </div>
  )
}