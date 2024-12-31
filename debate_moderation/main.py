# Import modules
from preprocessing.transcript_loader import TranscriptLoader
from preprocessing.text_cleaner import TextCleaner
from realtime.realtime_processor import RealTimeProcessor

# Initialize components
loader = TranscriptLoader()
cleaner = TextCleaner()
processor = RealTimeProcessor()  # Create processor instance

# Get file path dynamically
file_path = input("Enter the path to the transcript file: ").strip()
processor.set_file_path(file_path)

# Set moderator
moderator_name = input("Enter the moderator's name (leave blank if none): ")
if moderator_name:
    loader.set_moderator(moderator_name)

# State for storing processed data
import pandas as pd
data = pd.DataFrame(columns=[
    'speaker', 'text', 'cleaned_text', 'is_question', 'is_exclamation','is_moderator',
    'contains_negation', 'contains_reference', 'contains_agreement',
    'contains_disagreement', 'contains_emotion_words',
    'contains_personal_attack', 'contains_group_identity',
    'contains_emphasis', 'contains_conditional', 'sentence_length'
])


def process_block(new_lines):
    """
    Processes each new block fetched from the real-time processor.
    Args:
        new_lines (list): List of new transcript lines.
    """
    global data

    # Process each new line
    for line in new_lines:
        if ':' in line:  # Ensure valid format
            speaker, text = line.split(':', 1)
            speaker = speaker.strip()
            text = text.strip()

            # Preprocessing
            cleaned_text = cleaner.clean_text(text)

            # Feature tagging
            is_question = cleaner.is_question(cleaned_text)
            is_exclamation = cleaner.is_exclamation(cleaned_text)
            contains_negation = cleaner.contains_negation(cleaned_text)
            contains_reference = cleaner.contains_reference(cleaned_text)
            contains_agreement = cleaner.contains_agreement(cleaned_text)
            contains_disagreement = cleaner.contains_disagreement(cleaned_text)
            contains_emotion_words = cleaner.contains_emotion_words(cleaned_text)
            contains_personal_attack = cleaner.contains_personal_attack(cleaned_text)
            contains_group_identity = cleaner.contains_group_identity(cleaned_text)
            contains_emphasis = cleaner.contains_emphasis(cleaned_text)
            contains_conditional = cleaner.contains_conditional(cleaned_text)
            sentence_length = cleaner.sentence_length(cleaned_text)

            is_moderator = speaker.upper() == loader.moderator

            # Append results to DataFrame
            new_row = {
                'speaker': speaker,
                'text': text,
                'cleaned_text': cleaned_text,
                'is_question': is_question,
                'is_exclamation': is_exclamation,
                'is_moderator': is_moderator,
                'contains_negation': contains_negation,
                'contains_reference': contains_reference,
                'contains_agreement': contains_agreement,
                'contains_disagreement': contains_disagreement,
                'contains_emotion_words': contains_emotion_words,
                'contains_personal_attack': contains_personal_attack,
                'contains_group_identity': contains_group_identity,
                'contains_emphasis': contains_emphasis,
                'contains_conditional': contains_conditional,
                'sentence_length': sentence_length
            }
            data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)

            # Print updates (temporary output before visualizations)
            print(f"[{speaker}] {text}")
            print(f"Features: Question: {is_question}, Exclamation: {is_exclamation}, "
                  f"Negation: {contains_negation}, Reference: {contains_reference}\n")

    # Save updates to CSV (temporary for debugging)
    data.to_csv('/Users/sanjayravindran/Documents/dugree/outputs/processed_transcript_live.csv', index=False)


# Real-time processing loop
import time

print("Real-time processing started. Listening for updates...")
try:
    while True:
        # Fetch new data
        new_lines = processor.fetch_new_data()
        if new_lines:
            process_block(new_lines)  # Send data to processing pipeline
        time.sleep(2)  # Poll every 2 seconds
except KeyboardInterrupt:
    print("Stopped real-time processing.")
