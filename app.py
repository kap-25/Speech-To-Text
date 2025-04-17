from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import sounddevice as sd
import soundfile as sf
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure upload folder for temporary audio files
UPLOAD_FOLDER = 'temp_audio'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

recognizer = sr.Recognizer()

@app.route('/')
def index():
    """Render the main webpage."""
    return render_template('index.html')

@app.route('/start-listening', methods=['POST'])
def start_listening():
    """Handle microphone input and return the transcription."""
    try:
        language = request.json.get('language', 'en-US')
        samplerate = 16000  # Standard sample rate for speech recognition
        duration = 10  # Maximum recording duration in seconds
        channels = 1  # Mono audio

        print(f"Starting recording for {duration} seconds...")
        
        # Record audio
        audio = sd.rec(int(duration * samplerate),
                      samplerate=samplerate,
                      channels=channels,
                      dtype='float32')
        sd.wait()  # Wait until recording is finished

        # Save to temporary file
        temp_filename = secure_filename("recording.wav")
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], temp_filename)
        sf.write(temp_path, audio, samplerate)

        # Process audio with SpeechRecognition
        with sr.AudioFile(temp_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language=language)

        # Clean up temporary file
        os.remove(temp_path)

        return jsonify({
            'success': True,
            'transcription': text,
            'sample_rate': samplerate,
            'duration': duration
        })

    except sr.UnknownValueError:
        return jsonify({'success': False, 'error': 'Could not understand audio'})
    except sr.RequestError as e:
        return jsonify({'success': False, 'error': f'API unavailable: {str(e)}'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)