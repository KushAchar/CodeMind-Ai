export type Repository = {
  name: string
  description: string
  language: string
  languageColor: string
  updatedAt: string
  indexed: boolean
}

export type Activity = {
  icon: 'index' | 'chat' | 'analysis'
  title: string
  description: string
  time: string
}

export const repositories: Repository[] = [
  {
    name: 'codemind-ai',
    description: 'AI-powered codebase understanding platform',
    language: 'Python',
    languageColor: '#f0b429',
    updatedAt: '2 hours ago',
    indexed: true,
  },
  {
    name: 'acme-dashboard',
    description: 'Internal analytics and operations dashboard',
    language: 'TypeScript',
    languageColor: '#3b82f6',
    updatedAt: 'Yesterday',
    indexed: true,
  },
  {
    name: 'open-source-toolkit',
    description: 'Collection of developer productivity utilities',
    language: 'JavaScript',
    languageColor: '#eab308',
    updatedAt: '3 days ago',
    indexed: false,
  },
]

export const activities: Activity[] = [
  {
    icon: 'index',
    title: 'Repository indexed',
    description: 'codemind-ai is ready for AI-assisted exploration',
    time: '2 hours ago',
  },
  {
    icon: 'chat',
    title: 'New assistant session',
    description: 'You asked 8 questions about the services layer',
    time: '4 hours ago',
  },
  {
    icon: 'analysis',
    title: 'Code analysis completed',
    description: 'Dependency analysis finished for acme-dashboard',
    time: 'Yesterday',
  },
]
