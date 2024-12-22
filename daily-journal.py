#!/usr/bin/env python3
import os
import argparse
from datetime import datetime
import subprocess
from pathlib import Path

class DailyJournal:
    def __init__(self, journal_dir="~/journal"):
        self.journal_dir = os.path.expanduser(journal_dir)
        self.ensure_journal_directory()
        
    def ensure_journal_directory(self):
        """Create journal directory if it doesn't exist"""
        Path(self.journal_dir).mkdir(parents=True, exist_ok=True)
    
    def get_journal_template(self):
        """Return the daily journal template"""
        return f"""# Daily Journal - {datetime.now().strftime('%A, %B %d, %Y')}

## Morning Reflections
- How do you feel today?  
- What are your main goals for today?  
- What are you grateful for?  
- What are you looking forward to?  
- Is there a positive affirmation you'd like to focus on today?  

## Daily Accomplishments
- What went well today?  
- What did you learn?  
- What could have gone better?  
- What made you smile or laugh today?  
- Did you overcome any challenges?  

## Tomorrow's Planning
- What are your top priorities for tomorrow?  
- Any obstacles you need to address?  
- Is there someone you need to reach out to or follow up with?  
- What resources or tools will you need to succeed?  
- How can you set yourself up for a productive day?  

## Additional Notes
- Any personal reflections or insights?  
- Are there any habits or behaviors you'd like to improve?  
- Did you encounter or notice anything inspiring?  
- How are you feeling about your progress this week?  
- Is there something you'd like to document for future reference?  

## Mood Tracker
Energy Level (1-10): 
Stress Level (1-10): 
Overall Mood: 

---
Tags: #daily-journal #{datetime.now().strftime('%B').lower()} #{datetime.now().year}
"""

    def get_todays_filename(self):
        """Generate filename for today's journal entry"""
        return os.path.join(
            self.journal_dir,
            f"{datetime.now().strftime('%Y-%m-%d')}.md"
        )
    
    def create_todays_entry(self):
        """Create a new journal entry for today if it doesn't exist"""
        filename = self.get_todays_filename()
        
        if os.path.exists(filename):
            return filename, False
            
        with open(filename, 'w') as f:
            f.write(self.get_journal_template())
        
        return filename, True

    def open_editor(self, filename):
        """Open the journal entry in the default editor"""
        editor = os.environ.get('EDITOR', 'nano')  # Default to nano if no EDITOR is set
        subprocess.call([editor, filename])

    def list_recent_entries(self, count=5):
        """List the most recent journal entries"""
        entries = sorted(
            [f for f in os.listdir(self.journal_dir) if f.endswith('.md')],
            reverse=True
        )
        return entries[:count]

def main():
    parser = argparse.ArgumentParser(description='Daily Markdown Journal')
    parser.add_argument('--list', '-l', action='store_true', help='List recent entries')
    parser.add_argument('--directory', '-d', help='Journal directory path')
    args = parser.parse_args()

    journal = DailyJournal(args.directory if args.directory else "~/journal")

    if args.list:
        print("\nRecent journal entries:")
        for entry in journal.list_recent_entries():
            print(f"- {entry}")
        return

    filename, is_new = journal.create_todays_entry()
    
    if is_new:
        print(f"\nCreated new journal entry: {filename}")
    else:
        print(f"\nOpening existing journal entry: {filename}")
    
    journal.open_editor(filename)
    print("\nJournal entry saved! Happy writing! 📝")

if __name__ == "__main__":
    main()
