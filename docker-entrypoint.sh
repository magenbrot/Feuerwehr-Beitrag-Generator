#!/bin/sh
set -e

MEDIA_DIR="/usr/share/nginx/html/media"

# Seed default media on first run (when volume is empty or missing files)
if [ ! -f "${MEDIA_DIR}/.seeded" ]; then
    echo "First run: seeding default media..."
    mkdir -p "${MEDIA_DIR}/templates"
    cp -n /defaults/logo.png "${MEDIA_DIR}/logo.png" 2>/dev/null || true
    cp -n /defaults/templates/*.png "${MEDIA_DIR}/templates/" 2>/dev/null || true
    touch "${MEDIA_DIR}/.seeded"
    echo "Default media seeded. Replace files in ${MEDIA_DIR} to customize."
else
    echo "Media already present, skipping seed."
fi

# Generate templates manifest (valid JSON array of template images)
# Strategy: collect entries separated by newlines, then transform to JSON
TEMPLATES_DIR="${MEDIA_DIR}/templates"
MANIFEST="${TEMPLATES_DIR}/manifest.json"

if [ -d "${TEMPLATES_DIR}" ]; then
    TMPFILE="$(mktemp)"

    for ext in png jpg jpeg webp gif PNG JPG JPEG WEBP GIF; do
        for filepath in "${TEMPLATES_DIR}"/*.${ext}; do
            [ -f "$filepath" ] || continue
            filename=$(basename "$filepath")
            name="${filename%.*}"
            path="/media/templates/${filename}"
            printf '{"name":"%s","path":"%s"}\n' "$name" "$path" >> "$TMPFILE"
        done
    done

    LINE_COUNT=$(wc -l < "$TMPFILE" | tr -d ' ')
    if [ "$LINE_COUNT" -gt 0 ]; then
        printf '[' > "${MANIFEST}"
        LINE_NUM=0
        while IFS= read -r line; do
            LINE_NUM=$((LINE_NUM + 1))
            if [ "$LINE_NUM" -eq 1 ]; then
                printf '\n  %s' "$line" >> "${MANIFEST}"
            else
                printf ',\n  %s' "$line" >> "${MANIFEST}"
            fi
        done < "$TMPFILE"
        printf '\n]\n' >> "${MANIFEST}"
    else
        printf '[]\n' > "${MANIFEST}"
    fi
    rm -f "$TMPFILE"
    echo "Generated templates manifest: ${MANIFEST}"
fi

exec nginx -g 'daemon off;'
