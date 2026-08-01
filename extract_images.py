#!/usr/bin/env python3
import re
import base64
from pathlib import Path

# Ler o arquivo HTML
html_path = Path('/workspace/portifolio')
html_content = html_path.read_text()

# Padrão para encontrar imagens base64
pattern = r'data:image/(jpeg|png|webp);base64,([A-Za-z0-9+/=]+)'

# Encontrar todas as imagens
images = re.findall(pattern, html_content)
print(f"Encontradas {len(images)} imagens base64")

# Extrair cada imagem
for i, (img_type, img_data) in enumerate(images):
    try:
        # Decodificar base64
        img_bytes = base64.b64decode(img_data)
        
        # Salvar como arquivo
        img_filename = f'image_{i+1:02d}.{img_type}'
        img_path = Path('/workspace/assets/projects') / img_filename
        
        with open(img_path, 'wb') as f:
            f.write(img_bytes)
        
        print(f"Salvo: {img_filename} ({len(img_bytes)} bytes)")
    except Exception as e:
        print(f"Erro na imagem {i+1}: {e}")

print("\nExtração concluída!")
