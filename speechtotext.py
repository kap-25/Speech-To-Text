import speech_recognition as sr
import nltk
from nltk.tokenize import word_tokenize
import sounddevice as sd
import soundfile as sf
import os

# Download required NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def initialize_recognizer():
    """Initialize the speech recognizer."""
    return sr.Recognizer()

def capture_audio(recognizer, samplerate=16000, duration=10):
    """Capture live audio using sounddevice."""
    try:
        print("\nStarting recording... Speak now!")
        audio = sd.rec(int(duration * samplerate),
                       samplerate=samplerate,
                       channels=1,
                       dtype='float32')
        sd.wait()  # Wait until recording is finished
        
        # Save to temporary file
        temp_file = "temp_recording.wav"
        sf.write(temp_file, audio, samplerate)
        
        # Load with SpeechRecognition
        with sr.AudioFile(temp_file) as source:
            print("Processing audio...")
            audio_data = recognizer.record(source)
        
        # Clean up
        os.remove(temp_file)
        return audio_data
        
    except Exception as e:
        print(f"Error capturing audio: {e}")
        return None

def speech_to_text(recognizer, audio):
    """Convert audio to text using Google Speech Recognition."""
    if audio is None:
        return None
    try:
        text = recognizer.recognize_google(audio)
        print("\nTranscription:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results: {e}")
        return None

def apply_pos_tagging(text):
    """Apply POS tagging to the transcribed text."""
    if text is None:
        return None
    try:
        tokens = word_tokenize(text)
        pos_tags = nltk.pos_tag(tokens)
        return pos_tags
    except Exception as e:
        print(f"Error during POS tagging: {e}")
        return None

def format_pos_output(pos_tags):
    """Format the POS tagged output for readability."""
    if pos_tags is None:
        return "No POS tags available."
    
    tag_descriptions = {
        'NN': 'Noun, singular',
        'NNS': 'Noun, plural',
        'VB': 'Verb, base form',
        'VBD': 'Verb, past tense',
        'VBG': 'Verb, gerund/present participle',
        'VBN': 'Verb, past participle',
        'VBP': 'Verb, non-3rd person singular present',
        'VBZ': 'Verb, 3rd person singular present',
        'JJ': 'Adjective',
        'RB': 'Adverb',
        'IN': 'Preposition',
        'DT': 'Determiner',
        'PRP': 'Personal pronoun',
        'CC': 'Coordinating conjunction'
    }
    
    formatted_output = "\nPOS Tagging Results:\n"
    formatted_output += "-" * 50 + "\n"
    formatted_output += f"{'Word':<20} {'POS Tag':<10} {'Description'}\n"
    formatted_output += "-" * 50 + "\n"
    
    for word, tag in pos_tags:
        description = tag_descriptions.get(tag, 'Other')
        formatted_output += f"{word:<20} {tag:<10} {description}\n"
    
    return formatted_output

def main():
    """Main function to run the speech-to-text system with POS tagging."""
    recognizer = initialize_recognizer()
    
    print("Speech-to-Text System with POS Tagging")
    print("Speak clearly into your microphone. Say 'exit' to quit.")
    
    while True:
        audio = capture_audio(recognizer)
        
        if audio is None:
            continue
        
        text = speech_to_text(recognizer, audio)
        
        if text and text.lower().strip() == 'exit':
            print("Exiting program.")
            break
            
        pos_tags = apply_pos_tagging(text)
        if pos_tags:
            print(format_pos_output(pos_tags))

if __name__ == "__main__":
    main()