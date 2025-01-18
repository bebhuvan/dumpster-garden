import os
import re
import yaml
from pathlib import Path
from datetime import datetime

def fix_datetime(date_obj):
    """Convert datetime object to string format"""
    if isinstance(date_obj, datetime):
        return date_obj.strftime('%Y-%m-%d')
    if isinstance(date_obj, str):
        return date_obj.split('T')[0]
    return str(date_obj).split('T')[0]

def convert_content(content):
    """Convert content while preserving Substack images"""
    # Keep Substack images intact
    content = content.replace('<img loading="lazy" decoding="async"', '<img')
    content = re.sub(
        r'<img[^>]*src="(https://substackcdn.com/[^"]+)"[^>]*>',
        r'![\1](\1)',
        content
    )
    
    # Remove WordPress formatting
    content = re.sub(r'\s*{\..*?}', '', content)
    content = re.sub(r'<(figure|figcaption)[^>]*>', '', content)
    content = re.sub(r'</(figure|figcaption)>', '', content)
    
    # Convert blockquotes
    content = re.sub(
        r'<blockquote[^>]*>\s*<p>(.*?)</p>\s*(?:<cite>(.*?)</cite>)?\s*</blockquote>',
        lambda m: f'> {m.group(1)}\n' + (f'> \n> — {m.group(2)}\n' if m.group(2) else '\n'),
        content,
        flags=re.DOTALL
    )
    
    # Clean other HTML
    content = re.sub(r'<p>\s*', '', content)
    content = re.sub(r'</p>', '\n\n', content)
    content = re.sub(r'<br\s*/?>', '\n', content)
    content = re.sub(r'<hr[^>]*>', '---', content)
    
    # Remove any remaining HTML tags
    content = re.sub(r'<[^>]+>', '', content)
    
    return content.strip()

def determine_category(metadata):
    """Map WordPress categories to Quartz folders"""
    categories = metadata.get('categories', [])
    category_map = {
        'handpicked': 'dumpster-diving',
        'good stuff': 'landfill',
        'quick thoughts': 'litter',
        'quotes': 'scribbles'
    }
    
    for cat in categories:
        if cat.lower() in category_map:
            return category_map[cat.lower()]
    return 'salvage'

def convert_post(input_file, quartz_dir):
    """Convert a single post"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split front matter and content
    _, front_matter, main_content = content.split('---', 2)
    metadata = yaml.safe_load(front_matter)
    
    # Fix date format
    date = fix_datetime(metadata.get('date', ''))
    
    # Create new metadata
    new_metadata = {
        'title': metadata.get('title', ''),
        'date': date,
        'tags': metadata.get('categories', []) + metadata.get('tags', [])
    }
    
    # Determine category and convert content
    category = determine_category(metadata)
    converted_content = convert_content(main_content)
    
    # Create output file
    output_file = quartz_dir / 'content' / category / Path(input_file).name
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('---\n')
        f.write(yaml.dump(new_metadata, allow_unicode=True))
        f.write('---\n\n')
        f.write(converted_content)
    
    print(f'Converted {input_file.name} -> {output_file}')

def main():
    quartz_dir = Path('/home/bhuvanesh/Documents/personal/new_gardens')
    posts_dir = Path('/home/bhuvanesh/Downloads/hugo-export/posts')
    
    # Create category directories if they don't exist
    for category in ['landfill', 'dumpster-diving', 'litter', 'scribbles', 'salvage']:
        (quartz_dir / 'content' / category).mkdir(parents=True, exist_ok=True)
    
    # Convert all posts
    for post_file in posts_dir.glob('*.md'):
        try:
            convert_post(post_file, quartz_dir)
        except Exception as e:
            print(f'Error converting {post_file.name}: {str(e)}')

if __name__ == "__main__":
    main()
