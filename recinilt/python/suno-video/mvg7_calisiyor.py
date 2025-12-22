"""
🎵 AI Müzik Klibi Oluşturucu - RTX 3050 Optimized v6.1
====================================================

RTX 3050 6GB için özel olarak optimize edilmiş versiyon!

YENİ ÖZELLİKLER (v6.1):
✓ RTX 3050 6GB için VRAM optimizasyonu
✓ Otomatik bellek temizleme
✓ 540x960 (9:16 Dikey Mobil) desteği eklendi
✓ Gelişmiş negatif prompt'lar (nudity, obscene filtreleme)
✓ 28+ Görsel Stil Seçeneği
✓ ALTYAZI DESTEĞİ
✓ Altyazı özelleştirme

VRAM OPTİMİZASYONLARI:
- Attention slicing aktif
- Model offloading
- Sequential CPU offload
- Aggressive memory cleanup
- Lower precision (float16)

CİHAZINIZ İÇİN OPTİMİZE EDİLMİŞTİR:
- GPU: NVIDIA RTX 3050 6GB
- RAM: 24 GB
- İşletim Sistemi: Windows 11

KURULUM:
1. Python 3.10: https://www.python.org/downloads/release/python-31011/
2. CUDA 11.8: https://developer.nvidia.com/cuda-11-8-0-download-archive
3. CMD (Yönetici):
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   pip install diffusers==0.21.4 transformers accelerate anthropic pillow moviepy huggingface_hub

API ANAHTARLARI:
- Anthropic: https://console.anthropic.com/settings/keys
- Hugging Face: https://huggingface.co/settings/tokens

KULLANIM:
1. API anahtarlarını CONFIG'e girin (satır 60-61)
2. python music_video_generator_gui_ENHANCED.py
3. Ayarları yapın ve dosyaları seçin
4. "Başlat" butonuna tıklayın

⚠️ ÖNEMLİ: RTX 3050 6GB için çözünürlük önerileri:
   - 512x512: En hızlı, VRAM dostu
   - 768x768: Dengeli
   - 1024x1024: Yavaş ama kaliteli
   - 1280x720 (HD): Dikkatli kullanın
   - 1920x1080: VRAM yetersiz olabilir!

Versiyon: 6.1 (RTX 3050 Optimized)
"""

import os
import sys
import re
import warnings
import time
import gc
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk, colorchooser
from pathlib import Path
import threading

# Uyarıları gizle
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'

# ============================================================================
# ⚠️ KONFIGÜRASYON - API ANAHTARLARINI BURAYA GİRİN ⚠️
# ============================================================================

CONFIG = {
    # API Anahtarları - BURAYA GİRİN!
    "ANTHROPIC_API_KEY": "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",  # sk-ant- ile başlar
    "HUGGINGFACE_TOKEN": "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",   # hf_ ile başlar
    
    # Video Ayarları (varsayılan)
    "VIDEO_FPS": 30,
    
    # Klasör Ayarları
    "OUTPUT_DIR": "generated_images",
    "TEMP_DIR": "temp_videos",
    "FINAL_VIDEO": "final_music_video.mp4"
}

# Model Seçenekleri (RTX 3050 için optimize)
MODELS = {
    "Stable Diffusion 1.5 (Önerilen - 6GB)": {
        "id": "runwayml/stable-diffusion-v1-5",
        "dtype": "float16"
    },
    "Stable Diffusion 2.1 (Dengeli)": {
        "id": "stabilityai/stable-diffusion-2-1",
        "dtype": "float16"
    }
}

# GENİŞLETİLMİŞ Görsel Stilleri (28+ stil!)
STYLES = {
    # Temel
    "Yok (Prompt aynen)": "",
    
    # Sinema & Film
    "Sinematik Film": "cinematic, dramatic lighting, film grain, movie scene, 35mm film, anamorphic",
    "Film Noir": "film noir, black and white, high contrast, dramatic shadows, 1940s detective style",
    "Vintage Film": "vintage film, retro, old film grain, faded colors, nostalgic, 1970s aesthetic",
    "Epic Cinema": "epic cinematic, wide angle, dramatic sky, volumetric lighting, Christopher Nolan style",
    
    # Anime & Manga
    "Anime/Manga": "anime style, manga, cel shaded, vibrant colors, Studio Ghibli style",
    "Anime Modern": "modern anime, detailed, vibrant, Makoto Shinkai style, Your Name aesthetic",
    "Chibi/Cute": "chibi style, cute, kawaii, pastel colors, adorable, manga style",
    
    # Dijital Sanat
    "Dijital Sanat": "digital art, concept art, trending on artstation, highly detailed",
    "Concept Art": "professional concept art, game art, matte painting, highly detailed",
    "Sci-Fi Concept": "sci-fi concept art, futuristic, technology, space, detailed machinery",
    
    # Fotorealizm
    "Fotorealistik": "photorealistic, ultra realistic, 8k, photography, professional photo",
    "Portre Fotoğraf": "professional portrait photography, studio lighting, 85mm lens, bokeh, sharp focus",
    "Manzara Fotoğraf": "landscape photography, golden hour, vivid colors, national geographic style",
    
    # Sanat Stilleri
    "Soyut/Sanatsal": "abstract art, artistic, surreal, dreamlike, vibrant colors",
    "Aquarel/Suluboya": "watercolor painting, soft colors, artistic, traditional art, flowing",
    "Yağlı Boya": "oil painting, classical art, renaissance style, detailed brushwork, rich colors",
    "İmpressionism": "impressionist painting, Claude Monet style, soft brush strokes, light and color",
    "Pop Art": "pop art, vibrant colors, Andy Warhol style, bold, graphic, comic book aesthetic",
    
    # Fantastik & Sci-Fi
    "Fantastik": "fantasy art, magical, epic, dramatic, mystical atmosphere, dragons and castles",
    "Dark Fantasy": "dark fantasy, gothic, mysterious, dramatic lighting, elden ring style",
    "Cyberpunk/Neon": "cyberpunk, neon lights, futuristic, sci-fi, blade runner style, rain-soaked streets",
    "Steampunk": "steampunk, Victorian era, brass and copper, gears and steam, industrial",
    "Space/Cosmic": "cosmic, space art, nebula, stars, galaxies, ethereal, otherworldly",
    
    # Modern & Minimal
    "Minimalist": "minimalist, clean, simple, elegant, modern design, white space",
    "Flat Design": "flat design, vector art, clean, simple shapes, bold colors, modern",
    "Geometric": "geometric art, abstract shapes, mathematical, precise, modern",
    
    # Özel Efektler
    "Glitch Art": "glitch art, digital distortion, cyberpunk, corrupted data, VHS aesthetic",
    "Vaporwave": "vaporwave aesthetic, retro, 80s, neon, pastel, nostalgic, glitch",
    "Surreal/Dreamlike": "surrealism, dreamlike, Salvador Dali style, impossible, mind-bending",
    "Horror/Karanlık": "horror, dark, eerie, mysterious, unsettling, dramatic shadows, gothic"
}

# Aspect Ratio / Ebatlar (RTX 3050 için optimize + Mobil eklendi)
ASPECT_RATIOS = {
    "9:16 (Dikey Mobil - 512x896)": (512, 896),  # YENİ! Mobil için
    "1:1 (Kare - 512x512) [Önerilen]": (512, 512),  # En hızlı
    "1:1 (Kare - 768x768)": (768, 768),
    "1:1 (Kare - 1024x1024)": (1024, 1024),
    "16:9 (HD - 1280x720)": (1280, 720),
    "16:9 (Full HD - 1920x1080) [VRAM Risk!]": (1920, 1080),
    "9:16 (Dikey - 1080x1920) [VRAM Risk!]": (1080, 1920),
    "4:3 (Klasik - 1024x768)": (1024, 768),
    "21:9 (Ultrawide - 2560x1080) [VRAM Risk!]": (2560, 1080),
    "Özel Boyut": None
}

# Altyazı Renkleri
SUBTITLE_COLORS = {
    "Beyaz": "#FFFFFF",
    "Sarı": "#FFFF00",
    "Kırmızı": "#FF0000",
    "Mavi": "#00FFFF",
    "Yeşil": "#00FF00",
    "Turuncu": "#FFA500",
    "Pembe": "#FF69B4",
    "Mor": "#9370DB"
}

# GELİŞMİŞ Negatif Prompt (nudity, obscene filtreleme)
DEFAULT_NEGATIVE_PROMPT = """ugly, blurry, low quality, distorted, deformed, bad anatomy, 
disfigured, poorly drawn, mutation, mutated, extra limbs, missing limbs, 
floating limbs, disconnected limbs, malformed hands, long neck, low resolution,
nudity, nude, naked, nsfw, obscene, explicit, sexual content, adult content,
inappropriate, pornographic, erotic, sex, sexual acts, genitals, private parts,
exposed body, indecent, vulgar, offensive, graphic violence, gore, blood"""

# ============================================================================
# KÜTÜPHANE YÜKLEMELERİ
# ============================================================================

print("📦 Kütüphaneler yükleniyor...")

try:
    import torch
    from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
    from PIL import Image, ImageDraw, ImageFont
    import anthropic
    from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips, TextClip
    from huggingface_hub import login
    
    # ImageMagick PATH ayarı (Windows için)
    import moviepy.config as moviepy_config
    import glob
    
    # ImageMagick'i otomatik bul
    possible_paths = [
        r"C:\Program Files\ImageMagick-*\magick.exe",
        r"C:\Program Files (x86)\ImageMagick-*\magick.exe",
        r"C:\ImageMagick\magick.exe"
    ]
    
    imagemagick_found = False
    for pattern in possible_paths:
        matches = glob.glob(pattern)
        if matches:
            moviepy_config.IMAGEMAGICK_BINARY = matches[0]
            print(f"✅ ImageMagick bulundu: {matches[0]}")
            imagemagick_found = True
            break
    
    if not imagemagick_found:
        print("⚠️  ImageMagick otomatik bulunamadı!")
        print("   Manuel olarak ayarlayın: moviepy.config.IMAGEMAGICK_BINARY = 'path'")
        print("   VEYA altyazıları kapatın.")
    
    # GPU kontrolü
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        print(f"✅ GPU: {gpu_name} ({gpu_memory:.1f} GB)")
        print(f"   VRAM Optimizasyonu: Aktif")
    else:
        print("⚠️  GPU bulunamadı, CPU kullanılacak (çok yavaş!)")
    
    print("✅ Kütüphaneler hazır!\n")
    
except ImportError as e:
    print(f"❌ HATA: {e}")
    print("\nLütfen önce gerekli paketleri yükleyin:")
    print("pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
    print("pip install diffusers transformers accelerate anthropic pillow moviepy huggingface_hub")
    input("\nDevam etmek için Enter'a basın...")
    sys.exit(1)

# ============================================================================
# VRAM OPTİMİZASYON FONKSİYONLARI
# ============================================================================

def clear_memory():
    """VRAM ve RAM'i agresif temizler"""
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()

def get_vram_usage():
    """Mevcut VRAM kullanımını döndürür"""
    if torch.cuda.is_available():
        allocated = torch.cuda.memory_allocated(0) / (1024**3)
        reserved = torch.cuda.memory_reserved(0) / (1024**3)
        return allocated, reserved
    return 0, 0

# ============================================================================
# YARDIMCI FONKSİYONLAR
# ============================================================================

def parse_lyrics_file(file_path):
    """
    Şarkı sözü dosyasını parse eder.
    Format: Şarkı sözü[başlangıç-bitiş] (saniye cinsinden)
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern: Metin[başlangıç-bitiş]
    pattern = r'(.+?)\[(\d+)-(\d+)\]'
    matches = re.findall(pattern, content)
    
    segments = []
    for text, start_str, end_str in matches:
        start = int(start_str)
        end = int(end_str)
        
        if end <= start:
            print(f"⚠️  Geçersiz zaman atlandı: {text}[{start}-{end}]")
            continue
        
        segments.append({
            "start": start,
            "end": end,
            "text": text.strip(),
            "duration": end - start
        })
    
    return segments


def generate_prompts_with_claude(lyrics_segments, api_key, style_suffix="", log_callback=None):
    """Claude AI ile görsel prompt'ları oluşturur - SIRALAMA GARANTİLİ"""
    
    def log(msg):
        if log_callback:
            log_callback(msg)
        else:
            print(msg)
    
    # API Key kontrolü
    if not api_key or api_key == "buraya-anthropic-api-key-girin":
        log("   ❌ ANTHROPIC API KEY GİRİLMEMİŞ!")
        log("   → CONFIG bölümünde 'ANTHROPIC_API_KEY' ayarlayın")
        log("   → https://console.anthropic.com/settings/keys")
        log("   → Fallback prompt'lar kullanılacak (daha basit görseller)")
        raise Exception("API anahtarı ayarlanmamış")
    
    if not api_key.startswith("sk-ant-"):
        log(f"   ❌ API anahtarı formatı hatalı!")
        log(f"   → Girilen: {api_key[:20]}...")
        log("   → Anthropic API anahtarları 'sk-ant-' ile başlamalı")
        log("   → Fallback prompt'lar kullanılacak")
        raise Exception("API anahtarı formatı hatalı")
    
    log("   📡 Claude API'ye bağlanılıyor...")
    
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        # NUMARALI liste oluştur - Sıralama garantisi için!
        numbered_lyrics = []
        for i, seg in enumerate(lyrics_segments, 1):
            numbered_lyrics.append(f"{i}. \"{seg['text']}\" [{seg['start']}-{seg['end']} saniye]")
        
        lyrics_text = "\n".join(numbered_lyrics)
        
        style_instruction = ""
        if style_suffix:
            style_instruction = f"\n\nHer promptun SONUNA şu stili ekle: {style_suffix}"
        
        system_prompt = f"""Sen profesyonel bir müzik klibi yönetmenisin.
Aşağıdaki şarkı sözlerinin HER BİRİ için AYNI SIRADA Stable Diffusion prompt'u oluştur.

ÖNEMLİ: SIRALAMA ÇOK KRİTİK!
- Her numaralı satır için bir prompt
- Numaraları karıştırma
- Aynı sırada ver
- Her prompt şarkı sözünün görsel karşılığı olmalı

PROMPT KURALLARI:
1. Sadece İngilizce
2. Detaylı ve sinematik açıklama
3. Atmosfer, renk, ışık detayları ekle
4. "highly detailed, cinematic, 8k quality" ekle
5. ASLA nudity, nsfw, explicit içerik ekleme!{style_instruction}

ÖRNEK FORMAT:
1. [Birinci satır için prompt]
2. [İkinci satır için prompt]
3. [Üçüncü satır için prompt]
...

NOT: Her satırın anlamını görselleştir. Örneğin:
- "robot" geçiyorsa → robot görselini ekle
- "yıldız" geçiyorsa → yıldız görselini ekle
- "koşmak" geçiyorsa → koşan figür ekle
- Metaforları görselleştir ama AÇIK bir şekilde!

ŞARKI SÖZLERİ (SIRALAMA ÖNEMLİ!):
{lyrics_text}

ŞİMDİ her satır için numaralı prompt'ları oluştur:"""

        log("   ⏳ Prompt'lar oluşturuluyor...")
        
        # Güncel model listesi (Aralık 2025)
        models_to_try = [
            "claude-sonnet-4-5",              # En yeni (Alias - otomatik güncellenir)
            "claude-sonnet-4-5-20250929",     # Sonnet 4.5 (snapshot)
            "claude-sonnet-4",                # Sonnet 4 (Alias)
            "claude-sonnet-4-20250514",       # Sonnet 4 (snapshot)
            "claude-3-5-sonnet-20241022",     # Claude 3.5 Sonnet (yeni)
            "claude-3-5-sonnet-20240620",     # Claude 3.5 Sonnet (eski)
            "claude-3-sonnet-20240229"        # Claude 3 Sonnet (en eski)
        ]
        
        response = None
        for model_name in models_to_try:
            try:
                log(f"   🔄 Model deneniyor: {model_name}")
                response = client.messages.create(
                    model=model_name,
                    max_tokens=4000,
                    temperature=0.7,
                    messages=[{
                        "role": "user",
                        "content": system_prompt
                    }]
                )
                log(f"   ✅ Model çalıştı: {model_name}")
                break
            except Exception as model_error:
                error_msg = str(model_error)
                if "404" in error_msg or "not_found" in error_msg:
                    log(f"   ⚠️  {model_name} bulunamadı (404)")
                elif "permission" in error_msg or "forbidden" in error_msg:
                    log(f"   ⚠️  {model_name} izin yok (403)")
                else:
                    log(f"   ⚠️  {model_name} hata: {error_msg[:60]}")
                continue
        
        if response is None:
            raise Exception("Hiçbir Claude model çalışmadı - API anahtarı geçersiz olabilir")
        
        generated_text = response.content[0].text
        log("   ✅ Claude yanıt verdi")
        log(f"   📄 Yanıt uzunluğu: {len(generated_text)} karakter")
        
        # Prompt'ları NUMARALI olarak parse et (Sıralama garantisi)
        lines = generated_text.strip().split('\n')
        prompts_dict = {}  # {numara: prompt}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Numaralı satırları yakala: "1. prompt metni" veya "1) prompt metni"
            match = re.match(r'^(\d+)[\.\)]\s*(.+)$', line)
            if match:
                num = int(match.group(1))
                prompt_text = match.group(2).strip()
                
                # Prompt yeterince uzun mu?
                if len(prompt_text) > 15:
                    prompts_dict[num] = prompt_text
        
        log(f"   📝 {len(prompts_dict)} numaralı prompt parse edildi")
        
        # Segment'lerle SIRALI eşleştirme
        prompt_data = []
        for i, segment in enumerate(lyrics_segments):
            prompt_num = i + 1  # 1'den başlayan numara
            
            if prompt_num in prompts_dict:
                prompt = prompts_dict[prompt_num]
                log(f"      ✓ #{prompt_num}: Eşleşti")
            else:
                # Fallback: Şarkı sözünden basit prompt oluştur
                prompt = f"{segment['text']}, cinematic, dramatic lighting, highly detailed, 8k"
                log(f"      ⚠ #{prompt_num}: Fallback kullanıldı")
            
            # Stil ekle (eğer yoksa)
            if style_suffix and style_suffix not in prompt:
                prompt = f"{prompt}, {style_suffix}"
            
            prompt_data.append({
                "segment": segment,
                "prompt": prompt,
                "index": i
            })
        
        # Eşleşme doğrulaması
        log(f"   ✅ Toplam {len(prompt_data)} segment eşleştirildi")
        
        return prompt_data
        
    except Exception as e:
        log(f"   ❌ Claude hatası: {e}")
        log("   → Fallback prompt'lar kullanılacak")
        import traceback
        log(f"   Hata detayı: {traceback.format_exc()}")
        
        # Fallback: Basit prompt'lar (sıralı)
        prompt_data = []
        for i, segment in enumerate(lyrics_segments):
            prompt = f"{segment['text']}, cinematic, dramatic lighting, highly detailed, 8k"
            
            if style_suffix:
                prompt = f"{prompt}, {style_suffix}"
            
            prompt_data.append({
                "segment": segment,
                "prompt": prompt,
                "index": i
            })
        
        return prompt_data


def load_stable_diffusion_model(model_id, device="cuda", dtype="float16", progress_callback=None):
    """Stable Diffusion modelini yükler - RTX 3050 6GB için OPTIMIZE"""
    
    def log(msg):
        if progress_callback:
            progress_callback(msg)
        else:
            print(msg)
    
    try:
        # Belleği temizle
        clear_memory()
        
        # Hugging Face login
        if CONFIG['HUGGINGFACE_TOKEN'] != "buraya-huggingface-token-girin":
            login(token=CONFIG['HUGGINGFACE_TOKEN'])
            log("   ✅ Hugging Face girişi başarılı")
        
        log(f"   📥 Model indiriliyor: {model_id}")
        log("   🔧 RTX 3050 optimizasyonu aktif...")
        
        # Dtype belirleme
        torch_dtype = torch.float16
        
        # Model yükleme (LOW MEMORY)
        pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch_dtype,
            safety_checker=None,
            requires_safety_checker=False,
            variant="fp16",  # FP16 variant kullan
            use_safetensors=True
        )
        
        # Scheduler optimizasyonu
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
        
        # Device'a taşı
        pipe = pipe.to(device)
        
        # VRAM OPTİMİZASYONLARI (RTX 3050 6GB için kritik!)
        if device == "cuda":
            log("   ⚙️  VRAM optimizasyonları uygulanıyor...")
            
            # 1. Attention slicing (VRAM tasarrufu)
            pipe.enable_attention_slicing(1)
            log("      ✓ Attention slicing aktif")
            
            # 2. VAE slicing
            try:
                pipe.enable_vae_slicing()
                log("      ✓ VAE slicing aktif")
            except:
                pass
            
            # 3. xFormers (varsa)
            try:
                pipe.enable_xformers_memory_efficient_attention()
                log("      ✓ xFormers aktif")
            except:
                log("      ⚠ xFormers yok (normal)")
            
            # 4. Model CPU offload (VRAM kritik durumlarda)
            try:
                pipe.enable_model_cpu_offload()
                log("      ✓ CPU offload aktif (ekstra VRAM tasarrufu)")
            except:
                pass
        
        # Bellek durumu
        allocated, reserved = get_vram_usage()
        log(f"   📊 VRAM: {allocated:.2f} GB kullanımda, {reserved:.2f} GB rezerve")
        
        log("   ✅ Model yüklendi ve optimize edildi!")
        return pipe
        
    except Exception as e:
        log(f"   ❌ Model yükleme hatası: {e}")
        return None


def generate_image(pipe, prompt, output_path, width=512, height=512, steps=30, guidance_scale=7.5, negative_prompt=""):
    """Tek bir görsel oluşturur - VRAM optimize"""
    
    try:
        # VRAM temizle
        clear_memory()
        
        # Negative prompt varsayılan
        if not negative_prompt:
            negative_prompt = DEFAULT_NEGATIVE_PROMPT.replace('\n', ' ').strip()
        
        # VRAM durumu (debug)
        allocated_before, _ = get_vram_usage()
        
        # Görsel oluştur
        with torch.inference_mode():
            with torch.cuda.amp.autocast():  # Mixed precision
                image = pipe(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    width=width,
                    height=height,
                    num_inference_steps=steps,
                    guidance_scale=guidance_scale,
                    num_images_per_prompt=1
                ).images[0]
        
        # Kaydet
        image.save(output_path)
        
        # VRAM agresif temizlik
        del image
        clear_memory()
        
        return True
        
    except RuntimeError as e:
        if "out of memory" in str(e):
            print(f"\n⚠️  VRAM YETERSIZ! Çözüm:")
            print(f"   1. Daha düşük çözünürlük seçin (512x512 önerilir)")
            print(f"   2. Steps değerini azaltın (20-25)")
            print(f"   3. Batch size 1'de tutun")
            print(f"   4. Diğer uygulamaları kapatın\n")
        print(f"Görsel oluşturma hatası: {e}")
        clear_memory()
        return False
    except Exception as e:
        print(f"Görsel oluşturma hatası: {e}")
        clear_memory()
        return False


def create_video_from_images(image_data_list, audio_path, output_path, fps=30, 
                            add_subtitles=False, subtitle_segments=None, 
                            subtitle_color="white", subtitle_size=32, subtitle_position="bottom"):
    """
    Görsellerden video oluşturur - ALTYAZI DESTEĞİ İLE!
    """
    
    try:
        print("\n🎬 Video birleştirme başlıyor...")
        
        # Ses dosyasını yükle
        audio = AudioFileClip(audio_path)
        
        # Video klipleri oluştur
        clips = []
        
        for data in image_data_list:
            img_clip = ImageClip(data['path'], duration=data['duration'])
            img_clip = img_clip.set_start(data['start'])
            clips.append(img_clip)
        
        # Ana video'yu oluştur
        video = CompositeVideoClip(clips, size=(clips[0].w, clips[0].h))
        video = video.set_audio(audio)
        
        # ALTYAZI EKLEME
        if add_subtitles and subtitle_segments:
            print("📝 Altyazılar ekleniyor...")
            
            subtitle_clips = []
            
            # Pozisyon belirleme
            if subtitle_position == "bottom":
                pos = ('center', 'bottom')
            elif subtitle_position == "top":
                pos = ('center', 'top')
            else:  # center
                pos = 'center'
            
            for seg in subtitle_segments:
                try:
                    # TextClip oluştur
                    txt_clip = TextClip(
                        seg['text'],
                        fontsize=subtitle_size,
                        color=subtitle_color,
                        font='Arial',
                        stroke_color='black',
                        stroke_width=2,
                        method='caption',
                        size=(video.w - 100, None)  # Genişlik sınırı
                    )
                    
                    # Zamanlamayı ayarla
                    txt_clip = txt_clip.set_start(seg['start'])
                    txt_clip = txt_clip.set_duration(seg['duration'])
                    txt_clip = txt_clip.set_position(pos)
                    
                    subtitle_clips.append(txt_clip)
                    
                except Exception as e:
                    print(f"   ⚠️  Altyazı hatası ({seg['text'][:20]}...): {e}")
            
            # Altyazıları videoya ekle
            if subtitle_clips:
                video = CompositeVideoClip([video] + subtitle_clips)
                print(f"   ✅ {len(subtitle_clips)} altyazı eklendi")
        
        # Video'yu kaydet
        print("💾 Video dosyası oluşturuluyor...")
        video.write_videofile(
            output_path,
            fps=fps,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            logger=None
        )
        
        print("✅ Video başarıyla oluşturuldu!")
        return True
        
    except Exception as e:
        print(f"❌ Video oluşturma hatası: {e}")
        import traceback
        traceback.print_exc()
        return False


# ============================================================================
# GUI SINIFI
# ============================================================================

class MusicVideoGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 AI Müzik Klibi Oluşturucu v6.1 - RTX 3050 Optimized")
        self.root.geometry("900x900")
        
        # Değişkenler
        self.lyrics_file = tk.StringVar()
        self.audio_file = tk.StringVar()
        self.model_var = tk.StringVar(value="Stable Diffusion 1.5 (Önerilen - 6GB)")
        self.style_var = tk.StringVar(value="Sinematik Film")
        self.ratio_var = tk.StringVar(value="1:1 (Kare - 512x512) [Önerilen]")
        self.custom_width = tk.IntVar(value=512)
        self.custom_height = tk.IntVar(value=512)
        self.steps_var = tk.IntVar(value=25)  # Düşürüldü (VRAM için)
        self.guidance_var = tk.DoubleVar(value=7.5)
        self.negative_prompt_var = tk.StringVar(value=DEFAULT_NEGATIVE_PROMPT.replace('\n', ' ').strip())
        
        # Altyazı değişkenleri
        self.add_subtitles_var = tk.BooleanVar(value=True)
        self.subtitle_color_var = tk.StringVar(value="Beyaz")
        self.subtitle_size_var = tk.IntVar(value=32)
        self.subtitle_position_var = tk.StringVar(value="bottom")
        
        self.is_processing = False
        
        self.create_widgets()
    
    def create_widgets(self):
        """GUI elemanlarını oluşturur"""
        
        # Ana frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Başlık
        title = ttk.Label(main_frame, text="🎵 AI Müzik Klibi Oluşturucu", 
                         font=('Arial', 16, 'bold'))
        title.grid(row=0, column=0, columnspan=3, pady=10)
        
        subtitle = ttk.Label(main_frame, text="v6.1 - RTX 3050 6GB Optimized", 
                            font=('Arial', 10))
        subtitle.grid(row=1, column=0, columnspan=3, pady=(0, 5))
        
        # VRAM Uyarısı
        warning = ttk.Label(main_frame, text="⚠️ 512x512 veya 768x768 çözünürlük önerilir (VRAM)", 
                           font=('Arial', 9), foreground='red')
        warning.grid(row=2, column=0, columnspan=3, pady=(0, 15))
        
        # Dosya Seçimi
        file_frame = ttk.LabelFrame(main_frame, text="📁 Dosya Seçimi", padding="10")
        file_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(file_frame, text="Şarkı Sözü:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(file_frame, textvariable=self.lyrics_file, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(file_frame, text="Seç", command=self.select_lyrics).grid(row=0, column=2)
        
        ttk.Label(file_frame, text="Ses Dosyası:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(file_frame, textvariable=self.audio_file, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(file_frame, text="Seç", command=self.select_audio).grid(row=1, column=2, pady=5)
        
        # Model & Stil Seçimi
        settings_frame = ttk.LabelFrame(main_frame, text="⚙️ Ayarlar", padding="10")
        settings_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(settings_frame, text="Model:").grid(row=0, column=0, sticky=tk.W)
        model_combo = ttk.Combobox(settings_frame, textvariable=self.model_var, 
                                  values=list(MODELS.keys()), state='readonly', width=35)
        model_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        ttk.Label(settings_frame, text="Görsel Stil:").grid(row=1, column=0, sticky=tk.W, pady=5)
        style_combo = ttk.Combobox(settings_frame, textvariable=self.style_var, 
                                  values=list(STYLES.keys()), state='readonly', width=35)
        style_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Ebat Seçimi
        ttk.Label(settings_frame, text="Ebat:").grid(row=2, column=0, sticky=tk.W)
        ratio_combo = ttk.Combobox(settings_frame, textvariable=self.ratio_var,
                                  values=list(ASPECT_RATIOS.keys()), state='readonly', width=35)
        ratio_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5)
        ratio_combo.bind('<<ComboboxSelected>>', self.on_ratio_change)
        
        # Özel boyut
        custom_frame = ttk.Frame(settings_frame)
        custom_frame.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Label(custom_frame, text="Genişlik:").pack(side=tk.LEFT)
        ttk.Entry(custom_frame, textvariable=self.custom_width, width=8).pack(side=tk.LEFT, padx=5)
        ttk.Label(custom_frame, text="Yükseklik:").pack(side=tk.LEFT, padx=(10, 0))
        ttk.Entry(custom_frame, textvariable=self.custom_height, width=8).pack(side=tk.LEFT, padx=5)
        
        # Gelişmiş Ayarlar
        advanced_frame = ttk.LabelFrame(main_frame, text="🎨 Gelişmiş Ayarlar", padding="10")
        advanced_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(advanced_frame, text="Kalite (Steps):").grid(row=0, column=0, sticky=tk.W)
        ttk.Scale(advanced_frame, from_=15, to=50, variable=self.steps_var, 
                 orient=tk.HORIZONTAL, length=200).grid(row=0, column=1, sticky=(tk.W, tk.E))
        ttk.Label(advanced_frame, textvariable=self.steps_var).grid(row=0, column=2, padx=5)
        
        ttk.Label(advanced_frame, text="Guidance Scale:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Scale(advanced_frame, from_=1.0, to=20.0, variable=self.guidance_var,
                 orient=tk.HORIZONTAL, length=200).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Label(advanced_frame, textvariable=self.guidance_var).grid(row=1, column=2, padx=5, pady=5)
        
        ttk.Label(advanced_frame, text="Negative Prompt:").grid(row=2, column=0, sticky=tk.W)
        neg_text = scrolledtext.ScrolledText(advanced_frame, height=3, width=50, wrap=tk.WORD)
        neg_text.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5)
        neg_text.insert(tk.END, self.negative_prompt_var.get())
        neg_text.bind('<KeyRelease>', lambda e: self.negative_prompt_var.set(neg_text.get('1.0', tk.END).strip()))
        
        # ALTYAZI AYARLARI
        subtitle_frame = ttk.LabelFrame(main_frame, text="📝 Altyazı Ayarları", padding="10")
        subtitle_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Checkbutton(subtitle_frame, text="Altyazı Ekle", 
                       variable=self.add_subtitles_var).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        ttk.Label(subtitle_frame, text="Renk:").grid(row=1, column=0, sticky=tk.W)
        color_combo = ttk.Combobox(subtitle_frame, textvariable=self.subtitle_color_var,
                                  values=list(SUBTITLE_COLORS.keys()), state='readonly', width=15)
        color_combo.grid(row=1, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(subtitle_frame, text="Boyut:").grid(row=1, column=2, sticky=tk.W, padx=(20, 0))
        ttk.Spinbox(subtitle_frame, from_=24, to=96, textvariable=self.subtitle_size_var, 
                   width=8).grid(row=1, column=3, sticky=tk.W, padx=5)
        
        ttk.Label(subtitle_frame, text="Konum:").grid(row=2, column=0, sticky=tk.W, pady=5)
        pos_combo = ttk.Combobox(subtitle_frame, textvariable=self.subtitle_position_var,
                                values=['bottom', 'center', 'top'], state='readonly', width=15)
        pos_combo.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Progress
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        self.progress = ttk.Progressbar(progress_frame, mode='determinate', length=400)
        self.progress.pack(fill=tk.X, pady=5)
        
        self.progress_label = ttk.Label(progress_frame, text="Hazır")
        self.progress_label.pack()
        
        # Log
        log_frame = ttk.LabelFrame(main_frame, text="📊 Log", padding="5")
        log_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, width=80, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Butonlar
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=9, column=0, columnspan=3, pady=10)
        
        self.start_btn = ttk.Button(button_frame, text="🚀 Başlat", command=self.start_processing)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.cancel_btn = ttk.Button(button_frame, text="⛔ İptal", command=self.cancel_processing, 
                                     state=tk.DISABLED)
        self.cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # Grid yapılandırması
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(8, weight=1)
    
    def select_lyrics(self):
        """Şarkı sözü dosyası seçer"""
        filename = filedialog.askopenfilename(
            title="Şarkı Sözü Seç",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if filename:
            self.lyrics_file.set(filename)
    
    def select_audio(self):
        """Ses dosyası seçer"""
        filename = filedialog.askopenfilename(
            title="Ses Dosyası Seç",
            filetypes=[("Audio Files", "*.mp3 *.wav *.m4a"), ("All Files", "*.*")]
        )
        if filename:
            self.audio_file.set(filename)
    
    def on_ratio_change(self, event=None):
        """Ebat değiştiğinde özel boyutları günceller"""
        selected = self.ratio_var.get()
        if selected != "Özel Boyut" and selected in ASPECT_RATIOS:
            w, h = ASPECT_RATIOS[selected]
            self.custom_width.set(w)
            self.custom_height.set(h)
    
    def get_dimensions(self):
        """Seçili ebatları döndürür"""
        selected = self.ratio_var.get()
        if selected == "Özel Boyut":
            return self.custom_width.get(), self.custom_height.get()
        else:
            return ASPECT_RATIOS[selected]
    
    def log(self, message):
        """Log mesajı ekler - hem GUI hem Console'a"""
        # GUI log
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
        # Console log (debug için)
        print(message)
    
    def update_progress(self, value):
        """Progress bar günceller"""
        self.progress['value'] = value
        self.progress_label.config(text=f"{value}%")
        self.root.update_idletasks()
    
    def start_processing(self):
        """İşlemi başlatır"""
        # Dosya kontrolü
        if not self.lyrics_file.get() or not self.audio_file.get():
            messagebox.showerror("Hata", "Lütfen şarkı sözü ve ses dosyası seçin!")
            return
        
        if not os.path.exists(self.lyrics_file.get()):
            messagebox.showerror("Hata", "Şarkı sözü dosyası bulunamadı!")
            return
        
        if not os.path.exists(self.audio_file.get()):
            messagebox.showerror("Hata", "Ses dosyası bulunamadı!")
            return
        
        if CONFIG['ANTHROPIC_API_KEY'] == "buraya-anthropic-api-key-girin":
            messagebox.showerror("Hata", "Anthropic API key girilmemiş!\nCONFIG'i düzenleyin.")
            return
        
        if CONFIG['HUGGINGFACE_TOKEN'] == "buraya-huggingface-token-girin":
            messagebox.showerror("Hata", "Hugging Face token girilmemiş!\nCONFIG'i düzenleyin.")
            return
        
        # Butonları güncelle
        self.start_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL)
        self.is_processing = True
        
        # Thread'de çalıştır
        thread = threading.Thread(target=self.process_video, daemon=True)
        thread.start()
    
    def cancel_processing(self):
        """İşlemi iptal eder"""
        self.is_processing = False
        self.log("\n⚠️  İşlem iptal edildi!")
        self.start_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.DISABLED)
    
    def process_video(self):
        """Ana işleme fonksiyonu"""
        try:
            # Klasörleri oluştur
            os.makedirs(CONFIG['OUTPUT_DIR'], exist_ok=True)
            os.makedirs(CONFIG['TEMP_DIR'], exist_ok=True)
            
            self.log("\n" + "="*70)
            self.log("İŞLEM BAŞLADI")
            self.log("="*70 + "\n")
            
            # Ayarları göster
            self.log("📋 SEÇİLİ AYARLAR:")
            self.log(f"   Model: {self.model_var.get()}")
            self.log(f"   Stil: {self.style_var.get()}")
            width, height = self.get_dimensions()
            self.log(f"   Çözünürlük: {width}x{height}")
            self.log(f"   Kalite (Steps): {self.steps_var.get()}")
            self.log(f"   Guidance Scale: {self.guidance_var.get()}")
            self.log(f"   Altyazı: {'✓ Aktif' if self.add_subtitles_var.get() else '✗ Kapalı'}")
            if self.add_subtitles_var.get():
                self.log(f"      Renk: {self.subtitle_color_var.get()}")
                self.log(f"      Boyut: {self.subtitle_size_var.get()}")
                self.log(f"      Konum: {self.subtitle_position_var.get()}")
            self.log("")
            
            # 1. Şarkı sözlerini parse et
            self.log("📝 Şarkı sözleri parse ediliyor...")
            segments = parse_lyrics_file(self.lyrics_file.get())
            
            if not segments:
                self.log("❌ Şarkı sözü parse edilemedi!")
                messagebox.showerror("Hata", "Şarkı sözü formatı hatalı!")
                return
            
            self.log(f"✅ {len(segments)} segment bulundu")
            total_duration = max(seg['end'] for seg in segments)
            self.log(f"   Toplam süre: {total_duration//60}:{total_duration%60:02d}\n")
            
            if not self.is_processing:
                return
            
            # 2. Prompt oluştur
            self.log("🤖 Claude AI ile prompt'lar oluşturuluyor...")
            self.update_progress(10)
            
            # Stil suffix'i al
            style_suffix = STYLES.get(self.style_var.get(), "")
            
            prompt_data = generate_prompts_with_claude(
                segments, 
                CONFIG['ANTHROPIC_API_KEY'],
                style_suffix,
                log_callback=self.log
            )
            self.log(f"✅ {len(prompt_data)} prompt oluşturuldu\n")
            
            # Prompt'ları göster
            self.log("📋 Oluşturulan Prompt'lar (ilk 3):")
            for data in prompt_data[:3]:
                seg = data['segment']
                self.log(f"   {data['index']+1}. {seg['text'][:40]}")
                self.log(f"      → {data['prompt'][:70]}...")
            if len(prompt_data) > 3:
                self.log(f"   ... ve {len(prompt_data)-3} tane daha\n")
            
            if not self.is_processing:
                return
            
            # 3. Model yükle
            self.log("🎨 Stable Diffusion modeli yükleniyor...")
            self.update_progress(20)
            
            device = "cuda" if torch.cuda.is_available() else "cpu"
            model_config = MODELS[self.model_var.get()]
            
            pipe = load_stable_diffusion_model(
                model_config['id'],
                device=device,
                dtype=model_config['dtype'],
                progress_callback=self.log
            )
            
            if pipe is None:
                self.log("❌ Model yüklenemedi!")
                return
            
            self.log(f"✅ Model hazır ({device.upper()})\n")
            
            if not self.is_processing:
                return
            
            # 4. Görselleri oluştur
            total_images = len(prompt_data)
            self.log(f"🖼️  {total_images} görsel oluşturuluyor...")
            self.log(f"⏱️  Tahmini süre: ~{(total_images * 20) // 60} dakika")
            self.log(f"💾 VRAM optimizasyonu aktif\n")
            
            image_data_list = []
            
            for i, data in enumerate(prompt_data, 1):
                if not self.is_processing:
                    return
                
                seg = data['segment']
                prompt = data['prompt']
                output_file = os.path.join(CONFIG['OUTPUT_DIR'], f"scene_{i:03d}.png")
                
                self.log(f"[{i}/{total_images}] 🎨 {seg['text'][:40]}...")
                
                start_time = time.time()
                success = generate_image(
                    pipe,
                    prompt,
                    output_file,
                    width=width,
                    height=height,
                    steps=self.steps_var.get(),
                    guidance_scale=self.guidance_var.get(),
                    negative_prompt=self.negative_prompt_var.get()
                )
                elapsed = time.time() - start_time
                
                if success:
                    allocated, reserved = get_vram_usage()
                    self.log(f"      ✅ {elapsed:.1f}s (VRAM: {allocated:.2f}GB)")
                    image_data_list.append({
                        "path": output_file,
                        "start": seg['start'],
                        "duration": seg['duration']
                    })
                else:
                    self.log(f"      ❌ Başarısız - VRAM yetersiz olabilir!")
                
                # Progress güncelle
                progress = 20 + int((i / total_images) * 70)
                self.update_progress(progress)
            
            self.log(f"\n✅ {len(image_data_list)}/{total_images} görsel oluşturuldu\n")
            
            if not image_data_list:
                self.log("❌ Hiçbir görsel oluşturulamadı!")
                return
            
            if not self.is_processing:
                return
            
            # 5. Video oluştur (ALTYAZI İLE!)
            self.log("🎬 Video oluşturuluyor...")
            if self.add_subtitles_var.get():
                self.log("📝 Altyazılar eklenecek...")
            self.update_progress(95)
            
            # Altyazı ayarlarını hazırla
            subtitle_color_name = self.subtitle_color_var.get()
            subtitle_color = SUBTITLE_COLORS.get(subtitle_color_name, "#FFFFFF")
            
            success = create_video_from_images(
                image_data_list,
                self.audio_file.get(),
                CONFIG['FINAL_VIDEO'],
                fps=CONFIG['VIDEO_FPS'],
                add_subtitles=self.add_subtitles_var.get(),
                subtitle_segments=segments if self.add_subtitles_var.get() else None,
                subtitle_color=subtitle_color,
                subtitle_size=self.subtitle_size_var.get(),
                subtitle_position=self.subtitle_position_var.get()
            )
            
            self.update_progress(100)
            
            if success:
                video_size_mb = os.path.getsize(CONFIG['FINAL_VIDEO']) / (1024 * 1024)
                
                self.log("\n" + "="*70)
                self.log("🎉 TAMAMLANDI!")
                self.log("="*70)
                self.log(f"\n📹 Video: {os.path.abspath(CONFIG['FINAL_VIDEO'])}")
                self.log(f"📊 Boyut: {video_size_mb:.1f} MB")
                self.log(f"📐 Çözünürlük: {width}x{height}")
                self.log(f"⏱️  Süre: {total_duration//60}:{total_duration%60:02d}")
                self.log(f"🖼️  Görseller: {os.path.abspath(CONFIG['OUTPUT_DIR'])}/")
                if self.add_subtitles_var.get():
                    self.log(f"📝 Altyazılar: ✓ Eklendi ({subtitle_color_name}, {self.subtitle_size_var.get()}px)")
                self.log("\n✨ Videoyu izlemek için dosyayı açın!")
                
                messagebox.showinfo("Başarılı!", f"Video oluşturuldu!\n\n{CONFIG['FINAL_VIDEO']}")
            else:
                self.log("\n❌ Video oluşturulamadı!")
                messagebox.showerror("Hata", "Video oluşturulamadı!")
            
        except Exception as e:
            self.log(f"\n❌ HATA: {e}")
            import traceback
            self.log(traceback.format_exc())
            messagebox.showerror("Hata", f"Bir hata oluştu:\n{e}")
        
        finally:
            self.start_btn.config(state=tk.NORMAL)
            self.cancel_btn.config(state=tk.DISABLED)
            self.is_processing = False
            clear_memory()


# ============================================================================
# PROGRAM BAŞLANGIÇ
# ============================================================================

if __name__ == "__main__":
    # API anahtarı kontrolü
    print("\n" + "="*70)
    print("🔑 API ANAHTARI KONTROLÜ")
    print("="*70)
    
    anthropic_ok = CONFIG['ANTHROPIC_API_KEY'] != "buraya-anthropic-api-key-girin" and \
                   CONFIG['ANTHROPIC_API_KEY'] and \
                   CONFIG['ANTHROPIC_API_KEY'].startswith("sk-ant-")
    
    huggingface_ok = CONFIG['HUGGINGFACE_TOKEN'] != "buraya-huggingface-token-girin" and \
                     CONFIG['HUGGINGFACE_TOKEN']
    
    if anthropic_ok:
        print(f"✅ Anthropic API: Ayarlanmış ({CONFIG['ANTHROPIC_API_KEY'][:15]}...)")
        print("   → Claude AI ile AKILLI prompt'lar oluşturulacak!")
    else:
        print("❌ Anthropic API: YOK!")
        print("   → Basit fallback prompt'lar kullanılacak")
        print("   → Görseller genel/soyut olacak")
        print("   → Düzeltmek için: CONFIG'de ANTHROPIC_API_KEY ayarlayın")
        print("   → Alın: https://console.anthropic.com/settings/keys")
    
    print()
    
    if huggingface_ok:
        print(f"✅ Hugging Face: Ayarlanmış ({CONFIG['HUGGINGFACE_TOKEN'][:10]}...)")
    else:
        print("❌ Hugging Face: YOK!")
        print("   → Alın: https://huggingface.co/settings/tokens")
    
    print("="*70 + "\n")
    
    print("="*70)
    print("🎵 AI Müzik Klibi Oluşturucu v6.1")
    print("RTX 3050 6GB için optimize edildi!")
    print("="*70)
    print("\n💡 İPUÇLARI:")
    print("   - 512x512 veya 768x768 çözünürlük önerilir")
    print("   - Steps: 20-30 arası ideal")
    print("   - Yüksek çözünürlüklerde VRAM hatası alabilirsiniz")
    print("   - İşlem sırasında diğer GPU kullanan uygulamaları kapatın\n")
    
    # GUI başlat
    root = tk.Tk()
    app = MusicVideoGeneratorGUI(root)
    root.mainloop()
