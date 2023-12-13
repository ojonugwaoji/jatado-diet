import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run("app.main:app", port=port, reload=True)
