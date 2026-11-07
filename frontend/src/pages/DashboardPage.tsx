import { Bell, ChevronDown, Command, Plus, Sparkles } from 'lucide-react'
import ActivityList from '../components/ActivityList'
import RepositoryList from '../components/RepositoryList'
import Sidebar from '../components/Sidebar'
import StatCard from '../components/StatCard'

export default function DashboardPage() {
  return (
    <div className="app-shell">
      <Sidebar />
      <main className="main-content">
        <header className="topbar">
          <div className="breadcrumb"><span>Workspace</span><ChevronDown size={14} /><strong>Dashboard</strong></div>
          <div className="topbar-actions">
            <button className="command-button"><Command size={14} /> <span>Quick search</span><kbd>⌘ K</kbd></button>
            <button className="icon-button notification-button" aria-label="Notifications"><Bell size={18} /><i /></button>
            <div className="mini-avatar">KA</div>
          </div>
        </header>
        <div className="content-wrap">
          <section className="welcome-row">
            <div>
              <p className="eyebrow">Friday, November 06, 2026</p>
              <h1>Good afternoon, Khush <span>✦</span></h1>
              <p className="welcome-copy">Here&apos;s what&apos;s happening across your codebase today.</p>
            </div>
            <button className="primary-button"><Plus size={17} /> Add repository</button>
          </section>

          <section className="stats-grid">
            <StatCard label="Total repositories" value="12" detail="+ 2 this month" type="repositories" />
            <StatCard label="Indexed repositories" value="8" detail="67% of total" type="indexed" />
            <article className="insight-card">
              <div className="insight-glow" />
              <div className="insight-icon"><Sparkles size={18} /></div>
              <p className="eyebrow">AI insight</p>
              <strong>Your codebase is getting smarter</strong>
              <span>Ask CodeMind anything about your repositories.</span>
              <button className="insight-button">Start exploring <ChevronDown size={14} /></button>
            </article>
          </section>

          <div className="dashboard-grid">
            <RepositoryList />
            <ActivityList />
          </div>
        </div>
      </main>
    </div>
  )
}
