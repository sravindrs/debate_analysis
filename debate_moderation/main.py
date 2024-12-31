# Import modules
from preprocessing.transcript_loader import TranscriptLoader
from preprocessing.text_cleaner import TextCleaner

# Initialize components
loader = TranscriptLoader()
cleaner = TextCleaner()

# Define file path
file_path = '/Users/sanjayravindran/Documents/dugree/debate_moderation/data/transcript.txt'  # Replace with your path

# Load the transcript
df = loader.load_transcript(file_path)

# Clean text
df['cleaned_text'] = df['text'].apply(cleaner.clean_text)

# Feature tagging
df['is_question'] = df['cleaned_text'].apply(cleaner.is_question)
df['is_exclamation'] = df['cleaned_text'].apply(cleaner.is_exclamation)
df['contains_negation'] = df['cleaned_text'].apply(cleaner.contains_negation)
df['contains_reference'] = df['cleaned_text'].apply(cleaner.contains_reference)

# Additional features
df['contains_agreement'] = df['cleaned_text'].apply(cleaner.contains_agreement)
df['contains_disagreement'] = df['cleaned_text'].apply(cleaner.contains_disagreement)
df['contains_emotion_words'] = df['cleaned_text'].apply(cleaner.contains_emotion_words)
df['contains_personal_attack'] = df['cleaned_text'].apply(cleaner.contains_personal_attack)
df['contains_group_identity'] = df['cleaned_text'].apply(cleaner.contains_group_identity)
df['contains_emphasis'] = df['cleaned_text'].apply(cleaner.contains_emphasis)
df['contains_conditional'] = df['cleaned_text'].apply(cleaner.contains_conditional)
df['sentence_length'] = df['cleaned_text'].apply(cleaner.sentence_length)

# Print results
print(df.head())  # Preview the first 5 rows

# Save processed data to a new CSV for inspection
output_path = '/Users/sanjayravindran/Documents/dugree/outputs/output.csv'
df.to_csv(output_path, index=False)
print(f"Processed data saved to: {output_path}")
