import json
import re

input_file = "train.jsonl"
output_file = "children_stories_cleaned.txt"

def clean_story(text):
    # Normalize newlines
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    # Remove author lines or "From ..."
    text = re.sub(r'\[.*?\]', '', text)        # remove [From ...]
    text = re.sub(r'From .*', '', text, flags=re.IGNORECASE)

    # Normalize quotes
    text = text.replace('“', '"').replace('”', '"') \
               .replace('‘', "'").replace('’', "'")

    # Remove special characters (except punctuation)
    text = re.sub(r'[*#@~^]', '', text)

    # 🔹 Replace ONLY "\n\nThe End." (or case variants) with <|endoftext|>
    text = re.sub(
        r'\n\s*\n\s*The End\.',
        '\n<|endoftext|>',
        text,
        flags=re.IGNORECASE
    )

    # Remove extra blank lines INSIDE the story
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    text = ' '.join(lines)

    return text

cleaned_stories = []

with open(input_file, 'r', encoding='utf-8') as f:
    for line in f:
        story_obj = json.loads(line)
        text = story_obj.get("text", "")
        cleaned_text = clean_story(text)
        cleaned_stories.append(cleaned_text)

# Save all stories in a text file, one story per line
with open(output_file, 'w', encoding='utf-8') as f:
    for story in cleaned_stories:
        f.write(story + '\n')

print(f"Saved {len(cleaned_stories)} cleaned stories to {output_file}")
