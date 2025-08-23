import { useEffect, useState } from 'react'
import PageHeader from '@/components/PageHeader'
import Button from '@/components/Button'
import { getAnalytics } from '@/lib/api'
import type { AnalyticsData } from '@/lib/schemas'

export default function Analytics(){
	const [data, setData] = useState<AnalyticsData|undefined>()
	const [loading, setLoading] = useState(true)

	const load = async ()=>{
		setLoading(true)
		const resp = await getAnalytics()
		setData(resp)
		setLoading(false)
	}

	useEffect(()=>{ load() }, [])

	return (
		<div>
			<PageHeader title="Analytics" subtitle="Operational KPIs and band distribution" actions={<Button onClick={load} variant='subtle'>Refresh</Button>} />
			<div className="grid grid-cols-12 gap-6">
				<div className="col-span-12">
					<div className="grid grid-cols-2 md:grid-cols-4 gap-4">
						{['precision','recall','alert_volumes','sla_ms'].map((k)=> (
							<div key={k} className="rounded border border-border/60 p-4 bg-neutral-950">
								<div className="text-xs text-gray-400 uppercase">{k.replace('_',' ')}</div>
								<div className="text-2xl mt-1">{ loading ? '…' : (data as any)?.[k] ?? 'N/A' }</div>
							</div>
						))}
					</div>
				</div>
				<div className="col-span-12">
					<div className="rounded border border-border/60 p-4 bg-neutral-950">
						<div className="text-sm text-gray-300 mb-2">Band Distribution</div>
						{loading ? 'Loading…' : (
							<div className="flex items-end gap-2 h-40" role="figure" aria-label="Band distribution">
								{(['low','medium','high'] as const).map((band)=>{
									const v = data?.band_distribution[band] ?? 0
									return <div key={band} className="flex-1 flex flex-col items-center" aria-label={`${band} ${v}`}>
										<div className="w-full bg-neutral-800" style={{height: `${v/2}%`}} />
										<span className="text-xs mt-1">{band}</span>
									</div>
								})}
							</div>
						)}
					</div>
				</div>
				<div className="col-span-12">
					<div className="rounded border border-border/60 p-4 bg-neutral-950">
						<div className="text-sm text-gray-300 mb-2">Raw Data (JSON)</div>
						<pre className="text-xs overflow-auto bg-neutral-900 p-3 rounded">
							{JSON.stringify(data ?? {}, null, 2)}
						</pre>
					</div>
				</div>
			</div>
		</div>
	)
}


