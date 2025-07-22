from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
import os
from datetime import datetime
import json
import asyncio
from contextlib import asynccontextmanager

# Pydantic models
class PaymentRequest(BaseModel):
    amount: float
    currency: str = "USD"
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class PaymentResponse(BaseModel):
    id: str
    status: str
    amount: float
    currency: str
    created_at: datetime
    transaction_hash: Optional[str] = None

class HealthStatus(BaseModel):
    status: str
    timestamp: datetime
    services: Dict[str, str]
    ngrok_url: Optional[str] = None

# Global variables
app_state = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app_state["start_time"] = datetime.now()
    app_state["services"] = {
        "database": "connected",
        "blockchain": "synced",
        "payment_processor": "active"
    }
    yield
    # Shutdown
    app_state.clear()

# FastAPI app initialization
app = FastAPI(
    title="SOVR Pay API",
    description="Enterprise Financial Infrastructure - Historic Walmart Transaction System",
    version="2.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "SOVR Pay API - Enterprise Financial Infrastructure",
        "version": "2.0.0",
        "status": "operational",
        "docs": "/docs"
    }

@app.get("/health", response_model=HealthStatus, tags=["Health"])
async def health_check():
    """Comprehensive health check endpoint"""
    return HealthStatus(
        status="healthy",
        timestamp=datetime.now(),
        services=app_state.get("services", {}),
        ngrok_url=os.getenv("NGROK_URL", "http://localhost:8000")
    )

@app.post("/api/v1/payments", response_model=PaymentResponse, tags=["Payments"])
async def create_payment(payment: PaymentRequest):
    """Create a new payment transaction"""
    transaction_id = f"txn_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    
    # Simulate payment processing
    await asyncio.sleep(0.5)
    
    return PaymentResponse(
        id=transaction_id,
        status="completed",
        amount=payment.amount,
        currency=payment.currency,
        created_at=datetime.now(),
        transaction_hash=f"0x{transaction_id}"
    )

@app.get("/api/v1/payments/{payment_id}", response_model=PaymentResponse, tags=["Payments"])
async def get_payment(payment_id: str):
    """Retrieve payment details by ID"""
    return PaymentResponse(
        id=payment_id,
        status="completed",
        amount=100.00,
        currency="USD",
        created_at=datetime.now(),
        transaction_hash=f"0x{payment_id}"
    )

@app.get("/api/v1/transactions/history", tags=["Transactions"])
async def get_transaction_history(
    limit: int = 10,
    offset: int = 0,
    currency: Optional[str] = None
):
    """Get historic transaction data"""
    mock_transactions = [
        {
            "id": f"txn_{i}",
            "amount": 100.0 + (i * 10),
            "currency": currency or "USD",
            "status": "completed",
            "created_at": datetime.now().isoformat(),
            "description": f"Walmart Transaction #{i}"
        }
        for i in range(offset, offset + limit)
    ]
    return {
        "transactions": mock_transactions,
        "total": 1000,
        "limit": limit,
        "offset": offset
    }

@app.get("/api/v1/blockchain/status", tags=["Blockchain"])
async def blockchain_status():
    """Get blockchain synchronization status"""
    return {
        "status": "synced",
        "block_height": 18500000,
        "last_block_time": datetime.now().isoformat(),
        "network": "mainnet"
    }

@app.post("/api/v1/blockchain/monitor", tags=["Blockchain"])
async def start_blockchain_monitor():
    """Start blockchain transaction monitoring"""
    return {
        "status": "monitoring_started",
        "monitor_id": f"mon_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "endpoint": "/api/v1/blockchain/events"
    }

@app.get("/api/v1/system/info", tags=["System"])
async def system_info():
    """Get system configuration and status"""
    return {
        "environment": os.getenv("ENVIRONMENT", "development"),
        "api_version": "2.0.0",
        "uptime": str(datetime.now() - app_state.get("start_time", datetime.now())),
        "services": app_state.get("services", {}),
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "payments": "/api/v1/payments",
            "transactions": "/api/v1/transactions",
            "blockchain": "/api/v1/blockchain"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
