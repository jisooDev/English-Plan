from flask import Blueprint, session, redirect, url_for, render_template , request, Response
import pyrebase

config = {
    "apiKey": "AIzaSyDExn5Hbtc_w4IT2-hUe-VT7XE7OkIT5b8",
    "authDomain": "english-plan-c76bf.firebaseapp.com",
    "databaseURL": "https://english-plan-c76bf.firebaseapp.com",
    "projectId": "english-plan-c76bf",
    "storageBucket": "english-plan-c76bf.appspot.com",
    "messagingSenderId": "806298914847",
    "appId": "1:806298914847:web:7fe7508345e15b62a0452a",
    "measurementId": "G-7PWV72Z2QX"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()