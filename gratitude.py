#!/usr/bin/env python3
"""
Gratitude Journal Manager
- Search entries by keyword or date range
- Export to HTML
- Add new entries
"""

import json
import sys
from datetime import datetime
from pathlib import Path

ENTRIES_FILE = Path(__file__).parent / "entries.json"


def load_entries():
    """Load entries from JSON file."""
    if not ENTRIES_FILE.exists():
        return []
    with open(ENTRIES_FILE, "r") as f:
        return json.load(f)


def save_entries(entries):
    """Save entries to JSON file."""
    with open(ENTRIES_FILE, "w") as f:
        json.dump(entries, f, indent=2)


def search(keyword=None, start_date=None, end_date=None):
    """Search entries by keyword or date range."""
    entries = load_entries()
    results = entries

    if keyword:
        keyword = keyword.lower()
        results = [
            e
            for e in results
            if keyword in e["text"].lower() or any(keyword in c.lower() for c in e["category"])
        ]

    if start_date:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        results = [e for e in results if datetime.strptime(e["date"], "%Y-%m-%d").date() >= start]

    if end_date:
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
        results = [e for e in results if datetime.strptime(e["date"], "%Y-%m-%d").date() <= end]

    return results


def add_entry(text, mood=None, category=None):
    """Add a new entry."""
    entries = load_entries()
    new_id = max([e["id"] for e in entries], default=0) + 1
    
    entry = {
        "id": new_id,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": "custom",
        "mood": mood or "grateful",
        "category": category or ["general"],
        "text": text,
    }
    entries.append(entry)
    save_entries(entries)
    print(f"✓ Entry added (ID: {new_id})")
    return entry


def export_html(output_file=None, keyword=None, start_date=None, end_date=None):
    """Export entries to HTML."""
    results = search(keyword, start_date, end_date)
    output_file = output_file or "gratitude_journal.html"

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gratitude Journal</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        h1 {
            color: white;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .subtitle {
            color: rgba(255, 255, 255, 0.9);
            text-align: center;
            margin-bottom: 30px;
            font-size: 0.95em;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        .stat-box {
            background: rgba(255, 255, 255, 0.15);
            color: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            backdrop-filter: blur(10px);
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
        }
        .stat-label {
            font-size: 0.85em;
            opacity: 0.9;
        }
        .entry {
            background: white;
            margin-bottom: 20px;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            animation: slideIn 0.3s ease-out;
        }
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        .entry-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 15px;
        }
        .entry-date {
            font-size: 0.95em;
            color: #667eea;
            font-weight: 600;
        }
        .entry-time {
            font-size: 0.85em;
            color: #999;
            text-transform: capitalize;
        }
        .entry-mood {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            text-transform: capitalize;
        }
        .entry-categories {
            margin-top: 10px;
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }
        .category-tag {
            background: #f0e6ff;
            color: #667eea;
            padding: 4px 10px;
            border-radius: 15px;
            font-size: 0.8em;
            text-transform: capitalize;
        }
        .entry-text {
            color: #333;
            line-height: 1.6;
            margin-top: 12px;
            font-size: 0.95em;
        }
        .footer {
            color: rgba(255, 255, 255, 0.8);
            text-align: center;
            margin-top: 40px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🙏 Gratitude Journal</h1>
        <p class="subtitle">Celebrating moments of gratitude</p>
        
        <div class="stats">
            <div class="stat-box">
                <div class="stat-number">{}</div>
                <div class="stat-label">Total Entries</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{}</div>
                <div class="stat-label">Categories</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{}</div>
                <div class="stat-label">Moods</div>
            </div>
        </div>
        
        <div class="entries">
{}</div>
        
        <div class="footer">
            <p>Generated on {}</p>
        </div>
    </div>
</body>
</html>
"""

    # Generate entry HTML
    entries_html = ""
    for entry in results:
        categories_html = "".join(
            f'<span class="category-tag">{cat}</span>' for cat in entry["category"]
        )
        entry_html = f"""
            <div class="entry">
                <div class="entry-header">
                    <div>
                        <div class="entry-date">{entry['date']}</div>
                        <div class="entry-time">{entry['time']}</div>
                    </div>
                    <span class="entry-mood">{entry['mood']}</span>
                </div>
                <div class="entry-categories">{categories_html}</div>
                <div class="entry-text">{entry['text']}</div>
            </div>
"""
        entries_html += entry_html

    # Calculate stats
    all_categories = set()
    all_moods = set()
    for entry in results:
        all_categories.update(entry["category"])
        all_moods.add(entry["mood"])

    html = html_content.format(
        len(results),
        len(all_categories),
        len(all_moods),
        entries_html,
        datetime.now().strftime("%B %d, %Y at %H:%M"),
    )

    with open(output_file, "w") as f:
        f.write(html)
    print(f"✓ HTML exported to {output_file}")


def main():
    """Command-line interface."""
    if len(sys.argv) < 2:
        print("Gratitude Journal Manager")
        print("\nUsage:")
        print("  python gratitude.py search [--keyword WORD] [--from DATE] [--to DATE]")
        print("  python gratitude.py export [output.html] [--keyword WORD] [--from DATE] [--to DATE]")
        print("  python gratitude.py add 'Your gratitude text' [--mood happy] [--category learning,health]")
        print("  python gratitude.py list")
        print("\nExamples:")
        print("  python gratitude.py search --keyword learning")
        print("  python gratitude.py search --from 2026-03-20 --to 2026-03-25")
        print("  python gratitude.py export journal.html")
        print("  python gratitude.py add 'Grateful for coffee' --mood happy --category food")
        return

    command = sys.argv[1]

    if command == "list":
        entries = load_entries()
        if not entries:
            print("No entries yet.")
            return
        for entry in entries:
            print(
                f"[{entry['id']}] {entry['date']} ({entry['mood']}) - {entry['text'][:60]}..."
            )

    elif command == "search":
        keyword = None
        start_date = None
        end_date = None

        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "--keyword" and i + 1 < len(sys.argv):
                keyword = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--from" and i + 1 < len(sys.argv):
                start_date = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--to" and i + 1 < len(sys.argv):
                end_date = sys.argv[i + 1]
                i += 2
            else:
                i += 1

        results = search(keyword, start_date, end_date)
        if not results:
            print("No entries found.")
            return

        print(f"\nFound {len(results)} entry(ies):\n")
        for entry in results:
            print(f"[{entry['id']}] {entry['date']} ({entry['mood']})")
            print(f"    Categories: {', '.join(entry['category'])}")
            print(f"    {entry['text']}\n")

    elif command == "export":
        output_file = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else "gratitude_journal.html"
        keyword = None
        start_date = None
        end_date = None

        i = 2 if output_file == "gratitude_journal.html" else 3
        while i < len(sys.argv):
            if sys.argv[i] == "--keyword" and i + 1 < len(sys.argv):
                keyword = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--from" and i + 1 < len(sys.argv):
                start_date = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--to" and i + 1 < len(sys.argv):
                end_date = sys.argv[i + 1]
                i += 2
            else:
                i += 1

        export_html(output_file, keyword, start_date, end_date)

    elif command == "add":
        if len(sys.argv) < 3:
            print("Error: Please provide the gratitude text")
            return
        text = sys.argv[2]
        mood = None
        category = None

        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--mood" and i + 1 < len(sys.argv):
                mood = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--category" and i + 1 < len(sys.argv):
                category = sys.argv[i + 1].split(",")
                i += 2
            else:
                i += 1

        add_entry(text, mood, category)

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
