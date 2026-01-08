from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from database import get_db, ClickEvent
from typing import List, Dict

app = FastAPI(title="Real-Time Analytics API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Real-Time Analytics API", "status": "running"}

@app.get("/api/stats/overview")
def get_overview_stats(db: Session = Depends(get_db)):
    """Get overall statistics"""
    
    # Last 24 hours
    last_24h = datetime.utcnow() - timedelta(hours=24)
    
    total_events = db.query(ClickEvent).filter(ClickEvent.timestamp >= last_24h).count()
    total_users = db.query(ClickEvent.user_id).filter(ClickEvent.timestamp >= last_24h).distinct().count()
    total_sessions = db.query(ClickEvent.session_id).filter(ClickEvent.timestamp >= last_24h).distinct().count()
    
    # Total revenue
    total_revenue = db.query(func.sum(ClickEvent.revenue)).filter(
        ClickEvent.timestamp >= last_24h,
        ClickEvent.event_type == 'purchase'
    ).scalar() or 0
    
    return {
        "total_events": total_events,
        "total_users": total_users,
        "total_sessions": total_sessions,
        "total_revenue": round(float(total_revenue), 2)
    }

@app.get("/api/stats/events-by-type")
def get_events_by_type(db: Session = Depends(get_db)):
    """Get event counts grouped by type"""
    last_24h = datetime.utcnow() - timedelta(hours=24)
    
    results = db.query(
        ClickEvent.event_type,
        func.count(ClickEvent.id).label('count')
    ).filter(
        ClickEvent.timestamp >= last_24h
    ).group_by(
        ClickEvent.event_type
    ).all()
    
    return [{"event_type": r.event_type, "count": r.count} for r in results]

@app.get("/api/stats/events-by-country")
def get_events_by_country(db: Session = Depends(get_db)):
    """Get event counts grouped by country"""
    last_24h = datetime.utcnow() - timedelta(hours=24)
    
    results = db.query(
        ClickEvent.country,
        func.count(ClickEvent.id).label('count')
    ).filter(
        ClickEvent.timestamp >= last_24h
    ).group_by(
        ClickEvent.country
    ).order_by(
        desc('count')
    ).limit(10).all()
    
    return [{"country": r.country, "count": r.count} for r in results]

@app.get("/api/stats/events-by-device")
def get_events_by_device(db: Session = Depends(get_db)):
    """Get event counts grouped by device"""
    last_24h = datetime.utcnow() - timedelta(hours=24)
    
    results = db.query(
        ClickEvent.device,
        func.count(ClickEvent.id).label('count')
    ).filter(
        ClickEvent.timestamp >= last_24h
    ).group_by(
        ClickEvent.device
    ).all()
    
    return [{"device": r.device, "count": r.count} for r in results]

@app.get("/api/stats/top-pages")
def get_top_pages(db: Session = Depends(get_db)):
    """Get most visited pages"""
    last_24h = datetime.utcnow() - timedelta(hours=24)
    
    results = db.query(
        ClickEvent.page_url,
        func.count(ClickEvent.id).label('count')
    ).filter(
        ClickEvent.timestamp >= last_24h
    ).group_by(
        ClickEvent.page_url
    ).order_by(
        desc('count')
    ).limit(10).all()
    
    return [{"page": r.page_url, "views": r.count} for r in results]

@app.get("/api/stats/timeline")
def get_timeline_data(db: Session = Depends(get_db)):
    """Get events over time (last 24 hours, grouped by hour)"""
    last_24h = datetime.utcnow() - timedelta(hours=24)
    
    # SQLite/PostgreSQL compatible hour extraction
    results = db.query(
        func.date_trunc('hour', ClickEvent.timestamp).label('hour'),
        func.count(ClickEvent.id).label('count')
    ).filter(
        ClickEvent.timestamp >= last_24h
    ).group_by(
        'hour'
    ).order_by(
        'hour'
    ).all()
    
    return [
        {
            "hour": r.hour.strftime("%Y-%m-%d %H:00"),
            "count": r.count
        } for r in results
    ]

@app.get("/api/events/recent")
def get_recent_events(limit: int = 20, db: Session = Depends(get_db)):
    """Get most recent events"""
    events = db.query(ClickEvent).order_by(
        desc(ClickEvent.timestamp)
    ).limit(limit).all()
    
    return [
        {
            "id": e.id,
            "user_id": e.user_id,
            "event_type": e.event_type,
            "page_url": e.page_url,
            "timestamp": e.timestamp.isoformat(),
            "country": e.country,
            "device": e.device,
            "revenue": e.revenue
        } for e in events
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)