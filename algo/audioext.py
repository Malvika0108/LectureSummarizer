#This file takes the audio segments and transcribes the audio
from googlesearch import search
import yake
import librosa
from pydub import AudioSegment
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer

def transcription(filename):
    # loading model and tokenizer
    tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
    model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

    # The base model pretrained and fine-tuned on 960 hours of Librispeech on 16kHz sampled speech audio.
    # When using the model make sure that your speech input is also sampled at 16Khz.

    # loading audio file
    mp3_audio = AudioSegment.from_file(filename, format="wav")
    collection_of_text = []

    for i in range(round(len(mp3_audio)/(1000*30))):

        speech, rate = librosa.load(f"{i+1}_{filename}", sr=16000)

        input_values = tokenizer(speech, return_tensors='pt').input_values
        # Store logits (non-normalized predictions)
        with torch.no_grad():
            logits = model(input_values).logits

        # Store predicted id's
        predicted_ids = torch.argmax(logits, dim=-1)

        # decode the audio to generate text
        # Passing the prediction to the tokenzer decode to get the transcription
        transcription = tokenizer.batch_decode(predicted_ids)[0]

        print(transcription)
        collection_of_text.append(transcription)

    print(collection_of_text)
    final_complete_speech = ""
    wordtime = ""

    # convert batch of text into one complete sentence
    for i in collection_of_text:
        final_complete_speech += i.capitalize()
        final_complete_speech += ". "  # transcribed

    # Writing into a file
    file = open("{filename}_op.txt", "w")
    file.write(final_complete_speech)
    file.close()
    return final_complete_speech


# Keyword extraction using Yake
def key_ext_link_rec(filename):
    file = open("{filename}_op.txt")
    final_text = file.read()
    print()

    kw_extractor = yake.KeywordExtractor(top=10, stopwords=None, dedupLim=0.3, n=1)
    keywords = kw_extractor.extract_keywords(final_text)

    # Printing keywords
    query = "KEYWORDS\n"
    keywords = sorted(keywords, key=lambda v: v in keywords, reverse=True)
    for kw, v in keywords:
        query += kw +"\n"
        print(f"Keyphrase: {kw} \t|score: {round(1-v, 3)}")

    print()
    query+="LINKS\n"
    file = open("{filename}_links.txt", "w")
    for j in search(query, tld="com", lang="english", num=10, stop=10, pause=2):
        print(j)
        query+=j+" \n"
        file.write(j+"\n")

    file.close()
    return query
