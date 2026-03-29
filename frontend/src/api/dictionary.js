/**
 * Fetches the definition of a given English word from the free Dictionary API.
 *
 * @param {string} word - The word to define.
 * @returns {Promise<Object|null>} - Returns the first dictionary entry object if found, or null if not found or on error.
 *
 * The function:
 * - Converts the word to lowercase
 * - Removes non-alphabetic characters
 * - Calls https://api.dictionaryapi.dev
 */

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