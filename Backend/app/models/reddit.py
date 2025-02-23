from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RedditStockMention(BaseModel):
    ticker: str
    mentions_count: int
    total_upvotes: int
    total_comments: int
    posts_scraped: int
    timestamp: Optional[datetime] = datetime.utcnow()

class RedditStockMentionInDB(RedditStockMention):
    id: str  # MongoDB document ID

    class Config:
        orm_mode = True