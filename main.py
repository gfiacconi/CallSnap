import streamlit as st
import os
import openai
import pyttsx3
import speech_recognition as sr
import webbrowser
import urllib.parse


os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_completion(prompt, model='gpt-3.5-turbo', temperature=0):

    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]

def compose_email(to_email, subject, body):
    mailto_link = f"mailto:{to_email}?subject={subject}&body={body}"
    return mailto_link

# Definizione della funzione recognize_audio()
def recognize_audio(audio_file):
        
        audio_bytes = audio_file.read()
        r = sr.Recognizer()
        engine = pyttsx3.init()
        
        # Converti l'audio in un oggetto audio di speech_recognition
        audio = sr.AudioData(memoryview(audio_bytes), sample_rate=44100, sample_width=2)
        
        # Splitta il file audio in segmenti di 30 secondi
        audio_segments = split_audio(audio, 30)
        
        # Trascrivi e stampa il testo per ogni segmento
        full_text = ""
        for i, segment in enumerate(audio_segments):
            text = recognize_segment(segment, r)
            st.write(f"Testo segmento {i+1}:")
            st.write(text)
            full_text += text + " "
        
        st.write("Hai detto:")
        st.write(full_text)
        st.write("Registrazione audio avvenuta con successo.")

        prompt = f"""
                 Sei un esperto nella scrittura di email che riassumono le call. Ti viene dato un contenuto delimitato da ```.
                 Leggi il contenuto fornito.
                 Scrivi un'email riassuntiva di questo pezzo di una call per un CDA, scrivi in modo chiaro e preciso usando questa formattazione: 
                 Buongiorno Colleghi
                 [testo]
                 Cordiali saluti
                 PWC
                 Questo è il testo da analizzare
                 ```{full_text}```
                 """

        completion = get_completion(prompt)
        st.write(completion)

        encoded_completion = urllib.parse.quote(completion)
        mailto_link = f"mailto:prova@gmail.com?subject=minutacall&body={encoded_completion}"
        st.markdown(f"[invia]({mailto_link})")
        # Bottone per aprire la pagina di composizione email
        # Componi l'email con il testo generato

# Funzione per splittare il file audio in segmenti di n secondi
def split_audio(audio, segment_duration):
    segment_length = int(audio.sample_rate * segment_duration)
    audio_duration = len(audio.frame_data) / audio.sample_rate
    num_segments = int(audio_duration / segment_duration)
    segments = []
    for i in range(num_segments):
        start = i * segment_length
        end = start + segment_length
        segment = audio.frame_data[start:end]
        segments.append(segment)
    return segments

# Funzione per riconoscere il testo in un segmento audio
def recognize_segment(segment, recognizer):
    audio_segment = sr.AudioData(segment.tobytes(), sample_rate=44100, sample_width=2)
    try:
        text = recognizer.recognize_google(audio_segment, language="it-IT")
        return text
    except Exception as e:
        return "Errore: " + str(e)

# Funzione principale main()
def main():
    # Link "Genera email"
    st.title("CallSnap - Non ascoltare più le tue chiamate")
    st.write("Riassunti delle chiamate direttamente sulla tua email")
    # mailto_link = f"mailto:ciao?subject=ciao&body=ciao"
    # st.markdown(f"[invia]({mailto_link})")
    # Inserimento dell'indirizzo email
    email = st.text_input("Inserisci il tuo indirizzo email")

    # Caricamento del file audio
    audio_file = st.file_uploader("Carica un file audio", type=["mp3", "wav"])

    # Elaborazione del caricamento
    if st.button("Submit") and email and audio_file:
        # Esegui l'elaborazione del caricamento del file audio e l'invio alla email
        st.write("Caricamento in corso...")

        # Chiamata alla funzione recognize_audio()
        recognize_audio(audio_file)


# Esegui la funzione principale main()
if __name__ == "__main__":
    main()
