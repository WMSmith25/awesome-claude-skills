#!/usr/bin/env python3
"""
Index and summarize awesome-claude-skills repository items.
Parses README.md and generates a JSON index of all skills.
"""

import json
import re
from typing import List, Dict, Any


def parse_readme(readme_path: str) -> Dict[str, Any]:
    """
    Parse README.md and extract skills organized by category.
    
    Args:
        readme_path: Path to README.md file
        
    Returns:
        Dictionary containing indexed skills
    """
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Initialize the index structure
    index = {
        "metadata": {
            "title": "Awesome Claude Skills",
            "description": "A curated index of Claude skills organized by category",
            "total_skills": 0,
            "total_categories": 0
        },
        "categories": []
    }
    
    # Split content into sections by headers
    lines = content.split('\n')
    current_category = None
    current_category_data = None
    
    for line in lines:
        # Check for category header (## followed by emoji and text)
        category_match = re.match(r'^##\s+(.+)$', line)
        if category_match:
            category_full_name = category_match.group(1).strip()
            
            # Skip Table of Contents and non-skill sections
            if any(skip in category_full_name for skip in ['Table of Contents', 'Contribution', 'Contact']):
                # Save previous category if exists before skipping
                if current_category_data:
                    index["categories"].append(current_category_data)
                current_category = None
                current_category_data = None
                continue
            
            # Save previous category if exists
            if current_category_data:
                index["categories"].append(current_category_data)
            
            # Start new category
            current_category = category_full_name
            current_category_data = {
                "name": category_full_name,
                "skills": []
            }
            continue
        
        # Check for skill entry (- [skill-name](url) - description)
        if current_category and line.strip().startswith('-') and '[' in line and '](' in line:
            # Handle various whitespace characters (spaces, tabs) between parts
            skill_match = re.match(r'^-\s+\[([^\]]+)\]\(([^)]+)\)\s+-\s+(.+)$', line.strip())
            if not skill_match:
                # Try alternative pattern with tab or other whitespace before description
                skill_match = re.match(r'^-\s+\[([^\]]+)\]\(([^)]+)\)\s*-?\s*(.+)$', line.strip())
            if skill_match:
                skill_name = skill_match.group(1).strip()
                skill_url = skill_match.group(2).strip()
                skill_description = skill_match.group(3).strip()
                
                current_category_data["skills"].append({
                    "name": skill_name,
                    "url": skill_url,
                    "description": skill_description
                })
    
    # Add the last category
    if current_category_data:
        index["categories"].append(current_category_data)
    
    # Calculate totals
    total_skills = sum(len(cat["skills"]) for cat in index["categories"])
    index["metadata"]["total_skills"] = total_skills
    index["metadata"]["total_categories"] = len(index["categories"])
    
    return index


def main():
    """Main function to parse README and generate JSON index."""
    readme_path = 'README.md'
    output_path = 'skills-index.json'
    
    print(f"Parsing {readme_path}...")
    index = parse_readme(readme_path)
    
    print(f"Found {index['metadata']['total_categories']} categories")
    print(f"Found {index['metadata']['total_skills']} skills")
    
    # Write JSON output with pretty formatting
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    
    print(f"\nJSON index written to {output_path}")
    
    # Print summary
    print("\n=== Summary by Category ===")
    for category in index["categories"]:
        print(f"{category['name']}: {len(category['skills'])} skills")


if __name__ == '__main__':
    main()
