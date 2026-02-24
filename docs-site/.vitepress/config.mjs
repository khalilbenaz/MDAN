import { defineConfig } from 'vitepress'

export default defineConfig({
  title: "MDAN v2",
  description: "Multi-Agent Development Agentic Network",
  themeConfig: {
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Guide', link: '/guide/getting-started' }
    ],

    sidebar: [
      {
        text: 'Introduction',
        items: [
          { text: 'Getting Started', link: '/guide/getting-started' },
          { text: 'Core Concepts', link: '/guide/concepts' }
        ]
      },
      {
        text: 'Phases',
        items: [
          { text: '1. Discover', link: '/phases/discover' },
          { text: '2. Design', link: '/phases/design' }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/khalilbenaz/MDAN' }
    ]
  }
})
