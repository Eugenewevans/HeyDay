import React from 'react'
import { api } from '../../util/api'

export function Databases(){
  const [items, setItems] = React.useState([])
  const [name, setName] = React.useState('')
  const [desc, setDesc] = React.useState('')

  async function refresh(){ const r = await api.get('/datasets'); setItems(r.data) }
  async function create(){ await api.post('/datasets/', { name, description: desc||null }); setName(''); setDesc(''); refresh() }
  React.useEffect(()=>{ refresh() },[])

  return (
    <>
      <h1>Databases</h1>
      <div className="card">
        <div className="row">
          <input placeholder="Name" value={name} onChange={e=>setName(e.target.value)} />
          <input placeholder="Description" value={desc} onChange={e=>setDesc(e.target.value)} />
          <button onClick={create}>Create</button>
        </div>
      </div>
      <div className="card">
        <table><thead><tr><th>ID</th><th>Name</th><th>Description</th></tr></thead>
          <tbody>{items.map(x=>(<tr key={x.id}><td>{x.id}</td><td>{x.name}</td><td>{x.description||''}</td></tr>))}</tbody>
        </table>
      </div>
    </>
  )
}

