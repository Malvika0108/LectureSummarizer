
from sumy.summarizers.lsa import LsaSummarizer
import nltk
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from pydub import AudioSegment
from googlesearch import search
import yake
import librosa
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
#import audiosplit as asp
#import audioext as ae
#mport summarizer as sm

# This file cuts an audio segemnt into 30 second clips


def aud_split(filename):

    from pydub import AudioSegment
    mp3_audio = AudioSegment.from_file(filename, format="wav")

    print(len(mp3_audio)/(1000*30))

    counter_audio = 30
    split_audio = [mp3_audio[:30*1000]]
    for i in range(round(len(mp3_audio)/(1000*30))):
        split_audio.append(
            mp3_audio[counter_audio*1000:(counter_audio+30)*1000])
        counter_audio += 30

    count = 0

    for count, audio_object in enumerate(split_audio):
        count += 1
        with open(f"{filename}{count}.wav", 'wb') as out_f:
            audio_object.export(out_f, format='wav')


# This file takes the audio segments and transcribes the audio


def transcription(filename):
    # loading model and tokenizer
    tokenizer = Wav2Vec2Tokenizer.from_pretrained(
        "facebook/wav2vec2-base-960h")
    model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

    # The base model pretrained and fine-tuned on 960 hours of Librispeech on 16kHz sampled speech audio.
    # When using the model make sure that your speech input is also sampled at 16Khz.

    # loading audio file
    mp3_audio = AudioSegment.from_file(filename, format="wav")
    collection_of_text = []

    for i in range(round(len(mp3_audio)/(1000*30))):

        speech, rate = librosa.load(f"{filename}{i+1}.wav", sr=16000)

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
        i.capitalize()
        final_complete_speech += i
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

    kw_extractor = yake.KeywordExtractor(
        top=10, stopwords=None, dedupLim=0.3, n=1)
    keywords = kw_extractor.extract_keywords(final_text)

    # Printing keywords
    query = ""
    keywords = sorted(keywords, key=lambda v: v in keywords, reverse=True)
    for kw, v in keywords:
        query += kw + "\n"
        print(f"Keyphrase: {kw} \t|score: {round(1-v, 3)}")

    print()
    links = "LINKS\n"
    file = open("{filename}_links.txt", "w")
    for j in search(query, tld="com", lang="english", num=10, stop=10, pause=2):
        print(j)
        links += j+" \n"
        file.write(j+"\n")

    file.close()
    return [query,links]


def summarizer(filename):
    # Text to summarize
    f = open("{filename}_op.txt", "r")
    #original_text = 'Junk foods taste good that’s why it is mostly liked by everyone of any age group especially kids and school going children. They generally ask for the junk food daily because they have been trend so by their parents from the childhood. They never have been discussed by their parents about the harmful effects of junk foods over health. According to the research by scientists, it has been found that junk foods have negative effects on the health in many ways. They are generally fried food found in the market in the packets. They become high in calories, high in cholesterol, low in healthy nutrients, high in sodium mineral, high in sugar, starch, unhealthy fat, lack of protein and lack of dietary fibers. Processed and junk foods are the means of rapid and unhealthy weight gain and negatively impact the whole body throughout the life. It makes able a person to gain excessive weight which is called as obesity. Junk foods tastes good and looks good however do not fulfil the healthy calorie requirement of the body. Some of the foods like french fries, fried foods, pizza, burgers, candy, soft drinks, baked goods, ice cream, cookies, etc are the example of high-sugar and high-fat containing foods. It is found according to the Centres for Disease Control and Prevention that Kids and children eating junk food are more prone to the type-2 diabetes. In type-2 diabetes our body become unable to regulate blood sugar level. Risk of getting this disease is increasing as one become more obese or overweight. It increases the risk of kidney failure. Eating junk food daily lead us to the nutritional deficiencies in the body because it is lack of essential nutrients, vitamins, iron, minerals and dietary fibers. It increases risk of cardiovascular diseases because it is rich in saturated fat, sodium and bad cholesterol. High sodium and bad cholesterol diet increases blood pressure and overloads the heart functioning. One who like junk food develop more risk to put on extra weight and become fatter and unhealthier. Junk foods contain high level carbohydrate which spike blood sugar level and make person more lethargic, sleepy and less active and alert. Reflexes and senses of the people eating this food become dull day by day thus they live more sedentary life. Junk foods are the source of constipation and other disease like diabetes, heart ailments, clogged arteries, heart attack, strokes, etc because of being poor in nutrition. Junk food is the easiest way to gain unhealthy weight. The amount of fats and sugar in the food makes you gain weight rapidly. However, this is not a healthy weight. It is more of fats and cholesterol which will have a harmful impact on your health. Junk food is also one of the main reasons for the increase in obesity nowadays.This food only looks and tastes good, other than that, it has no positive points. The amount of calorie your body requires to stay fit is not fulfilled by this food. For instance, foods like French fries, burgers, candy, and cookies, all have high amounts of sugar and fats. Therefore, this can result in long-term illnesses like diabetes and high blood pressure. This may also result in kidney failure. Above all, you can get various nutritional deficiencies when you don’t consume the essential nutrients, vitamins, minerals and more. You become prone to cardiovascular diseases due to the consumption of bad cholesterol and fat plus sodium. In other words, all this interferes with the functioning of your heart. Furthermore, junk food contains a higher level of carbohydrates. It will instantly spike your blood sugar levels. This will result in lethargy, inactiveness, and sleepiness. A person reflex becomes dull overtime and they lead an inactive life. To make things worse, junk food also clogs your arteries and increases the risk of a heart attack. Therefore, it must be avoided at the first instance to save your life from becoming ruined.The main problem with junk food is that people don’t realize its ill effects now. When the time comes, it is too late. Most importantly, the issue is that it does not impact you instantly. It works on your overtime; you will face the consequences sooner or later. Thus, it is better to stop now.You can avoid junk food by encouraging your children from an early age to eat green vegetables. Their taste buds must be developed as such that they find healthy food tasty. Moreover, try to mix things up. Do not serve the same green vegetable daily in the same style. Incorporate different types of healthy food in their diet following different recipes. This will help them to try foods at home rather than being attracted to junk food.In short, do not deprive them completely of it as that will not help. Children will find one way or the other to have it. Make sure you give them junk food in limited quantities and at healthy periods of time. '
    nltk.download('punkt')  # Parsing the text string using PlaintextParser
    parser = PlaintextParser.from_string(
        f.read().lower(), Tokenizer('english'))

    # creating the summarizer
    lsa_summarizer = LsaSummarizer()
    lsa_summary = lsa_summarizer(parser.document, 10)
    
    summary = ""
    print("summary")
    # Printing the summary
    for sentence in lsa_summary:
        print(str(sentence))
        summary += (str(sentence).capitalize())

    return summary

def map(filename):
    aud_split(filename)
    final_speech = transcription(filename)
    links = key_ext_link_rec(filename)
    summary = summarizer(filename)
    op = str(summary)+"\n"+str(links)

    return op

# map("adio.wav")