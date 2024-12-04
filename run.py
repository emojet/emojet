import os
import json
import time
import base64
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler

# 设置静态文件目录
src_path = os.path.join(os.getcwd(), 'src')

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # 重写translate_path方法
        # 将请求路径转换到./src/目录
        path = super().translate_path(path)
        relpath = os.path.relpath(path, os.getcwd())
        return os.path.join(src_path, relpath)

    def do_GET(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            # 如果路径是目录，尝试返回index.html
            index_path = os.path.join(path, 'index.html')
            if os.path.exists(index_path):
                path = index_path
        self.path = os.path.relpath(path, src_path)
        return super().do_GET()

    def do_POST(self):
        if self.path == '/add':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                form_data = json.loads(post_data)
                root_class = form_data['root_class']
                emotion = form_data['emotion']
                ext = form_data['ext']
                img = base64.b64decode(form_data['img'])
                form_data['img'] = img
                self.handle_add(form_data)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"JSON data received and processed.")
            except (json.JSONDecodeError, KeyError) as e:
                self.send_error(400, f"Bad Request: {str(e)}")

        else:
            self.send_error(404, "File not found")

    def handle_add(self, form_data):
        root_class = form_data['root_class']
        emotion = form_data['emotion']
        ext = form_data['ext']
        img_base_path = os.path.join(os.getcwd(), 'pages', root_class)
        if not os.path.exists(img_base_path):
            os.makedirs(img_base_path)
        img_path = os.path.join(img_base_path, emotion + '.' + ext)
        # 如果文件已存在，则返回409响应
        if os.path.exists(img_path):
            self.send_error(409, "File already exists")
            return
        # 保存文件
        with open(img_path, 'wb') as f:
            f.write(form_data['img'])

        # 更新索引
        json_index_path: str = os.path.join(os.getcwd(), 'pages', root_class, 'index.json')
        if os.path.exists(json_index_path):
            with open(json_index_path, 'r', encoding="utf-8") as f:
                index = json.load(f)
        else:
            index = {}
        index[emotion] = f"{emotion}.{ext}"
        with open(json_index_path, 'w', encoding="utf-8") as f:
            json.dump(index, f, ensure_ascii=False, indent=4)
        root_json_index_path: str = os.path.join(os.getcwd(), 'pages', 'index.json')
        if os.path.exists(root_json_index_path):
            with open(root_json_index_path, 'r', encoding="utf-8") as f:
                root_index = json.load(f)
        else:
            root_index = {
                "emotions": {},
                "classes": []
            }
        root_index["emotions"][emotion] = root_index.get(emotion, []) + [f"{root_class}/{emotion}.{ext}"]
        root_index["classes"] = list(set(root_index["classes"] + [root_class]))
        with open(root_json_index_path, 'w', encoding="utf-8") as f:
            json.dump(root_index, f, ensure_ascii=False, indent=4)


# 设置服务器地址和端口
server_address = ('', 8000)
httpd = HTTPServer(server_address, CustomHTTPRequestHandler)

print(f"Serving HTTP on port {server_address[1]}...")
print(f"You can access the server at http://localhost:{server_address[1]}/")
print(f"The browser will open automatically.")
time.sleep(2)
webbrowser.open(f"http://localhost:{server_address[1]}/")
httpd.serve_forever()