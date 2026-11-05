import { useEffect, useMemo, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Bar, BarChart, CartesianGrid, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis,
} from 'recharts'
import { BarChart3, CheckCircle2, Cpu, Globe2, Loader2, Sparkles, Target, XCircle } from 'lucide-react'

/* ---------- Types ---------- */
type Rate = { label: string; rate: number; count: number }
type Stats = { total: number; banked_rate: number; by_country: Rate[]; by_education: Rate[]; by_job: Rate[] }
type ModelMetrics = {
  model: string; threshold: number; accuracy: number; precision: number; recall: number; f1_score: number; roc_auc: number
}
type Metrics = { all_models: ModelMetrics[]; best_model: ModelMetrics }
type Prediction = { probability: number; threshold: number; banked: boolean }

/* ---------- Options du formulaire (identiques au dataset) ---------- */
const OPTIONS = {
  country: ['Kenya', 'Rwanda', 'Tanzania', 'Uganda'],
  location_type: ['Urban', 'Rural'],
  cellphone_access: ['Yes', 'No'],
  gender_of_respondent: ['Female', 'Male'],
  relationship_with_head: ['Head of Household', 'Spouse', 'Child', 'Parent', 'Other relative', 'Other non-relatives', 'Dont know'],
  marital_status: ['Married/Living together', 'Single/Never Married', 'Widowed', 'Divorced/Seperated', 'Don’t know'],
  education_level: ['No formal education', 'Primary education', 'Secondary education', 'Vocational/Specialised training', 'Tertiary education', 'Other/Dont know/RTA'],
  job_type: ['Formally employed Private', 'Formally employed Government', 'Self employed', 'Informally employed', 'Farming and Fishing', 'Remittance Dependent', 'Government Dependent', 'Other Income', 'No Income', 'Dont Know/Refuse to answer'],
}
const LABELS: Record<string, string> = {
  country: 'Pays', location_type: 'Milieu', cellphone_access: 'Téléphone portable', gender_of_respondent: 'Genre',
  relationship_with_head: 'Lien avec le chef de ménage', marital_status: 'Statut matrimonial',
  education_level: "Niveau d'éducation", job_type: "Type d'emploi",
}
const INITIAL = {
  country: 'Kenya', year: 2018, location_type: 'Urban', cellphone_access: 'Yes', household_size: 4, age_of_respondent: 35,
  gender_of_respondent: 'Female', relationship_with_head: 'Head of Household', marital_status: 'Married/Living together',
  education_level: 'Secondary education', job_type: 'Self employed',
}
type Form = typeof INITIAL

const YEAR_BY_COUNTRY: Record<string, number> = { Kenya: 2018, Rwanda: 2016, Tanzania: 2017, Uganda: 2018 }

/* ---------- Petits composants UI (style 21st.dev / shadcn) ---------- */
const Card = ({ children, className = '' }: { children: React.ReactNode; className?: string }) => (
  <div className={`rounded-2xl border border-[var(--border)] bg-[var(--card)]/80 backdrop-blur p-6 shadow-xl shadow-black/20 ${className}`}>
    {children}
  </div>
)

const Select = ({ name, value, onChange }: { name: keyof typeof OPTIONS; value: string; onChange: (v: string) => void }) => (
  <label className="block">
    <span className="mb-1.5 block text-xs font-semibold uppercase tracking-wide text-[var(--muted-foreground)]">{LABELS[name]}</span>
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="w-full rounded-xl border border-[var(--border)] bg-[#0d1424] px-3 py-2.5 text-sm text-white outline-none transition focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/30"
    >
      {OPTIONS[name].map((o) => <option key={o} value={o}>{o}</option>)}
    </select>
  </label>
)

const Slider = ({ label, value, min, max, onChange }: { label: string; value: number; min: number; max: number; onChange: (v: number) => void }) => (
  <label className="block">
    <span className="mb-2 flex items-center justify-between text-xs font-semibold uppercase tracking-wide text-[var(--muted-foreground)]">
      {label}<span className="mono rounded-md bg-emerald-500/10 px-2 py-0.5 text-sm text-emerald-400">{value}</span>
    </span>
    <input type="range" min={min} max={max} value={value} onChange={(e) => onChange(Number(e.target.value))} />
  </label>
)

const Kpi = ({ label, value, hint, accent }: { label: string; value: string; hint?: string; accent: string }) => (
  <Card className="relative overflow-hidden">
    <div className={`absolute -right-8 -top-8 h-24 w-24 rounded-full blur-2xl ${accent}`} />
    <p className="text-xs font-bold uppercase tracking-wider text-[var(--muted-foreground)]">{label}</p>
    <p className="mono mt-2 text-3xl font-bold text-white">{value}</p>
    {hint && <p className="mt-1 text-xs text-[var(--muted-foreground)]">{hint}</p>}
  </Card>
)

/* ---------- Jauge animée (SVG) ---------- */
function Gauge({ value, threshold, banked }: { value: number; threshold: number; banked: boolean }) {
  const R = 90, C = Math.PI * R // demi-cercle
  const color = banked ? '#10b981' : '#fbbf24'
  const angle = (threshold * 180 - 180) * (Math.PI / 180)
  const tx = 110 + (R + 4) * Math.cos(angle), ty = 110 + (R + 4) * Math.sin(angle)
  const tx2 = 110 + (R - 16) * Math.cos(angle), ty2 = 110 + (R - 16) * Math.sin(angle)
  return (
    <div className="relative mx-auto w-full max-w-[280px]">
      <svg viewBox="0 0 220 125" className="w-full">
        <path d="M 20 110 A 90 90 0 0 1 200 110" fill="none" stroke="#1e293b" strokeWidth="16" strokeLinecap="round" />
        <motion.path
          d="M 20 110 A 90 90 0 0 1 200 110" fill="none" stroke={color} strokeWidth="16" strokeLinecap="round"
          strokeDasharray={C} initial={{ strokeDashoffset: C }} animate={{ strokeDashoffset: C * (1 - value) }}
          transition={{ duration: 1.1, ease: 'easeOut' }} style={{ filter: `drop-shadow(0 0 8px ${color}80)` }}
        />
        <line x1={tx} y1={ty} x2={tx2} y2={ty2} stroke="#f43f5e" strokeWidth="3" strokeLinecap="round" />
      </svg>
      <div className="absolute inset-x-0 bottom-0 text-center">
        <motion.span key={value} initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} className="mono text-4xl font-bold text-white">
          {(value * 100).toFixed(1)}%
        </motion.span>
      </div>
    </div>
  )
}

/* ---------- Graphique en barres ---------- */
function RateChart({ title, data, horizontal = false }: { title: string; data: Rate[]; horizontal?: boolean }) {
  const sorted = useMemo(() => [...data].sort((a, b) => b.rate - a.rate), [data])
  return (
    <Card>
      <h3 className="mb-4 text-sm font-bold text-white">{title}</h3>
      <div style={{ height: horizontal ? sorted.length * 46 + 40 : 240 }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={sorted} layout={horizontal ? 'vertical' : 'horizontal'} margin={{ left: horizontal ? 70 : 0, right: 24 }}>
            <CartesianGrid stroke="#1e293b" strokeDasharray="3 3" horizontal={!horizontal} vertical={horizontal} />
            {horizontal ? (
              <>
                <XAxis type="number" stroke="#64748b" tickFormatter={(v) => `${v}%`} fontSize={12} />
                <YAxis type="category" dataKey="label" stroke="#94a3b8" fontSize={11} width={130} />
              </>
            ) : (
              <>
                <XAxis dataKey="label" stroke="#94a3b8" fontSize={12} />
                <YAxis stroke="#64748b" tickFormatter={(v) => `${v}%`} fontSize={12} />
              </>
            )}
            <Tooltip
              cursor={{ fill: 'rgba(16,185,129,0.06)' }}
              contentStyle={{ background: '#0d1424', border: '1px solid #1e293b', borderRadius: 12, color: '#fff' }}
              formatter={(v) => [`${v}%`, 'Bancarisés']}
            />
            <Bar dataKey="rate" isAnimationActive={false} radius={horizontal ? [0, 6, 6, 0] : [6, 6, 0, 0]}>
              {sorted.map((_, i) => <Cell key={i} fill={`rgba(16,185,129,${1 - i * (0.6 / Math.max(sorted.length, 1))})`} />)}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </Card>
  )
}

/* ---------- Application ---------- */
const TABS = [
  { id: 'predict', label: 'Prédiction', icon: Target },
  { id: 'data', label: 'Données', icon: BarChart3 },
  { id: 'models', label: 'Modèles', icon: Cpu },
] as const

export default function App() {
  const [tab, setTab] = useState<(typeof TABS)[number]['id']>('predict')
  const [form, setForm] = useState<Form>(INITIAL)
  const [result, setResult] = useState<Prediction | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [stats, setStats] = useState<Stats | null>(null)
  const [metrics, setMetrics] = useState<Metrics | null>(null)

  useEffect(() => {
    fetch('/api/stats').then((r) => r.json()).then(setStats).catch(() => {})
    fetch('/api/metrics').then((r) => r.json()).then(setMetrics).catch(() => {})
  }, [])

  const set = <K extends keyof Form>(k: K, v: Form[K]) => setForm((f) => {
    const next = { ...f, [k]: v }
    if (k === 'country') next.year = YEAR_BY_COUNTRY[v as string] ?? f.year
    return next
  })

  async function predict() {
    setLoading(true); setError(null)
    try {
      const r = await fetch('/api/predict', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form) })
      if (!r.ok) throw new Error((await r.json()).detail ?? 'Erreur du serveur')
      setResult(await r.json())
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Impossible de joindre l’API (est-elle lancée ?)')
    } finally { setLoading(false) }
  }

  const best = metrics?.best_model

  return (
    <div className="mx-auto max-w-6xl px-5 pb-16 pt-8">
      {/* En-tête */}
      <header className="mb-8 flex flex-wrap items-end justify-between gap-4">
        <div>
          <span className="inline-flex items-center gap-2 rounded-full border border-emerald-500/30 bg-emerald-500/10 px-3 py-1 text-xs font-semibold text-emerald-300">
            <Globe2 size={13} /> Zindi · Financial Inclusion in Africa
          </span>
          <h1 className="mt-3 text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
            Finclusion <span className="bg-gradient-to-r from-emerald-400 to-teal-300 bg-clip-text text-transparent">Africa</span>
          </h1>
          <p className="mt-2 max-w-2xl text-sm text-[var(--muted-foreground)]">
            Estimez la probabilité qu’une personne possède un compte bancaire en Afrique de l’Est à partir de son profil socio-démographique.
          </p>
        </div>
        {best && (
          <div className="text-right text-xs text-[var(--muted-foreground)]">
            Modèle actif <div className="mono mt-0.5 text-sm font-bold text-emerald-400">{best.model} · AUC {best.roc_auc.toFixed(3)}</div>
          </div>
        )}
      </header>

      {/* Onglets */}
      <nav className="mb-6 inline-flex rounded-xl border border-[var(--border)] bg-[var(--card)]/70 p-1">
        {TABS.map(({ id, label, icon: Icon }) => (
          <button key={id} onClick={() => setTab(id)}
            className={`relative flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-semibold transition ${tab === id ? 'text-white' : 'text-[var(--muted-foreground)] hover:text-white'}`}>
            {tab === id && <motion.span layoutId="tab" className="absolute inset-0 rounded-lg bg-emerald-500/15 ring-1 ring-emerald-500/40" />}
            <Icon size={16} className="relative" /><span className="relative">{label}</span>
          </button>
        ))}
      </nav>

      <AnimatePresence mode="wait">
        <motion.main key={tab} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.2 }}>
          {/* ===== PRÉDICTION ===== */}
          {tab === 'predict' && (
            <div className="grid gap-6 lg:grid-cols-5">
              <Card className="lg:col-span-3">
                <h2 className="mb-5 flex items-center gap-2 text-lg font-bold text-white"><Sparkles size={18} className="text-emerald-400" /> Profil de la personne</h2>
                <div className="grid gap-4 sm:grid-cols-2">
                  <Select name="country" value={form.country} onChange={(v) => set('country', v)} />
                  <Select name="location_type" value={form.location_type} onChange={(v) => set('location_type', v)} />
                  <Select name="gender_of_respondent" value={form.gender_of_respondent} onChange={(v) => set('gender_of_respondent', v)} />
                  <Select name="cellphone_access" value={form.cellphone_access} onChange={(v) => set('cellphone_access', v)} />
                  <Slider label="Âge" value={form.age_of_respondent} min={16} max={100} onChange={(v) => set('age_of_respondent', v)} />
                  <Slider label="Taille du ménage" value={form.household_size} min={1} max={20} onChange={(v) => set('household_size', v)} />
                  <Select name="education_level" value={form.education_level} onChange={(v) => set('education_level', v)} />
                  <Select name="job_type" value={form.job_type} onChange={(v) => set('job_type', v)} />
                  <Select name="marital_status" value={form.marital_status} onChange={(v) => set('marital_status', v)} />
                  <Select name="relationship_with_head" value={form.relationship_with_head} onChange={(v) => set('relationship_with_head', v)} />
                </div>
                <button onClick={predict} disabled={loading}
                  className="mt-6 flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-400 px-5 py-3 text-sm font-bold text-[#04130d] shadow-lg shadow-emerald-500/20 transition hover:brightness-110 active:scale-[0.99] disabled:opacity-60">
                  {loading ? <Loader2 size={18} className="animate-spin" /> : <Target size={18} />} Calculer la probabilité
                </button>
                {error && <p className="mt-3 rounded-lg border border-red-500/30 bg-red-500/10 px-3 py-2 text-sm text-red-300">{error}</p>}
              </Card>

              <Card className="flex flex-col justify-center lg:col-span-2">
                {!result ? (
                  <div className="py-10 text-center text-sm text-[var(--muted-foreground)]">
                    <Target size={36} className="mx-auto mb-3 opacity-40" />
                    Renseignez un profil puis lancez le calcul.
                  </div>
                ) : (
                  <motion.div initial={{ opacity: 0, scale: 0.97 }} animate={{ opacity: 1, scale: 1 }}>
                    <Gauge value={result.probability} threshold={result.threshold} banked={result.banked} />
                    <div className={`mt-5 flex items-start gap-3 rounded-xl border p-4 ${result.banked ? 'border-emerald-500/30 bg-emerald-500/10' : 'border-amber-400/30 bg-amber-400/10'}`}>
                      {result.banked ? <CheckCircle2 className="mt-0.5 shrink-0 text-emerald-400" /> : <XCircle className="mt-0.5 shrink-0 text-amber-300" />}
                      <div>
                        <p className={`text-sm font-bold ${result.banked ? 'text-emerald-300' : 'text-amber-200'}`}>
                          {result.banked ? 'Profil probablement bancarisé' : 'Profil probablement non bancarisé'}
                        </p>
                        <p className="mt-1 text-xs leading-relaxed text-[var(--muted-foreground)]">
                          Seuil de décision : <span className="mono">{(result.threshold * 100).toFixed(1)}%</span> (marqueur rouge), choisi pour maximiser le F1-score.
                        </p>
                      </div>
                    </div>
                  </motion.div>
                )}
              </Card>
            </div>
          )}

          {/* ===== DONNÉES ===== */}
          {tab === 'data' && (
            stats ? (
              <div className="space-y-6">
                <div className="grid gap-4 sm:grid-cols-3">
                  <Kpi label="Personnes enquêtées" value={stats.total.toLocaleString('fr-FR')} hint="Train.csv" accent="bg-emerald-500/30" />
                  <Kpi label="Taux de bancarisation" value={`${stats.banked_rate}%`} hint="Cible déséquilibrée" accent="bg-sky-500/30" />
                  <Kpi label="Pays" value="4" hint="Kenya · Rwanda · Tanzanie · Ouganda" accent="bg-amber-400/30" />
                </div>
                <div className="grid gap-6 lg:grid-cols-2">
                  <RateChart title="Bancarisation par pays" data={stats.by_country} />
                  <RateChart title="Bancarisation par niveau d’éducation" data={stats.by_education} horizontal />
                </div>
                <RateChart title="Bancarisation par type d’emploi" data={stats.by_job} horizontal />
              </div>
            ) : <p className="text-sm text-[var(--muted-foreground)]">Chargement… (l’API est-elle lancée ?)</p>
          )}

          {/* ===== MODÈLES ===== */}
          {tab === 'models' && (
            metrics && best ? (
              <div className="space-y-6">
                <div className="grid gap-4 sm:grid-cols-4">
                  <Kpi label="Meilleur modèle" value={best.model} accent="bg-emerald-500/30" />
                  <Kpi label="ROC-AUC" value={best.roc_auc.toFixed(4)} accent="bg-sky-500/30" />
                  <Kpi label="F1-score" value={best.f1_score.toFixed(4)} hint={`Seuil ${best.threshold.toFixed(2)}`} accent="bg-amber-400/30" />
                  <Kpi label="Accuracy" value={`${(best.accuracy * 100).toFixed(1)}%`} accent="bg-fuchsia-500/30" />
                </div>
                <Card className="overflow-x-auto">
                  <h3 className="mb-4 text-sm font-bold text-white">Comparaison des modèles (jeu de test)</h3>
                  <table className="w-full min-w-[560px] text-sm">
                    <thead>
                      <tr className="border-b border-[var(--border)] text-left text-xs uppercase tracking-wide text-[var(--muted-foreground)]">
                        {['Modèle', 'Accuracy', 'Précision', 'Rappel', 'F1', 'ROC-AUC'].map((h) => <th key={h} className="pb-3 pr-4 font-semibold">{h}</th>)}
                      </tr>
                    </thead>
                    <tbody>
                      {metrics.all_models.map((m) => (
                        <tr key={m.model} className={`border-b border-[var(--border)]/60 ${m.model === best.model ? 'bg-emerald-500/5' : ''}`}>
                          <td className="py-3 pr-4 font-semibold text-white">{m.model.replace('_', ' ')}{m.model === best.model && <span className="ml-2 rounded-full bg-emerald-500/20 px-2 py-0.5 text-[11px] text-emerald-300">retenu</span>}</td>
                          <td className="mono pr-4">{(m.accuracy * 100).toFixed(1)}%</td>
                          <td className="mono pr-4">{(m.precision * 100).toFixed(1)}%</td>
                          <td className="mono pr-4">{(m.recall * 100).toFixed(1)}%</td>
                          <td className="mono pr-4">{m.f1_score.toFixed(4)}</td>
                          <td className="mono pr-4 text-emerald-400">{m.roc_auc.toFixed(4)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </Card>
              </div>
            ) : <p className="text-sm text-[var(--muted-foreground)]">Chargement… (l’API est-elle lancée ?)</p>
          )}
        </motion.main>
      </AnimatePresence>
    </div>
  )
}
