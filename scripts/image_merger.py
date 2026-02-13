from io import BytesIO
from PIL import Image
from config.constants import ScraperConfig
import requests

class ImageMerger:
    def download_images(urls: list[str], session: requests.Session = None) -> list[BytesIO]:
        if session is None:
            session = requests.Session()
            session.headers.update({"User-Agent": ScraperConfig.USER_AGENT})
        images = []
        for url in urls:
            try:
                r = session.get(url, timeout=ScraperConfig.TIMEOUT)
                r.raise_for_status()
                images.append(BytesIO(r.content))
            except requests.exceptions.RequestException:
                # ダウンロード失敗の画像はスキップ
                continue
        if not images:
            raise RuntimeError("failed to download any images")
        return images
    
    def merge_images(
            image_datas: list[BytesIO],
            direction: str = "horizontal",
            spacing: int = 0,
            bg_color: tuple[int, int, int] = (255, 255, 255)
    )->BytesIO:
        pillow_imgs = [Image.open(b).convert("RGBA") for b in image_datas]
        if direction == "horizontal":
            total_w = sum(img.width for img in pillow_imgs) + spacing * (len(pillow_imgs) - 1)
            max_h = max(img.height for img in pillow_imgs)
            out = Image.new("RGBA", (total_w, max_h), bg_color + (255,))
            x = 0
            for img in pillow_imgs:
                out.paste(img, (x, 0), img)
                x += img.width + spacing
        else:  # vertical
            total_h = sum(img.height for img in pillow_imgs) + spacing * (len(pillow_imgs) - 1)
            max_w = max(img.width for img in pillow_imgs)
            out = Image.new("RGBA", (max_w, total_h), bg_color + (255,))
            y = 0
            for img in pillow_imgs:
                out.paste(img, (0, y), img)
                y += img.height + spacing

        buf = BytesIO()
        out.convert("RGBA").save(buf, format="PNG")
        buf.seek(0)
        return buf

    def merge_from_urls(urls: list[str], session: requests.Session = None, **kwargs) -> BytesIO:
        datas = ImageMerger.download_images(urls, session=session)
        return ImageMerger.merge_images(datas, **kwargs)
