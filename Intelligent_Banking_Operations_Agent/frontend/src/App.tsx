import { useEffect, useState } from 'react'
import { NavLink, Route, Routes } from 'react-router-dom'
import { Toaster } from 'sonner'
import { motion, AnimatePresence } from 'framer-motion'
import FraudTriage from '@/pages/FraudTriage'
import CreditTriage from '@/pages/CreditTriage'
import Analytics from '@/pages/Analytics'
import Button from './components/Button';
import HelpModal from './components/HelpModal';

function Header() {
	const [isHelpVisible, setHelpVisible] = useState(false);
	const [isDarkMode, setDarkMode] = useState(true);

	useEffect(() => {
		document.documentElement.classList.toggle('dark', isDarkMode);
	}, [isDarkMode]);

	return (
		<header className="border-b border-border/60 sticky top-0 z-40 backdrop-blur bg-black/40">
			<div className="container-max h-14 flex items-center justify-between">
				<div className="flex items-center gap-3">
					<div className="w-7 h-7 rounded bg-primary shadow-soft" aria-hidden />
					<h1 className="text-sm sm:text-base font-semibold tracking-wide">Intelligent Banking Operations Agent</h1>
				</div>
				<nav className="hidden sm:flex items-center gap-2 text-sm">
					<NavLink to="/" className={({isActive}) => isActive ? 'font-semibold border-b-2 border-primary pb-1' : 'text-gray-300 hover:text-white pb-1'}>Fraud Triage</NavLink>
					<NavLink to="/credit" className={({isActive}) => isActive ? 'font-semibold border-b-2 border-primary pb-1' : 'text-gray-300 hover:text-white pb-1'}>Credit Triage</NavLink>
					<NavLink to="/analytics" className={({isActive}) => isActive ? 'font-semibold border-b-2 border-primary pb-1' : 'text-gray-300 hover:text-white pb-1'}>Analytics</NavLink>
				</nav>
				<div className="flex items-center gap-2">
					<Button variant="ghost" size="icon" onClick={() => setDarkMode(p => !p)} aria-label="Toggle theme">
						{isDarkMode ? '☀️' : '🌙'}
					</Button>
					<Button variant="ghost" size="icon" onClick={() => setHelpVisible(true)} aria-label="Help">?</Button>
				</div>
			</div>
			{isHelpVisible && <HelpModal onClose={() => setHelpVisible(false)} />}
		</header>
	)
}

export default function App() {
	return (
		<div className="min-h-full">
			<Header />
			<Toaster position="top-right" richColors />
			<main className="container-max py-6">
				<AnimatePresence mode="wait">
					<Routes>
						<Route path="/" element={
							<motion.div key="fraud" initial={{opacity: 0, y: 8}} animate={{opacity: 1, y: 0}} exit={{opacity: 0, y: -6}} transition={{duration: 0.15}}>
								<FraudTriage />
							</motion.div>
						} />
						<Route path="/credit" element={
							<motion.div key="credit" initial={{opacity: 0, y: 8}} animate={{opacity: 1, y: 0}} exit={{opacity: 0, y: -6}} transition={{duration: 0.15}}>
								<CreditTriage />
							</motion.div>
						} />
						<Route path="/analytics" element={
							<motion.div key="analytics" initial={{opacity: 0, y: 8}} animate={{opacity: 1, y: 0}} exit={{opacity: 0, y: -6}} transition={{duration: 0.15}}>
								<Analytics />
							</motion.div>
						} />
					</Routes>
				</AnimatePresence>
			</main>
		</div>
	)
}


