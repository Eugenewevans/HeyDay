import React from 'react'
import { api } from '../../util/api'
import { UploadWizard } from './UploadWizard'

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
  const [mapping, setMapping] = React.useState({ name_col:'', email_col:'', phone_col:'', birthday_col:'' })

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
              const res = await api.post(`/datasets/${String(datasetId).trim()}/import/csv`, fd)
              const n = res?.data?.imported ?? 0
              setImportMsg(`Imported ${n} record${n===1?'':'s'}.`)
              const r = await api.get(`/datasets/${datasetId}/customers`); setCustomers(r.data)
            } catch(e){ setImportMsg('Import failed') }
          }}>Upload CSV</button>
        </div>
        {importMsg ? <div className="muted">{importMsg}</div> : null}
        <div className="muted small">Auto-detects: name, email, phone, birthday. If headers differ, provide mapping below and upload again.</div>
        <div className="row" style={{marginTop: '.5rem'}}>
          <input placeholder="Name column (optional)" value={mapping.name_col} onChange={e=>setMapping({...mapping, name_col:e.target.value})} />
          <input placeholder="Email column" value={mapping.email_col} onChange={e=>setMapping({...mapping, email_col:e.target.value})} />
          <input placeholder="Phone column" value={mapping.phone_col} onChange={e=>setMapping({...mapping, phone_col:e.target.value})} />
          <input placeholder="Birthday column" value={mapping.birthday_col} onChange={e=>setMapping({...mapping, birthday_col:e.target.value})} />
          <button onClick={async()=>{
            setImportMsg('')
            if(!datasetId || !csvFile){ setImportMsg('Select dataset and CSV'); return }
            try {
              const fd = new FormData();
              fd.append('file', csvFile)
              if(mapping.name_col) fd.append('name_col', mapping.name_col)
              if(mapping.email_col) fd.append('email_col', mapping.email_col)
              if(mapping.phone_col) fd.append('phone_col', mapping.phone_col)
              if(mapping.birthday_col) fd.append('birthday_col', mapping.birthday_col)
              const res = await api.post(`/datasets/${String(datasetId).trim()}/import/csv-map`, fd)
              const n = res?.data?.imported ?? 0
              setImportMsg(`Imported ${n} record${n===1?'':'s'} with mapping.`)
              const r = await api.get(`/datasets/${datasetId}/customers`); setCustomers(r.data)
            } catch(e){ setImportMsg('Import with mapping failed') }
          }}>Upload with mapping</button>
        </div>
      </div>

      <div className="card">
        <h2>Upload Wizard (Flexible Schema)</h2>
        <div className="row" style={{marginBottom:'.5rem'}}>
          <input placeholder="Dataset ID" value={datasetId} onChange={e=>setDatasetId(e.target.value)} />
        </div>
        {datasetId && <UploadWizard datasetId={datasetId} onComplete={refresh} />}
      </div>
    </>
  )
}

