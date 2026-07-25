import os
import json
from PIL import Image

def analyze_frames(f1_path, f2_path):
    img1 = Image.open(f1_path)
    img2 = Image.open(f2_path)
    # Check simple pixel difference between f1 and f2 to help detect product movement
    # Resize both to small 64x64 and compare mean diff
    i1 = img1.resize((64, 64)).convert('RGB')
    i2 = img2.resize((64, 64)).convert('RGB')
    
    b1 = list(i1.getdata())
    b2 = list(i2.getdata())
    
    diff = sum(abs(b1[k][c] - b2[k][c]) for k in range(len(b1)) for c in range(3)) / (len(b1) * 3)
    return diff

print("Frame analyzer ready")
