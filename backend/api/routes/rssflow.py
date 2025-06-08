from configFiles.models import RssFlowLibrary
from config import db
from fastapi import APIRouter

router = APIRouter()

@router.get("/getRssFlow")
async def getRssFlow():
    rssFlows = db.query(RssFlowLibrary).limit(1000).all()
    return {"rssFlows": rssFlows}
