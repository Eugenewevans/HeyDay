import React from 'react'
import { api } from '../../util/api'

export function UploadWizard({ datasetId, onComplete }) {
  const [file, setFile] = React.useState(null)
  const [step, setStep] = React.useState(1) // 1: upload, 2: confirm schema
  const [schema, setSchema] = React.useState([])
  const [msg, setMsg] = React.useState('')

  async function uploadAndDetect() {
    if (!file || !datasetId) { setMsg('Select file and dataset'); return }
    try {
      const fd = new FormData()
      fd.append('file', file)
      const r = await api.post(`/datasets-v2/${datasetId}/import-flexible`, fd)
      setSchema(r.data.detected_schema || [])
      setMsg(`Detected ${r.data.detected_schema?.length || 0} columns. Imported ${r.data.imported} records.`)
      setStep(2)
    } catch { setMsg('Upload failed') }
  }

  async function confirmSchema() {
    try {
      const payload = schema.map(s => ({ dataset_id: parseInt(datasetId), column_name: s.column_name, semantic_role: s.semantic_role, is_trigger_candidate: s.is_trigger_candidate }))
      await api.post(`/datasets-v2/${datasetId}/schema`, payload)
      setMsg('Schema saved.')
      if (onComplete) onComplete()
    } catch { setMsg('Save failed') }
  }

  return (
    <div>
      {step === 1 && (
        <div className="card">
          <h2>Step 1: Upload CSV</h2>
          <input type="file" accept=".csv" onChange={e => setFile(e.target.files?.[0])} />
          <button onClick={uploadAndDetect} style={{marginTop:'.5rem'}}>Upload & Detect Schema</button>
          {msg && <div className="muted" style={{marginTop:'.5rem'}}>{msg}</div>}
        </div>
      )}
      {step === 2 && (
        <div className="card">
          <h2>Step 2: Confirm Detected Schema</h2>
          <table style={{marginBottom:'1rem'}}>
            <thead><tr><th>Column</th><th>Role</th><th>Trigger?</th></tr></thead>
            <tbody>
              {schema.map((col, i) => (
                <tr key={i}>
                  <td>{col.column_name}</td>
                  <td>
                    <select value={col.semantic_role || ''} onChange={e => {
                      const s2 = [...schema]; s2[i].semantic_role = e.target.value || null; setSchema(s2)
                    }}>
                      <option value="">none</option>
                      <option value="name">name</option>
                      <option value="email">email</option>
                      <option value="phone">phone</option>
                      <option value="date">date</option>
                      <option value="text">text</option>
                      <option value="number">number</option>
                    </select>
                  </td>
                  <td>
                    <input type="checkbox" checked={col.is_trigger_candidate} onChange={e => {
                      const s2 = [...schema]; s2[i].is_trigger_candidate = e.target.checked; setSchema(s2)
                    }} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <button onClick={confirmSchema}>Confirm & Save</button>
          {msg && <div className="muted" style={{marginTop:'.5rem'}}>{msg}</div>}
        </div>
      )}
    </div>
  )
}

