from dotenv import load_dotenv
import os
import tweepy

# .env dosyasını yükle
load_dotenv()

# API anahtarlarını yükle
API_KEY = os.getenv("API_KEY")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# Tweepy ile kimlik doğrulama
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Tweet gönderme
tweet = "Sonsuza kadar yaşamak istemiyoruz, hiç istemedik. Sonsuza kadar yaşamak isteyeceğimiz anlar yaşamak istiyoruz. Murat AVCIOĞLU"
try:
    api.update_status(tweet)
    print("Tweet başarıyla gönderildi!")
except Exception as e:
    print("Tweet gönderilirken bir hata oluştu:", e)
