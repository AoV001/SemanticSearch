export const getDefinition = async (word) => {
  const clean = word.toLowerCase().replace(/[^a-z]/g, '')
  if (!clean) return null
  try {
    const res = await fetch(`https://api.dictionaryapi.dev/api/v2/entries/en/${clean}`)
    if (!res.ok) return null
    const data = await res.json()
    return data[0] || null
  } catch {
    return null
  }
}