import { useState } from 'react'
import Highlight, { defaultProps } from 'prism-react-renderer'

export default function CodeBlock({ code, language='json', className }: { code: string, language?: string, className?: string }){
	const [copied, setCopied] = useState(false)
	return (
		<div className={`relative rounded-md border border-border/60 bg-neutral-900 ${className||''}`}>
			<button aria-label="Copy code" className="absolute right-2 top-2 text-xs px-2 py-1 bg-neutral-800 rounded focus-ring" onClick={() => { navigator.clipboard.writeText(code); setCopied(true); setTimeout(()=>setCopied(false), 1200) }}>{copied?'Copied':'Copy'}</button>
			<Highlight {...defaultProps} code={code} language={language as any}>
				{({className, style, tokens, getLineProps, getTokenProps}) => (
					<pre className={`${className} m-0 overflow-auto text-xs p-4`} style={style}>
						{tokens.map((line, i) => (
							<div key={i} {...getLineProps({line, key: i})}>
								{line.map((token, key) => (
									<span key={key} {...getTokenProps({ token, key })} />
								))}
							</div>
						))}
					</pre>
				)}
			</Highlight>
		</div>
	)
}


