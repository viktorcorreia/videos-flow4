import json
from PIL import Image

data = json.load(open('manifest.json', 'r', encoding='utf-8'))

html = """
<!DOCTYPE html>
<html>
<head>
<style>
body { background: #18181b; color: #f4f4f5; font-family: sans-serif; padding: 20px; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
.card { background: #27272a; border-radius: 8px; padding: 12px; border: 1px solid #3f3f46; }
.card h3 { font-size: 13px; margin: 0 0 8px 0; word-break: break-all; color: #a1a1aa; }
.imgs { display: flex; gap: 8px; }
.imgs img { width: 50%; border-radius: 4px; object-fit: cover; }
</style>
</head>
<body>
<h2>Catálogo de Frames</h2>
<div class="grid">
"""

for i, item in enumerate(data):
    fn = item['arquivo']
    f1 = item['frames'][0]
    f2 = item['frames'][1]
    html += f"""
    <div class="card">
        <h3>#{i+1:02d}: {fn}</h3>
        <div class="imgs">
            <img src="{f1}">
            <img src="{f2}">
        </div>
    </div>
    """

html += """
</div>
</body>
</html>
"""

with open('catalog_preview.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("catalog_preview.html criado com sucesso!")
