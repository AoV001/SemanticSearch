const DEP_DESCRIPTIONS = {
  "nsubj":     "is the subject of",
  "nsubjpass": "is the passive subject of",
  "dobj":      "is the object of",
  "advcl":     "is the reason/condition for",
  "prep":      "is related to",
  "attr":      "describes",
  "advmod":    "modifies",
  "amod":      "describes",
  "compound":  "forms a compound with",
  "pobj":      "is the object of preposition in",
  "iobj":      "is indirectly affected by",
  "conj":      "is connected to",
  "xcomp":     "is the result of",
  "ccomp":     "is implied by",
  "poss":      "belongs to",
  "neg":       "negates",
}

function DependencyGraph({ triplets, answer }) {
  if (!triplets || triplets.length === 0) return null

  // Собираем уникальные узлы
  const nodeSet = new Set()
  triplets.forEach(t => { nodeSet.add(t.from); nodeSet.add(t.to) })
  const nodes = Array.from(nodeSet)

  const W = 600
  const H = Math.max(200, nodes.length * 60)
  const cx = W / 2
  const r = Math.min(180, (H / 2) - 40)

  // Располагаем узлы по кругу
  const positions = {}
  nodes.forEach((node, i) => {
    const angle = (2 * Math.PI * i) / nodes.length - Math.PI / 2
    positions[node] = {
      x: cx + r * Math.cos(angle),
      y: H / 2 + r * Math.sin(angle)
    }
  })

  const isAnswer = (node) => node.toLowerCase() === answer?.toLowerCase()

  return (
    <svg width="100%" viewBox={`0 0 ${W} ${H}`} style={{maxHeight: '280px'}}>
      <defs>
        <marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
          <path d="M0,0 L0,6 L8,3 z" fill="#2dd4bf" />
        </marker>
        <marker id="arrow-pink" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
          <path d="M0,0 L0,6 L8,3 z" fill="#f472b6" />
        </marker>
      </defs>

      {/* Рёбра */}
      {triplets.map((t, i) => {
        const from = positions[t.from]
        const to = positions[t.to]
        if (!from || !to) return null

        const dx = to.x - from.x
        const dy = to.y - from.y
        const dist = Math.sqrt(dx*dx + dy*dy)
        const nx = dx / dist
        const ny = dy / dist
        const nodeR = 28

        const x1 = from.x + nx * nodeR
        const y1 = from.y + ny * nodeR
        const x2 = to.x - nx * (nodeR + 8)
        const y2 = to.y - ny * (nodeR + 8)

        const mx = (x1 + x2) / 2
        const my = (y1 + y2) / 2 - 20

        const isAnswerEdge = isAnswer(t.from) || isAnswer(t.to)
        const color = isAnswerEdge ? '#f472b6' : '#2dd4bf'
        const markerId = isAnswerEdge ? 'arrow-pink' : 'arrow'

        return (
          <g key={i}>
            <path
              d={`M ${x1} ${y1} Q ${mx} ${my} ${x2} ${y2}`}
              stroke={color} strokeWidth="1.5" fill="none"
              markerEnd={`url(#${markerId})`} opacity="0.7"
            />
            <text x={mx} y={my - 4} textAnchor="middle"
              fontSize="9" fill={color} opacity="0.9">
              {t.rel}
            </text>
          </g>
        )
      })}

      {/* Узлы */}
      {nodes.map((node) => {
        const pos = positions[node]
        const highlight = isAnswer(node)
        return (
          <g key={node}>
            <circle cx={pos.x} cy={pos.y} r={28}
              fill={highlight ? 'rgba(244,114,182,0.2)' : 'rgba(45,212,191,0.1)'}
              stroke={highlight ? '#f472b6' : '#2dd4bf'}
              strokeWidth={highlight ? 2 : 1}
            />
            <text x={pos.x} y={pos.y + 4} textAnchor="middle"
              fontSize="11" fill={highlight ? '#f472b6' : '#e2e8f0'}
              fontWeight={highlight ? 'bold' : 'normal'}>
              {node}
            </text>
          </g>
        )
      })}
    </svg>
  )
}

export default function ResultModal({ result, onClose }) {
  if (!result) return null
  const { question, results } = result
  const top = results[0]
  if (!top) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4"
      style={{background: 'rgba(0,0,0,0.8)'}}>
      <div className="rounded-2xl w-full max-w-3xl max-h-[90vh] flex flex-col overflow-hidden"
        style={{background: '#1a1d27', border: '1px solid #2a2d3a'}}>

        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 shrink-0"
          style={{borderBottom: '1px solid #2a2d3a'}}>
          <p className="text-sm" style={{color: '#64748b'}}>Q: {question}</p>
          <button onClick={onClose} className="text-xl" style={{color: '#64748b'}}>✕</button>
        </div>

        <div className="overflow-y-auto px-6 py-5 space-y-6">

          {/* Ответ */}
          <div>
            <p className="text-xs uppercase tracking-wide mb-1" style={{color: '#64748b'}}>Answer</p>
            <p className="text-4xl font-bold" style={{color: '#2dd4bf'}}>{top.answer}</p>
            <p className="text-xs mt-1" style={{color: '#64748b'}}>
              Confidence: {Math.round(top.confidence * 100)}%
            </p>
          </div>

          {/* Граф */}
          <div>
            <p className="text-xs uppercase tracking-wide mb-3" style={{color: '#64748b'}}>Dependency Graph</p>
            <div className="rounded-xl p-4" style={{background: '#0f1117', border: '1px solid #2a2d3a'}}>
              <DependencyGraph triplets={top.triplets} answer={top.answer} />
            </div>
          </div>

          {/* Evidence — красивые карточки */}
          <div>
            <p className="text-xs uppercase tracking-wide mb-3" style={{color: '#64748b'}}>Key Relationships</p>
            <div className="space-y-2">
              {top.triplets?.map((t, i) => (
                <div key={i} className="flex items-center gap-2 px-3 py-2 rounded-lg"
                  style={{background: '#222536', border: '1px solid #2a2d3a'}}>
                  <span className="text-sm font-medium px-2 py-0.5 rounded"
                    style={{background: 'rgba(45,212,191,0.1)', color: '#2dd4bf'}}>
                    {t.from}
                  </span>
                  <span className="text-xs" style={{color: '#64748b'}}>
                    {DEP_DESCRIPTIONS[t.rel] || t.rel}
                  </span>
                  <span className="text-sm font-medium px-2 py-0.5 rounded"
                    style={{background: 'rgba(244,114,182,0.1)', color: '#f472b6'}}>
                    {t.to}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Контекст */}
          <div>
            <p className="text-xs uppercase tracking-wide mb-2" style={{color: '#64748b'}}>Context</p>
            <p className="text-sm leading-relaxed p-4 rounded-xl"
              style={{background: '#0f1117', color: '#e2e8f0', border: '1px solid #2a2d3a'}}>
              {top.context}
            </p>
          </div>

        </div>
      </div>
    </div>
  )
}