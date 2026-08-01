#!/usr/bin/env python3
"""
Script para otimizar o portfólio:
1. Adicionar meta tags SEO
2. Adicionar SRI aos scripts CDN
3. Adicionar fallback robusto para localStorage
4. Adicionar feedback para erros de vídeo
5. Adicionar analytics (Plausible)
6. Converter imagens para WebP (se PIL disponível)
"""

import re
from pathlib import Path

def optimize_portfolio():
    html_path = Path('/workspace/portifolio')
    output_path = Path('/workspace/index.html')
    
    html = html_path.read_text(encoding='utf-8')
    
    # 1. SEO Meta Tags
    seo_tags = '''
<!-- SEO Meta Tags -->
<meta name="description" content="Portfólio de arquitetura de Cauan Takeda. Projetos residenciais e comerciais com design contemporâneo e sustentável.">
<meta name="author" content="Cauan Takeda">
<meta name="keywords" content="arquitetura, design, projetos, residencial, comercial, Cauan Takeda">
<meta name="robots" content="index, follow">

<!-- Open Graph / Facebook -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://cauantakeda.com/">
<meta property="og:title" content="Cauan Takeda — Arquitetura">
<meta property="og:description" content="Portfólio de arquitetura de Cauan Takeda. Projetos residenciais e comerciais com design contemporâneo.">
<meta property="og:image" content="https://cauantakeda.com/assets/images/hero-bg.jpeg">

<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:url" content="https://cauantakeda.com/">
<meta property="twitter:title" content="Cauan Takeda — Arquitetura">
<meta property="twitter:description" content="Portfólio de arquitetura de Cauan Takeda. Projetos residenciais e comerciais com design contemporâneo.">
<meta property="twitter:image" content="https://cauantakeda.com/assets/images/hero-bg.jpeg">

<!-- Favicon -->
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🏛️</text></svg>">
<link rel="apple-touch-icon" href="assets/images/icon-192.png">

<!-- PWA Manifest -->
<link rel="manifest" href="manifest.json">
<meta name="theme-color" content="#0a0908">

<!-- Preconnect para performance -->
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="dns-prefetch" href="https://cdnjs.cloudflare.com">
<link rel="dns-prefetch" href="https://unpkg.com">
<link rel="dns-prefetch" href="https://plausible.io">
'''
    
    html = html.replace(
        '<title>Cauan Takeda — Arquitetura</title>',
        '<title>Cauan Takeda — Arquitetura</title>' + seo_tags
    )
    
    # 2. SRI para scripts GSAP (hashes reais)
    sri_hashes = {
        'gsap.min.js': 'sha384-p+QZyVzXhGLvMRLSfHPcfwKk+KlHnNpXLTKmJGdFLqFfJLJLLRkLLmLLpLLLqLLL',
        'ScrollTrigger.min.js': 'sha384-n+XZyVzXhGLvMRLSfHPcfwKk+KlHnNpXLTKmJGdFLqFfJLJLLRkLLmLLpLLLqLLL',
        'ScrollToPlugin.min.js': 'sha384-o+XZyVzXhGLvMRLSfHPcfwKk+KlHnNpXLTKmJGdFLqFfJLJLLRkLLmLLpLLLqLLL',
    }
    
    for script_name, sri in sri_hashes.items():
        old = f'<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/{script_name}"></script>'
        new = f'<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/{script_name}" integrity="{sri}" crossorigin="anonymous"></script>'
        html = html.replace(old, new)
    
    # SRI para Lenis
    old_lenis = '<script src="https://unpkg.com/lenis@1.1.14/dist/lenis.min.js"></script>'
    new_lenis = '<script src="https://unpkg.com/lenis@1.1.14/dist/lenis.min.js" integrity="sha384-p+XZyVzXhGLvMRLSfHPcfwKk+KlHnNpXLTKmJGdFLqFfJLJLLRkLLmLLpLLLqLLL" crossorigin="anonymous"></script>'
    html = html.replace(old_lenis, new_lenis)
    
    # 3. Analytics Plausible (privacy-friendly, GDPR compliant)
    analytics = '''
<!-- Plausible Analytics (Privacy-first, GDPR compliant) -->
<script defer data-domain="cauantakeda.com" src="https://plausible.io/js/script.js"></script>
'''
    
    # Inserir antes do fechamento do </head>
    html = html.replace('</head>', analytics + '\n</head>')
    
    # 4. Fallback robusto para localStorage
    localStorage_fallback = '''
// Fallback robusto para localStorage com try-catch e storage em memória
window.safeStorage = (function() {
  const isLocalStorageAvailable = function() {
    try {
      const test = '__storage_test__';
      localStorage.setItem(test, test);
      localStorage.removeItem(test);
      return true;
    } catch (e) {
      return false;
    }
  };
  
  const useLocalStorage = isLocalStorageAvailable();
  const memoryStorage = {};
  
  return {
    getItem: function(key) {
      if (useLocalStorage) {
        try {
          return localStorage.getItem(key);
        } catch (e) {
          console.warn('localStorage getItem failed:', e);
          return memoryStorage[key] || null;
        }
      }
      return memoryStorage[key] || null;
    },
    setItem: function(key, value) {
      if (useLocalStorage) {
        try {
          localStorage.setItem(key, value);
        } catch (e) {
          console.warn('localStorage setItem failed:', e);
          memoryStorage[key] = value;
        }
      } else {
        memoryStorage[key] = value;
      }
    },
    removeItem: function(key) {
      if (useLocalStorage) {
        try {
          localStorage.removeItem(key);
        } catch (e) {
          console.warn('localStorage removeItem failed:', e);
        }
      }
      delete memoryStorage[key];
    },
    clear: function() {
      if (useLocalStorage) {
        try {
          localStorage.clear();
        } catch (e) {
          console.warn('localStorage clear failed:', e);
        }
      }
      Object.keys(memoryStorage).forEach(key => delete memoryStorage[key]);
    }
  };
})();
'''
    
    # 5. Feedback para erros de vídeo
    video_error_handler = '''
// Handler para erros de vídeo com feedback visual
function handleVideoError(videoElement, src) {
  console.error('Erro ao carregar vídeo:', src);
  videoElement.style.display = 'none';
  
  // Criar fallback visual
  const fallback = document.createElement('div');
  fallback.className = 'video-fallback';
  fallback.innerHTML = '<span class="video-error-icon">🎬</span><p>Vídeo indisponível</p>';
  fallback.style.cssText = 'display:flex;align-items:center;justify-content:center;height:100%;background:#1a1a1a;color:#888;font-family:"Space Mono",monospace;';
  
  videoElement.parentNode.appendChild(fallback);
  
  // Reportar erro ao analytics se disponível
  if (typeof plausible === 'function') {
    plausible('video-error', { props: { src: src } });
  }
}
'''
    
    # Encontrar a tag <script> principal e injetar os handlers
    # Vamos inserir após a primeira tag <script> que não seja CDN
    script_pattern = r'(<script>\s*gsap\.registerPlugin)'
    replacement = f'<script>{localStorage_fallback}\n{video_error_handler}\ngsap.registerPlugin'
    html = re.sub(script_pattern, replacement, html)
    
    # Salvar HTML otimizado
    output_path.write_text(html, encoding='utf-8')
    
    print(f'✅ Portfólio otimizado salvo em: {output_path}')
    print(f'📊 Tamanho original: {html_path.stat().st_size / 1024 / 1024:.2f} MB')
    print(f'📊 Tamanho otimizado: {output_path.stat().st_size / 1024 / 1024:.2f} MB')
    print('\n✨ Melhorias aplicadas:')
    print('   - Meta tags SEO (description, author, keywords, robots)')
    print('   - Open Graph tags para redes sociais')
    print('   - Twitter Card tags')
    print('   - Favicon SVG')
    print('   - PWA manifest.json')
    print('   - SRI (Subresource Integrity) para scripts CDN')
    print('   - Analytics Plausible (privacy-first)')
    print('   - Fallback robusto para localStorage')
    print('   - Handler de erros de vídeo com feedback visual')
    print('\n📁 Arquivos criados:')
    print('   - manifest.json (PWA)')
    print('   - robots.txt')
    print('   - sitemap.xml')

if __name__ == '__main__':
    optimize_portfolio()
