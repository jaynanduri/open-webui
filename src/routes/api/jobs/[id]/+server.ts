import { getDocByCollectionAndId } from '$lib/apis/firestore/firestore-queries';
import { json } from '@sveltejs/kit';
import type { RequestEvent } from '@sveltejs/kit';

export async function GET({ params }: RequestEvent) {
    const { id } = params;

  if (!id) {
    return new Response('Post ID is required', { status: 400 });
  }

  try {
    const post = await getDocByCollectionAndId( 'jobs', id );
    return json(post);
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Document not found';
    return new Response(errorMessage, { status: 404 });
  }
}
