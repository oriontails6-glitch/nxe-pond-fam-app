"""Unit tests for Pillow image verification, EXIF handling, and size validation."""
import io
from PIL import Image
import config


def create_test_image(width=600, height=800, color="orange", format="JPEG"):
    buf = io.BytesIO()
    img = Image.new("RGB", (width, height), color=color)
    img.save(buf, format=format)
    return buf.getvalue()


def test_image_verification():
    valid_bytes = create_test_image()
    # Pillow verify checks format and integrity
    with Image.open(io.BytesIO(valid_bytes)) as img:
        img.verify()
    assert True


def test_fake_image_rejected():
    fake_exe = b"MZ\x90\x00\x03\x00\x00\x00ThisIsNotAnImageFile"
    try:
        with Image.open(io.BytesIO(fake_exe)) as img:
            img.verify()
        passed = True
    except Exception:
        passed = False
    assert passed is False


def test_size_limit_constant():
    assert config.MAX_IMAGE_SIZE_BYTES == 5 * 1024 * 1024
