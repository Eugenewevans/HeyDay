import React from 'react'
import { api } from '../../util/api'

export function Databases(){
  const [items, setItems] = React.useState([])
  const [name, setName] = React.useState('')
  const [desc, setDesc] = React.useState('')
  const [msg, setMsg] = React.useState('')
  const [loading, setLoading] = React.useState(false)
  const [datasetId, setDatasetId] = React.useState('')
  const [customers, setCustomers] = React.useState([])
  const [csvFile, setCsvFile] = React.useState(null)
  const [importMsg, setImportMsg] = React.useState('')

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

      <div className="card">
        <h2>Dataset details</h2>
        <div className="row" style={{marginBottom: '.5rem'}}>
          <input placeholder="Dataset ID" value={datasetId} onChange={e=>setDatasetId(e.target.value)} />
          <button onClick={async()=>{
            if(!datasetId) return;
            try { const r = await api.get(`/datasets/${datasetId}/customers`); setCustomers(r.data) } catch {}
          }}>Load Customers</button>
        </div>
        <table><thead><tr><th>ID</th><th>Name</th><th>Phone</th><th>Email</th><th>Birthday</th></tr></thead>
          <tbody>{customers.map(c=>(<tr key={c.id}><td>{c.id}</td><td>{c.name}</td><td>{c.phone||''}</td><td>{c.email||''}</td><td>{c.birthday||''}</td></tr>))}</tbody>
        </table>
      </div>

      <div className="card">
        <h2>Import CSV</h2>
        <div className="row" style={{marginBottom: '.5rem'}}>
          <input placeholder="Dataset ID" value={datasetId} onChange={e=>setDatasetId(e.target.value)} />
          <input type="file" accept=".csv" onChange={e=>setCsvFile(e.target.files?.[0]||null)} />
          <button onClick={async()=>{
            setImportMsg('')
            if(!datasetId || !csvFile){ setImportMsg('Select dataset and CSV'); return }
            try {
              const fd = new FormData();
              fd.append('file', csvFile)
              await api.post(`/datasets/${datasetId}/import/csv`, fd)
              setImportMsg('Imported.')
              const r = await api.get(`/datasets/${datasetId}/customers`); setCustomers(r.data)
            } catch(e){ setImportMsg('Import failed') }
          }}>Upload CSV</button>
        </div>
        {importMsg ? <div className="muted">{importMsg}</div> : null}
        <div className="muted small">Auto-detects: name, email, phone, birthday.</div>
      </div>
    </>
  )
}

