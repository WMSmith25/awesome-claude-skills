# Skills Indexer

This script parses the `README.md` file and generates a JSON index of all Claude skills.

## Usage

Run the indexer script:

```bash
python3 index_skills.py
```

This will:
1. Parse `README.md` to extract all skills organized by category
2. Generate `skills-index.json` with a structured index of all skills
3. Display a summary of categories and skill counts

## Output Format

The generated `skills-index.json` contains:

```json
{
  "metadata": {
    "title": "Awesome Claude Skills",
    "description": "A curated index of Claude skills organized by category",
    "total_skills": 33,
    "total_categories": 9
  },
  "categories": [
    {
      "name": "📄 Document Skills",
      "skills": [
        {
          "name": "docx",
          "url": "https://github.com/anthropics/skills/tree/main/document-skills/docx",
          "description": "Create, edit, analyze Word docs with tracked changes, comments, formatting."
        }
      ]
    }
  ]
}
```

## Requirements

- Python 3.x
- No external dependencies required (uses only standard library)
