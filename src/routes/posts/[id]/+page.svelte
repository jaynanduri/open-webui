<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { get } from 'svelte/store';
	import { formatDistanceToNow } from 'date-fns';
	import {
		ThumbsUp,
		MessageCircle,
		Share2,
		Send,
		Image,
		Video,
		Calendar,
		FileText,
		BrainCircuit,
		Briefcase,
		Search,
		Home,
		Users,
		Bookmark
	} from 'lucide-svelte';

	let postData: any = null;
	let error: string | null = null;
	let loading = true;
	let isLiked = false;

	function formatTimestamp(timestamp: number): string {
		try {
			const date = new Date(timestamp * 1000);
			return formatDistanceToNow(date, { addSuffix: true });
		} catch (err) {
			return 'Invalid date';
		}
	}

	function toggleLike() {
		if (!postData) return;
		isLiked = !isLiked;
		// In a real app, you would update this in the database
	}

	onMount(async () => {
		const id = get(page).params.id;

		try {
			const response = await fetch(`/api/posts/${id}`);
			if (!response.ok) {
				throw new Error(await response.text());
			}
			postData = await response.json();
			// Initialize like status based on if current user is in the likes array
			// This would need user authentication info in a real app
		} catch (err: unknown) {
			error = err instanceof Error ? err.message : String(err);
		} finally {
			loading = false;
		}
	});

	function parseContent(content: string) {
		// Split content by line breaks and process each line
		if (!content) return [];
		return content.split('\n').map((line) => {
			// Check if line starts with a hashtag pattern
			const hashtagRegex = /#[a-zA-Z0-9_]+/g;
			const processedLine = line.replace(
				hashtagRegex,
				(match) =>
					`<a href="/hashtag/${match.substring(1)}" class="text-blue-600 hover:underline">${match}</a>`
			);
			return processedLine;
		});
	}
</script>

<svelte:head>
	<style>
		body {
			overflow-y: auto !important;
			height: 100vh;
		}
	</style>
</svelte:head>

<div class="bg-gray-100 min-h-screen">
	<!-- Header -->
	<header class="bg-white border-b sticky top-0 z-10">
		<div class="max-w-6xl mx-auto px-4 flex items-center justify-between h-16">
			<div class="flex items-center">
				<div class="text-blue-700 font-bold text-3xl mr-8">LinkedLens</div>
				<div class="relative">
					<input type="text" placeholder="Search" class="bg-gray-100 p-2 pl-10 rounded-md w-64" />
					<Search class="absolute left-3 top-2.5 text-gray-500" size={18} />
				</div>
			</div>

			<nav class="flex items-center space-x-6">
				<a href="/" class="flex flex-col items-center text-gray-500 hover:text-black">
					<Home size={20} />
					<span class="text-xs mt-1">Home</span>
				</a>
				<a href="#" class="flex flex-col items-center text-gray-500 hover:text-black">
					<Users size={20} />
					<span class="text-xs mt-1">Network</span>
				</a>
				<a href="#" class="flex flex-col items-center text-gray-500 hover:text-black">
					<Briefcase size={20} />
					<span class="text-xs mt-1">Jobs</span>
				</a>
				<a href="/lens" class="flex flex-col items-center text-gray-500 hover:text-black relative">
					<BrainCircuit class="text-blue-700" size={20} />
					<span class="text-blue-700 text-xs mt-1">Lens</span>
				</a>
				<div class="h-8 w-8 rounded-full bg-gray-300 cursor-pointer" />
			</nav>
		</div>
	</header>

	<!-- Main Content -->
	<div class="py-6">
		<div class="max-w-2xl mx-auto">
			{#if loading}
				<div class="bg-white rounded-lg shadow p-6 flex justify-center">
					<p>Loading post...</p>
				</div>
			{:else if error}
				<div class="bg-white rounded-lg shadow p-6">
					<p class="text-red-500">Error: {error}</p>
				</div>
			{:else if postData}
				<div class="bg-white rounded-lg shadow mb-4">
					<!-- Post Header -->
					<div class="p-4">
						<div class="flex items-start">
							<!-- This would be the actual user avatar in a real app -->
							<div
								class="h-12 w-12 rounded-full bg-blue-600 text-white flex items-center justify-center text-xl font-bold mr-3"
							>
								{postData.author ? postData.author.charAt(0).toUpperCase() : 'U'}
							</div>
							<div>
								<h3 class="font-medium">
									{postData.author || 'Anonymous User'}
									{#if postData.author_title}
										<span class="font-normal text-sm text-gray-500">
											• {postData.author_title}</span
										>
									{/if}
								</h3>
								<p class="text-gray-500 text-xs">
									{formatTimestamp(postData.createdAt)} • 🌐
								</p>
							</div>
						</div>

						<!-- Post Content -->
						<div class="mt-3 whitespace-pre-line">
							{#if postData.content}
								{#each parseContent(postData.content) as line}
									<p class="my-1">{@html line}</p>
								{/each}
							{:else}
								<p>No content available</p>
							{/if}
						</div>
					</div>

					<!-- Post Stats -->
					<div class="px-4 py-2 border-t">
						<div class="flex text-gray-500 text-sm">
							<span class="flex items-center mr-4">
								<ThumbsUp
									size={14}
									class="text-blue-600 mr-1"
									fill={isLiked ? '#2563EB' : 'none'}
								/>
								{(postData.likes ? postData.likes.length : 0) +
									(isLiked && !postData.likes?.includes('current-user-id') ? 1 : 0)}
							</span>
							<span>{postData.comments ? postData.comments.length : 0} comments</span>
							<span class="ml-2">{postData.repost?.count || 0} shares</span>
							<span class="ml-auto">{postData.views || 0} views</span>
						</div>
					</div>

					<!-- Post Actions -->
					<div class="px-4 py-1 border-t flex justify-between">
						<button
							class="flex items-center px-4 py-2 rounded hover:bg-gray-100 {isLiked
								? 'text-blue-600'
								: 'text-gray-500'}"
							on:click={toggleLike}
						>
							<ThumbsUp size={18} class="mr-2" fill={isLiked ? '#2563EB' : 'none'} />
							<span>Like</span>
						</button>
						<button class="flex items-center text-gray-500 px-4 py-2 rounded hover:bg-gray-100">
							<MessageCircle size={18} class="mr-2" />
							<span>Comment</span>
						</button>
						<button class="flex items-center text-gray-500 px-4 py-2 rounded hover:bg-gray-100">
							<Share2 size={18} class="mr-2" />
							<span>Repost</span>
						</button>
						<button class="flex items-center text-gray-500 px-4 py-2 rounded hover:bg-gray-100">
							<Send size={18} class="mr-2" />
							<span>Send</span>
						</button>
					</div>

					<!-- Comments Section (would be expanded in a complete implementation) -->
					<div class="p-4 border-t">
						<div class="flex">
							<div class="h-10 w-10 rounded-full bg-gray-300 mr-3"></div>
							<div class="flex-1 bg-gray-100 rounded-full px-4 py-2 text-gray-500">
								Add a comment...
							</div>
						</div>

						{#if postData.comments && postData.comments.length > 0}
							<div class="mt-4">
								<!-- Display comments here -->
								<p class="text-blue-600 font-medium text-sm cursor-pointer hover:underline">
									View all {postData.comments.length} comments
								</p>
							</div>
						{/if}
					</div>
				</div>
			{/if}
		</div>
	</div>
</div>
