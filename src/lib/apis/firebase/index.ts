import { WEBUI_API_BASE_URL } from '$lib/constants';

export const getPostById = async (token: string, postId: string) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/posts/${postId}`, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			error = err;
			console.error('Error fetching post:', err);
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

export const getJobById = async (token: string, jobId: string) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/jobs/${jobId}`, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			error = err;
			console.error('Error fetching job:', err);
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};
