import uvicorn
import sys
import os

if __name__ == "__main__":
    # 切换到 generals-mvp 目录
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    port = 8000
    uvicorn.run("generals-mvp.server.app:app", host="127.0.0.1", port=port, reload=True)