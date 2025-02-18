#!/bin/bash

# Create icons directory if it doesn't exist
mkdir -p icons.iconset

# Generate different icon sizes from base png
sips -z 16 16     friday.png --out icons.iconset/icon_16x16.png
sips -z 32 32     friday.png --out icons.iconset/icon_16x16@2x.png
sips -z 32 32     friday.png --out icons.iconset/icon_32x32.png
sips -z 64 64     friday.png --out icons.iconset/icon_32x32@2x.png
sips -z 128 128   friday.png --out icons.iconset/icon_128x128.png
sips -z 256 256   friday.png --out icons.iconset/icon_128x128@2x.png
sips -z 256 256   friday.png --out icons.iconset/icon_256x256.png
sips -z 512 512   friday.png --out icons.iconset/icon_256x256@2x.png
sips -z 512 512   friday.png --out icons.iconset/icon_512x512.png
sips -z 1024 1024 friday.png --out icons.iconset/icon_512x512@2x.png

# Create icns file
iconutil -c icns icons.iconset -o friday.icns

# Cleanup
rm -rf icons.iconset
