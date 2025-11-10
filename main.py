from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, chat

app = FastAPI(title="Helfer Chat Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {"message": "Backend running successfully 🚀"}
