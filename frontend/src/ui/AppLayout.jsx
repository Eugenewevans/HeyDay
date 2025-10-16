import React from 'react'
import { NavLink, Outlet } from 'react-router-dom'

export function AppLayout(){
  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="brand">HeyDay</div>
        <nav className="nav">
          <NavLink to="/" end>Dashboard</NavLink>
          <NavLink to="/databases">Databases</NavLink>
          <NavLink to="/events">Events</NavLink>
          <NavLink to="/queue">Queue</NavLink>
          <NavLink to="/templates">Templates</NavLink>
          <NavLink to="/settings">Settings</NavLink>
        </nav>
      </aside>
      <main className="content">
        <div className="page">
          <Outlet />
        </div>
      </main>
    </div>
  )
}

