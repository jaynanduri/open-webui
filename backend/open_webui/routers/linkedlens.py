# open_webui/routers/linkedlens.py
import logging
from typing import Optional, Dict, Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from open_webui.constants import ERROR_MESSAGES
from open_webui.env import SRC_LOG_LEVELS
from open_webui.utils.auth import get_verified_user
from open_webui.utils.firebase import get_doc_by_collection_and_id

logger = logging.getLogger(__name__)
logger.setLevel(SRC_LOG_LEVELS.get("ROUTERS", logging.INFO))

router = APIRouter()

class PostResponse(BaseModel):
    id: str
    content: Optional[str] = None
    author: Optional[str] = None
    author_title: Optional[str] = None
    createdAt: Optional[int] = None
    likes: Optional[list] = None
    comments: Optional[list] = None
    views: Optional[int] = 0

class JobResponse(BaseModel):
    id: str
    title: Optional[str] = None
    company: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    salary: Optional[str] = None
    requirements: Optional[list] = None
    createdAt: Optional[int] = None

@router.get("/posts/{post_id}", response_model=PostResponse)
async def get_post_by_id(post_id: str, user=Depends(get_verified_user)):
    """Get a post by ID"""
    if not post_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post ID is required",
        )
        
    try:
        # Fetch post document
        logger.info(f"Fetching post with ID: {post_id}")
        post = await get_doc_by_collection_and_id('posts', post_id)
        
        # Default author name
        author_name = "Unknown"
        
        # If post has an author reference, try to fetch author details
        if post and post.get("author"):
            try:
                logger.info(f"Fetching author with ID: {post['author']}")
                user_data = await get_doc_by_collection_and_id('users', post["author"])
                
                # Construct author name from first and last name
                first_name = user_data.get("first_name", "")
                last_name = user_data.get("last_name", "")
                if first_name or last_name:
                    author_name = f"{first_name} {last_name}".strip()
            except Exception as e:
                # If author fetch fails, continue with default author name
                logger.error(f"Error fetching author data: {e}")
        
        # Return the post with author name
        return {
            **post,
            "author": author_name
        }
    
    except ValueError as e:
        error_message = str(e)
        logger.error(f"Error in get_post_by_id: {error_message}")
        
        if "not found" in error_message:
            status_code = status.HTTP_404_NOT_FOUND
        elif "not initialized" in error_message:
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            error_message = "Firebase service unavailable"
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            
        raise HTTPException(
            status_code=status_code,
            detail=error_message,
        )
        
    except Exception as e:
        logger.exception(f"Unexpected error in get_post_by_id: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )

@router.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job_by_id(job_id: str, user=Depends(get_verified_user)):
    """Get a job by ID"""
    if not job_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job ID is required",
        )
        
    try:
        # Fetch job document
        logger.info(f"Fetching job with ID: {job_id}")
        job = await get_doc_by_collection_and_id('jobs', job_id)
        return job
        
    except ValueError as e:
        error_message = str(e)
        logger.error(f"Error in get_job_by_id: {error_message}")
        
        if "not found" in error_message:
            status_code = status.HTTP_404_NOT_FOUND
        elif "not initialized" in error_message:
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            error_message = "Firebase service unavailable"
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            
        raise HTTPException(
            status_code=status_code,
            detail=error_message,
        )
        
    except Exception as e:
        logger.exception(f"Unexpected error in get_job_by_id: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )