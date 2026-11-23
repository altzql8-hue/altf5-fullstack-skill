import { useState } from 'react';

const areas = [
  { title: 'Frontend', detail: 'Responsive React + TypeScript design systems', icon: '◫' },
  { title: '3D Graphics', detail: 'Three.js rendering, disposal and adaptive quality', icon: '◇' },
  { title: 'Backend', detail: 'Validated APIs, predictable errors and observability', icon: '{ }' },
];

export function App() {
  const [filter, setFilter] = useState('all');
  const [query, setQuery] = useState('');
  const shown = areas.filter((area) => (filter === 'all' || area.title === filter) && area.title.toLowerCase().includes(query.toLowerCase().trim()));
  return <main className="shell">
    <a className="skip-link" href="#projects">Skip to projects</a>
    <nav className="nav" aria-label="Main navigation"><span className="brand"><span className="mark">A/</span> AltF5<span className="muted"> Engineering</span></span><a href="https://github.com" rel="noopener noreferrer" target="_blank">GitHub ↗</a></nav>
    <section className="hero"><span className="eyebrow">BUILD WITH INTENT — V1.0</span>
      <h1>Engineering with <span>clarity.</span></h1>
      <p>Starter dashboard: accessible, responsive and deliberately simple. Replace these example modules with real project data.</p>
      <a className="cta" href="#projects">Explore modules ↓</a>
    </section>
    <section id="projects" aria-labelledby="heading"><div className="section-head"><div><span className="eyebrow">CAPABILITIES</span><h2 id="heading">Core modules</h2></div><span className="muted">{shown.length} results</span></div>
      <div className="toolbar"><label htmlFor="search">Find a module</label><input id="search" placeholder="Search modules" value={query} onChange={e => setQuery(e.target.value)} />
      <label htmlFor="filter">Category</label><select id="filter" value={filter} onChange={e => setFilter(e.target.value)}><option value="all">All</option>{areas.map(a=><option key={a.title} value={a.title}>{a.title}</option>)}</select></div>
      <div className="cards">{shown.map(area=><article className="card" key={area.title}><span aria-hidden="true" className="symbol">{area.icon}</span><h3>{area.title}</h3><p>{area.detail}</p></article>)}
      {shown.length === 0 && <p role="status" className="empty">No modules match. Try a different search or category.</p>}</div>
    </section><footer>AltF5 • Built for working software, not mockups.</footer>
  </main>;
}
