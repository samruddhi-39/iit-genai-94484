import os
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()

api_key=os.getenv("GROQ_API_KEY")
url="https://api.groq.com/openai/v1/chat/completions"
headers={
    "Authorization":f"Bearer {api_key}",
    "Content-Type":"application/json"
}

gemini_api_key=os.getenv("GEMINI_API_KEY")
gemini_url="https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
gemini_headers={
    "Authorization":f"Bearer {gemini_api_key}",
    "Content-Type":"application/json"
}

user_prompt=input("Ask anything:\n")

groq_data={
    "model":"llama-3.3-70b-versatile",
    "messages":[
        {"role":"user","content":user_prompt}
    ]
}

gemini_data={
    "model":"gemini-2.5-flash",
    "messages":[
        {"role":"user","content":user_prompt}
    ]
}

t1_start=time.perf_counter()
r1=requests.post(url,headers=headers,json=groq_data)
t1_end=time.perf_counter()
t1=t1_end-t1_start

t2_start=time.perf_counter()
r2=requests.post(gemini_url,headers=gemini_headers,json=gemini_data)
t2_end=time.perf_counter()
t2=t2_end-t2_start

print("Groq Status:",r1.status_code)

if r1.status_code==200:
    print("Groq Answer:",r1.json()["choices"][0]["message"]["content"])
else:
    print("Groq Answer: Service unavailable")

print("Groq Response Time:",t1,"seconds")
print("\n")

print("Gemini Status:",r2.status_code)

if r2.status_code==200:
    print("Gemini Answer:",r2.json()["choices"][0]["message"]["content"])
else:
    print("Gemini Answer: Service unavailable")

print("Gemini Response Time:",t2,"seconds")
print("\n")

print("Groq vs Gemini Speed Comparison:")
print("Groq:",t1,"sec")
print("Gemini:",t2,"sec")
print("\n")

if t1<t2:
    print("Groq was faster")
elif t2<t1:
    print("Gemini was faster")
else:
    print("Both took the same time")