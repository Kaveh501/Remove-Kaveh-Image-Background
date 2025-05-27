

import streamlit as st
from rembg import remove
from PIL import Image
import io
import time
from pathlib import Path
import base64

st.set_page_config(page_title="BG Remover", layout="wide")

# ==== استایل کلی + بنر مینیمال آبی ====
st.markdown('''
<style>
    .custom-banner {
        background-image: url('https://images.unsplash.com/photo-1593642634367-d91a135587b5?auto=format&fit=crop&w=1400&q=80');
        background-size: cover;
        background-position: center;
        height: 220px;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .image-container {
        width: 400px;
        height: 400px;
        overflow: hidden;
        border: 1px solid #ddd;
        border-radius: 6px;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 12px;
        background: #f9f9f9;
    }
    .image-container img {
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
    }
    .btn-anim-container {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-top: 12px;
    }
    .animation-img {
        width: 60px;
        height: 60px;
    }
    button[kind="primary"] {
        padding: 6px 14px !important;
        font-size: 0.85rem !important;
        min-width: 100px !important;
        height: 32px !important;
    }
    .stSelectbox > div > div > select {
        font-size: 0.85rem !important;
        width: 120px !important;
    }
    .language-label {
        font-weight: bold;
        font-size: 12px;
        margin-bottom: 4px;
    }
    .animation-fixed-bottom-center {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 9999;
        pointer-events: none;
    }
</style>
<div class="custom-banner"></div>
''', unsafe_allow_html=True)

# ==== زبان ====
texts = {
    "English": {
        "title": "Remove Kaveh Image Background",
        "upload": "Upload an image (JPG, PNG)",
        "original": "Original Image",
        "processing": "Removing background...",
        "done": "✅ Background successfully removed!",
        "result": "Image without background",
        "download": "Download PNG file",
        "start_button": "Start"
    },
    "فارسی": {
        "title":  "حذف پس زمینه تصویر کاوه",
        "upload": "یک تصویر انتخاب کن (JPG, PNG)",
        "original": "تصویر اصلی",
        "processing": "در حال حذف پس‌زمینه...",
        "done": "✅ پس‌زمینه با موفقیت حذف شد!",
        "result": "تصویر بدون پس‌زمینه",
        "download": "دانلود فایل PNG",
        "start_button": "شروع کن"
    }
}

# ==== UI ====
st.markdown('<div class="language-label">Language | زبان</div>',
            unsafe_allow_html=True)
lang = st.selectbox("", ["English", "فارسی"],
                    key="lang_select", label_visibility="collapsed")
t = texts[lang]

st.title(t["title"])

uploaded_file = st.file_uploader(
    t["upload"], type=["jpg", "jpeg", "png"], key="file_up")

if uploaded_file is not None:
    input_image = Image.open(uploaded_file)

    original_img_slot = st.empty()
    original_img_slot.image(
        input_image, caption=t["original"], use_container_width=False, width=380)

    start_button = st.button(t["start_button"], key="start_btn")

    if start_button:
        animation_path = Path("assets/walk.gif")
        with open(animation_path, "rb") as f:
            gif_bytes = f.read()

        b64_gif = base64.b64encode(gif_bytes).decode()

        st.markdown(f'''
            <div class="animation-fixed-bottom-center">
                <img src="data:image/gif;base64,{b64_gif}" width="60" />
            </div>
        ''', unsafe_allow_html=True)

        with st.spinner(t["processing"]):
            output_image = remove(input_image)
            time.sleep(1)

        # حذف انیمیشن
        st.markdown(
            '<script>document.querySelector(".animation-fixed-bottom-center").remove()</script>', unsafe_allow_html=True)

        st.success(t["done"])

        output_img_slot = st.empty()
        output_img_slot.image(
            output_image, caption=t["result"], use_container_width=False, width=380)

        buf = io.BytesIO()
        output_image.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.download_button(label=t["download"], data=byte_im,
                           file_name="no_background.png", mime="image/png", key="download_btn")
