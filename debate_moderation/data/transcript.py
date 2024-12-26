import json

def convert_transcript_to_json(transcript_text):
    transcript_lines = transcript_text.strip().split('\n')
    transcript = []
    
    for line in transcript_lines:
        # Check if line contains the expected structure with "]:" to avoid splitting errors
        if ']: ' not in line or ' [' not in line:
            # Skip any lines that do not fit the expected pattern
            continue
        
        try:
            speaker_info, text = line.split(']: ', 1)
            speaker, time_info = speaker_info.split(' [', 1)
            start_time, end_time = time_info[:-1].split(' - ')
            
            # Append parsed information to the transcript list
            transcript.append({
                "speaker": speaker.strip(),
                "start_time": start_time.strip(),
                "end_time": end_time.strip(),
                "text": text.strip()
            })
        except ValueError:
            # Skip lines that still do not match after basic checks
            continue
    
    transcript_json = {
        "transcript": transcript
    }
    
    return json.dumps(transcript_json, indent=2)

# Reading the transcript from the file
file_path = 'transcript (2).txt'
with open(file_path, 'r', encoding='utf-8') as file:
    transcript_text = file.read()

# Converting the transcript to JSON
transcript_json = convert_transcript_to_json(transcript_text)

# Saving the resulting JSON to a new file
output_file_path = 'transcript.json'
with open(output_file_path, 'w', encoding='utf-8') as json_file:
    json_file.write(transcript_json)

print("Transcript successfully converted and saved as 'transcript.json'")
