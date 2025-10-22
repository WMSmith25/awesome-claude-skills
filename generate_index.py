#!/usr/bin/env python3
"""
Script to parse README.md and generate a JSON index of all Claude skills.
"""

import json
import re
from typing import Dict, List


def parse_readme(readme_path: str) -> Dict:
    """Parse the README.md file and extract skills organized by category."""
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract all category sections
    # Pattern: ## emoji Category Name followed by skill items
    category_pattern = r'## (.+?)\n((?:-\s+\[.+?\].*\n?)*)'
    
    categories = {}
    
    for match in re.finditer(category_pattern, content):
        category_title = match.group(1).strip()
        skills_text = match.group(2).strip()
        
        # Skip non-skill sections like "Contribution" or "Contact"
        if not skills_text or 'Contribution' in category_title or 'Contact' in category_title or 'Table of Contents' in category_title:
            continue
        
        # Extract individual skills
        # Pattern: - [name](url) - description (with optional leading spaces)
        skill_pattern = r'-\s+\[(.+?)\]\((.+?)\) - (.+?)(?:\n|$)'
        
        skills = []
        for skill_match in re.finditer(skill_pattern, skills_text):
            skill_name = skill_match.group(1).strip()
            skill_url = skill_match.group(2).strip()
            skill_description = skill_match.group(3).strip()
            
            skills.append({
                "name": skill_name,
                "url": skill_url,
                "description": skill_description
            })
        
        if skills:
            # Remove emoji from category name for cleaner JSON
            category_clean = re.sub(r'[^\w\s&-]', '', category_title).strip()
            categories[category_clean] = {
                "title": category_title,
                "skills": skills,
                "count": len(skills)
            }
    
    # Build the final index structure
    index = {
        "repository": "Awesome Claude Skills",
        "description": "A curated list of Claude AI skills organized by category",
        "total_skills": sum(cat["count"] for cat in categories.values()),
        "total_categories": len(categories),
        "categories": categories,
        "generated_at": "2025-10-22T00:57:59.893Z"
    }
    
    return index


def generate_markdown_summary(index: Dict, output_path: str):
    """Generate a markdown summary of the index."""
    
    lines = [
        "# Awesome Claude Skills - Index Summary",
        "",
        "## Overview",
        f"- **Total Skills:** {index['total_skills']}",
        f"- **Total Categories:** {index['total_categories']}",
        f"- **Last Updated:** {index['generated_at'][:10]}",
        "",
        "## Skills by Category",
        ""
    ]
    
    for category_key, category_data in index['categories'].items():
        lines.append(f"### {category_data['title']} ({category_data['count']} skills)")
        
        for i, skill in enumerate(category_data['skills'], 1):
            lines.append(f"{i}. **{skill['name']}** - {skill['description']}")
            lines.append(f"   - URL: {skill['url']}")
            lines.append("")
        
        lines.append("")
    
    lines.append("---")
    lines.append("")
    lines.append("*This summary was automatically generated from README.md*")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def main():
    """Main function to generate the index."""
    readme_path = 'README.md'
    json_output_path = 'index.json'
    md_output_path = 'INDEX_SUMMARY.md'
    
    print(f"Parsing {readme_path}...")
    index = parse_readme(readme_path)
    
    print(f"Found {index['total_skills']} skills in {index['total_categories']} categories")
    
    # Write JSON with pretty formatting
    with open(json_output_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    
    print(f"JSON index written to {json_output_path}")
    
    # Write markdown summary
    generate_markdown_summary(index, md_output_path)
    print(f"Markdown summary written to {md_output_path}")
    
    # Print summary
    print("\nCategories:")
    for category_key, category_data in index['categories'].items():
        print(f"  - {category_data['title']}: {category_data['count']} skills")


if __name__ == '__main__':
    main()
