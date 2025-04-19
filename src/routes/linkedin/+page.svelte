<!-- LinkedInFeed.svelte -->
<script>
	import { onMount } from 'svelte';
	import {
		ThumbsUp,
		Heart,
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

	// State variables
	// let isOpen = false;
	let messages = [
		{
			id: 1,
			text: "Hello! I'm your professional assistant. Looking for job posts, recruiter insights, or interview prep help?",
			sender: 'bot',
			liked: false,
			disliked: false
		}
	];
	// let inputValue = '';
	// let showRagChatbot = false;

	// State for posts
	let posts = [
		{
			id: 1,
			author: {
				name: 'Sarah Chen',
				title: 'UI/UX Designer at Creative Solutions',
				avatar:
					'https://media.istockphoto.com/id/1437816897/photo/business-woman-manager-or-human-resources-portrait-for-career-success-company-we-are-hiring.jpg?s=612x612&w=0&k=20&c=tyLvtzutRh22j9GqSGI33Z4HpIwv9vL_MZw_xOE19NQ='
			},
			timeAgo: '2h',
			content:
				"Just finished the redesign for our client's e-commerce platform. Increased conversion rates by 24% through improved navigation and checkout flow. #UXDesign #ConversionOptimization",
			image: '/api/placeholder/600/400',
			likes: 128,
			comments: 14,
			shares: 5,
			isLiked: false
		},
		{
			id: 2,
			author: {
				name: 'Tech Innovations Inc.',
				title: 'Technology Company • 15,242 followers',
				avatar:
					'https://www.shutterstock.com/shutterstock/photos/2278726727/display_1500/stock-vector-minimalistic-circular-logo-sample-vector-2278726727.jpg'
			},
			timeAgo: '5h',
			content:
				"We're excited to announce our new AI-powered chatbot integration platform that helps businesses improve customer engagement and support. Join our webinar next week to learn how it can transform your customer experience! #AI #CustomerExperience",
			likes: 243,
			comments: 28,
			shares: 42,
			isLiked: false
		},
		{
			id: 3,
			author: {
				name: 'Alex Johnson',
				title: 'Frontend Developer at TechStart',
				avatar:
					'https://t4.ftcdn.net/jpg/03/64/21/11/360_F_364211147_1qgLVxv1Tcq0Ohz3FawUfrtONzz8nq3e.jpg'
			},
			timeAgo: '1d',
			content:
				"Just completed the React & Firebase masterclass. Here's my capstone project - a real-time collaboration tool with embedded AI assistant. Always looking to connect with other developers interested in similar technologies! #ReactJS #WebDev",
			image: 'https://miro.medium.com/v2/resize:fit:1200/1*7WZKo5CikczXJpMR4fwNCQ.png',
			likes: 75,
			comments: 23,
			shares: 7,
			isLiked: true
		}
	];

	/**
	 * @param {number} postId
	 */
	function toggleLike(postId) {
		posts = posts.map((post) => {
			if (post.id === postId) {
				return {
					...post,
					isLiked: !post.isLiked,
					likes: post.isLiked ? post.likes - 1 : post.likes + 1
				};
			}
			return post;
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
				<a href="/linkedin" class="flex flex-col items-center text-gray-500 hover:text-black">
					<Home class="text-blue-700" size={20} />
					<span class=" text-blue-700 text-xs mt-1">Home</span>
				</a>
				<a href="#" class="flex flex-col items-center text-gray-500 hover:text-black">
					<Users size={20} />
					<span class="text-xs mt-1">Network</span>
				</a>
				<a href="#" class="flex flex-col items-center text-gray-500 hover:text-black">
					<Briefcase size={20} />
					<span class="text-xs mt-1">Jobs</span>
				</a>
				<a href="/" class="flex flex-col items-center text-gray-500 hover:text-black relative">
					<BrainCircuit class="text-blue-700" size={20} />
					<span class="text-blue-700 text-xs mt-1">Lens</span>
				</a>
				<img
					src="https://png.pngtree.com/png-vector/20220807/ourmid/pngtree-man-avatar-wearing-gray-suit-png-image_6102786.png"
					alt="Profile picture"
					class="h-8 w-8 rounded-full bg-gray-300 cursor-pointer"
				/>
			</nav>
		</div>
	</header>

	<!-- Main Content -->
	<main class="max-w-6xl mx-auto px-4 py-6 flex">
		<!-- Left Sidebar -->
		<div class="w-1/4 pr-4">
			<div class="bg-white rounded-lg shadow mb-4 overflow-hidden">
				<div class="h-16 bg-blue-100"></div>
				<div class="p-4 relative">
					<img
						src="https://png.pngtree.com/png-vector/20220807/ourmid/pngtree-man-avatar-wearing-gray-suit-png-image_6102786.png"
						alt="Profile picture"
						class="h-16 w-16 rounded-full border-2 border-white absolute -top-8 left-4 object-cover"
					/>
					<div class="mt-10">
						<h2 class="font-medium text-lg">Jon Doe</h2>
						<p class="text-gray-500 text-sm">Product Designer | UI/UX Specialist</p>
					</div>
					<hr class="my-3" />
					<div class="text-sm">
						<div class="flex justify-between mb-1">
							<span class="text-gray-500">Who viewed your profile</span>
							<span class="text-blue-600 font-medium">42</span>
						</div>
						<div class="flex justify-between mb-1">
							<span class="text-gray-500">Views of your post</span>
							<span class="text-blue-600 font-medium">167</span>
						</div>
					</div>
					<hr class="my-3" />
					<div class="text-sm">
						<a href="#" class="text-gray-500 flex items-center">
							<Bookmark size={16} class="mr-2" />
							My items
						</a>
					</div>
				</div>
			</div>

			<div class="bg-white rounded-lg shadow p-4">
				<h3 class="font-medium text-sm mb-3">Recent</h3>
				<ul class="text-sm">
					<li class="mb-2">
						<a href="#" class="text-gray-500 hover:text-black flex items-center">
							<Users size={14} class="mr-2" />
							UI/UX Design Group
						</a>
					</li>
					<li class="mb-2">
						<a href="#" class="text-gray-500 hover:text-black flex items-center">
							<Calendar size={14} class="mr-2" />
							Product Design Conference
						</a>
					</li>
					<li class="mb-2">
						<a href="#" class="text-gray-500 hover:text-black flex items-center">
							<Briefcase size={14} class="mr-2" />
							Product Designer jobs
						</a>
					</li>
				</ul>
				<h3 class="font-medium text-sm text-blue-600 mt-4">Groups</h3>
				<h3 class="font-medium text-sm text-blue-600 mt-2">Events</h3>
				<h3 class="font-medium text-sm text-blue-600 mt-2">Followed Hashtags</h3>
			</div>
		</div>

		<!-- Main Feed -->
		<div class="w-2/4 px-4">
			<!-- Post Creation -->
			<div class="bg-white rounded-lg shadow mb-4 p-4">
				<div class="flex">
					<img
						src="https://png.pngtree.com/png-vector/20220807/ourmid/pngtree-man-avatar-wearing-gray-suit-png-image_6102786.png"
						alt="Profile picture"
						class="h-12 w-12 rounded-full bg-gray-300 mr-3"
					/>
					<input
						type="text"
						placeholder="Start a post"
						class="bg-white border border-gray-300 rounded-full flex-1 px-4 py-2"
					/>
				</div>
				<div class="flex justify-between mt-3">
					<button class="flex items-center text-gray-500 hover:bg-gray-100 px-3 py-1 rounded">
						<Image size={18} class="mr-2 text-blue-500" />
						<span>Photo</span>
					</button>
					<button class="flex items-center text-gray-500 hover:bg-gray-100 px-3 py-1 rounded">
						<Video size={18} class="mr-2 text-green-500" />
						<span>Video</span>
					</button>
					<button class="flex items-center text-gray-500 hover:bg-gray-100 px-3 py-1 rounded">
						<Calendar size={18} class="mr-2 text-orange-500" />
						<span>Event</span>
					</button>
					<button class="flex items-center text-gray-500 hover:bg-gray-100 px-3 py-1 rounded">
						<FileText size={18} class="mr-2 text-red-500" />
						<span>Write article</span>
					</button>
				</div>
			</div>

			<!-- Feed Posts -->
			{#each posts as post (post.id)}
				<div class="bg-white rounded-lg shadow mb-4 overflow-hidden">
					<div class="p-4">
						<div class="flex items-start">
							<img src={post.author.avatar} alt="" class="h-12 w-12 rounded-full mr-3" />
							<div>
								<h3 class="font-medium">{post.author.name}</h3>
								<p class="text-gray-500 text-sm">{post.author.title}</p>
								<p class="text-gray-500 text-xs">{post.timeAgo} • <span>🌐</span></p>
							</div>
						</div>
						<p class="mt-3">{post.content}</p>
					</div>

					{#if post.image}
						<img src={post.image} alt="" class="w-full" />
					{/if}

					<div class="px-4 py-2 border-t">
						<div class="flex text-gray-500 text-sm">
							<span class="flex items-center mr-4">
								<Heart size={14} class="text-blue-600 mr-1" fill="#2563EB" />
								{post.likes}
							</span>
							<span>{post.comments} comments</span>
							<span class="ml-2">{post.shares} shares</span>
						</div>
					</div>

					<div class="px-4 py-1 border-t flex justify-between">
						<button
							class={`flex items-center px-4 py-2 rounded hover:bg-gray-100 ${post.isLiked ? 'text-blue-600' : 'text-gray-500'}`}
							on:click={() => toggleLike(post.id)}
						>
							<ThumbsUp size={18} class="mr-2" fill={post.isLiked ? '#2563EB' : 'none'} />
							<span>Like</span>
						</button>
						<button class="flex items-center text-gray-500 px-4 py-2 rounded hover:bg-gray-100">
							<MessageCircle size={18} class="mr-2" />
							<span>Comment</span>
						</button>
						<button class="flex items-center text-gray-500 px-4 py-2 rounded hover:bg-gray-100">
							<Share2 size={18} class="mr-2" />
							<span>Share</span>
						</button>
						<button class="flex items-center text-gray-500 px-4 py-2 rounded hover:bg-gray-100">
							<Send size={18} class="mr-2" />
							<span>Send</span>
						</button>
					</div>
				</div>
			{/each}
		</div>

		<!-- Right Sidebar -->
		<div class="w-1/4 pl-4">
			<div class="bg-white rounded-lg shadow p-4 mb-4">
				<h2 class="font-medium mb-3">LinkedIn News</h2>
				<ul class="text-sm">
					<li class="mb-3">
						<a href="#" class="font-medium hover:text-blue-600">Tech hiring rebounds in Q2</a>
						<p class="text-gray-500 text-xs mt-1">5h ago • 4,287 readers</p>
					</li>
					<li class="mb-3">
						<a href="#" class="font-medium hover:text-blue-600">The rise of AI in UX design</a>
						<p class="text-gray-500 text-xs mt-1">2d ago • 8,154 readers</p>
					</li>
					<li class="mb-3">
						<a href="#" class="font-medium hover:text-blue-600">Remote work trends for 2025</a>
						<p class="text-gray-500 text-xs mt-1">3d ago • 15,742 readers</p>
					</li>
					<li class="mb-3">
						<a href="#" class="font-medium hover:text-blue-600">Startups securing major funding</a>
						<p class="text-gray-500 text-xs mt-1">1d ago • 2,874 readers</p>
					</li>
				</ul>
				<a href="#" class="text-gray-500 text-sm flex items-center mt-1"> Show more </a>
			</div>

			<div class="bg-white rounded-lg shadow p-4">
				<h2 class="font-medium mb-3">People you may know</h2>
				<ul>
					<li class="flex mb-4">
						<img
							src="https://cdn.pixabay.com/photo/2019/08/11/18/59/icon-4399701_640.png"
							alt=""
							class="h-12 w-12 rounded-full mr-3"
						/>
						<div class="flex-1 text-sm">
							<h3 class="font-medium">David Park</h3>
							<p class="text-gray-500 text-xs">UX Researcher at DesignLab</p>
							<button
								class="border border-gray-500 text-gray-500 rounded-full px-3 py-1 mt-2 hover:bg-gray-100 flex items-center"
							>
								<Users size={14} class="mr-1" />
								Connect
							</button>
						</div>
					</li>
					<li class="flex mb-4">
						<img
							src="https://cdn.pixabay.com/photo/2019/08/11/18/59/icon-4399701_640.png"
							alt=""
							class="h-12 w-12 rounded-full mr-3"
						/>
						<div class="flex-1 text-sm">
							<h3 class="font-medium">Priya Sharma</h3>
							<p class="text-gray-500 text-xs">Product Manager at TechCorp</p>
							<button
								class="border border-gray-500 text-gray-500 rounded-full px-3 py-1 mt-2 hover:bg-gray-100 flex items-center"
							>
								<Users size={14} class="mr-1" />
								Connect
							</button>
						</div>
					</li>
					<li class="flex">
						<img
							src="https://cdn.pixabay.com/photo/2019/08/11/18/59/icon-4399701_640.png"
							alt=""
							class="h-12 w-12 rounded-full mr-3"
						/>
						<div class="flex-1 text-sm">
							<h3 class="font-medium">Michael Chen</h3>
							<p class="text-gray-500 text-xs">Frontend Developer at WebSolutions</p>
							<button
								class="border border-gray-500 text-gray-500 rounded-full px-3 py-1 mt-2 hover:bg-gray-100 flex items-center"
							>
								<Users size={14} class="mr-1" />
								Connect
							</button>
						</div>
					</li>
				</ul>
			</div>
		</div>
	</main>
</div>
