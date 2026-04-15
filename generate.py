import requests, os, time
from PIL import Image, ImageFilter
import img2pdf

HF_TOKEN = os.environ["HF_TOKEN"]
API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

os.makedirs("output/images", exist_ok=True)

with open("prompts.txt") as f:
    prompts = [line.strip() for line in f if line.strip()]

image_paths = []

for i, prompt in enumerate(prompts):
    print(f"Generating image {i+1}: {prompt}")
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    if response.status_code == 200:
        img_path = f"output/images/image_{i+1}.png"
        with open(img_path, "wb") as f:
            f.write(response.content)
        img = Image.open(img_path).convert("L")
        img = img.filter(ImageFilter.SHARPEN)
        img = img.point(lambda x: 0 if x < 128 else 255)
        img.save(img_path)
        image_paths.append(img_path)
        print(f"Image {i+1} saved!")
    else:
        print(f"Failed: {response.text}")
    time.sleep(2)

print("Creating PDF...")
with open("output/coloring_book.pdf", "wb") as f:
    f.write(img2pdf.convert(image_paths))
print("PDF Ready!")
