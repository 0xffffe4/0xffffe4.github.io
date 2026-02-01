#!/usr/bin/env python3

from bs4 import BeautifulSoup
import re
import cssbeautifier

# Read the original HTML
with open('mirrored_site/web/20250203070757/https:/katharsis.cytres.com/index.html', 'r') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Extract the style tag
style_tag = soup.find('style')
if not style_tag:
    print("No style tag found!")
    exit(1)

css = style_tag.string

# Extract font-face declarations
font_faces = re.findall(r'@font-face\{[^}]+\}', css)

# Extract relevant Telegraph classes
relevant_patterns = [
    r'body[^}]*\{[^}]*\}',
    r'\.tl_page_wrap[^}]*\{[^}]*\}',
    r'\.tl_page[^}]*\{[^}]*\}',
    r'\.tl_article[^}]*\{[^}]*\}',
    r'\.tl_article_header[^}]*\{[^}]*\}',
    r'\.tl_article_content[^}]*\{[^}]*\}',
    r'\.index[^}]*\{[^}]*\}',
    r'\.index img[^}]*\{[^}]*\}',
    r'\.index a[^}]*\{[^}]*\}',
]

# Build clean CSS
clean_css = []

# Add fonts
for font in font_faces:
    clean_css.append(font)

# Add relevant styles
for pattern in relevant_patterns:
    matches = re.findall(pattern, css)
    for match in matches:
        if match not in clean_css:
            clean_css.append(match)

# Beautify and save
beautified = cssbeautifier.beautify('\n'.join(clean_css))

with open('extracted_exact.css', 'w') as f:
    f.write(beautified)

print(f"Extracted {len(clean_css)} CSS rules")
print(f"Total size: {len(beautified)} characters")

# Also extract the exact HTML structure
index_div = soup.find('div', class_='index')
if index_div:
    with open('extracted_index.html', 'w') as f:
        f.write(index_div.prettify())
    print("Extracted index HTML structure")
