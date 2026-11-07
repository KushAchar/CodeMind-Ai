import { Routes, Route } from 'react-router-dom'
import DashboardPage from './pages/DashboardPage'

function PlaceholderPage() {
  return (
    <div className="placeholder-page">
      <p className="eyebrow">Coming next</p>
      <h1>This workspace is ready for your next workflow.</h1>
    </div>
  )
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<DashboardPage />} />
      <Route path="*" element={<PlaceholderPage />} />
    </Routes>
  )
}
