import React from 'react'
import { api } from '../../util/api'

export function Templates(){
  const [items, setItems] = React.useState([])
  const [name, setName] = React.useState('')
  const [channel, setChannel] = React.useState('sms')
  const [content, setContent] = React.useState('Happy {{name}}!')

  async function refresh(){ const r = await api.get('/templates/'); setItems(r.data) }
  async function create(){ await api.post('/templates/', { name, channel, content }); setName(''); setContent(''); refresh() }
  React.useEffect(()=>{ refresh() },[])

  return (
    <>
      <h1>Templates</h1>
      <div className="card">
        <div className="row">
          <input placeholder="Name" value={name} onChange={e=>setName(e.target.value)} />
          <select value={channel} onChange={e=>setChannel(e.target.value)}><option>sms</option><option>email</option></select>
        </div>
        <div className="row">
          <textarea rows={3} value={content} onChange={e=>setContent(e.target.value)} style={{width:'100%'}}></textarea>
        </div>
        <button onClick={create}>Create</button>
      </div>
      <div className="card">
        <table><thead><tr><th>ID</th><th>Name</th><th>Channel</th><th>Content</th></tr></thead>
          <tbody>{items.map(x=>(<tr key={x.id}><td>{x.id}</td><td>{x.name}</td><td>{x.channel}</td><td>{x.content}</td></tr>))}</tbody>
        </table>
      </div>
    </>
  )
}

