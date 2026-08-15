#!/usr/bin/env python3
"""
Image Processing Script for Photo Galleries
Converts images to WebP format and extracts metadata for gallery generation.

Usage:
    python process_images.py <source_dir> [--quality 85] [--max-width 2400]

Example:
    python process_images.py ../590LEC/files/Field\ Testing/ --quality 85
"""

import argparse
import json
import os
import sys
from pathlib import Path
from PIL import Image, ImageOps
from PIL.ExifTags import TAGS
from datetime import datetime


def get_exif_data(image_path):
    """Extract EXIF metadata from image."""
    try:
        img = Image.open(image_path)
        exif_data = {}
        
        if hasattr(img, '_getexif') and img._getexif() is not None:
            exif = img._getexif()
            for tag_id, value in exif.items():
                tag = TAGS.get(tag_id, tag_id)
                exif_data[tag] = value
        
        return exif_data
    except Exception as e:
        print(f"Warning: Could not read EXIF from {image_path}: {e}")
        return {}


def convert_to_webp(input_path, output_path, quality=85, max_width=2400):
    """
    Convert image to WebP format with optional resizing.
    
    Args:
        input_path: Source image file
        output_path: Destination WebP file
        quality: WebP quality (0-100, default 85)
        max_width: Maximum width in pixels (maintains aspect ratio)
    
    Returns:
        dict: Metadata about the converted image
    """
    try:
        img = Image.open(input_path)
        
        # Apply EXIF orientation so portrait photos display correctly
        # (phone cameras store portrait images as landscape pixels with a
        # "rotate 90°" EXIF tag — this bakes the rotation into the pixels)
        img = ImageOps.exif_transpose(img)
        
        # Get original dimensions (after orientation fix)
        orig_width, orig_height = img.size
        
        # Resize if needed
        if orig_width > max_width:
            ratio = max_width / orig_width
            new_height = int(orig_height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            print(f"  Resized from {orig_width}x{orig_height} to {max_width}x{new_height}")
        
        # Convert to RGB if necessary (WebP doesn't support all modes)
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Save as WebP
        img.save(output_path, 'WEBP', quality=quality, method=6)
        
        # Get file sizes
        orig_size = os.path.getsize(input_path)
        new_size = os.path.getsize(output_path)
        savings = (1 - new_size / orig_size) * 100
        
        print(f"  Converted: {orig_size/1024:.1f}KB → {new_size/1024:.1f}KB ({savings:.1f}% smaller)")
        
        return {
            'original_width': orig_width,
            'original_height': orig_height,
            'final_width': img.size[0],
            'final_height': img.size[1],
            'original_size': orig_size,
            'webp_size': new_size,
            'savings_percent': round(savings, 1)
        }
        
    except Exception as e:
        print(f"Error converting {input_path}: {e}")
        return None


def process_directory(source_dir, quality=85, max_width=2400):
    """
    Process all images in a directory.
    
    Creates a 'webp' subdirectory and generates a metadata JSON file.
    """
    source_path = Path(source_dir).resolve()
    
    if not source_path.exists():
        print(f"Error: Directory not found: {source_dir}")
        sys.exit(1)
    
    # Create output directory
    webp_dir = source_path / 'webp'
    webp_dir.mkdir(exist_ok=True)
    
    # Supported image formats
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
    
    # Find all images
    image_files = [f for f in source_path.iterdir() 
                   if f.is_file() and f.suffix.lower() in image_extensions]
    
    if not image_files:
        print(f"No images found in {source_dir}")
        sys.exit(1)
    
    print(f"Found {len(image_files)} images to process\n")
    
    # Process each image
    metadata_list = []
    
    for img_file in sorted(image_files):
        print(f"Processing: {img_file.name}")
        
        # Output filename
        webp_filename = img_file.stem + '.webp'
        webp_path = webp_dir / webp_filename
        
        # Convert image
        conversion_info = convert_to_webp(img_file, webp_path, quality, max_width)
        
        if conversion_info:
            # Extract EXIF
            exif = get_exif_data(img_file)
            
            # Build metadata entry
            metadata = {
                'original_filename': img_file.name,
                'webp_filename': webp_filename,
                'webp_relative_path': f'webp/{webp_filename}',
                'width': conversion_info['final_width'],
                'height': conversion_info['final_height'],
                'aspect_ratio': round(conversion_info['final_width'] / conversion_info['final_height'], 3),
                'orientation': 'landscape' if conversion_info['final_width'] > conversion_info['final_height'] else 'portrait',
                'file_size_kb': round(conversion_info['webp_size'] / 1024, 1),
                'date_taken': exif.get('DateTime', ''),
                'description': '',  # User can fill this in
                'order': 0  # User can set custom order
            }
            
            metadata_list.append(metadata)
        
        print()
    
    # Save metadata JSON
    json_path = source_path / 'gallery_metadata.json'
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(metadata_list, f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Processed {len(metadata_list)} images")
    print(f"[OK] WebP files saved to: {webp_dir}")
    print(f"[OK] Metadata saved to: {json_path}")
    print(f"\nNext steps:")
    print(f"1. Edit {json_path.name} to add descriptions and set display order")
    print(f"2. Run generate_gallery.py to create the HTML page")


def main():
    parser = argparse.ArgumentParser(
        description='Convert images to WebP and extract metadata for photo galleries'
    )
    parser.add_argument('source_dir', help='Directory containing images to process')
    parser.add_argument('--quality', type=int, default=85, 
                       help='WebP quality (0-100, default: 85)')
    parser.add_argument('--max-width', type=int, default=2400,
                       help='Maximum width in pixels (default: 2400)')
    
    args = parser.parse_args()
    
    # Validate quality
    if not 0 <= args.quality <= 100:
        print("Error: Quality must be between 0 and 100")
        sys.exit(1)
    
    process_directory(args.source_dir, args.quality, args.max_width)


if __name__ == '__main__':
    main()
