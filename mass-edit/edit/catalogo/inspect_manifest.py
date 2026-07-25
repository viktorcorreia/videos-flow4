import json
import os

with open('manifest.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for i, item in enumerate(data):
    fn = item['arquivo']
    f1 = item['frames'][0]
    f2 = item['frames'][1]
    print(f"{i+1:02d}: {fn}")
