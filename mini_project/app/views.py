from django.shortcuts import render, redirect
from django.contrib.auth.models import User,auth
import numpy as np
import tensorflow as tf
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from .models import *
from django.contrib.auth.models import User,auth
from django.contrib import messages
from werkzeug.utils import secure_filename
import statistics as st

# Create your views here.
def index(request):
    return render(request,'index1.html')
    
def try1(request):
    return render(request,'try.html')

def logout(request):
    auth.logout(request)
    return redirect("/")

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect("/")
        else:
            messages.info(request,'Invalid credentials')
            return redirect('login')
    else:
        return render(request,'login.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username already taken!')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
                messages.info(request,'User Created!')
                return redirect("/")
        else:
            messages.info(request,'Passwords do not match')
            return render(request,'signup.html')

    else:  
        return render(request,'signup.html')


def camera():
    i=0
    GR_dict={0:(0,255,0),1:(0,0,255)}
    model = tf.keras.models.load_model('app/final_model.h5')
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    output=[]
    cap = cv2.VideoCapture(0)
    while (i<=30):
        ret, img = cap.read()
        faces = face_cascade.detectMultiScale(img,1.05,5)

        for x,y,w,h in faces:

            face_img = img[y:y+h,x:x+w] 

            resized = cv2.resize(face_img,(224,224))
            reshaped=resized.reshape(1, 224,224,3)/255
            predictions = model.predict(reshaped)

            max_index = np.argmax(predictions[0])

            emotions = ('Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Neutral', 'Surprise')
            predicted_emotion = emotions[max_index]
            output.append(predicted_emotion)

            cv2.rectangle(img,(x,y),(x+w,y+h),GR_dict[1],2)
            cv2.rectangle(img,(x,y-40),(x+w,y),GR_dict[1],-1)
            cv2.putText(img, predicted_emotion, (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
        i = i+1

        cv2.imshow('LIVE', img)
        key = cv2.waitKey(1)
        if key == 27: 
            cap.release()
            cv2.destroyAllWindows()
            break
    print(output)
    cap.release()
    cv2.destroyAllWindows()
    final_output1 = st.mode(output)
    return final_output1


def emotion(request):
    if request.user.is_authenticated:
        print(request.user.id)
        user = User.objects.get(id=request.user.id)
        final_output1 = camera()
        emotions = Emotion.objects.filter(name=final_output1)
        emotion = emotions[0]
        emotion1 = str(emotion)
        if emotion == "":
            messages.info(request,'No Emotion Detected!')
            return redirect("/")
        else:
            user_emotion= UserEmotion.objects.create(user=user,emotion=emotion1)
            user_emotion.save()
        emotion_id = emotion.id
        return render(request,'emotion.html',{"emotion_id":emotion_id, "emotion":emotion})
    else:
        return redirect("/")


def movie(request,id):
    if request.user.is_authenticated:
        movies = Movie.objects.filter(genre=id)
        print(movies[0].genre)
        movie_genre = movies[0].genre
        return render(request,'movies.html',{"movies":movies,"movie_genre":movie_genre})
    else:
        return redirect("/")


def song(request,id):
    if request.user.is_authenticated:
        songs = Song.objects.filter(genre=id)
        print(songs[0].genre)
        song_genre = songs[0].genre
        return render(request,'songs1.html',{"songs":songs,"song_genre":song_genre})
    else:
        return redirect("/")