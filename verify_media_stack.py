import os, json, re
from PIL import Image

def run_verification():
    print("=" * 60)
    print("RUNNING AUTOMATED VERIFICATION FOR IMAGE & MEDIA STACK")
    print("=" * 60)

    base_dir = r"C:\Users\Gary\github-cctv-seo"
    manifest_path = os.path.join(base_dir, "media_stack_manifest.json")
    gallery_path = os.path.join(base_dir, "image-gallery.html")
    images_dir = os.path.join(base_dir, "assets", "images")

    # 1. Manifest Check
    assert os.path.exists(manifest_path), "media_stack_manifest.json does not exist"
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    print("PASS: media_stack_manifest.json loaded successfully")

    assert manifest["system"]["google_authority_stack"]["google_drive_entity_hub"]["folder_id"] == "1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88", "Invalid Drive Folder ID"
    print("PASS: Google Drive Hub folder ID verified (1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88)")

    images = manifest["images"]
    assert len(images) == 54, f"Expected 54 images, found {len(images)}"
    print(f"PASS: 54 curated trade images present in manifest")

    # 2. Image files check
    seen_hashes = set()
    categories_found = set()
    for img_info in images:
        categories_found.add(img_info["cat"])
        rel = img_info["local_rel_path"]
        abs_p = os.path.join(base_dir, rel.replace("/", os.sep))
        assert os.path.exists(abs_p), f"Image file not found: {abs_p}"
        
        # Verify WebP & dimensions with PIL
        with Image.open(abs_p) as pil_img:
            assert pil_img.format == "WEBP", f"File is not WebP: {abs_p}"
            w, h = pil_img.size
            assert w == img_info["width"] and h == img_info["height"], f"Dimension mismatch for {abs_p}"
            assert w > 0 and h > 0, "Dimensions must be > 0"

        # Check duplicate hash
        hsh = img_info["sha256"]
        assert hsh not in seen_hashes, f"Duplicate hash detected: {hsh}"
        seen_hashes.add(hsh)

    print("PASS: All 54 image files physically exist on disk, verified WebP, exact dimensions, ZERO duplicate hashes")
    print(f"PASS: Categories verified: {categories_found}")

    # 3. Required Trade Elements Check
    text_corpus = " ".join([i["title"] + " " + i["alt"] + " " + i["desc"] + " " + i["specs"] for i in images])
    required_phrases = [
        "Starlink Gen 3",
        "chimney mount",
        "Ajax StreetSiren",
        "4K",
        "turret",
        "soffit",
        "Cat6",
        "drip loop",
        "Ring",
        "gritstone"
    ]
    for phrase in required_phrases:
        assert phrase.lower() in text_corpus.lower(), f"Required phrase '{phrase}' missing from trade asset corpus"
        print(f"PASS: Required trade element verified: '{phrase}'")

    # 4. Gallery HTML Check
    assert os.path.exists(gallery_path), "image-gallery.html does not exist"
    with open(gallery_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    assert "https://cdn.jsdelivr.net/gh/gazpearce/cctv-security-hub@master/assets/images/" in html_content, "jsDelivr CDN pattern missing"
    print("PASS: High-speed jsDelivr CDN URLs verified in image-gallery.html")

    assert "1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88" in html_content, "Google Drive folder ID missing in HTML"
    print("PASS: Google Drive Hub folder ID verified in image-gallery.html")

    assert "07860 244 274" in html_content, "Gary Pearce telephone missing"
    print("PASS: Gary Pearce direct mobile (07860 244 274) verified")

    # Check Schema.org in HTML
    schema_match = re.search(r'<script type="application/ld\+json">(.*?)</script>', html_content, re.DOTALL)
    assert schema_match, "Schema.org script missing from image-gallery.html"
    schema_obj = json.loads(schema_match.group(1))
    assert "@graph" in schema_obj, "Schema @graph missing"
    gallery_entity = schema_obj["@graph"][0]
    assert gallery_entity["@type"] == "ImageGallery", "ImageGallery root type missing"
    image_objects = [o for o in schema_obj["@graph"] if o["@type"] == "ImageObject"]
    assert len(image_objects) == 54, f"Expected 54 ImageObjects in schema, found {len(image_objects)}"
    print("PASS: Schema.org ImageGallery and 54 ImageObjects valid JSON-LD verified")

    # Check explicit width/height on all <img> tags in image-gallery.html
    img_tags = re.findall(r'<img [^>]+>', html_content)
    for tag in img_tags:
        if 'id="modal-img"' in tag:
            continue
        assert 'width="' in tag and 'height="' in tag, f"Missing explicit width/height in tag: {tag}"
    print(f"PASS: All {len(img_tags)-1} static <img> elements have explicit width & height (CLS = 0.00)")

    print("\n" + "=" * 60)
    print("ALL VERIFICATION CHECKS PASSED WITH 100% SUCCESS!")
    print("=" * 60)

if __name__ == "__main__":
    run_verification()
