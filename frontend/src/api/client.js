const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const uploadFile = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  const res = await fetch(`${API_URL}/api/upload`, {
    method: 'POST',
    body: formData
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export const getFiles = async () => {
  const res = await fetch(`${API_URL}/api/files`)
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export const deleteFile = async (filename) => {
  const res = await fetch(`${API_URL}/api/files/${encodeURIComponent(filename)}`, {
    method: 'DELETE'
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export const searchFile = async (filename, questions, top_k = 3) => {
  const res = await fetch(`${API_URL}/api/search`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ filename, questions, top_k })
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export const getHistory = async () => {
  const res = await fetch(`${API_URL}/api/history`)
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export const getFileHistory = async (filename) => {
  const res = await fetch(`${API_URL}/api/history/${encodeURIComponent(filename)}`)
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export const getFileText = async (filename) => {
  const res = await fetch(`${API_URL}/api/files/${encodeURIComponent(filename)}/text`)
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}