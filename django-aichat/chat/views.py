from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import ChatForm
from . import openai_chat
from django.shortcuts import redirect
from .models import ChatModel
from .forms import SettingsForm
from .forms import CharaimageModelForm
from .models import CharaimageModel
from django.db.models import Count

global chat
chat = []
global thread
thread = []
def transmit_dialogue(request):
  if not request.user.is_authenticated:
    return redirect(f"login/?next={request.path}")
  else:
    print(ChatModel.objects.count())
    if CharaimageModel.objects.count() == 0:
      return redirect("change_charaimage/")
    if ChatModel.objects.count() == 0:
      return redirect("settings/")
    charaimageModel = CharaimageModel.objects.order_by('-id').first()
    charaimage = charaimageModel.charaimage
    chatModel = ChatModel.objects.order_by('-id').first()
    name = chatModel.name
    if request.method == "POST":
        form = ChatForm(request.POST)
        if form.is_valid():
            user_dialogue = form.cleaned_data.get('user_dialogue')
            assistant_dialogue = openai_chat.chat(user_dialogue, thread)
            if len(chat) == 10:
              del chat[:2]
            chat.append(user_dialogue)
            chat.append(assistant_dialogue)
            return render(request, "dialogue.html", {"form": form, "assistant_dialogue": assistant_dialogue, "chat": chat, "charaimage":charaimage, "name":name})
    else:
        form = ChatForm()
    return render(request, "dialogue.html", {"form": form,"chat": chat, "charaimage":charaimage, "name":name})

def settings(request):
  if not request.user.is_authenticated:
    return redirect(f"../login/?next={request.path}")
  else:
    chatModel = ChatModel.objects.order_by('-id').first()
    if request.method == "POST":
        form = SettingsForm(request.POST)
        if form.is_valid():
            chatModel = ChatModel()
            chatModel.system_dialogue = form.cleaned_data.get('system_dialogue')
            chatModel.name = form.cleaned_data.get('name')
            chatModel.save()
            chat.clear()
            thread.clear()
            return render(request, "settings.html", {"form": form})
    else:
        form = SettingsForm()
    return render(request, "settings.html", {"form": form})

def change_charaimage(request):
  if not request.user.is_authenticated:
    return redirect(f"../login/?next={request.path}")
  else:
    if request.method == 'POST':
        form = CharaimageModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('transmit_dialogue') 
    else:
        form = CharaimageModelForm()
    return render(request, 'change_charaimage.html', {'form': form})
