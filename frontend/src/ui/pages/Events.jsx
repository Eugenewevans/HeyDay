import React from 'react'
import { api } from '../../util/api'

export function Events(){
  const [items, setItems] = React.useState([])
  const [form, setForm] = React.useState({ name:'', dataset_id:'', event_type_id:'', template_id:'', trigger_column_name:'', day_offset:0, send_time:'09:00', channel:'sms', mode:'preview', active:false })
  const [schemaColumns, setSchemaColumns] = React.useState([])

  async function refresh(){ const r = await api.get('/automations/'); setItems(r.data) }
  async function loadSchema(dsId){
    if(!dsId) return
    try { const r = await api.get(`/datasets-v2/${dsId}/schema`); setSchemaColumns(r.data.filter(c=>c.is_trigger_candidate)) } catch{}
  }
  async function create(){
    if (!form.name.trim() || !form.dataset_id || !form.event_type_id || !form.template_id || !form.trigger_column_name) { alert('Please fill all required fields'); return }
    const payload = { ...form, dataset_id:parseInt(form.dataset_id), event_type_id:parseInt(form.event_type_id), template_id:parseInt(form.template_id), day_offset:parseInt(form.day_offset) }
    await api.post('/automations/', payload); setForm({ ...form, name:'', dataset_id:'', event_type_id:'', template_id:'', trigger_column_name:'' }); refresh()
  }
  React.useEffect(()=>{ refresh() },[])

  return (
    <>
      <h1>Events</h1>
      <div className="card">
        <div className="row">
          <input placeholder="Name" value={form.name} onChange={e=>setForm({...form, name:e.target.value})} />
          <input placeholder="Dataset ID" value={form.dataset_id} onChange={e=>{setForm({...form, dataset_id:e.target.value}); loadSchema(e.target.value)}} />
          <input placeholder="Event Type ID" value={form.event_type_id} onChange={e=>setForm({...form, event_type_id:e.target.value})} />
          <input placeholder="Template ID" value={form.template_id} onChange={e=>setForm({...form, template_id:e.target.value})} />
          <select value={form.trigger_column_name} onChange={e=>setForm({...form, trigger_column_name:e.target.value})}>
            <option value="">Trigger column...</option>
            {schemaColumns.map(c=><option key={c.column_name} value={c.column_name}>{c.column_name}</option>)}
          </select>
          <input placeholder="Offset" value={form.day_offset} onChange={e=>setForm({...form, day_offset:e.target.value})} />
          <input placeholder="HH:MM" value={form.send_time} onChange={e=>setForm({...form, send_time:e.target.value})} />
          <select value={form.channel} onChange={e=>setForm({...form, channel:e.target.value})}><option>sms</option><option>email</option></select>
          <select value={form.mode} onChange={e=>setForm({...form, mode:e.target.value})}><option>preview</option><option>auto</option></select>
          <label className="row"><input type="checkbox" checked={form.active} onChange={e=>setForm({...form, active:e.target.checked})}/> Active</label>
          <button onClick={create}>Create</button>
        </div>
      </div>
      <div className="card">
        <table><thead><tr><th>ID</th><th>Name</th><th>Dataset</th><th>Event</th><th>Template</th><th>Offset</th><th>Time</th><th>Chan</th><th>Active</th></tr></thead>
          <tbody>{items.map(x=>(<tr key={x.id}><td>{x.id}</td><td>{x.name}</td><td>{x.dataset_id}</td><td>{x.event_type_id}</td><td>{x.template_id}</td><td>{x.day_offset}</td><td>{x.send_time}</td><td>{x.channel}</td><td>{x.active?'on':'off'}</td></tr>))}</tbody>
        </table>
      </div>
    </>
  )
}

