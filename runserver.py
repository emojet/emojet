from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

class CustomStaticFiles(StaticFiles):
    async def get_response(self, path, scope):
        full_path = os.path.join(self.directory, path)
        if os.path.isdir(full_path):
            index_path = os.path.join(full_path, 'index.html')
            if os.path.exists(index_path):
                path = os.path.join(path, 'index.html')
        return await super().get_response(path, scope)

app = FastAPI()

# 设置静态文件目录
pages_path = os.path.join(os.getcwd(), 'pages')

# 挂载静态文件目录
app.mount("/", CustomStaticFiles(directory=pages_path), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)