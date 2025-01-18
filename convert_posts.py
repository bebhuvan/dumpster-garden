import os
import re
import yaml
from pathlib import Path
from datetime import datetime

def fix_frontmatter(metadata):
    """Create clean frontmatter"""
    try:
        date = metadata.get('date', '')
        if isinstance(date, datetime):
            date = date.strftime('%Y-%m-%d')
        elif isinstance(date, str):
            date = date.split('T')[0]
            
        return {
            'title': metadata.get('title', ''),
            'date': date,
            'tags': metadata.get('categories', [])
        }
    except Exception as e:
        print(f"Error in frontmatter: {str(e)}")
        return metadata

def clean_quotes(content):
    """Convert blockquotes properly to Markdown"""
    # Handle blockquotes with citations
    content = re.sub(
        r'<blockquote[^>]*>\s*<p>(.*?)</p>\s*(?:<cite>(.*?)</cite>)?\s*</blockquote>',
        lambda m: f'\n> {m.group(1).strip()}\n' + (f'> \n> — {m.group(2).strip()}\n' if m.group(2) else '\n'),
        content,
        flags=re.DOTALL
    )
    
    # Clean up any nested tags inside quotes
    content = re.sub(r'</?p>', '', content)
    content = re.sub(r'</?strong>', '**', content)
    content = re.sub(r'</?em>', '_', content)
    
    return content

def clean_html(content):
    """Clean up HTML formatting"""
    # Preserve links before general cleanup
    def preserve_link(match):
        text = match.group(1)
        url = match.group(2)
        return f'[{text}]({url})'
    
    content = re.sub(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', preserve_link, content, flags=re.DOTALL)
    
    # Clean basic HTML
    content = re.sub(r'<p[^>]*>', '', content)
    content = re.sub(r'</p>', '\n\n', content)
    content = re.sub(r'<br\s*/?>', '\n', content)
    content = re.sub(r'<hr[^>]*>', '\n---\n', content)
    
    # Handle lists
    content = re.sub(r'<[ou]l[^>]*>', '\n', content)
    content = re.sub(r'</[ou]l>', '\n', content)
    content = re.sub(r'<li[^>]*>(.*?)</li>', r'* \1', content, flags=re.DOTALL)
    
    # Remove remaining HTML tags
    content = re.sub(r'<[^>]+>', '', content)
    
    return content

def format_text(content):
    """Format text for better readability"""
    # Fix multiple newlines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # Add proper spacing around headers
    content = re.sub(r'(#{1,6}\s+[^\n]+)', r'\n\1\n', content)
    
    # Fix list spacing
    content = re.sub(r'\n\*\s+', '\n* ', content)
    
    return content.strip()

def convert_post(input_file, quartz_dir):
    """Convert a WordPress post to Quartz format"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split frontmatter and content
        _, front_matter, main_content = content.split('---', 2)
        metadata = yaml.safe_load(front_matter)
        
        # Process the content in stages
        content = clean_quotes(main_content)
        content = clean_html(content)
        content = format_text(content)
        
        # Create new metadata
        new_metadata = fix_frontmatter(metadata)
        
        # Determine category
        categories = metadata.get('categories', [])
        category_map = {
            'handpicked': 'dumpster-diving',
            'good stuff': 'landfill',
            'quick thoughts': 'litter',
            'quotes': 'scribbles'
        }
        category = next((category_map[cat.lower()] for cat in categories 
                      if cat.lower() in category_map), 'salvage')
        
        # Create output file
        output_file = quartz_dir / 'content' / category / Path(input_file).name
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('---\n')
            f.write(yaml.dump(new_metadata, allow_unicode=True))
            f.write('---\n\n')
            f.write(content)
        
        print(f'Converted {input_file.name} -> {output_file}')
        
    except Exception as e:
        print(f"Error converting {input_file.name}: {str(e)}")

def main():
    quartz_dir = Path('/home/bhuvanesh/Documents/personal/new_gardens')
    posts_dir = Path('/home/bhuvanesh/Downloads/hugo-export/posts')
    
    # Create category directories if needed
    for category in ['landfill', 'dumpster-diving', 'litter', 'scribbles', 'salvage']:
        (quartz_dir / 'content' / category).mkdir(parents=True, exist_ok=True)
    
    # Convert all posts
    for post_file in posts_dir.glob('*.md'):
        convert_post(post_file, quartz_dir)

if __name__ == "__main__":
    main()
