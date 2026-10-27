"""
Image validation, EXIF stripping, WebP resizing, and Supabase Storage upload pipeline.
Strictly handles mobile phone uploads, strips metadata, and generates random UUID filenames.
"""
import io
import uuid
from PIL import Image, ImageOps
import config
from db import get_supabase_client


def process_and_upload_avatar(
    file_bytes: bytes,
    filename: str,
    old_image_path: str | None = None,
    old_thumb_path: str | None = None
) -> tuple[bool, str, str | None, str | None]:
    """
    Validates, strips EXIF, resizes to main (1080px) and thumb (480px) as WebP,
    and uploads to the public 'avatars' bucket in Supabase.
    Deletes old images if replacing an existing avatar.
    Returns (success, message, main_public_url, thumb_public_url).
    """
    if not file_bytes:
        return False, "Please select an avatar photo to upload.", None, None

    # 1. Size check (max 5MB)
    if len(file_bytes) > config.MAX_IMAGE_SIZE_BYTES:
        return False, "That photo is bursting with too much goblin power! Maximum allowed size is 5 MB.", None, None

    # 2. Extension check
    fname_lower = (filename or "").lower()
    if not (fname_lower.endswith(".jpg") or fname_lower.endswith(".jpeg") or fname_lower.endswith(".png") or fname_lower.endswith(".webp")):
        return False, "That picture is shy! Please upload a PNG or JPG photo.", None, None

    # 3. Pillow integrity verification
    try:
        stream = io.BytesIO(file_bytes)
        with Image.open(stream) as test_img:
            test_img.verify()
    except Exception:
        return False, "The ghosts could not read that image file. It may be corrupted. Please try another photo.", None, None

    # 4. Processing and metadata stripping
    try:
        proc_stream = io.BytesIO(file_bytes)
        with Image.open(proc_stream) as img:
            # Handle phone EXIF orientation
            img = ImageOps.exif_transpose(img)

            # Convert to RGB (strips transparency/CMYK/palette)
            if img.mode != "RGB":
                img = img.convert("RGB")

            # A. Process Main Image (max 1080px on longest side)
            main_img = img.copy()
            main_img.thumbnail((config.IMAGE_LONG_SIDE_MAX, config.IMAGE_LONG_SIDE_MAX), Image.Resampling.LANCZOS)
            main_buf = io.BytesIO()
            try:
                main_img.save(main_buf, format="WEBP", quality=config.WEBP_QUALITY, method=6)
                content_type = "image/webp"
                ext = "webp"
            except Exception:
                # Fallback to JPEG if WebP encoder is unavailable
                main_img.save(main_buf, format="JPEG", quality=85, optimize=True)
                content_type = "image/jpeg"
                ext = "jpg"
            main_bytes = main_buf.getvalue()

            # B. Process Thumbnail (max 480px width)
            thumb_img = img.copy()
            thumb_img.thumbnail((config.THUMB_WIDTH, config.THUMB_WIDTH), Image.Resampling.LANCZOS)
            thumb_buf = io.BytesIO()
            try:
                thumb_img.save(thumb_buf, format="WEBP", quality=75, method=4)
            except Exception:
                thumb_img.save(thumb_buf, format="JPEG", quality=80, optimize=True)
            thumb_bytes = thumb_buf.getvalue()

    except Exception:
        return False, "Unable to process this image format. Please convert your photo to a standard PNG or JPG and try again.", None, None

    # 5. Upload to Supabase Storage 'avatars' bucket
    client = get_supabase_client()
    file_uuid = uuid.uuid4().hex
    main_filename = f"{file_uuid}_main.{ext}"
    thumb_filename = f"{file_uuid}_thumb.{ext}"

    try:
        # Upload main image
        client.storage.from_("avatars").upload(
            path=main_filename,
            file=main_bytes,
            file_options={"content-type": content_type, "cache-control": "3600", "upsert": "true"}
        )

        # Upload thumbnail
        client.storage.from_("avatars").upload(
            path=thumb_filename,
            file=thumb_bytes,
            file_options={"content-type": content_type, "cache-control": "3600", "upsert": "true"}
        )

        # Retrieve public URLs
        main_url = client.storage.from_("avatars").get_public_url(main_filename)
        thumb_url = client.storage.from_("avatars").get_public_url(thumb_filename)

        # Clean up old images if replacing
        if old_image_path:
            try:
                old_main = old_image_path.split("/")[-1]
                client.storage.from_("avatars").remove([old_main])
            except Exception:
                pass
        if old_thumb_path:
            try:
                old_thumb = old_thumb_path.split("/")[-1]
                client.storage.from_("avatars").remove([old_thumb])
            except Exception:
                pass

        return True, "Costume avatar uploaded successfully!", main_url, thumb_url

    except Exception:
        return False, "Ghostly storage hiccup! Failed to upload photo to the avatars bucket. Please ensure the 'avatars' bucket exists and is set to Public, then try again.", None, None
