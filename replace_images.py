#!/usr/bin/env python3
import re
from pathlib import Path

# Ler o arquivo HTML original
html_path = Path('/workspace/portifolio.backup')
html_content = html_path.read_text()

# Mapeamento das imagens base64 para arquivos externos
# (extraído na ordem em que aparecem no HTML)
image_mapping = [
    'assets/images/hero-bg.jpeg',  # image_01 - já existia
    'assets/projects/image_02.jpeg',
    'assets/projects/image_03.jpeg',
    'assets/projects/image_04.jpeg',
    'assets/projects/image_05.jpeg',
    'assets/projects/image_06.jpeg',
    'assets/projects/image_07.jpeg',
    'assets/projects/image_08.jpeg',
    'assets/projects/image_09.jpeg',
    'assets/projects/image_10.jpeg',
    'assets/projects/image_11.jpeg',
]

# Padrão para encontrar imagens base64 JPEG
pattern = r'data:image/jpeg;base64,[A-Za-z0-9+/=]+'

# Contador para substituição
count = 0

def replace_image(match):
    global count
    if count < len(image_mapping):
        replacement = image_mapping[count]
        count += 1
        return replacement
    return match.group(0)

# Substituir todas as imagens base64 por caminhos de arquivos
new_html_content = re.sub(pattern, replace_image, html_content)

# Salvar o novo HTML
output_path = Path('/workspace/portifolio')
output_path.write_text(new_html_content)

print(f"Substituídas {count} imagens base64 por arquivos externos")
print("Arquivo atualizado: /workspace/portifolio")
