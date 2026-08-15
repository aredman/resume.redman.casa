# Photo Gallery Generator System

A simple, maintainable system for creating photo galleries on your static HTML website.

## Overview

This system solves two main problems:
1. **Manual HTML editing** - No more copying/pasting image filenames for each photo
2. **Large image files** - Automatically converts JPG to WebP (typically 25-40% smaller)
3. **Poor lightbox display** - Improved CSS that adapts to different image aspect ratios

## Philosophy

- **Direct control**: You manage which photos appear via a simple JSON file
- **No backend required**: Pure static HTML generation
- **Fast & lean**: WebP images load faster, improved CSS is minimal
- **Linux-friendly**: Python scripts work on any platform

## Workflow

```
1. Take photos → 2. Process images → 3. Edit metadata → 4. Generate HTML
```

### Step 1: Process Images

Convert your images to WebP and extract metadata:

```bash
cd scripts
python process_images.py ../590LEC/files/Field\ Testing/ --quality 85
```

**Options:**
- `--quality 85` - WebP quality (0-100, default: 85)
- `--max-width 2400` - Maximum width in pixels (default: 2400)

**Output:**
- Creates `webp/` subdirectory with converted images
- Generates `gallery_metadata.json` with image metadata

### Step 2: Edit Metadata

Open the generated `gallery_metadata.json` and customize:

```json
[
  {
    "original_filename": "20260402_114513.jpg",
    "webp_filename": "20260402_114513.webp",
    "webp_relative_path": "webp/20260402_114513.webp",
    "width": 2400,
    "height": 1800,
    "aspect_ratio": 1.333,
    "orientation": "landscape",
    "file_size_kb": 245.3,
    "date_taken": "2026:04:02 11:45:13",
    "description": "Testing the optical transceiver outdoors",
    "order": 1,
    "section": ""
  }
]
```

**Editable fields:**
- `description` - Alt text for the image (important for accessibility)
- `order` - Display order (lower numbers first, 0 = first)
- `section` - Optional section name for grouping photos

**Tips:**
- Set `order` to control which photos appear first
- Leave `order` at 0 for all photos to sort alphabetically
- Use `section` to create multiple galleries on one page (e.g., "SSTV", "Field Day")
- Remove entries from the JSON to exclude photos from the gallery

### Step 3: Generate HTML

Create the gallery HTML page:

```bash
python generate_gallery.py \
    ../590LEC/files/Field\ Testing/gallery_metadata.json \
    --output ../590LEC/590LEC_PhotoGallery.html \
    --title "EE 590LEC Field Testing Photos" \
    --base-path "./files/Field Testing" \
    --breadcrumb "Home,../index.html" "590LEC,590LEC.html" "Photo Gallery"
```

**Required arguments:**
- `metadata.json` - Path to your metadata file
- `--output` - Where to save the HTML file
- `--title` - Page title

**Optional arguments:**
- `--base-path` - Path to images relative to output HTML (default: `./files/Field Testing`)
- `--breadcrumb` - Navigation breadcrumbs (format: `"Text,url"` or `"Text"` for current page)
- `--style` - Path to main CSS (default: `style.css`)
- `--gallery-style` - Path to gallery CSS (default: `photogallery_style.css`)
- `--favicon` - Path to favicon (default: `../files/favicon.png`)

### Step 4: Update CSS (One-time)

Copy the improved CSS to your gallery directories:

```bash
cp photogallery_style.css ../590LEC/
cp photogallery_style.css ../AmateurRadio/
```

## Complete Example

Here's a full workflow for the Amateur Radio gallery:

```bash
# 1. Process images
cd scripts
python process_images.py ../AmateurRadio/files/Photos/ --quality 85

# 2. Edit the metadata
nano ../AmateurRadio/files/Photos/gallery_metadata.json
# (Add descriptions, set order, create sections)

# 3. Generate HTML
python generate_gallery.py \
    ../AmateurRadio/files/Photos/gallery_metadata.json \
    --output ../AmateurRadio/radio_PhotoGallery.html \
    --title "Amateur Radio Photo Gallery" \
    --base-path "./files/Photos" \
    --breadcrumb "Home,../index.html" "Amateur Radio,radio.html" "Photo Gallery"

# 4. Copy CSS (if not already done)
cp photogallery_style.css ../AmateurRadio/
```

## File Structure

```
UBWebsite/
├── scripts/
│   ├── README.md                    # This file
│   ├── process_images.py            # Image converter
│   ├── generate_gallery.py          # HTML generator
│   └── photogallery_style.css       # Improved CSS
│
├── 590LEC/
│   ├── files/
│   │   └── Field Testing/
│   │       ├── *.jpg                # Original images
│   │       ├── webp/                # Converted WebP images
│   │       └── gallery_metadata.json # Photo database
│   ├── 590LEC_PhotoGallery.html     # Generated gallery
│   └── photogallery_style.css       # Gallery CSS
│
└── AmateurRadio/
    ├── files/
    │   └── Photos/
    │       ├── *.jpg                # Original images
    │       ├── webp/                # Converted WebP images
    │       └── gallery_metadata.json # Photo database
    ├── radio_PhotoGallery.html      # Generated gallery
    └── photogallery_style.css       # Gallery CSS
```

## Dependencies

Install required Python packages:

```bash
pip install Pillow
```

That's it! No other dependencies needed.

## CSS Improvements

The new `photogallery_style.css` includes:

- **Better lightbox sizing**: Uses `object-fit: contain` to maintain aspect ratios
- **Responsive design**: Adapts to mobile screens
- **Improved close button**: Circular button with hover effect
- **Smoother animations**: Subtle hover effects on thumbnails

## Maintenance Tips

### Adding New Photos

1. Copy new photos to the appropriate directory
2. Re-run `process_images.py` (it will only process new images)
3. Edit `gallery_metadata.json` to add descriptions/order
4. Re-run `generate_gallery.py` to update the HTML

### Updating Existing Galleries

Just re-run the `generate_gallery.py` command - it will overwrite the HTML file.

### Keeping Original Images

The original JPG files are never deleted. You can:
- Keep them for archival purposes
- Delete them after verifying WebP quality
- Use them to regenerate WebP at different quality settings

### Regenerating WebP Images

To regenerate with different settings:

```bash
# Delete the webp directory
rm -rf ../590LEC/files/Field\ Testing/webp/

# Regenerate with new settings
python process_images.py ../590LEC/files/Field\ Testing/ --quality 90 --max-width 3000
```

## Troubleshooting

### "No module named 'PIL'"

Install Pillow:
```bash
pip install Pillow
```

### Images not displaying

Check that `--base-path` matches the actual path from your HTML file to the images.

Example:
- HTML file: `590LEC/590LEC_PhotoGallery.html`
- Images: `590LEC/files/Field Testing/webp/`
- Base path: `./files/Field Testing`

### Lightbox not working

Ensure you've copied the new `photogallery_style.css` to your gallery directory and it's linked in the HTML.

### Images too large/small in lightbox

The CSS uses `max-width: 95%` and `max-height: 95vh`. You can adjust these in `photogallery_style.css`:

```css
.lightbox img {
  max-width: 90%;      /* Adjust this */
  max-height: 90vh;    /* Adjust this */
  /* ... */
}
```

## Advanced Usage

### Multiple Sections

To create galleries with multiple sections, add a `section` field to your metadata:

```json
[
  {
    "webp_filename": "radio1.webp",
    "description": "My HF station",
    "order": 1,
    "section": "Equipment"
  },
  {
    "webp_filename": "sstv1.webp",
    "description": "SSTV reception",
    "order": 1,
    "section": "SSTV"
  }
]
```

The generator will create separate titled sections in the HTML.

### Custom Ordering

Photos are sorted by:
1. `order` field (ascending)
2. `webp_filename` (alphabetically)

To manually order photos, set the `order` field:
- First photo: `"order": 1`
- Second photo: `"order": 2`
- etc.

### Batch Processing

To process multiple galleries at once:

```bash
#!/bin/bash
# process_all_galleries.sh

for dir in ../*/files/*/; do
    if [ -d "$dir" ]; then
        echo "Processing $dir"
        python process_images.py "$dir" --quality 85
    fi
done
```

## Future Enhancements

Possible improvements you could add:

- **Thumbnail generation**: Create smaller thumbnails for faster grid loading
- **EXIF preservation**: Copy EXIF data to WebP files
- **Automatic descriptions**: Use EXIF comments or AI to generate descriptions
- **Gallery templates**: Different layouts (masonry, carousel, etc.)
- **Image optimization**: Automatic rotation based on EXIF orientation

## License

This is your personal website tooling - use it however you like!
