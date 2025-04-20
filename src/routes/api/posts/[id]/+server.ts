// src/routes/api/posts/[id]/+server.ts
import { getDocByCollectionAndId } from '$lib/apis/firestore/firestore-queries';
import { json } from '@sveltejs/kit';
import type { RequestEvent } from '@sveltejs/kit';

export async function GET({ params }: RequestEvent) {
    const { id } = params;

  if (!id) {
    return new Response('Post ID is required', { status: 400 });
  }

  try {
    const post:any = await getDocByCollectionAndId( 'posts', id );
    console.log( 'post', post );
    
    let authorName = "Unknown"

    // Check if post has a key called 'author'
    if ( post && post.author )
    {
      // Fetch user data using the author ID
      const userData: any = await getDocByCollectionAndId('users', post.author);
      authorName = userData.first_name + ' ' + userData.last_name
    }

    return json( {
      ...post,
      author: authorName
    } );
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Document not found';
    return new Response(errorMessage, { status: 404 });
  }
}

