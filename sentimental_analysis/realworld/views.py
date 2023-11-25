# MIT License

# Copyright (c) 2020 Sharath Bangalore Ramesh Kumar
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import sys
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from django.template.defaulttags import register
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from .utilityFunctions import *
import os
from moviepy.editor import VideoFileClip
import subprocess
import json
import speech_recognition as sr
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import cv2
import tensorflow as tf
from moviepy.editor import VideoFileClip
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np
from werkzeug.utils import secure_filename
from .video import pred, removeout, vidframe, ssimscore1
from matplotlib import pyplot as plt
import io
import base64
import urllib
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage

# Determine the base directory(SE_Project1) of your project
result = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'])
base_directory = result.decode('utf-8').strip()

def pdfparser(data):


    fp = open(data, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        data =  retstr.getvalue()

    text_file = open("Output.txt", "w", encoding="utf-8")
    text_file.write(data)

    text_file = open("Output.txt",'r', encoding="utf-8")
    a = ""
    for x in text_file:
            if len(x)>2:
                b = x.split()
                for i in b:
                    a+=" "+i
    final_comment = a.split('.')
    return final_comment

def analysis(request):
    return render(request,'realworld/index.html')

def get_clean_text(text):
    text = removeLinks(text)
    text = stripEmojis(text)
    text = removeSpecialChar(text)
    text = stripPunctuations(text)
    text = stripExtraWhiteSpaces(text)

    #Tokenize using nltk
    try:
        nltk.data.find('corpora/stopwords.zip')
    except LookupError:
        nltk.download('stopwords')
    tokens = nltk.word_tokenize(text)

    #Import stopwords
    stop_words = set(stopwords.words('english'))
    stop_words.add('rt')
    stop_words.add('')
    
    #Remove tokens which are in stop_words
    newtokens = [item for item in tokens if item not in stop_words]

    textclean = ' '.join(newtokens)
    return textclean

def detailed_analysis(result):
    result_dict = {}
    neg_count = 0
    pos_count = 0
    neu_count = 0
    total_count = len(result)

    for item in result:
        print(item)
        cleantext = get_clean_text(str(item))
        print(cleantext)
        sentiment = sentiment_scores(cleantext)
        print(sentiment)
        compound_score = sentiment['compound']

        pos_count += sentiment['pos']
        neu_count += sentiment['neu']
        neg_count += sentiment['neg']
    
    total = pos_count + neu_count + neg_count
    result_dict['pos'] = (pos_count/total)
    result_dict['neu'] = (neu_count/total)
    result_dict['neg'] = (neg_count/total)

    return result_dict

def detailed_analysis2(sentiment_score):
    result_dict = {}
    neg_count = 0
    pos_count = 0
    neu_count = 0
    if sentiment_score>0:
        result_dict['pos'] = 100*sentiment_score
        result_dict['neu'] = 100-(100*sentiment_score)
        result_dict['neg'] = 0
    elif sentiment_score<0:
        result_dict['pos'] = 0
        result_dict['neu'] = 100-(100*abs(sentiment_score))
        result_dict['neg'] = 100 * abs(sentiment_score)
    elif sentiment_score==0:
        result_dict['pos'] = 0
        result_dict['neu'] = 100
        result_dict['neg'] = 0

    return result_dict

def detailed_analysis3(pos,neu,neg):
    result_dict = {}
    result_dict['pos']=pos
    result_dict['neu']=neu
    result_dict['neg']=neg
    return result_dict


def input(request):
    if request.method=='POST':
        file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(file.name,file)
        pathname = "media/"
        extension_name = file.name
        extension_name = extension_name[len(extension_name)-3:]
        path = pathname+file.name
        result = {}
        if extension_name == 'pdf':
            value = pdfparser(path)
            result = detailed_analysis(value)
        elif extension_name == 'txt':
            text_file = open(path, 'r', encoding="utf-8")
            a = ""
            for x in text_file:
                if len(x) > 2:
                    b = x.split()
                    for i in b:
                        a += " " + i
            final_comment = a.split('.')
            result = detailed_analysis(final_comment)
        elif extension_name=='wav':
            r = sr.Recognizer()
            with sr.AudioFile(path) as source:
                # listen for the data (load audio to memory)
                audio_data = r.record(source)
                # recognize (convert from speech to text)
                text = r.recognize_google(audio_data)
                value = text.split('.')
                result = detailed_analysis(value)
        # Sentiment Analysis

        os.system(f'cd {os.path.join(base_directory, "sentimental_analysis/media/")} && rm -rf *')
        return render(request, 'realworld/sentiment_graph.html', {'sentiment': result})
    else:
        note = "Please insert the document you want to analyze"
        return render(request, 'realworld/home.html', {'note': note})

def productanalysis(request):
    if request.method == 'POST':
        blogname = request.POST.get("blogname", "")

        # text_file = open(
        #     "D:/All Documents/Documents/2. Pro documents/Nokia final/Documents/MS/5. Universities/1. Done/NCSU/SE/project/SE_Project1/Amazon_Comments_Scrapper/amazon_reviews_scraping/amazon_reviews_scraping/spiders/ProductAnalysis.txt",
        #     "w")
        # text_file.write(blogname)
        # text_file.close()
        os.system(
            f'scrapy runspider {os.path.join(base_directory, "Amazon_Comments_Scrapper/amazon_reviews_scraping/amazon_reviews_scraping/spiders/amazon_review.py")} -o reviews.json')
        final_comment = []        
        with open(os.path.join(base_directory, "sentimental_analysis/reviews.json")) as json_file:
            data = json.load(json_file)
            for p in range(1, len(data) - 1):
                a = data[p]['comment']
                final_comment.append(a)

        # final_comment is a list of strings!
        result = detailed_analysis(final_comment)
        print(result)
        return render(request, 'realworld/sentiment_graph.html', {'sentiment': result})

    else:
        note = "Please enter the product blog link for analysis"
        return render(request, 'realworld/productanalysis.html', {'note': note})

# Custom template filter to retrieve a dictionary value by key.


def textanalysis(request):
    if request.method == 'POST':
        text = request.POST.get("Text", "")
        blob = TextBlob(text)

        # Split the text into sentences
        sentences = blob.sentences
        results=[]
        positive_score=0
        negative_score=0
        neutral_score=0

        for sentence in sentences:
            sentiment_polarity = sentence.sentiment.polarity

            # Determine sentiment based on polarity
            if sentiment_polarity > 0:
                sentiment = "positive"
            elif sentiment_polarity < 0:
                sentiment = "negative"
            else:
                sentiment = "neutral"

            # Calculate separate positive, negative, and neutral scores
            positive_score += max(0, sentiment_polarity)
            negative_score += max(0, -sentiment_polarity)
            neutral_score += (1 - positive_score - negative_score)

        # You can return or use the 'results' list as needed
        result = detailed_analysis3(positive_score, neutral_score, negative_score)
        return render(request, 'realworld/sentiment_graph.html', {'sentiment': result})
    else:
        note = "Enter the text to be analyzed!"
        return render(request, 'realworld/textanalysis.html', {'note': note})


def tweetanalysis(request):
    if request.method == 'POST':
        tweetlink = request.POST.get("tweetlink", "")
        response = requests.get(tweetlink)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            webpage_text = ' '.join([p.get_text() for p in soup.find_all('p')])
            blob = TextBlob(webpage_text)
            sentiment_score = blob.sentiment.polarity
            if sentiment_score > 0:
                sentiment = "positive"
            elif sentiment_score < 0:
                sentiment = "negative"
            else:
                sentiment = "neutral"
        print("Webpage Analysis:")
        result = detailed_analysis2(sentiment_score)
        print(result)
        return render(request, 'realworld/sentiment_graph.html', {'sentiment': result})
    else:
        note = "Enter the tweet url to be analysed!"
        return render(request, 'realworld/tweetanalysis.html', {'note': note})



def imageanalysis(request):
    note = "Please add the image to be analysed"
    if request.method == 'POST':
        imgfile = request.FILES['imgfile']
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = CLIPModel.from_pretrained("openai/clip-vit-base-patch16")
        processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch16")
        image = Image.open(imgfile)
        text = ["a happy image", "a sad image", "a joyful image"]
        inputs = processor(text, images=image, return_tensors="pt", padding=True)
        inputs = {k: v.to(device) for k, v in inputs.items()}
        with torch.no_grad():
            image_features = model.get_image_features(pixel_values=inputs['pixel_values'])
            text_features = model.get_text_features(input_ids=inputs['input_ids'])
        similarity_scores = (image_features @ text_features.T).squeeze(0)
        positive_score = similarity_scores[0].item()
        negative_score = similarity_scores[1].item()
        neutral_score = similarity_scores[2].item()
        if positive_score > negative_score and positive_score > neutral_score:
            sentiment = "Positive"
        elif negative_score > positive_score and negative_score > neutral_score:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        print(f"Sentiment: {sentiment}")
        print(f"Positive Score: {positive_score}")
        print(f"Negative Score: {negative_score}")
        print(f"Neutral Score: {neutral_score}")
        result = detailed_analysis3(positive_score,neutral_score, negative_score)
        return render(request, 'realworld/sentiment_graph.html', {'sentiment': result})
    else:
        note = "Insert the image to be analysed!"
        return render(request, 'realworld/imageanalysis.html', {'note': note})


def audioanalysis(request):
    if request.method == 'POST':
        file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(file.name,file)
        pathname = "media/"
        extension_name = file.name
        extension_name = extension_name[len(extension_name)-3:]
        path = pathname+file.name
        result = {}
        print(path)
        text = speech_to_text(path)
        result = sentiment_analyzer_scores(text)
        print("Result")
        print(result)
        # Sentiment Analysis
        os.system(f'cd {os.path.join(base_directory, "sentimental_analysis/media/")} && rm -rf *')
        return render(request, 'realworld/sentiment_graph.html', {'sentiment': result})
    else:
        note = "Please enter the audio file you want to analyze"
        return render(request, 'realworld/audio.html', {'note': note})

def eateryanalysis(request):
    if request.method == 'POST':
        blogname = request.POST.get("blogname", "")

        # text_file = open(
        #     "D:/All Documents/Documents/2. Pro documents/Nokia final/Documents/MS/5. Universities/1. Done/NCSU/SE/project/SE_Project1/Amazon_Comments_Scrapper/amazon_reviews_scraping/amazon_reviews_scraping/spiders/ProductAnalysis.txt",
        #     "w")
        # text_file.write(blogname)
        # text_file.close()
        os.system(
            f'scrapy runspider {os.path.join(base_directory, "Amazon_Comments_Scrapper/amazon_reviews_scraping/amazon_reviews_scraping/spiders/amazon_review.py")} -o reviews.json')
        final_comment = []        
        with open(os.path.join(base_directory, "sentimental_analysis/reviews.json")) as json_file:
            data = json.load(json_file)
            for p in range(1, len(data) - 1):
                a = data[p]['comment']
                final_comment.append(a)

        # final_comment is a list of strings!
        result = detailed_analysis(final_comment)
        print(result)
        return render(request, 'realworld/sentiment_graph.html', {'sentiment': result})

    else:
        note = "Please enter the restaurant review link for analysis"
        return render(request, 'realworld/eateryanalysis.html', {'note': note})

def speech_to_text(filename):
    r = sr.Recognizer()

    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
        print("TExt")
        print(text)
        return text

def sentiment_analyzer_scores(sentence):
    analyser = SentimentIntensityAnalyzer()
    print("Scores analysed")
    score = analyser.polarity_scores(sentence)
    # print("{:-<40} {}".format(sentence, str(score)))
    return score



def videoanalysis(request):
    if request.method == 'POST':

        f = request.FILES['video']  #getting uploaded video 
        # print(f)
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'uploads', secure_filename(f.name))
        fs = FileSystemStorage(location=os.path.join(basepath, 'uploads'))
        fs.save(f.name, f)
        # file_name = default_storage.save(file_path, f)

        result, face = vidframe(file_path) #running vidframe with the uploaded video
        os.remove(file_path)  #removing the video as we dont need it anymore

        try:
            smileindex=result.count('happy')/len(result)  #smileIndex
            smileindex=round(smileindex,2)

        except:
            smileindex=0

        ssimscore=[ssimscore1(i,j) for i, j in zip(face[: -1],face[1 :])]  # calculating similarityscore for images
        if np.mean(ssimscore)<0.6:
            posture="Not Good"
        else:
            posture="Good"
        fig = plt.figure()     #matplotlib plot
        ax = fig.add_axes([0,0,1,1])
        ax.axis('equal')
        emotion = ['angry','disgust','fear', 'happy', 'sad']
        counts = [result.count('angry'),result.count('disgust'),result.count('fear'),result.count('happy'),result.count('sad')]
        res_dict = {}
        for i in range(len(emotion)):
            res_dict[emotion[i]] = int(counts[i])
        total_value = 0
        for i in res_dict:
            total_value += res_dict[i]
        for i in res_dict:
            res_dict[i] = res_dict[i]/total_value
        ax.pie(counts, labels = emotion,autopct='%1.2f%%')   #adding pie chart
        img = io.BytesIO()
        plt.savefig(img, format='png')   #saving piechart
        img.seek(0)
        plot_data = urllib.parse.quote(base64.b64encode(img.read()).decode()) #piechart object that can be returned to the html
        return render(request, "realworld/videoprediction.html", {'posture': posture, 'smileindex': smileindex, 'plot_url': plot_data, 'sentiment': res_dict}) #returning all the three variable that can be displayed in html
    else:
        note = "Please enter the video file you want to analyze"
        return render(request, 'realworld/videoanalysis.html', {'note': note})


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key, 0)
