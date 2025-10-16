import React from 'react'
import { api } from '../../util/api'

export function Queue(){
  const [items, setItems] = React.useState([])
  async function refresh(){ const r = await api.get('/messages/'); setItems(r.data) }
  async function approve(id){ await api.post(`/messages/${id}/approve`); refresh() }
  async function cancel(id){ await api.post(`/messages/${id}/cancel`); refresh() }
  React.useEffect(()=>{ refresh() },[])
  return (
    <>
      <h1>Queue</h1>
      <div className="card">
        <button onClick={refresh}>Refresh</button>
      </div>
      <div className="card">
        <table><thead><tr><th>ID</th><th>Customer</th><th>Channel</th><th>Status</th><th>Scheduled</th><th></th></tr></thead>
          <tbody>
            {items.map(x=> (
              <tr key={x.id}>
                <td>{x.id}</td><td>{x.customer_id}</td><td>{x.channel}</td><td>{x.status}</td><td>{x.scheduled_for||''}</td>
                <td>
                  <button onClick={()=>approve(x.id)}>Approve</button>
                  <button onClick={()=>cancel(x.id)} style={{marginLeft:'.4rem', background:'#334155'}}>Cancel</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  )
}

