from fastapi import APIRouter
from api.routes import import_tool, property_stack


api_router = APIRouter()
api_router.include_router(import_tool.router, prefix="/import_tool", tags=["Import Tool"])
api_router.include_router(property_stack.router, prefix="/property_stack", tags=["Property Stack"])

