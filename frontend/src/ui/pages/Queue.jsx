import React from 'react'
import { api } from '../../util/api'

export function Queue(){
  const [items, setItems] = React.useState([])
  const [filter, setFilter] = React.useState('generated') // pending|generated|approved|sent
  async function refresh(){ const r = await api.get(`/messages/?status=${filter}`); setItems(r.data) }
  async function approve(id){ await api.post(`/messages/${id}/approve`); refresh() }
  async function cancel(id){ await api.post(`/messages/${id}/cancel`); refresh() }
  React.useEffect(()=>{ refresh() },[filter])
  return (
    <>
      <h1>Queue</h1>
      <div className="card">
        <div className="row">
          <button onClick={refresh}>Refresh</button>
          <select value={filter} onChange={e=>setFilter(e.target.value)}>
            <option value="pending">Pending</option>
            <option value="generated">Generated (awaiting approval)</option>
            <option value="approved">Approved</option>
            <option value="sent">Sent</option>
          </select>
        </div>
      </div>
      <div className="card">
        <table><thead><tr><th>ID</th><th>Record</th><th>Channel</th><th>Status</th><th>Body</th><th>Scheduled</th><th></th></tr></thead>
          <tbody>
            {items.map(x=> (
              <tr key={x.id}>
                <td>{x.id}</td><td>{x.record_id}</td><td>{x.channel}</td><td>{x.status}</td><td style={{maxWidth:'200px',overflow:'hidden',textOverflow:'ellipsis'}}>{x.body||''}</td><td>{x.scheduled_for||''}</td>
                <td>
                  {x.status==='generated' && (
                    <>
                      <button onClick={()=>approve(x.id)}>Approve</button>
                      <button onClick={()=>cancel(x.id)} style={{marginLeft:'.4rem', background:'#334155'}}>Cancel</button>
                    </>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  )
}

