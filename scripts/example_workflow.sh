#!/bin/bash
# Example workflow for creating a photo gallery
# This demonstrates the complete process for the 590LEC gallery

set -e  # Exit on error

echo "=== Photo Gallery Generation Example ==="
echo ""

# Step 1: Process images
echo "Step 1: Processing images..."
python3 process_images.py \
    ../590LEC/files/Field\ Testing/ \
    --quality 85 \
    --max-width 2400

echo ""
echo "Step 2: Edit the metadata file (MANUAL STEP)"
echo "  File: ../590LEC/files/Field Testing/gallery_metadata.json"
echo "  - Add descriptions to the 'description' field"
echo "  - Set 'order' to control photo sequence"
echo "  - Add 'section' to group photos (optional)"
echo ""
read -p "Press Enter when you've finished editing the metadata..."

# Step 3: Generate HTML
echo ""
echo "Step 3: Generating HTML gallery..."
python3 generate_gallery.py \
    ../590LEC/files/Field\ Testing/gallery_metadata.json \
    --output ../590LEC/590LEC_PhotoGallery.html \
    --title "EE 590LEC Field Testing Photos" \
    --base-path "./files/Field Testing" \
    --breadcrumb "Home,../index.html" "590LEC,590LEC.html" "Photo Gallery"

# Step 4: Copy CSS
echo ""
echo "Step 4: Copying improved CSS..."
cp photogallery_style.css ../590LEC/

echo ""
echo "=== Gallery generation complete! ==="
echo "Open ../590LEC/590LEC_PhotoGallery.html in your browser to view."
