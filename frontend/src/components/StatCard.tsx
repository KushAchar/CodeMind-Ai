import { ArrowUpRight, CheckCircle2, FolderGit2, GitBranch } from 'lucide-react'

type Props = {
  label: string
  value: string
  detail: string
  type: 'repositories' | 'indexed'
}

export default function StatCard({ label, value, detail, type }: Props) {
  const Icon = type === 'repositories' ? FolderGit2 : CheckCircle2
  return (
    <article className="stat-card">
      <div className="stat-topline">
        <div className={`stat-icon ${type}`}><Icon size={19} /></div>
        <span className="stat-trend"><ArrowUpRight size={14} /> 12%</span>
      </div>
      <div className="stat-value">{value}</div>
      <div className="stat-label">{label}</div>
      <div className="stat-detail"><GitBranch size={13} /> {detail}</div>
    </article>
  )
}
