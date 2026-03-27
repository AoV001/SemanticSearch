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
      <header className="px-6 py-3 shrink-0 flex items-center justify-between"
  style={{background: '#1a1d27', borderBottom: '1px solid #2a2d3a'}}>

  <div className="flex items-center gap-3">
    {/* Логотип — простая SVG иконка */}
    <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
      <circle cx="7" cy="14" r="3" fill="#2dd4bf"/>
      <circle cx="21" cy="7" r="3" fill="#f472b6"/>
      <circle cx="21" cy="21" r="3" fill="#2dd4bf"/>
      <line x1="10" y1="14" x2="18" y2="8" stroke="#2dd4bf" strokeWidth="1.5"/>
      <line x1="10" y1="14" x2="18" y2="20" stroke="#f472b6" strokeWidth="1.5"/>
      <line x1="21" y1="10" x2="21" y2="18" stroke="#2a2d3a" strokeWidth="1.5"/>
    </svg>
    <div>
      <h1 className="text-base font-bold" style={{color: '#2dd4bf'}}>Semantic Search</h1>
      <p className="text-xs" style={{color: '#64748b'}}>graph-based semantic search engine</p>
    </div>
  </div>

  <a href="https://github.com/AoV001" target="_blank" rel="noopener noreferrer"
    className="flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs transition"
    style={{border: '1px solid #2a2d3a', color: '#64748b'}}
    onMouseEnter={e => e.currentTarget.style.color = '#2dd4bf'}
    onMouseLeave={e => e.currentTarget.style.color = '#64748b'}
  >
    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/>
    </svg>
    AoV001
  </a>
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
      <footer className="shrink-0 px-6 py-3 flex items-center justify-between"
  style={{background: '#1a1d27', borderTop: '1px solid #2a2d3a'}}>

  <div className="flex items-center gap-4">
    <span className="text-xs" style={{color: '#64748b'}}>
      Built with
    </span>
    {['Python', 'FastAPI', 'spaCy', 'NetworkX', 'React'].map(tech => (
      <span key={tech} className="text-xs px-2 py-0.5 rounded"
        style={{background: '#222536', color: '#2dd4bf', border: '1px solid #2a2d3a'}}>
        {tech}
      </span>
    ))}
  </div>

  <div className="flex items-center gap-3">
    <span className="text-xs" style={{color: '#64748b'}}>Tony V.</span>
    <span className="text-xs" style={{color: '#2a2d3a'}}>·</span>
    <span className="text-xs" style={{color: '#64748b'}}>© 2026</span>
    <a href="https://github.com/AoV001" target="_blank" rel="noopener noreferrer"
      className="text-xs transition"
      style={{color: '#64748b'}}
      onMouseEnter={e => e.currentTarget.style.color = '#2dd4bf'}
      onMouseLeave={e => e.currentTarget.style.color = '#64748b'}
    >
      GitHub
    </a>
  </div>
</footer>
    </div>
  )
}