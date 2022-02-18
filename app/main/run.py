import uvicorn
from main import app
from core.config import settings

if __name__ == "__main__":
    print("Production:", settings.PRODUCTION, "- Type", type(settings.PRODUCTION))
    print("SQLITE:", settings.SQLITE, "- Type", type(settings.SQLITE))
    print("USER:", settings.USER, "- Type", type(settings.USER))
    print("PASSWORD:", settings.PASSWORD, "- Type", type(settings.PASSWORD))
    print("S3:", settings.REMOTE_STORAGE, "- Type", type(settings.REMOTE_STORAGE))
    print("Bucket:", settings.IMPORT_TOOL_BUCKET_NAME, "- Type", type(settings.IMPORT_TOOL_BUCKET_NAME))
    print("CORS_ALLOW_CUSTOM_ORIGINS_FLAG:", settings.CORS_ALLOW_CUSTOM_ORIGINS_FLAG, "- Type", type(settings.CORS_ALLOW_CUSTOM_ORIGINS_FLAG))
    print("PRODUCTION CORS ORIGINS", settings.PRODUCTION_CORS_ORIGINS, "- Type",
          type(settings.PRODUCTION_CORS_ORIGINS))
    print("MASTER:", settings.MASTER, "- Type", type(settings.MASTER))
    uvicorn.run(app, host="127.0.0.1", port=8000)
