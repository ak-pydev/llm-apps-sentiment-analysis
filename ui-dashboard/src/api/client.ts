const API_BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';

type Json = any;

export const client = {
	async get<T = Json>(path: string): Promise<T> {
		const url = path.startsWith('http') ? path : `${API_BASE}${path}`;
		const res = await fetch(url, {
			credentials: 'include',
			headers: {
				'Content-Type': 'application/json',
				Accept: 'application/json',
			},
		});
		if (!res.ok) {
			const text = await res.text().catch(() => '');
			throw new Error(`API GET ${url} failed: ${res.status} ${res.statusText} ${text}`);
		}
		return (await res.json()) as T;
	},
};

export default client;
