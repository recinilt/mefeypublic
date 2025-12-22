from openai import OpenAI
import base64

client = OpenAI(api_key="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")  # key otomatik env'den alınır

result = client.images.generate(
    model="gpt-image-1",
    prompt="Sinematik ışıklandırmalı, yağlı boya tarzı kedi",
    size="1024x1024"
)

image_base64 = result.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

with open("kedi.png", "wb") as f:
    f.write(image_bytes)

print("✔ Görsel oluşturuldu: kedi.png")
