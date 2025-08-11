import io
from PIL import ImageGrab, Image
import win32clipboard

# Log 設定
from utils.log4py import logger_factory
logger = logger_factory(logger_factory.FILE_LOGGER, "ClipboardImageUpscaler.log")

# 將圖片寫入剪貼簿（DIB格式）
def image_to_clipboard(img: Image.Image):
    """將 PIL 圖像物件轉換為 DIB 格式並寫入剪貼簿"""
    try:
        output = io.BytesIO()
        img.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]  # 去掉 BMP header
        output.close()

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
        logger.info("✅ 放大後圖片(4x)已複製到剪貼簿")
    except Exception as e:
        logger.error(f"⚠️ 複製圖片到剪貼簿時發生錯誤：{str(e)}")

# 主功能：從剪貼簿讀取圖像 → 放大 → 回寫到剪貼簿
def upscale_clipboard_image():
    """從剪貼簿讀取圖像，放大後再寫回剪貼簿"""
    try:
        img = ImageGrab.grabclipboard()
        if img is None:
            logger.info("❌ 剪貼簿中沒有圖像，請先使用 Win + Shift + S 截圖。")
            return

        # 固定放大倍率 4 倍
        width, height = img.size
        # 使用 Image.Resampling.BICUBIC 來處理縮放，這是較新的寫法
        img = img.resize((width * 4, height * 4), resample=Image.Resampling.BICUBIC)

        image_to_clipboard(img)
    except Exception as e:
        logger.error(f"⚠️ 發生錯誤：{str(e)}")

# 主程式入口
if __name__ == "__main__":
    upscale_clipboard_image()
