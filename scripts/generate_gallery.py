#!/usr/bin/env python3
"""
Photo Gallery HTML Generator
Generates a photo gallery HTML page from a metadata JSON file.

Usage:
    python generate_gallery.py <metadata_json> [options]

Example:
    python generate_gallery.py ../590LEC/files/Field_Testing/gallery_metadata.json \
        --title "Field Testing Photos" \
        --output ../590LEC/590LEC_PhotoGallery.html \
        --breadcrumb "Home,../index.html" "590LEC,590LEC.html" "Photo Gallery"
"""

import argparse
import json
import sys
from pathlib import Path


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <link rel="stylesheet" href="{style_css}">
    <link rel="stylesheet" href="{gallery_css}">
    <link rel="icon" type="image/png" href="{favicon}"/>
</head>
<body>

<nav class="breadcrumb">
    <ol>
{breadcrumb_html}
    </ol>
</nav>

{section_html}

<footer>
<center>
&copy; 2026 RedmanLabs
</center>
</footer>

</body>
</html>
"""

SECTION_TEMPLATE = """<h1>{section_title}</h1>

<div class="gallery-container">
{thumbnails}
{lightboxes}
</div>
"""

THUMBNAIL_TEMPLATE = """    <div class="photo-item">
        <a href="#img{index}">
            <img src="{image_path}" alt="{alt_text}" loading="lazy">
        </a>
    </div>
"""

LIGHTBOX_TEMPLATE = """    <div id="img{index}" class="lightbox">
        <a href="#" class="close-btn">&times;</a>
        <a href="#">
            <img src="{image_path}" alt="{alt_text}">
        </a>
    </div>
"""


def parse_breadcrumb(breadcrumb_args):
    """
    Parse breadcrumb arguments into a list of (text, url) tuples.
    
    Args:
        breadcrumb_args: List of strings in format "Text,url" or "Text" for current page
    
    Returns:
        List of tuples: [(text, url), ...] where url is None for current page
    """
    breadcrumbs = []
    
    for arg in breadcrumb_args:
        if ',' in arg:
            text, url = arg.split(',', 1)
            breadcrumbs.append((text.strip(), url.strip()))
        else:
            breadcrumbs.append((arg.strip(), None))
    
    return breadcrumbs


def generate_breadcrumb_html(breadcrumbs):
    """Generate HTML for breadcrumb navigation."""
    html_parts = []
    
    for text, url in breadcrumbs:
        if url:
            html_parts.append(f'        <li><a href="{url}">{text}</a></li>')
        else:
            html_parts.append(f'        <li class="current">{text}</li>')
    
    return '\n'.join(html_parts)


def generate_gallery_section(photos, base_path, section_title=None):
    """
    Generate HTML for a gallery section.
    
    Args:
        photos: List of photo metadata dicts
        base_path: Base path for image files (relative to HTML file)
        section_title: Optional section title
    
    Returns:
        str: HTML for the gallery section
    """
    thumbnails = []
    lightboxes = []
    
    for idx, photo in enumerate(photos, start=1):
        # Build image path
        img_path = f"{base_path}/{photo['webp_relative_path']}"
        
        # Use description as alt text, fallback to filename
        alt_text = photo.get('description', '') or photo['webp_filename'].replace('.webp', '')
        
        # Generate thumbnail
        thumbnails.append(THUMBNAIL_TEMPLATE.format(
            index=idx,
            image_path=img_path,
            alt_text=alt_text
        ))
        
        # Generate lightbox
        lightboxes.append(LIGHTBOX_TEMPLATE.format(
            index=idx,
            image_path=img_path,
            alt_text=alt_text
        ))
    
    # Combine into section
    section_html = SECTION_TEMPLATE.format(
        section_title=section_title or '',
        thumbnails='\n'.join(thumbnails),
        lightboxes='\n'.join(lightboxes)
    )
    
    return section_html if section_title else f"""
<div class="gallery-container">
{chr(10).join(thumbnails)}
{chr(10).join(lightboxes)}
</div>
"""


def generate_gallery_html(metadata_file, output_file, title, breadcrumbs, 
                          style_css='style.css', gallery_css='photogallery_style.css',
                          favicon='../files/favicon.png', base_path='./files/Field Testing'):
    """
    Generate complete gallery HTML file.
    
    Args:
        metadata_file: Path to gallery_metadata.json
        output_file: Path for output HTML file
        title: Page title
        breadcrumbs: List of (text, url) tuples
        style_css: Path to main stylesheet
        gallery_css: Path to gallery stylesheet
        favicon: Path to favicon
        base_path: Base path for images relative to output HTML
    """
    # Load metadata
    try:
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
    except Exception as e:
        print(f"Error loading metadata file: {e}")
        sys.exit(1)
    
    if not metadata:
        print("Error: No photos found in metadata file")
        sys.exit(1)
    
    # Sort photos by order field, then by filename
    metadata.sort(key=lambda x: (x.get('order', 999), x['webp_filename']))
    
    # Generate breadcrumb HTML
    breadcrumb_html = generate_breadcrumb_html(breadcrumbs)
    
    # Check if metadata has sections
    sections = {}
    for photo in metadata:
        section = photo.get('section', '')
        if section not in sections:
            sections[section] = []
        sections[section].append(photo)
    
    # Generate gallery sections
    if len(sections) == 1 and '' in sections:
        # Single section, no title
        section_html = generate_gallery_section(metadata, base_path)
    else:
        # Multiple sections
        section_parts = []
        for section_name, photos in sections.items():
            section_title = section_name if section_name else "Photos"
            section_parts.append(generate_gallery_section(photos, base_path, section_title))
        section_html = '\n'.join(section_parts)
    
    # Generate complete HTML
    html = HTML_TEMPLATE.format(
        title=title,
        style_css=style_css,
        gallery_css=gallery_css,
        favicon=favicon,
        breadcrumb_html=breadcrumb_html,
        section_html=section_html
    )
    
    # Write output file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"[OK] Generated gallery: {output_file}")
        print(f"[OK] Total photos: {len(metadata)}")
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Generate photo gallery HTML from metadata JSON',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Generate basic gallery:
    python generate_gallery.py gallery_metadata.json -o gallery.html -t "My Photos"
  
  With breadcrumbs:
    python generate_gallery.py data.json -o page.html -t "Photos" \\
        -b "Home,../index.html" "Gallery,gallery.html" "Photos"
  
  Custom paths:
    python generate_gallery.py data.json -o page.html -t "Photos" \\
        --base-path "./files/Photos" --style "../style.css"
        """
    )
    
    parser.add_argument('metadata', help='Path to gallery_metadata.json file')
    parser.add_argument('-o', '--output', required=True, help='Output HTML file path')
    parser.add_argument('-t', '--title', required=True, help='Page title')
    parser.add_argument('-b', '--breadcrumb', nargs='+', default=[],
                       help='Breadcrumb items as "Text,url" or "Text" for current page')
    parser.add_argument('--style', default='style.css', help='Path to main CSS file')
    parser.add_argument('--gallery-style', default='photogallery_style.css',
                       help='Path to gallery CSS file')
    parser.add_argument('--favicon', default='../files/favicon.png', help='Path to favicon')
    parser.add_argument('--base-path', default='./files/Field Testing',
                       help='Base path for images (relative to output HTML)')
    
    args = parser.parse_args()
    
    # Parse breadcrumbs
    breadcrumbs = parse_breadcrumb(args.breadcrumb) if args.breadcrumb else [('Photo Gallery', None)]
    
    # Generate gallery
    generate_gallery_html(
        metadata_file=args.metadata,
        output_file=args.output,
        title=args.title,
        breadcrumbs=breadcrumbs,
        style_css=args.style,
        gallery_css=args.gallery_style,
        favicon=args.favicon,
        base_path=args.base_path
    )


if __name__ == '__main__':
    main()
