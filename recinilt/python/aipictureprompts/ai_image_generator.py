#!/usr/bin/env python3
"""
AI Picture Prompts - Image Generator
Generates AI images for each style in the HTML and updates the HTML with thumbnails
"""

import os
import re
import time
import json
import base64
from pathlib import Path
from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO
import unicodedata
from datetime import datetime

# ============================================================================
# API KEYS - MANUEL OLARAK EKLE
# ============================================================================
ANTHROPIC_API_KEY = "api key buraya"  # Anthropic API Key buraya
OPENAI_API_KEY = "api key buraya"     # OpenAI API Key buraya

# ============================================================================
# CONFIGURATION
# ============================================================================
THUMBNAIL_SIZE = (150, 150)
DEFAULT_IMAGE_SIZE = "1024x1024"
REQUEST_DELAY = 2  # seconds between requests
MAX_RETRIES = 3  # maximum retry attempts for failed requests
OUTPUT_DIR = Path("generated_images")
HTML_INPUT_FILE = "aipictureprompts.html"
HTML_OUTPUT_FILE = "aipictureprompts_updated.html"
PROGRESS_FILE = "progress.json"

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def sanitize_filename(text):
    """Convert Turkish/special characters to ASCII for filename"""
    # Remove content in parentheses (English translation)
    text = re.sub(r'\([^)]*\)', '', text).strip()
    
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    
    # Replace spaces and special chars with underscore
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '_', text)
    
    return text.lower().strip('_')


def load_progress():
    """Load progress from JSON file"""
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Progress file corrupted: {e}")
            return None
    return None


def save_progress(progress_data):
    """Save progress to JSON file"""
    try:
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump(progress_data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"⚠️  Could not save progress: {e}")


def is_image_completed(filename, progress_data):
    """Check if an image was already generated"""
    if progress_data and 'completed_images' in progress_data:
        return filename in progress_data['completed_images']
    return False


def mark_image_completed(filename, progress_data):
    """Mark an image as completed in progress data"""
    if 'completed_images' not in progress_data:
        progress_data['completed_images'] = []
    progress_data['completed_images'].append(filename)
    progress_data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_progress(progress_data)


def get_user_choice(prompt_text, valid_choices):
    """Get user input with validation"""
    while True:
        try:
            choice = input(prompt_text).strip()
            if choice in valid_choices:
                return choice
            print(f"❌ Geçersiz seçim! Lütfen {'/'.join(valid_choices)} seçeneklerinden birini girin.")
        except KeyboardInterrupt:
            print("\n\n⚠️  Script durduruldu!")
            exit(0)


def handle_error(error_msg, category_name, cat_idx, total_cats, style, style_idx, total_styles):
    """Handle errors and ask user what to do"""
    print()
    print("=" * 70)
    print(f"❌ 3 deneme sonrası başarısız!")
    print(f"   Kategori: {category_name} ({cat_idx}/{total_cats})")
    print(f"   Stil: {style} ({style_idx}/{total_styles})")
    print(f"   Hata: {error_msg}")
    print()
    print("🔄 Ne yapmak istersiniz?")
    print("   1 - Tekrar dene")
    print("   2 - Bu görseli atla, devam et")
    print("   3 - Scripti durdur")
    print("=" * 70)
    
    choice = get_user_choice("Seçiminiz (1/2/3): ", ['1', '2', '3'])
    
    if choice == '3':
        print("\n⚠️  Script durduruldu! Progress kaydedildi.")
        exit(0)
    
    return choice  # '1' = retry, '2' = skip


def call_claude_api(prompt, max_retries=MAX_RETRIES):
    """Call Claude API to generate prompts with retry logic"""
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01"
    }
    
    data = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1000,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result['content'][0]['text'].strip()
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"      ⚠️  Deneme {attempt + 1}/{max_retries} başarısız, tekrar deneniyor...")
                time.sleep(REQUEST_DELAY)
            else:
                print(f"      ❌ Claude API Error (tüm denemeler başarısız): {e}")
                return None
    
    return None


def call_dalle_api(prompt, size="1024x1024", max_retries=MAX_RETRIES):
    """Call DALL-E API to generate images with retry logic"""
    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    
    data = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": size,
        "quality": "standard"
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            result = response.json()
            image_url = result['data'][0]['url']
            
            # Download the image
            img_response = requests.get(image_url, timeout=30)
            img_response.raise_for_status()
            
            return Image.open(BytesIO(img_response.content))
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"      ⚠️  Deneme {attempt + 1}/{max_retries} başarısız, tekrar deneniyor...")
                time.sleep(REQUEST_DELAY)
            else:
                print(f"      ❌ DALL-E API Error (tüm denemeler başarısız): {e}")
                return None
    
    return None


def create_thumbnail(image, size=THUMBNAIL_SIZE):
    """Create thumbnail from image"""
    img_copy = image.copy()
    img_copy.thumbnail(size, Image.Resampling.LANCZOS)
    return img_copy


def parse_html_categories(html_content):
    """Parse HTML and extract categories with their styles"""
    soup = BeautifulSoup(html_content, 'html.parser')
    categories = []
    
    grids = soup.find_all('div', class_='grid')
    
    for idx, grid in enumerate(grids, 1):
        category_name = grid.get('data-category', f'category_{idx}')
        
        # Find the h2 heading before this grid
        heading = grid.find_previous('h2')
        category_display_name = heading.text.strip() if heading else category_name
        
        # Extract all style options
        options = grid.find_all('div', class_='option')
        styles = [opt.text.strip() for opt in options]
        
        if styles:
            categories.append({
                'id': category_name,
                'name': category_display_name,
                'styles': styles,
                'index': idx,
                'grid_element': grid
            })
    
    return categories, soup


def get_image_size_for_style(category_id, style_text):
    """Ask Claude for image dimensions if it's a format category"""
    if category_id != 'format':
        return DEFAULT_IMAGE_SIZE
    
    prompt = f"""The user wants to generate an AI image for the format style: "{style_text}"

What image dimensions (size) should be used for DALL-E 3 API?

Available options are:
- 1024x1024 (square)
- 1024x1792 (portrait)
- 1792x1024 (landscape)

Respond with ONLY the dimensions in format: WIDTHxHEIGHT (e.g., "1024x1792")
No explanation needed, just the dimensions."""

    result = call_claude_api(prompt)
    
    if result and 'x' in result:
        # Extract dimensions from response
        match = re.search(r'(\d{3,4})x(\d{3,4})', result)
        if match:
            return match.group(0)
    
    return DEFAULT_IMAGE_SIZE


# ============================================================================
# MAIN PROCESS
# ============================================================================

def main():
    print("=" * 70)
    print("🎨 AI Picture Prompts - Image Generator")
    print("=" * 70)
    print()
    
    # Check API keys
    if ANTHROPIC_API_KEY == "buraya ekle" or OPENAI_API_KEY == "buraya ekle":
        print("❌ ERROR: Please add your API keys to the script!")
        print("   - ANTHROPIC_API_KEY")
        print("   - OPENAI_API_KEY")
        return
    
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Check for existing progress
    progress_data = load_progress()
    if progress_data:
        print("=" * 70)
        print("📂 Önceki çalıştırma bulundu!")
        completed_count = len(progress_data.get('completed_images', []))
        print(f"   Tamamlanan: {completed_count} görsel")
        print(f"   Tarih: {progress_data.get('timestamp', 'Bilinmiyor')}")
        print()
        print("✅ Kaldığı yerden devam edilsin mi?")
        print("   1 - Evet, devam et")
        print("   2 - Hayır, baştan başla (progress.json silinecek)")
        print("=" * 70)
        
        choice = get_user_choice("Seçiminiz (1/2): ", ['1', '2'])
        
        if choice == '2':
            if os.path.exists(PROGRESS_FILE):
                os.remove(PROGRESS_FILE)
            progress_data = {
                'completed_images': [],
                'total_categories': 0,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            print("✅ Progress temizlendi, baştan başlanıyor...")
        else:
            print("✅ Kaldığı yerden devam ediliyor...")
        print()
    else:
        progress_data = {
            'completed_images': [],
            'total_categories': 0,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    # Read HTML
    print("📄 Reading HTML file...")
    if not os.path.exists(HTML_INPUT_FILE):
        print(f"❌ HTML file not found: {HTML_INPUT_FILE}")
        return
    
    with open(HTML_INPUT_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Parse categories
    print("🔍 Parsing categories and styles...")
    categories, soup = parse_html_categories(html_content)
    
    progress_data['total_categories'] = len(categories)
    save_progress(progress_data)
    
    print(f"✅ Found {len(categories)} categories")
    print()
    
    # Process each category
    for cat_idx, category in enumerate(categories, 1):
        cat_name = category['name']
        cat_id = category['id']
        styles = category['styles']
        
        print("=" * 70)
        print(f"📂 Category {cat_idx}/{len(categories)}: {cat_name}")
        print(f"   ID: {cat_id}")
        print(f"   Styles: {len(styles)}")
        print("=" * 70)
        
        # Step 1: Generate base prompt for this category
        print(f"🤖 Asking Claude for base prompt...")
        
        claude_prompt = f"""Generate a simple, basic image prompt for the category: "{cat_name}"

This prompt will be used as a base, and different styles will be added to it.

The styles in this category are:
{chr(10).join(f'- {s}' for s in styles)}

Create ONE simple base prompt (1-2 sentences max) that works well with all these styles.

Respond with ONLY the base prompt, no explanation."""

        base_prompt = call_claude_api(claude_prompt)
        
        if not base_prompt:
            print("❌ Failed to get base prompt, skipping category...")
            continue
        
        print(f"✅ Base prompt: {base_prompt}")
        print()
        
        time.sleep(REQUEST_DELAY)
        
        # Step 2: Generate images for each style
        for style_idx, style in enumerate(styles, 1):
            # Check filename
            style_safe = sanitize_filename(style)
            cat_safe = sanitize_filename(cat_id)
            filename = f"{cat_idx:03d}_{cat_safe}_{style_idx:03d}_{style_safe}.png"
            
            # Skip if already completed
            if is_image_completed(filename, progress_data):
                print(f"  [{style_idx}/{len(styles)}] ✅ Zaten tamamlanmış: {style}")
                continue
            
            print(f"  [{style_idx}/{len(styles)}] Processing: {style}")
            
            # Retry loop for this specific image
            retry_user_choice = False
            while True:
                # Determine image size
                image_size = get_image_size_for_style(cat_id, style)
                if cat_id == 'format':
                    print(f"      📐 Size for this format: {image_size}")
                    time.sleep(REQUEST_DELAY)
                
                # Create full prompt with category and style at beginning and end
                full_prompt = f"Category: {cat_name} ({cat_id}), Style: {style}, {base_prompt}, Category: {cat_name} ({cat_id}), Style: {style}"
                print(f"      📝 Prompt: {full_prompt[:100]}...")
                
                # Generate image
                print(f"      🎨 Generating image...")
                image = call_dalle_api(full_prompt, image_size)
                
                if image is None:
                    # Auto-retry failed, ask user
                    user_choice = handle_error(
                        "Image generation failed",
                        cat_name,
                        cat_idx,
                        len(categories),
                        style,
                        style_idx,
                        len(styles)
                    )
                    
                    if user_choice == '1':  # Retry
                        print("      🔄 Tekrar deneniyor...")
                        continue
                    else:  # Skip (user_choice == '2')
                        print(f"      ⏭️  Atlanıyor...")
                        break
                
                # Success! Save the image
                filepath = OUTPUT_DIR / filename
                
                try:
                    image.save(filepath)
                    print(f"      💾 Saved: {filename}")
                    
                    # Create and save thumbnail
                    thumbnail = create_thumbnail(image)
                    thumb_filename = f"thumb_{filename}"
                    thumb_filepath = OUTPUT_DIR / thumb_filename
                    thumbnail.save(thumb_filepath)
                    print(f"      🖼️  Thumbnail: {thumb_filename}")
                    
                    # Update HTML - add image to the option element
                    option_elements = category['grid_element'].find_all('div', class_='option')
                    if style_idx - 1 < len(option_elements):
                        option = option_elements[style_idx - 1]
                        
                        # Create img tag
                        img_tag = soup.new_tag('img', 
                                               src=f"generated_images/{thumb_filename}",
                                               alt=style,
                                               attrs={
                                                   'class': 'style-thumbnail',
                                                   'data-fullimg': f"generated_images/{filename}",
                                                   'onclick': 'openLightbox(this.getAttribute("data-fullimg"))'
                                               })
                        img_tag['style'] = 'display:block; margin:5px auto; cursor:pointer; border-radius:4px;'
                        
                        # Insert image at the beginning of the option div
                        option.insert(0, img_tag)
                    
                    # Mark as completed in progress
                    mark_image_completed(filename, progress_data)
                    
                    print(f"      ✅ Completed and saved to progress")
                    print()
                    
                    time.sleep(REQUEST_DELAY)
                    break  # Success, exit retry loop
                    
                except Exception as e:
                    # File save error
                    user_choice = handle_error(
                        f"File save error: {e}",
                        cat_name,
                        cat_idx,
                        len(categories),
                        style,
                        style_idx,
                        len(styles)
                    )
                    
                    if user_choice == '1':  # Retry
                        print("      🔄 Tekrar deneniyor...")
                        continue
                    else:  # Skip
                        print(f"      ⏭️  Atlanıyor...")
                        break
        
        print(f"✅ Completed category: {cat_name}")
        print()
    
    # Add lightbox CSS and JavaScript to HTML
    print("📝 Adding lightbox functionality to HTML...")
    
    # Add CSS
    style_tag = soup.new_tag('style')
    style_tag.string = """
/* Lightbox Styles */
#lightbox {
    display: none;
    position: fixed;
    z-index: 9999;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.9);
    justify-content: center;
    align-items: center;
}

#lightbox.active {
    display: flex;
}

#lightbox img {
    max-width: 90%;
    max-height: 90%;
    object-fit: contain;
    border-radius: 8px;
}

#lightbox-close {
    position: absolute;
    top: 20px;
    right: 40px;
    color: white;
    font-size: 40px;
    font-weight: bold;
    cursor: pointer;
    background: none;
    border: none;
    transition: 0.3s;
}

#lightbox-close:hover {
    color: #ccc;
}

.style-thumbnail {
    transition: transform 0.2s;
}

.style-thumbnail:hover {
    transform: scale(1.05);
}
"""
    soup.head.append(style_tag)
    
    # Add lightbox HTML
    body = soup.body
    lightbox_html = soup.new_tag('div', id='lightbox')
    lightbox_html['onclick'] = 'closeLightbox(event)'
    
    close_btn = soup.new_tag('button', id='lightbox-close')
    close_btn['onclick'] = 'closeLightbox(event)'
    close_btn.string = '×'
    
    img_tag = soup.new_tag('img', id='lightbox-img', src='', alt='Full size image')
    
    lightbox_html.append(close_btn)
    lightbox_html.append(img_tag)
    body.append(lightbox_html)
    
    # Add JavaScript
    script_tag = soup.new_tag('script')
    script_tag.string = """
function openLightbox(imgSrc) {
    event.stopPropagation();
    document.getElementById('lightbox-img').src = imgSrc;
    document.getElementById('lightbox').classList.add('active');
}

function closeLightbox(event) {
    if (event.target.id === 'lightbox' || event.target.id === 'lightbox-close') {
        document.getElementById('lightbox').classList.remove('active');
    }
}

// Close on ESC key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        document.getElementById('lightbox').classList.remove('active');
    }
});
"""
    body.append(script_tag)
    
    # Save updated HTML
    print("💾 Saving updated HTML...")
    with open(HTML_OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))
    
    print()
    print("=" * 70)
    print("✅ ALL DONE!")
    print("=" * 70)
    print(f"📁 Images saved to: {OUTPUT_DIR}/")
    print(f"📄 Updated HTML saved to: {HTML_OUTPUT_FILE}")
    print()
    print("🎉 Open the HTML file in your browser to see the results!")


if __name__ == "__main__":
    main()
