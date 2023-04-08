from flask import Blueprint, session, redirect, url_for, render_template , request, Response
import pyrebase
import uuid
import base64
import query_helper as query
import json

btoa = lambda x:base64.b64decode(x)
atob = lambda x:base64.b64encode(bytes(x, 'utf-8')).decode('utf-8')

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

config_delete = {
    "apiKey": "AIzaSyDExn5Hbtc_w4IT2-hUe-VT7XE7OkIT5b8",
    "authDomain": "english-plan-c76bf.firebaseapp.com",
    "databaseURL": "https://english-plan-c76bf.firebaseapp.com",
    "projectId": "english-plan-c76bf",
    "storageBucket": "english-plan-c76bf.appspot.com",
    "messagingSenderId": "806298914847",
    "appId": "1:806298914847:web:7fe7508345e15b62a0452a",
    "measurementId": "G-7PWV72Z2QX",
    "serviceAccount" : "english-plan-c76bf-firebase-adminsdk-jk00w-35492bfa0f.json"
}

firebase_delete = pyrebase.initialize_app(config_delete)
storage_delete = firebase_delete.storage()