import React from 'react'
import { api } from '../../util/api'

export function Dashboard(){
  const [health, setHealth] = React.useState('')
  React.useEffect(()=>{ api.get('/health').then(r=>setHealth(JSON.stringify(r.data))).catch(()=>setHealth('error')) },[])
  return (
    <>
      <h1>Dashboard</h1>
      <div className="card">
        <div>API Health: <span className="muted">{health}</span></div>
      </div>
    </>
  )
}

