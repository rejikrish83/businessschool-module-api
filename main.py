from fastapi import FastAPI, Depends
from starlette.responses import JSONResponse

from endpoints.ProtectedEndpoint import router
from authLogic.authorizer import has_access
from authLogic.AppConfig import AppConfig
from fastapi.middleware.cors import CORSMiddleware


app  = FastAPI()
app.state.config = AppConfig()

# Enable all CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PROTECTED = [Depends(has_access)]
app.include_router(router, prefix="/v1", dependencies=PROTECTED)

@app.get("/health")
async def health_check():
    return JSONResponse(content={"status": "healthy"})