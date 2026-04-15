import requests, os, time
from PIL import Image, ImageFilter
import img2pdf
from io import BytesIO

os.makedirs("output/images", exist_ok=True)

with open("prompts.txt") as f:
    prompts = [line.strip() for line in f if line.strip()]

image_paths = []

for i, prompt in enumerate(prompts):
    print(f"Generating image {i+1}: {prompt}")
    encoded = requests.utils.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true"
    response = requests.get(url, timeout=60)
    if response.status_code == 200:
        img_path = f"output/images/image_{i+1}.png"
        img = Image.open(BytesIO(response.content)).convert("L")
        img = img.filter(ImageFilter.SHARPEN)
        img = img.point(lambda x: 0 if x < 128 else 255)
        img.save(img_path)
        image_paths.append(img_path)
        print(f"Image {i+1} saved!")
    else:
        print(f"Failed: {response.status_code}")
    time.sleep(3)

print("Creating PDF...")
with open("output/coloring_book.pdf", "wb") as f:
    f.write(img2pdf.convert(image_paths))
print("PDF Ready!")
