const ROOT = import.meta.env.VITE_API_URL || 'http://localhost:8000'
async function call(path, options) {
  const response = await fetch(`${ROOT}${path}`, { headers:{'Content-Type':'application/json'}, ...options })
  const data = await response.json()
  if (!response.ok) throw new Error(data.detail || 'Сервис временно недоступен')
  return data
}
export const partyApi = {
  check: inn => call('/api/v1/party/check', {method:'POST',body:JSON.stringify({inn})}),
  search: query => call('/api/v1/party/search', {method:'POST',body:JSON.stringify({query, count: 20})}),
}
export const dealsApi = { createEscrow: data => call('/api/v1/deals/create-escrow', {method:'POST',body:JSON.stringify(data)}) }
