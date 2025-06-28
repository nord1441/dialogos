from openai import OpenAI
import os
import subprocess
import json
import pathlib
from .models import ChatModel, ChatHistory

vars = {
  "openai_api_key": "",
  "dialogue_num_limit": 0,
  "openai_gpt_model": ""
}

def read_env(identifier):
  if(len(identifier)!=0):
    prefix = identifier + "_"
  else:
    prefix = ""
  vars["dialogue_num_limit"] = int(os.getenv(prefix + "DIALOGUE_NUM_LIMIT", default=5))
  vars["openai_api_key"] = os.getenv(prefix + "OPENAI_API_KEY", default="")
  vars["openai_gpt_model"] = os.getenv(prefix + "OPENAI_GPT_MODEL", default="gpt-4o-mini")

read_env("DJANGO_AICHAT")
client = OpenAI(
    api_key = vars["openai_api_key"]
)
def chat(input, thread, session_id):
  if len(thread) == 0:
    chatModel = ChatModel.objects.order_by('-id').first()
    thread.append({"role":"system", "content":chatModel.system_dialogue})
    # Save system message
    ChatHistory.objects.create(session_id=session_id, role="system", content=chatModel.system_dialogue)
  dialogue_content = input
  thread.append({"role": "user", "content": dialogue_content})
  # Save user message
  ChatHistory.objects.create(session_id=session_id, role="user", content=dialogue_content)
  chat_completion = client.chat.completions.create(model = vars["openai_gpt_model"],messages = thread)
  thread.append({'role': 'assistant','content': chat_completion.choices[0].message.content})
  # Save assistant message
  ChatHistory.objects.create(session_id=session_id, role="assistant", content=chat_completion.choices[0].message.content)
  if((len(thread)-1)/2 == vars["dialogue_num_limit"]+1):
    del thread[1:3]
  return chat_completion.choices[0].message.content
