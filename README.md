# 🙏 Gratitude Journal

A structured gratitude journal system with JSON storage, search functionality, and HTML export capabilities.

## Features

✨ **Structured JSON Format** — Entries stored with metadata (date, mood, category)  
🔍 **Search** — Find entries by keyword or date range  
📄 **HTML Export** — Generate beautiful formatted journals for sharing  
📝 **Easy CLI** — Simple command-line interface for managing entries

## Project Structure

```
gratitude-journal/
├── gratitude.md           # Original markdown journal
├── entries.json           # Structured entries database
├── gratitude.py           # Main script with all features
└── README.md              # This file
```

## Getting Started

### Prerequisites

- Python 3.6+

### Entry JSON Format

Each entry contains:
- `id`: Unique identifier
- `date`: Entry date (YYYY-MM-DD)
- `time`: Period of day (morning, afternoon, evening, etc.)
- `mood`: How you felt (grateful, happy, proud, peaceful, etc.)
- `category`: List of tags (learning, health, family, work, etc.)
- `text`: Your gratitude message

## Usage

### List All Entries

```bash
python gratitude.py list
```

Output:
```
[1] 2026-03-23 (motivated) - I am grateful that I am able to complete...
[2] 2026-03-23 (proud) - I am grateful for the progress I made today...
```

### Search Entries

**By keyword:**
```bash
python gratitude.py search --keyword learning
```

**By date range:**
```bash
python gratitude.py search --from 2026-03-20 --to 2026-03-25
```

**Combined:**
```bash
python gratitude.py search --keyword GitHub --from 2026-03-20 --to 2026-03-30
```

### Add New Entry

```bash
python gratitude.py add "Your gratitude message here"
```

**With mood and categories:**
```bash
python gratitude.py add "Grateful for morning coffee" --mood happy --category food,wellness
```

### Export to HTML

**Export all entries:**
```bash
python gratitude.py export
```

**Export with custom filename:**
```bash
python gratitude.py export my_journal.html
```

**Export filtered entries:**
```bash
python gratitude.py export journal_march.html --from 2026-03-01 --to 2026-03-30
```

**Export by keyword:**
```bash
python gratitude.py export learning_journal.html --keyword learning
```

## HTML Export Features

The exported HTML includes:
- 📊 Statistics (total entries, categories, moods)
- 🎨 Beautiful gradient design with smooth animations
- 📱 Responsive layout (mobile-friendly)
- 🏷️ Color-coded mood indicators and category tags
- 📅 Full entry dates and timestamps

## Examples

### Workflow Example

```bash
# View what you have
python gratitude.py list

# Search for learning-related entries
python gratitude.py search --keyword learning

# Add today's gratitude
python gratitude.py add "Grateful for completing features" --mood proud --category growth,coding

# Export March entries
python gratitude.py export march_journal.html --from 2026-03-01 --to 2026-03-31

# Export all GitHub-related entries
python gratitude.py export github_journey.html --keyword GitHub
```

## Tips

✨ Use consistent moods for better tracking: happy, grateful, proud, peaceful, hopeful, motivated  
🏷️ Create meaningful categories: family, health, work, learning, growth,friendship, travel  
📅 Search by date range to spot patterns and themes  
📤 Export monthly summaries to share or archive

## File Structure

**entries.json** — Your gratitude database in JSON format. Edit manually if needed:

```json
[
  {
    "id": 1,
    "date": "2026-03-23",
    "time": "morning",
    "mood": "motivated",
    "category": ["learning", "growth"],
    "text": "Your gratitude here..."
  }
]
```

## Technical Details

- All searches are case-insensitive
- Categories are space-separated in CLI (use commas without spaces: `learning,growth`)
- Mood and category are optional when adding entries (defaults: "grateful" and ["general"])
- Dates must follow YYYY-MM-DD format

## Future Enhancements

- Web interface for easier entry management
- Statistics dashboard with charts
- Email reminders to add entries
- Import/export from other formats
- Tag suggestions based on common patterns

---

**Daily gratitude entries from my AI Builder journey** 🚀
