import React from 'react'
import { api } from '../../util/api'

export function Dashboard(){
  const [health, setHealth] = React.useState('')
  const [automations, setAutomations] = React.useState([])
  const [messages, setMessages] = React.useState([])
  const [datasets, setDatasets] = React.useState([])

  React.useEffect(()=>{
    api.get('/health').then(r=>setHealth(JSON.stringify(r.data))).catch(()=>setHealth('error'))
    api.get('/automations/').then(r=>setAutomations(r.data.filter(a=>a.active))).catch(()=>{})
    api.get('/messages/?status=generated').then(r=>setMessages(r.data)).catch(()=>{})
    api.get('/datasets/').then(r=>setDatasets(r.data)).catch(()=>{})
  },[])

  return (
    <>
      <h1>Dashboard</h1>
      <div style={{display:'grid',gridTemplateColumns:'repeat(3,1fr)',gap:'1rem',marginBottom:'1rem'}}>
        <div className="card">
          <h2>Active Automations</h2>
          <div style={{fontSize:'2rem',fontWeight:600}}>{automations.length}</div>
        </div>
        <div className="card">
          <h2>Awaiting Approval</h2>
          <div style={{fontSize:'2rem',fontWeight:600}}>{messages.length}</div>
        </div>
        <div className="card">
          <h2>Datasets</h2>
          <div style={{fontSize:'2rem',fontWeight:600}}>{datasets.length}</div>
        </div>
      </div>

      <div className="card">
        <h2>Active Automations</h2>
        <table><thead><tr><th>Name</th><th>Dataset</th><th>Trigger</th><th>Mode</th></tr></thead>
          <tbody>{automations.map(a=>(<tr key={a.id}><td>{a.name}</td><td>{a.dataset_id}</td><td>{a.trigger_column_name}</td><td>{a.mode}</td></tr>))}</tbody>
        </table>
      </div>

      <div className="card">
        <h2>Recent Messages (Generated)</h2>
        <table><thead><tr><th>ID</th><th>Record</th><th>Channel</th><th>Scheduled</th></tr></thead>
          <tbody>{messages.slice(0,10).map(m=>(<tr key={m.id}><td>{m.id}</td><td>{m.record_id}</td><td>{m.channel}</td><td>{m.scheduled_for||''}</td></tr>))}</tbody>
        </table>
      </div>

      <div className="card">
        <div>API Health: <span className="muted">{health}</span></div>
      </div>
    </>
  )
}

