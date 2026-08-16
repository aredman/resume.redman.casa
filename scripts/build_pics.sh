###!/bin/bash
#python process_images.py ../590LEC/files/Field\ Testing/ --quality 85

#python generate_gallery.py \
#    ../590LEC/files/Field\ Testing/gallery_metadata.json \
#    --output ../590LEC/590LEC_PhotoGallery.html \
#    --title "EE 590LEC Field Testing Photos" \
#    --base-path "./files/Field Testing" \
#    --breadcrumb "Home,../index.html" "590LEC,590LEC.html" "Photo Gallery"

python generate_gallery.py \
    ../AmateurRadio/files/Photos/gallery_metadata.json \
    --output ../AmateurRadio/radio_PhotoGallery.html \
    --title "Amateur Radio Photo Gallery" \
    --base-path "./files/Photos" \
    --breadcrumb "Home,../index.html" "Amateur Radio,radio.html" "Photo Gallery"
