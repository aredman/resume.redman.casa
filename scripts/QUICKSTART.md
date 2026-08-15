# Quick Start Guide

## First Time Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Copy the improved CSS to your galleries:**
   ```bash
   cp photogallery_style.css ../590LEC/
   cp photogallery_style.css ../AmateurRadio/
   ```

## Creating a New Gallery

### Example: 590LEC Field Testing Gallery

```bash
cd scripts

# Step 1: Process images (convert to WebP)
python process_images.py "../590LEC/files/Field Testing/" --quality 85

# Step 2: Edit metadata (add descriptions, set order)
# Open: ../590LEC/files/Field Testing/gallery_metadata.json
# Edit the "description" and "order" fields

# Step 3: Generate HTML
python generate_gallery.py \
    "../590LEC/files/Field Testing/gallery_metadata.json" \
    --output ../590LEC/590LEC_PhotoGallery.html \
    --title "EE 590LEC Field Testing Photos" \
    --base-path "./files/Field Testing" \
    --breadcrumb "Home,../index.html" "590LEC,590LEC.html" "Photo Gallery"
```

### Example: Amateur Radio Gallery

```bash
cd scripts

# Step 1: Process images
python process_images.py "../AmateurRadio/files/Photos/" --quality 85

# Step 2: Edit metadata
# Open: ../AmateurRadio/files/Photos/gallery_metadata.json
# Add descriptions and sections (e.g., "Equipment", "SSTV")

# Step 3: Generate HTML
python generate_gallery.py \
    "../AmateurRadio/files/Photos/gallery_metadata.json" \
    --output ../AmateurRadio/radio_PhotoGallery.html \
    --title "Amateur Radio Photo Gallery" \
    --base-path "./files/Photos" \
    --breadcrumb "Home,../index.html" "Amateur Radio,radio.html" "Photo Gallery"
```

## Common Tasks

### Adding New Photos to Existing Gallery

```bash
# 1. Copy new photos to the directory
cp ~/new_photos/*.jpg "../590LEC/files/Field Testing/"

# 2. Re-run process_images (only processes new images)
python process_images.py "../590LEC/files/Field Testing/" --quality 85

# 3. Edit gallery_metadata.json to add descriptions for new photos

# 4. Regenerate HTML
python generate_gallery.py \
    "../590LEC/files/Field Testing/gallery_metadata.json" \
    --output ../590LEC/590LEC_PhotoGallery.html \
    --title "EE 590LEC Field Testing Photos" \
    --base-path "./files/Field Testing" \
    --breadcrumb "Home,../index.html" "590LEC,590LEC.html" "Photo Gallery"
```

### Changing Photo Order

1. Edit `gallery_metadata.json`
2. Set the `order` field (1 = first, 2 = second, etc.)
3. Re-run `generate_gallery.py`

### Creating Sections

1. Edit `gallery_metadata.json`
2. Add a `section` field to each photo (e.g., `"section": "SSTV"`)
3. Re-run `generate_gallery.py`

Photos with the same section name will be grouped together with a heading.

## Tips

- **Quality setting**: 85 is a good balance. Use 90+ for critical photos, 75-80 for web-only content
- **Max width**: 2400px is good for modern displays. Use 1920 for smaller file sizes
- **Descriptions**: These become alt text - important for accessibility!
- **Order**: Leave at 0 for all photos to sort alphabetically by filename

## Troubleshooting

**"No module named 'PIL'"**
```bash
pip install Pillow
```

**Images not showing in browser**
- Check that `--base-path` matches the actual directory structure
- Verify WebP files exist in the `webp/` subdirectory

**Want to start over?**
```bash
# Delete generated files
rm -rf "../590LEC/files/Field Testing/webp/"
rm "../590LEC/files/Field Testing/gallery_metadata.json"

# Re-run from step 1
```

## Windows Users

Use PowerShell or Git Bash. For paths with spaces, use quotes:

```powershell
python process_images.py "../590LEC/files/Field Testing/" --quality 85
```

Or escape spaces:
```bash
python process_images.py ../590LEC/files/Field\ Testing/ --quality 85
```
