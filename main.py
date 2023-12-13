import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    port = int(os.environ.get("PORT"))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
