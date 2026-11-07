import { Braces } from 'lucide-react'

export default function Logo() {
  return (
    <div className="brand">
      <div className="brand-mark">
        <Braces size={19} strokeWidth={2.5} />
      </div>
      <div>
        <strong>CodeMind</strong>
        <span>AI DEVELOPER TOOL</span>
      </div>
    </div>
  )
}
