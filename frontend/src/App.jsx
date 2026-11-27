import { useEffect, useMemo, useState } from 'react'
import { initialData } from './mockData'
import './App.css'

const sections = [
  { id: 'dashboard', name: 'Resumen general', icon: '▦' },
  { id: 'proveedores', name: 'Proveedores', icon: '♙' },
  { id: 'publicaciones', name: 'Publicaciones', icon: '▤' },
  { id: 'indicadores', name: 'Indicadores', icon: '▥' },
  { id: 'notificaciones', name: 'Notificaciones', icon: '✉' },
  { id: 'portal', name: 'Vista proveedor (demo)', icon: '◉' },
]
const storageKey = 'haceb-estudia-mvp-demo-v1'
const validSections = new Set(sections.map(s => s.id))
function sectionFromUrl() {
  const name = window.location.pathname.split('/').filter(Boolean).pop()
  return validSections.has(name) ? name : 'dashboard'
}
function loadData() {
  try {
    const value = window.localStorage.getItem(storageKey)
    if (!value) return structuredClone(initialData)
    const parsed = JSON.parse(value)
    if (['proveedores', 'publicaciones', 'indicadores', 'notificaciones'].every(k => Array.isArray(parsed[k]))) return parsed
  } catch { /* usar la semilla ficticia */ }
  return structuredClone(initialData)
}
const formatPeriod = value => {
  if (!value) return 'Sin período'
  const [year, month] = value.split('-').map(Number)
  return new Intl.DateTimeFormat('es-CO', { month: 'long', year: 'numeric' }).format(new Date(year, month - 1, 1))
}
const dateText = value => value ? new Intl.DateTimeFormat('es-CO', { day: '2-digit', month: 'short', year: 'numeric' }).format(new Date(value)) : 'Sin publicar'
const nextId = items => Math.max(0, ...items.map(item => item.id)) + 1
const Badge = ({ children, tone = 'neutral' }) => <span className={`badge badge--${tone}`}>{children}</span>
const Status = ({ value }) => <Badge tone={value === 'PUBLICADO' || value === 'ENVIADO' || value === 'Activo' ? 'good' : value === 'BORRADOR' || value === 'PENDIENTE' ? 'warning' : value === 'FALLIDO' || value === 'Inactivo' ? 'danger' : 'neutral'}>{value}</Badge>
const Empty = ({ title, detail }) => <div className="empty-state"><div className="empty-icon">⌕</div><strong>{title}</strong><p>{detail}</p></div>
const Card = ({ title, children, extra }) => <section className="panel"><div className="panel-head"><h2>{title}</h2>{extra}</div>{children}</section>

function App() {
  const [data, setData] = useState(loadData)
  const [page, setPage] = useState(sectionFromUrl)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [search, setSearch] = useState('')
  const [selectedSupplier, setSelectedSupplier] = useState(null)
  const [newPeriod, setNewPeriod] = useState('2026-11')
  const [indicatorForm, setIndicatorForm] = useState({ proveedor_id: '1', publicacion_id: '2', nombre: 'Cumplimiento de entregas', valor: '', unidad: '%' })
  const [feedback, setFeedback] = useState('')
  const [portalSupplier, setPortalSupplier] = useState('1')
  const [portalPeriod, setPortalPeriod] = useState('2026-09')
  const [confirmPublish, setConfirmPublish] = useState(null)
  const [showHelp, setShowHelp] = useState(false)

  useEffect(() => { window.localStorage.setItem(storageKey, JSON.stringify(data)) }, [data])
  useEffect(() => {
    const handler = () => { setPage(sectionFromUrl()); setSidebarOpen(false) }
    window.addEventListener('popstate', handler)
    return () => window.removeEventListener('popstate', handler)
  }, [])
  const navigate = id => {
    setPage(id); setSidebarOpen(false); setFeedback(''); setSelectedSupplier(null)
    window.history.pushState({}, '', `/admin/${id}`)
  }
  const notify = value => { setFeedback(value); window.scrollTo({ top: 0, behavior: 'smooth' }) }
  const draftPublications = data.publicaciones.filter(p => p.estado === 'BORRADOR')
  const publishedPublications = data.publicaciones.filter(p => p.estado === 'PUBLICADO')
  const activeSuppliers = data.proveedores.filter(p => p.activo).length
  const getSupplier = id => data.proveedores.find(p => p.id === Number(id))
  const getPublication = id => data.publicaciones.find(p => p.id === Number(id))
  const filteredSuppliers = useMemo(() => data.proveedores.filter(p => `${p.nombre} ${p.nit}`.toLowerCase().includes(search.toLowerCase())), [data.proveedores, search])
  const portalPeriods = publishedPublications.filter(pub => data.indicadores.some(i => i.publicacion_id === pub.id && i.proveedor_id === Number(portalSupplier)))
  const portalIndicators = data.indicadores.filter(i => i.proveedor_id === Number(portalSupplier) && publishedPublications.some(p => p.id === i.publicacion_id && p.periodo === portalPeriod))
  const resetDemo = () => { if (!window.confirm('¿Restablecer todos los datos ficticios del navegador?')) return; setData(structuredClone(initialData)); notify('Datos de demostración restablecidos.') }

  const createPublication = e => {
    e.preventDefault()
    if (!/^\d{4}-(0[1-9]|1[0-2])$/.test(newPeriod)) return notify('Selecciona un período válido.')
    if (data.publicaciones.some(p => p.periodo === newPeriod)) return notify('Ese período ya existe. No se permiten duplicados.')
    const item = { id: nextId(data.publicaciones), periodo: newPeriod, estado: 'BORRADOR', fecha_publicacion: null }
    setData(prev => ({ ...prev, publicaciones: [...prev.publicaciones, item] }))
    setIndicatorForm(prev => ({ ...prev, publicacion_id: String(item.id) }))
    notify(`Período ${formatPeriod(newPeriod)} creado en BORRADOR (solo demo).`)
  }
  const createIndicator = e => {
    e.preventDefault()
    const supplier = getSupplier(indicatorForm.proveedor_id)
    const publication = getPublication(indicatorForm.publicacion_id)
    const value = Number(indicatorForm.valor)
    if (!supplier || !publication || publication.estado !== 'BORRADOR') return notify('Selecciona un proveedor y una publicación en borrador.')
    if (!indicatorForm.nombre.trim() || indicatorForm.valor.trim() === '' || !Number.isFinite(value)) return notify('Completa el nombre y el valor numérico del indicador.')
    const item = { id: nextId(data.indicadores), proveedor_id: supplier.id, publicacion_id: publication.id, nombre: indicatorForm.nombre.trim(), valor: value, unidad: indicatorForm.unidad.trim() || '%' }
    setData(prev => ({ ...prev, indicadores: [...prev.indicadores, item] }))
    setIndicatorForm(prev => ({ ...prev, valor: '' }))
    notify('Indicador registrado en el borrador (solo demo).')
  }
  const publish = id => {
    const item = getPublication(id)
    if (!item || item.estado !== 'BORRADOR') return notify('Este período no se puede publicar.')
    const related = data.indicadores.filter(i => i.publicacion_id === id)
    if (!related.length) return notify('Agrega al menos un indicador antes de publicar.')
    const supplierIds = [...new Set(related.map(i => i.proveedor_id))]
    const emails = supplierIds.map(supplierId => getSupplier(supplierId)).filter(Boolean)
    setData(prev => ({
      ...prev,
      publicaciones: prev.publicaciones.map(p => p.id === id ? { ...p, estado: 'PUBLICADO', fecha_publicacion: new Date().toISOString() } : p),
      notificaciones: [...prev.notificaciones, ...emails.map((p, index) => ({ id: nextId(prev.notificaciones) + index, proveedor_id: p.id, publicacion_id: id, correo_destino: p.correo, fecha_envio: null, estado: 'PENDIENTE', error: null }))],
    }))
    setConfirmPublish(null)
    notify(`${formatPeriod(item.periodo)} publicado en la simulación. Se generaron ${emails.length} notificaciones PENDIENTE; no se enviaron correos.`)
  }

  return (
    <div className="app-shell">
      <aside className={`sidebar ${sidebarOpen ? 'sidebar--open' : ''}`}>
        <div className="brand"><div className="brand-mark">H</div><div><strong>HACEB</strong><small>Portal de indicadores</small></div></div>
        <div className="sidebar-caption">ESPACIO DE TRABAJO</div>
        <nav className="nav-menu" aria-label="Navegación principal">
          {sections.map(section => <button key={section.id} type="button" className={`nav-link ${page === section.id ? 'nav-link--active' : ''}`} onClick={() => navigate(section.id)}><span className="nav-icon" aria-hidden="true">{section.icon}</span>{section.name}</button>)}
        </nav>
        <div className="sidebar-foot"><div className="demo-notice"><strong>ENTORNO DE DEMOSTRACIÓN</strong><span>Datos ficticios en este navegador. Sin conexión a FastAPI.</span></div><button type="button" className="sidebar-reset" onClick={resetDemo}>↻ Restablecer datos demo</button></div>
      </aside>
      {sidebarOpen && <button type="button" className="mobile-overlay" aria-label="Cerrar menú" onClick={() => setSidebarOpen(false)} />}
      <div className="workspace">
        <header className="topbar"><button type="button" className="hamburger" onClick={() => setSidebarOpen(true)} aria-label="Abrir menú">☰</button><div className="breadcrumbs">Plataforma de proveedores <span> / </span> <strong>{sections.find(s => s.id === page)?.name}</strong></div><div className="topbar-user"><Badge tone="info">MODO DEMO</Badge><div className="avatar">AD</div><span>Administrador demo</span></div></header>
        <main className="main-content">
          <div className="page-heading"><div><p className="eyebrow">ESTUDIA · PROTOTIPO ACADÉMICO</p><h1>{page === 'dashboard' ? 'Resumen general' : sections.find(s => s.id === page)?.name}</h1><p>Gestión centralizada de indicadores de proveedores nacionales.</p></div><button type="button" className="btn btn--ghost" onClick={() => setShowHelp(true)}>ⓘ Acerca de esta demo</button></div>
          {feedback && <div className="feedback" role="status"><span>{feedback}</span><button aria-label="Cerrar mensaje" type="button" onClick={() => setFeedback('')}>×</button></div>}
          {page === 'dashboard' && <>
            <div className="stats">
              <div className="stat-card"><span>Proveedores registrados</span><strong>{data.proveedores.length}</strong><small>{activeSuppliers} activos</small></div>
              <div className="stat-card"><span>Indicadores cargados</span><strong>{data.indicadores.length}</strong><small>De todos los períodos</small></div>
              <div className="stat-card"><span>Períodos publicados</span><strong>{publishedPublications.length}</strong><small>{draftPublications.length} en borrador</small></div>
              <div className="stat-card"><span>Avisos pendientes</span><strong>{data.notificaciones.filter(n => n.estado === 'PENDIENTE').length}</strong><small>Sin envío real de correos</small></div>
            </div>
            <div className="two-columns"><Card title="Publicaciones mensuales" extra={<button className="text-action" onClick={() => navigate('publicaciones')}>Ver todas →</button>}><div className="table-scroll"><table><thead><tr><th>Período</th><th>Estado</th><th>Fecha</th></tr></thead><tbody>{[...data.publicaciones].sort((a,b) => b.periodo.localeCompare(a.periodo)).map(p => <tr key={p.id}><td><strong>{formatPeriod(p.periodo)}</strong></td><td><Status value={p.estado}/></td><td>{dateText(p.fecha_publicacion)}</td></tr>)}</tbody></table></div></Card>
            <Card title="Flujo del MVP"><div className="steps"><div><b>01</b><span><strong>Registrar indicadores</strong><small>Asociar proveedor y período</small></span></div><div><b>02</b><span><strong>Publicar el período</strong><small>Habilitar visibilidad del proveedor</small></span></div><div><b>03</b><span><strong>Consultar resultados</strong><small>Ver solo los publicados en el modo demo</small></span></div></div><button className="btn btn--primary" onClick={() => navigate('publicaciones')}>Gestionar publicaciones →</button></Card></div>
          </>}
          {page === 'proveedores' && <Card title="Directorio de proveedores" extra={<Badge tone="neutral">{filteredSuppliers.length} resultados</Badge>}><div className="toolbar"><input className="search-input" value={search} onChange={e => setSearch(e.target.value)} placeholder="Buscar por nombre o NIT…" aria-label="Buscar por nombre o NIT" /></div><div className="table-scroll"><table><thead><tr><th>NIT</th><th>Razón social</th><th>Correo</th><th>Estado</th><th></th></tr></thead><tbody>{filteredSuppliers.map(p => <tr key={p.id}><td>{p.nit}</td><td><strong>{p.nombre}</strong></td><td>{p.correo}</td><td><Status value={p.activo ? 'Activo' : 'Inactivo'}/></td><td><button className="text-action" onClick={() => setSelectedSupplier(p)}>Ver detalle</button></td></tr>)}</tbody></table></div>{filteredSuppliers.length === 0 && <Empty title="No encontramos proveedores" detail="Intenta otra búsqueda por nombre o NIT."/>}</Card>}
          {page === 'publicaciones' && <div className="two-columns two-columns--wide"><Card title="Publicaciones mensuales"><div className="table-scroll"><table><thead><tr><th>Período</th><th>Estado</th><th>Indicadores</th><th>Acción</th></tr></thead><tbody>{[...data.publicaciones].sort((a,b) => b.periodo.localeCompare(a.periodo)).map(p => <tr key={p.id}><td><strong>{formatPeriod(p.periodo)}</strong></td><td><Status value={p.estado}/></td><td>{data.indicadores.filter(i => i.publicacion_id === p.id).length}</td><td>{p.estado === 'BORRADOR' ? <button className="btn btn--small btn--primary" onClick={() => setConfirmPublish(p.id)}>Publicar</button> : <span className="muted">Publicado</span>}</td></tr>)}</tbody></table></div></Card><Card title="Nuevo período"><form onSubmit={createPublication} className="form-stack"><label>Mes de publicación<input required type="month" value={newPeriod} onChange={e => setNewPeriod(e.target.value)}/></label><p className="muted">Todo período nuevo comienza en estado BORRADOR.</p><button className="btn btn--primary" type="submit">+ Crear período</button></form></Card></div>}
          {page === 'indicadores' && <div className="content-stack"><Card title="Registrar indicador (demo)"><form onSubmit={createIndicator} className="form-grid"><label>Proveedor<select value={indicatorForm.proveedor_id} onChange={e => setIndicatorForm(v => ({ ...v, proveedor_id: e.target.value }))}>{data.proveedores.filter(p => p.activo).map(p => <option key={p.id} value={p.id}>{p.nombre}</option>)}</select></label><label>Período en borrador<select value={indicatorForm.publicacion_id} onChange={e => setIndicatorForm(v => ({ ...v, publicacion_id: e.target.value }))}>{draftPublications.map(p => <option key={p.id} value={p.id}>{formatPeriod(p.periodo)}</option>)}</select></label><label>Nombre del indicador<input required value={indicatorForm.nombre} onChange={e => setIndicatorForm(v => ({ ...v, nombre: e.target.value }))}/></label><label>Valor<input type="number" step="any" required value={indicatorForm.valor} onChange={e => setIndicatorForm(v => ({ ...v, valor: e.target.value }))} placeholder="Ej.: 95.5"/></label><label>Unidad<input required value={indicatorForm.unidad} onChange={e => setIndicatorForm(v => ({ ...v, unidad: e.target.value }))} placeholder="%, días, unidades"/></label><div className="form-action"><button className="btn btn--primary" disabled={!draftPublications.length} type="submit">+ Guardar indicador</button></div></form>{!draftPublications.length && <p className="muted">Primero crea un nuevo período en borrador.</p>}</Card><Card title="Indicadores registrados"><div className="table-scroll"><table><thead><tr><th>Proveedor</th><th>Período</th><th>Indicador</th><th>Resultado</th><th>Estado</th></tr></thead><tbody>{data.indicadores.map(i => <tr key={i.id}><td>{getSupplier(i.proveedor_id)?.nombre ?? '—'}</td><td>{getPublication(i.publicacion_id)?.periodo ?? '—'}</td><td><strong>{i.nombre}</strong></td><td>{i.valor} {i.unidad}</td><td><Status value={getPublication(i.publicacion_id)?.estado ?? '—'}/></td></tr>)}</tbody></table></div></Card></div>}
          {page === 'notificaciones' && <Card title="Historial de notificaciones simuladas" extra={<Badge tone="neutral">No se envían correos reales</Badge>}><div className="table-scroll"><table><thead><tr><th>Destinatario</th><th>Período</th><th>Estado</th><th>Fecha</th></tr></thead><tbody>{data.notificaciones.map(n => <tr key={n.id}><td>{n.correo_destino}</td><td>{getPublication(n.publicacion_id)?.periodo ?? '—'}</td><td><Status value={n.estado}/></td><td>{dateText(n.fecha_envio)}</td></tr>)}</tbody></table></div>{!data.notificaciones.length && <Empty title="Sin notificaciones" detail="Publica un período para generar avisos de demostración."/>}</Card>}
          {page === 'portal' && <div className="content-stack"><div className="demo-callout">Esta vista es una <strong>simulación educativa del proveedor</strong>, no una sesión autenticada. La seguridad real requiere FastAPI y permisos de backend.</div><Card title="Consultar indicadores como proveedor"><div className="form-grid"><label>Proveedor ficticio<select value={portalSupplier} onChange={e => { setPortalSupplier(e.target.value); setPortalPeriod('') }}>{data.proveedores.map(p => <option key={p.id} value={p.id}>{p.nombre}</option>)}</select></label><label>Período publicado<select value={portalPeriod} onChange={e => setPortalPeriod(e.target.value)}><option value="">Seleccionar período</option>{portalPeriods.map(p => <option key={p.id} value={p.periodo}>{formatPeriod(p.periodo)}</option>)}</select></label></div><div className="portal-results">{portalPeriod && portalIndicators.length ? <div className="result-grid">{portalIndicators.map(i => <div className="result-card" key={i.id}><small>{i.nombre}</small><strong>{i.valor} <span>{i.unidad}</span></strong><p>{formatPeriod(portalPeriod)}</p></div>)}</div> : <Empty title="No hay indicadores publicados para mostrar" detail="Selecciona un período publicado con indicadores. Los borradores nunca aparecen aquí."/>}</div></Card></div>}
          <footer className="footer">EstudIA · MVP académico · Datos ficticios · Sin conexión a servicios productivos</footer>
        </main>
      </div>
      {selectedSupplier && <div className="modal-backdrop" role="presentation" onClick={() => setSelectedSupplier(null)}><div className="modal" role="dialog" aria-modal="true" aria-label="Detalle del proveedor" onClick={e => e.stopPropagation()}><div className="modal-header"><h2>Detalle del proveedor</h2><button aria-label="Cerrar" onClick={() => setSelectedSupplier(null)}>×</button></div><dl className="detail-list"><div><dt>Razón social</dt><dd>{selectedSupplier.nombre}</dd></div><div><dt>NIT</dt><dd>{selectedSupplier.nit}</dd></div><div><dt>Correo de contacto</dt><dd>{selectedSupplier.correo}</dd></div><div><dt>Estado</dt><dd><Status value={selectedSupplier.activo ? 'Activo' : 'Inactivo'}/></dd></div></dl><button className="btn btn--primary" onClick={() => setSelectedSupplier(null)}>Cerrar</button></div></div>}
      {confirmPublish !== null && <div className="modal-backdrop" role="presentation" onClick={() => setConfirmPublish(null)}><div className="modal" role="dialog" aria-modal="true" aria-label="Confirmar publicación" onClick={e => e.stopPropagation()}><div className="modal-header"><h2>Confirmar publicación</h2><button aria-label="Cerrar" onClick={() => setConfirmPublish(null)}>×</button></div><p>¿Publicar <strong>{formatPeriod(getPublication(confirmPublish)?.periodo)}</strong> en la demostración?</p><p className="muted">Los indicadores pasarán a ser visibles en la vista simulada del proveedor y se generarán notificaciones pendientes. No se enviarán correos.</p><div className="modal-actions"><button className="btn btn--ghost" onClick={() => setConfirmPublish(null)}>Cancelar</button><button className="btn btn--primary" onClick={() => publish(confirmPublish)}>Confirmar publicación</button></div></div></div>}
      {showHelp && <div className="modal-backdrop" role="presentation" onClick={() => setShowHelp(false)}><div className="modal" role="dialog" aria-modal="true" aria-label="Acerca de la demostración" onClick={e => e.stopPropagation()}><div className="modal-header"><h2>Acerca de la demostración</h2><button aria-label="Cerrar" onClick={() => setShowHelp(false)}>×</button></div><p>Esta interfaz presenta una simulación académica del proceso de publicación de indicadores para proveedores.</p><p>Todos los datos son ficticios y los cambios se conservan únicamente en el almacenamiento local de este navegador.</p><p className="muted">No hay autenticación real, base de datos, conexión con Power BI ni envío de correos. Estas funcionalidades requieren los módulos de backend e integración.</p><button className="btn btn--primary" onClick={() => setShowHelp(false)}>Entendido</button></div></div>}
    </div>
  )
}

export default App
