# SOVR Pay Dashboard System

Enterprise Financial Infrastructure with Historic Walmart Transaction System

## 🚀 Quick Start

### Option 1: PowerShell (Recommended for Windows)
```powershell
.\start-sovr-ultimate.ps1
```

### Option 2: Python Scripts
```bash
# Install dependencies
pip install -r backend/requirements.txt

# Start all services
python scripts/start_all_services.py

# Or start individually
python scripts/start_backend.py
python scripts/start_ngrok_tunnel.py
```

### Option 3: Manual Start
```bash
# Start backend
cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# In another terminal, start ngrok
ngrok http 8000
```

## 📋 System Architecture

### Components
- **Backend**: FastAPI server with comprehensive endpoints
- **Frontend**: Local dashboard at `dashboard/dashboard.html`
- **Ngrok**: Dynamic URL management for public access
- **Monitoring**: Real-time service health checks

### API Endpoints
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /docs` - API documentation
- `POST /api/v1/payments` - Create payment
- `GET /api/v1/transactions/history` - Transaction history
- `GET /api/v1/blockchain/status` - Blockchain status

## 🌐 Network Configuration

### Local Development
- Backend: `http://localhost:8000`
- Dashboard: `file:///dashboard/dashboard.html`

### Production (with ngrok)
- Public URL: Auto-generated by ngrok
- Environment files: Auto-updated with current URL

## 🔧 Configuration

### Environment Files
- `.env.template` - Configuration template
- `.env.production` - Production environment
- `.env.development` - Development environment

### Dependencies
- Python 3.8+
- ngrok (for public URLs)
- FastAPI + Uvicorn

## 📊 Dashboard Features

### Real-time Monitoring
- Backend health status
- Ngrok tunnel status
- Payment system metrics
- Blockchain synchronization
- Recent transactions

### Service Control
- One-click service startup
- Automatic health checks
- Error handling and recovery

## 🛠️ Development

### Adding New Endpoints
1. Add route to `backend/main.py`
2. Update API documentation
3. Test with dashboard

### Custom Configuration
1. Copy `.env.template` to `.env.production`
2. Update values as needed
3. Restart services

## 🔍 Troubleshooting

### Common Issues
1. **Port 8000 in use**: Change port in scripts
2. **Ngrok not found**: Install from ngrok.com
3. **Dependencies missing**: Run `pip install -r backend/requirements.txt`

### Logs
- Backend logs: Terminal output
- Ngrok logs: http://localhost:4040

## 🎯 Production Deployment

### Vercel Frontend
- URL: https://sovr-pay-web-gateway.vercel.app
- Auto-deploys from main branch

### Backend Deployment
- Use ngrok for public URLs
- Environment variables auto-update
- Health checks ensure reliability
