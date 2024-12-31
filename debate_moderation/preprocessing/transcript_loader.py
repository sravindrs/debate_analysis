import json
import pandas as pd
from typing import List, Dict
import os


class TranscriptLoader:
    """Handles loading and parsing transcripts from flexible formats."""

    def __init__(self):
        self.supported_formats = ['json', 'txt', 'csv']
        self.moderator = None

    def set_moderator(self, moderator: str):
        self.moderator = moderator.strip().upper()

    def load_transcript(self, file_path: str) -> pd.DataFrame:
        """
        Loads transcript data from a file and returns standardized DataFrame.
        """
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Detect file type
        file_extension = file_path.split('.')[-1].lower()
        if file_extension == 'json':
            return self._load_json(file_path)
        elif file_extension == 'csv':
            return self._load_csv(file_path)
        elif file_extension == 'txt':
            return self._load_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

    def _load_json(self, file_path: str) -> pd.DataFrame:
        """Loads JSON transcript format."""
        with open(file_path, 'r') as file:
            data = json.load(file)
        if 'transcript' in data:  # Handle nested structure
            data = data['transcript']
        return pd.DataFrame(data)

    def _load_csv(self, file_path: str) -> pd.DataFrame:
        """Loads CSV transcript format."""
        return pd.read_csv(file_path)

    def _load_txt(self, file_path: str) -> pd.DataFrame:
        """
        Loads debate transcript format handling both speaker changes and paragraph breaks.
        Maintains debug output and structure from original implementation.
        """
        # Read entire content of the file
        with open(file_path, 'r') as file:
            content = file.read()
            print(f"Raw content length: {len(content)} characters")

        # Split into lines first
        lines = content.split('\n')
        print(f"Total lines: {len(lines)}")

        # Prepare list to store structured data
        data = []
        current_speaker = None
        current_text = []

        for line in lines:
            line = line.strip()
            print(f"Processing line: {line[:50]}...")  # Debug line preview

            # Handle empty lines
            if not line:
                if current_text:  # If we have text, add paragraph break
                    current_text.append('')
                continue

            # Check for new speaker (looking for CAPS followed by colon)
            if ':' in line and (line.split(':')[0].isupper() or 'SPEAKER' in line.split(':')[0]):
                # Save previous speaker's content if exists
                if current_speaker and current_text:
                    full_text = '\n'.join(current_text).strip()
                    data.append({
                        "speaker": current_speaker,
                        "text": full_text,
                        "start_time": None,
                        "end_time": None
                    })
                    print(f"Saved segment for {current_speaker}: {full_text[:50]}...")

                # Start new speaker
                current_speaker, text = line.split(':', 1)
                current_speaker = current_speaker.strip()
                current_text = [text.strip()]
                print(f"New speaker detected: {current_speaker}")
            else:
                # Continue with current speaker
                if current_speaker:
                    current_text.append(line)
                else:
                    print(f"Warning: Found text without speaker: {line}")

        # Don't forget the last segment
        if current_speaker and current_text:
            full_text = '\n'.join(current_text).strip()
            data.append({
                "speaker": current_speaker,
                "text": full_text,
                "start_time": None,
                "end_time": None
            })
            print(f"Saved final segment for {current_speaker}: {full_text[:50]}...")

        # Convert to DataFrame
        df = pd.DataFrame(data)
        print(f"Final DataFrame shape: {df.shape}")  # Debug final DataFrame size
        return df


# Example Usage
if __name__ == "__main__":
    # Replace with your test file path
    file_path = '/Users/sanjayravindran/Documents/dugree/debate_moderation/data/transcript.txt'
    loader = TranscriptLoader()

    try:
        # Load transcript
        df = loader.load_transcript(file_path)
        print(df.head())  # Display first few rows
    except Exception as e:
        print(f"Error: {e}")
