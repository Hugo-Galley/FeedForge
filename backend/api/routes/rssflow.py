from fastapi import APIRouter

from configFiles.models import RssFlowLibrary
from config import db

router = APIRouter()

@router.get("/getRssFlow")
async def get_rss_flow():
    rss_flow = (db.query(RssFlowLibrary)
                .limit(1000)
                .all())
    return {"rssFlows": rss_flow}
