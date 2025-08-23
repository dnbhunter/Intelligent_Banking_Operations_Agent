import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import PageHeader from '@/components/PageHeader'
import Button from '@/components/Button'
import { Card, CardContent, CardHeader } from '@/components/ui/Card'
import { Input, Select } from '@/components/ui/Inputs'
import { FraudPayloadSchema, type FraudPayload } from '@/lib/schemas'
import { runFraudTriage } from '@/lib/api'
import { useAppStore } from '@/store/useAppStore'
import { toast } from 'sonner'
import { AnimatePresence, motion } from 'framer-motion'

export default function FraudTriage(){
	const { setFraud } = useAppStore()
	const [result, setResult] = useState<ReturnType<typeof Object> | null>(null)
	const { register, handleSubmit, formState: { errors, isSubmitting }, reset } = useForm<FraudPayload>({
		resolver: zodResolver(FraudPayloadSchema),
		defaultValues: {
			amount: 120,
			currency: 'USD',
			merchant: 'Test Merchant',
			mcc: '7995',
			geo: 'US-NY',
			device_id: 'dev-123',
			account_id: 'acct-001',
			channel: 'ecommerce',
		},
	})

	const onSubmit = async (data: FraudPayload) => {
		try {
			const resp = await runFraudTriage(data)
			setResult(resp as any)
			setFraud(data, resp)
			toast.success(`Fraud: ${resp.decision} - Score ${resp.score}`)
		} catch (error) {
			console.error(error)
			toast.error('An unexpected error occurred.', {
				description: error instanceof Error ? error.message : 'Please check the console for more details.'
			})
		}
	}

	return (
		<div>
			<PageHeader title="Fraud Triage" subtitle="Run triage with explainable rationale" actions={<Button variant='subtle' onClick={()=>reset()}>Reset form</Button>} />
			<div className="grid grid-cols-12 gap-6">
				<form className="col-span-12 md:col-span-6 space-y-4" onSubmit={handleSubmit(onSubmit)} aria-label="Fraud Triage Form">
					<Card>
						<CardHeader title="Transaction" subtitle="Enter transaction details" />
						<CardContent>
							<div className="grid grid-cols-2 gap-4">
								<Input type="number" step="1" {...register('amount', { valueAsNumber: true })} label="Amount" />{errors.amount && <span className="text-red-400">{errors.amount.message}</span>}
								<Select {...register('currency')} label="Currency"><option>USD</option><option>EUR</option><option>INR</option></Select>{errors.currency && <span className="text-red-400">{errors.currency.message}</span>}
								<Input {...register('merchant')} label="Merchant" />{errors.merchant && <span className="text-red-400">{errors.merchant.message}</span>}
								<Input {...register('mcc')} label="MCC" />{errors.mcc && <span className="text-red-400">{errors.mcc.message}</span>}
								<Input {...register('geo')} label="Geo" />{errors.geo && <span className="text-red-400">{errors.geo.message}</span>}
								<Input {...register('device_id')} label="Device ID" />{errors.device_id && <span className="text-red-400">{errors.device_id.message}</span>}
								<Input {...register('account_id')} label="Account ID" />{errors.account_id && <span className="text-red-400">{errors.account_id.message}</span>}
								<Select {...register('channel')} label="Channel"><option>ecommerce</option><option>pos</option><option>atm</option><option>p2p</option></Select>{errors.channel && <span className="text-red-400">{errors.channel.message}</span>}
							</div>
							<div className="mt-4">
								<Button type="submit" disabled={isSubmitting}>{isSubmitting ? 'Running…' : 'Run Fraud Triage'}</Button>
							</div>
						</CardContent>
					</Card>
				</form>
				<div className="col-span-12 md:col-span-6">
					<AnimatePresence mode="wait">
						{result ? (
							<motion.div key="result" initial={{opacity: 0, y: 8}} animate={{opacity: 1, y: 0}} exit={{opacity: 0, y: -6}} transition={{duration: 0.15}} className="rounded border border-border/60 p-4 bg-neutral-950">
								<div className="flex items-center gap-3 mb-2">
									<span className={`px-2 py-1 rounded text-xs ${result.decision==='approve'?'bg-green-600':result.decision==='review'?'bg-amber-600':'bg-red-600'}`}>{(result as any).decision}</span>
									<div className="text-sm text-gray-300">Score {(result as any).score}</div>
								</div>
								<ul className="list-disc pl-5 text-sm">
									{(result as any).reasons?.map((r:string, i:number)=>(<li key={i}>{r}</li>))}
								</ul>
								{(result as any).sla_ms && <div className="text-xs text-gray-400 mt-2">SLA {(result as any).sla_ms} ms</div>}
							</motion.div>
						) : (
							<motion.div key="placeholder" initial={{opacity: 0}} animate={{opacity: 1}} exit={{opacity: 0}} className="rounded border border-dashed border-border/60 p-8 text-center text-gray-400">No results yet</motion.div>
						)}
					</AnimatePresence>
				</div>
			</div>
		</div>
	)
}


