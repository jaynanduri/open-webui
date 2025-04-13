<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { get } from 'svelte/store';
	import { formatDistanceToNow } from 'date-fns';
	import {
		Briefcase,
		MapPin,
		Clock,
		DollarSign,
		Building,
		Share2,
		Send,
		Bookmark,
		ThumbsDown
	} from 'lucide-svelte';

	let jobData: any = null;
	let error: string | null = null;
	let loading = true;
	let isSaved = false;

	function formatTimestamp(timestamp: number): string {
		try {
			const date = new Date(timestamp * 1000);
			return formatDistanceToNow(date, { addSuffix: true });
		} catch (err) {
			return 'Invalid date';
		}
	}

	function toggleSaved() {
		isSaved = !isSaved;
		// In a real app, you would update this in the database
	}

	function formatSalary(
		min: number | null,
		max: number | null,
		period: string | null,
		currency: string | null
	): string {
		if (!min && !max) return 'Not specified';

		const currencySymbol = currency || '$';
		const periodText = period ? ` ${period}` : '';

		if (min && max) {
			return `${currencySymbol}${min.toLocaleString()} - ${currencySymbol}${max.toLocaleString()}${periodText}`;
		} else if (min) {
			return `${currencySymbol}${min.toLocaleString()}+${periodText}`;
		} else if (max) {
			return `Up to ${currencySymbol}${max.toLocaleString()}${periodText}`;
		}

		return 'Not specified';
	}

	onMount(async () => {
		const id = get(page).params.id;

		try {
			const response = await fetch(`/api/jobs/${id}`);
			if (!response.ok) {
				throw new Error(await response.text());
			}
			jobData = await response.json();
		} catch (err: unknown) {
			error = err instanceof Error ? err.message : String(err);
		} finally {
			loading = false;
		}
	});
</script>

<svelte:head>
	<style>
		body {
			overflow-y: auto !important;
			height: 100vh;
		}
	</style>
</svelte:head>

<div class="bg-gray-100 min-h-screen py-6">
	<div class="max-w-4xl mx-auto">
		{#if loading}
			<div class="bg-white rounded-lg shadow p-6 flex justify-center">
				<p>Loading job details...</p>
			</div>
		{:else if error}
			<div class="bg-white rounded-lg shadow p-6">
				<p class="text-red-500">Error: {error}</p>
			</div>
		{:else if jobData}
			<div class="flex flex-col md:flex-row gap-4">
				<!-- Main Job Details -->
				<div class="bg-white rounded-lg shadow flex-1">
					<!-- Job Header -->
					<div class="p-6">
						<h1 class="text-2xl font-bold mb-1">{jobData.title || 'Job Title'}</h1>
						<p class="text-lg text-gray-700 mb-4">{jobData.company_name || 'Company'}</p>

						<div class="flex flex-wrap gap-y-2 text-sm text-gray-600 mb-4">
							<div class="flex items-center mr-4">
								<MapPin size={16} class="mr-1" />
								<span
									>{jobData.location || 'Location'}{jobData.remote_allowed ? ' (Remote)' : ''}</span
								>
							</div>
							<div class="flex items-center mr-4">
								<Clock size={16} class="mr-1" />
								<span>{formatTimestamp(jobData.createdAt)}</span>
							</div>
							{#if jobData.min_salary || jobData.max_salary}
								<div class="flex items-center mr-4">
									<DollarSign size={16} class="mr-1" />
									<span
										>{formatSalary(
											jobData.min_salary,
											jobData.max_salary,
											jobData.pay_period,
											jobData.currency
										)}</span
									>
								</div>
							{/if}
							{#if jobData.formatted_work_type}
								<div class="flex items-center">
									<Briefcase size={16} class="mr-1" />
									<span>{jobData.formatted_work_type}</span>
								</div>
							{/if}
						</div>

						<div class="flex flex-wrap gap-2 mb-6">
							<button
								class="bg-blue-600 text-white px-4 py-2 rounded-full font-medium hover:bg-blue-700"
							>
								Easy Apply
							</button>
							<button
								class="border px-4 py-2 rounded-full font-medium {isSaved
									? 'border-blue-600 text-blue-600'
									: 'border-gray-400 text-gray-700'} hover:bg-gray-50"
								on:click={toggleSaved}
							>
								<div class="flex items-center">
									<Bookmark size={16} class="mr-2" fill={isSaved ? '#2563EB' : 'none'} />
									<span>{isSaved ? 'Saved' : 'Save'}</span>
								</div>
							</button>
							<button
								class="border border-gray-400 text-gray-700 px-4 py-2 rounded-full font-medium hover:bg-gray-50 flex items-center"
							>
								<Share2 size={16} class="mr-2" />
								<span>Share</span>
							</button>
							<button
								class="border border-gray-400 text-gray-700 px-4 py-2 rounded-full font-medium hover:bg-gray-50 flex items-center"
							>
								<ThumbsDown size={16} class="mr-2" />
								<span>Not interested</span>
							</button>
						</div>

						<!-- Job Stats -->
						<div class="flex items-center text-sm text-gray-500 mb-2">
							<div class="mr-4">
								<span class="font-medium">{jobData.views || 0}</span> views
							</div>
							<div>
								<span class="font-medium">{jobData.applies || 0}</span> applicants
							</div>
						</div>
					</div>

					<!-- Job Description -->
					<div class="border-t p-6">
						<h2 class="text-xl font-bold mb-4">About the job</h2>
						<div class="prose prose-sm max-w-none whitespace-pre-line">
							{#if jobData.description}
								{jobData.description}
							{:else}
								<p>No description available</p>
							{/if}
						</div>

						{#if jobData.skills_desc}
							<h3 class="text-lg font-bold mt-6 mb-2">Skills</h3>
							<div class="prose prose-sm max-w-none">
								{jobData.skills_desc}
							</div>
						{/if}
					</div>

					<!-- Apply Section -->
					<div class="border-t p-6">
						<button
							class="w-full bg-blue-600 text-white py-3 rounded-full font-medium hover:bg-blue-700 mb-3"
						>
							Easy Apply
						</button>
						{#if jobData.application_url}
							<a
								href={jobData.application_url}
								target="_blank"
								rel="noopener noreferrer"
								class="block w-full text-center border border-blue-600 text-blue-600 py-3 rounded-full font-medium hover:bg-blue-50"
							>
								Apply on Company Website
							</a>
						{/if}
					</div>
				</div>

				<!-- Right Sidebar -->
				<div class="md:w-80">
					<!-- Company Info -->
					<div class="bg-white rounded-lg shadow p-4 mb-4">
						<h3 class="font-medium text-lg mb-3">About {jobData.company_name || 'the company'}</h3>
						<div class="flex items-center mb-4">
							<div
								class="h-16 w-16 bg-gray-200 rounded-full flex items-center justify-center text-2xl font-bold text-gray-500 mr-3"
							>
								{jobData.company_name ? jobData.company_name.charAt(0).toUpperCase() : 'C'}
							</div>
							<div>
								<h4 class="font-medium">{jobData.company_name || 'Company'}</h4>
								<p class="text-sm text-gray-500">Company • Staffing & Recruiting</p>
							</div>
						</div>

						<a
							href={`/company/${jobData.company_id}`}
							class="text-blue-600 font-medium text-sm hover:underline block mb-2"
						>
							View company page
						</a>

						<a
							href={`/company/${jobData.company_id}/jobs`}
							class="text-blue-600 font-medium text-sm hover:underline block"
						>
							See all jobs
						</a>
					</div>

					<!-- Similar Jobs -->
					<div class="bg-white rounded-lg shadow p-4">
						<h3 class="font-medium text-lg mb-3">Similar jobs</h3>
						<p class="text-gray-500 text-sm">
							We'll show similar jobs once you interact with this job.
						</p>
					</div>
				</div>
			</div>
		{/if}
	</div>
</div>
