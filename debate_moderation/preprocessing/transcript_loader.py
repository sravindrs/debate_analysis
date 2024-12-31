import json
import pandas as pd
from typing import List, Dict
import os


class TranscriptLoader:
    """Handles loading and parsing transcripts from flexible formats."""

    def __init__(self):
        self.supported_formats = ['json', 'txt', 'csv']

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
        Loads debate transcript format where speaker segments are divided by two newlines.
        Speaker name is identified before the first colon (':').
        """
        # Read entire content of the file
        with open(file_path, 'r') as file:
            content = file.read()
            print(f"Raw content length: {len(content)} characters")  # Debug content size

        # Split transcript into segments based on double newlines
        segments = content.split('\n\n')  # Split by double newlines
        print(f"Total segments: {len(segments)}")  # Debug segment count

        # Prepare list to store structured data
        data = []

        for segment in segments:
            # Remove extra whitespace from segment
            segment = segment.strip()
            print(f"Processing segment: {segment[:50]}...")  # Debug segment preview

            # Skip empty segments
            if not segment:
                continue

            # Extract speaker and text
            if ':' in segment:  # Ensure colon exists
                speaker, text = segment.split(':', 1)  # Split at the first colon
                speaker = speaker.strip()  # Clean speaker name
                text = text.strip()  # Clean text content

                # Append structured data
                data.append({
                    "speaker": speaker,
                    "text": text,
                    "start_time": None,
                    "end_time": None
                })
                print(f"Processed: {speaker}: {text[:50]}...")  # Debug processed entry
            else:
                # Handle non-speaker blocks if necessary (optional)
                print(f"Skipped non-speaker block: {segment[:50]}...")

        # Convert structured data to a DataFrame
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
