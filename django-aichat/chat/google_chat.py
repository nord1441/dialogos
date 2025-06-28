from google import genai
from google.genai import types
import os
import subprocess
import json
import pathlib
from .models import ChatModel, ChatHistory

vars = {
  "gemini_api_key": "",
  "dialogue_num_limit": 0,
  "gemini_model": ""
}

def read_env(identifier):
  if(len(identifier)!=0):
    prefix = identifier + "_"
  else:
    prefix = ""
  vars["dialogue_num_limit"] = int(os.getenv(prefix + "DIALOGUE_NUM_LIMIT", default=5))
  vars["gemini_api_key"] = os.getenv(prefix + "GEMINI_API_KEY", default="")
  vars["gemini_model"] = os.getenv(prefix + "GEMINI_MODEL", default="gemini-2.0-flash")

read_env("DJANGO_AICHAT")
client = genai.Client(
  api_key=vars["gemini_api_key"]
)
def chat(input, thread, session_id):
  if len(thread) == 0:
    chatModel = ChatModel.objects.order_by('-id').first()
    thread.append({"role":"system", "content":chatModel.system_dialogue})
    # Save system message
    ChatHistory.objects.create(session_id=session_id, role="system", content=chatModel.system_dialogue)
    global googlechat
    googlechat = client.chats.create(
      model=vars["gemini_model"],
      config=types.GenerateContentConfig(
        system_instruction=chatModel.system_dialogue,
      )
    )
  dialogue_content = input
  thread.append({"role": "user", "content": dialogue_content})
  # Save user message
  ChatHistory.objects.create(session_id=session_id, role="user", content=dialogue_content)
  chat_completion = googlechat.send_message(dialogue_content)
  thread.append({'role': 'assistant','content': chat_completion.text})
  # Save assistant message
  ChatHistory.objects.create(session_id=session_id, role="assistant", content=chat_completion.text)
  if((len(thread)-1)/2 == vars["dialogue_num_limit"]+1):
    del thread[1:3]
  return chat_completion.text
