from flask import Flask, render_template, request, jsonify
import speech_recognition as sr

app = Flask(__name__)

recognizer = sr.Recognizer()

@app.route('/')
def index():
    """Render the main webpage."""
    return render_template('index.html')

@app.route('/start-listening', methods=['POST'])
def start_listening():
    """Handle microphone input and return the transcription."""
    try:
        language = request.json.get('language', 'en-US')  # Default to English (US)
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=2)
            print("Listening for speech...")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
            print("Audio captured successfully!")
            text = recognizer.recognize_google(audio, language=language)
            return jsonify({'success': True, 'transcription': text})
    except sr.UnknownValueError:
        return jsonify({'success': False, 'error': 'Could not understand the audio.'})
    except sr.RequestError as e:
        return jsonify({'success': False, 'error': f'Request error: {e}'})
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error: {e}'})

if __name__ == '__main__':
    app.run(debug=True)
