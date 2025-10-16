import React from 'react'
import { api } from '../../util/api'

export function Databases(){
  const [items, setItems] = React.useState([])
  const [name, setName] = React.useState('')
  const [desc, setDesc] = React.useState('')
  const [msg, setMsg] = React.useState('')
  const [loading, setLoading] = React.useState(false)

  async function refresh(){
    try { const r = await api.get('/datasets/'); setItems(r.data) }
    catch { /* ignore */ }
  }

  async function create(){
    setMsg('')
    if (!name.trim()) { setMsg('Please enter a name.'); return }
    try {
      setLoading(true)
      await api.post('/datasets/', { name: name.trim(), description: desc.trim() || null })
      setName(''); setDesc('');
      setMsg('Created.')
      await refresh()
    } catch (e) {
      const detail = e?.response?.data?.detail
      setMsg(detail ? String(detail) : 'Create failed')
    } finally { setLoading(false) }
  }

  React.useEffect(()=>{ refresh() },[])

  return (
    <>
      <h1>Databases</h1>
      <div className="card">
        <div className="row" style={{marginBottom: '.5rem'}}>
          <input placeholder="Name" value={name} onChange={e=>setName(e.target.value)} />
          <input placeholder="Description" value={desc} onChange={e=>setDesc(e.target.value)} />
          <button onClick={create} disabled={loading}>{loading ? 'Creating…' : 'Create'}</button>
        </div>
        {msg ? <div className="muted">{msg}</div> : null}
      </div>
      <div className="card">
        <table><thead><tr><th>ID</th><th>Name</th><th>Description</th></tr></thead>
          <tbody>{items.map(x=>(<tr key={x.id}><td>{x.id}</td><td>{x.name}</td><td>{x.description||''}</td></tr>))}</tbody>
        </table>
      </div>
    </>
  )
}

