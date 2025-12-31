import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.auth import auth_routes
from api.wallet import wallet_routes
from core.database import init_db

app = FastAPI()
init_db()

# Configuração de CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(auth_routes.router)
app.include_router(wallet_routes.router)

# === Apenas para Railway ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Railway define a porta via variável de ambiente
    uvicorn.run(app, host="0.0.0.0", port=port)
