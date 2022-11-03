#This file cuts an audio segemnt into 30 second clips


def aud_split(filename):
    
    from pydub import AudioSegment  
    mp3_audio = AudioSegment.from_file(filename, format="wav")

    print(len(mp3_audio)/(1000*30))

    counter_audio = 30
    split_audio = [mp3_audio[:30*1000]]
    for i in range(round(len(mp3_audio)/(1000*30))):
        split_audio.append(mp3_audio[counter_audio*1000:(counter_audio+30)*1000])
        counter_audio += 30

    count = 0

    for count, audio_object in enumerate(split_audio):
        count += 1
        with open(f"{count}_{filename}", 'wb') as out_f:
            audio_object.export(out_f, format='wav')

