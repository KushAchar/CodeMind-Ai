import { Bot, CheckCircle2, Clock3, FileSearch } from 'lucide-react'
import { activities } from '../data/dashboard'

const icons = { index: CheckCircle2, chat: Bot, analysis: FileSearch }

export default function ActivityList() {
  return (
    <section className="panel activity-panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Timeline</p>
          <h2>Recent activity</h2>
        </div>
        <button className="icon-button" aria-label="Activity options"><Clock3 size={17} /></button>
      </div>
      <div className="activity-list">
        {activities.map((activity) => {
          const Icon = icons[activity.icon]
          return (
            <div className="activity-row" key={activity.title}>
              <div className={`activity-icon ${activity.icon}`}><Icon size={16} /></div>
              <div className="activity-copy">
                <strong>{activity.title}</strong>
                <span>{activity.description}</span>
              </div>
              <time>{activity.time}</time>
            </div>
          )
        })}
      </div>
    </section>
  )
}
