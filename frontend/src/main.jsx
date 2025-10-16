import React from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import './styles.css'
import { AppLayout } from './ui/AppLayout'
import { Dashboard } from './ui/pages/Dashboard'
import { Databases } from './ui/pages/Databases'
import { Events } from './ui/pages/Events'
import { Queue } from './ui/pages/Queue'
import { Templates } from './ui/pages/Templates'
import { Settings } from './ui/pages/Settings'

const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,
    children: [
      { index: true, element: <Dashboard /> },
      { path: 'databases', element: <Databases /> },
      { path: 'events', element: <Events /> },
      { path: 'queue', element: <Queue /> },
      { path: 'templates', element: <Templates /> },
      { path: 'settings', element: <Settings /> },
    ],
  },
])

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
)

