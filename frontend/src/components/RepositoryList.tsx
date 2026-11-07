import { ArrowUpRight, Clock3, FolderGit2, Search } from 'lucide-react'
import { repositories } from '../data/dashboard'

export default function RepositoryList() {
  return (
    <section className="panel repository-panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Your codebase</p>
          <h2>Recent repositories</h2>
        </div>
        <button className="text-button">View all <ArrowUpRight size={15} /></button>
      </div>
      <div className="repo-toolbar">
        <div className="search-box"><Search size={16} /><span>Search repositories</span></div>
        <button className="filter-button">All repositories</button>
      </div>
      <div className="repo-list">
        {repositories.map((repository) => (
          <div className="repo-row" key={repository.name}>
            <div className="repo-icon"><FolderGit2 size={18} /></div>
            <div className="repo-info">
              <strong>{repository.name}</strong>
              <span>{repository.description}</span>
            </div>
            <span className="repo-language"><i style={{ backgroundColor: repository.languageColor }} />{repository.language}</span>
            <span className={`index-status ${repository.indexed ? 'ready' : 'pending'}`}>
              {repository.indexed ? 'Indexed' : 'Not indexed'}
            </span>
            <span className="repo-updated"><Clock3 size={14} />{repository.updatedAt}</span>
          </div>
        ))}
      </div>
    </section>
  )
}
