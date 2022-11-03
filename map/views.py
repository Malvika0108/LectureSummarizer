from asyncio.windows_events import NULL
from django.urls import reverse
from django.shortcuts import redirect, render
import ast
# Create your views here.

from django.http import HttpResponse

from numpy import imag

# from sympy import re
from .models import User
from .forms import AudioForm
from algo.test import testing
import algo.audioextraction.main as al

import algo.audioextraction.audiosplit as asp
import algo.audioextraction.audioext as ae
import algo.audioextraction.summarizer as sm
from django.template.response import TemplateResponse


def index(request):
    user_model = NULL
    form = AudioForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        user_model = form.save(commit=True)
        audio_path = user_model.inputAudioPath
        user_id = user_model.id
        audio_path = "media/"+str(audio_path)
        # output = al.map(str(audio_path))
        al.aud_split(audio_path)
        final_speech = al.transcription(audio_path)
        links = al.key_ext_link_rec(audio_path)
        summary = al.summarizer(audio_path)
        links[1] = links[1].split("\n")
        user_model.outputSummary = summary
        user_model.outputKeywords = links[0]
        user_model.outputLinks = links[1]

        user_model.save()
        return redirect(user_model)

    context = {
        'form': form
    }

    return render(request, 'map/index.html', context)


def show_op(request, id):
    user = User.objects.filter(id=id).first()
    # context = {
    #     'output' : user.o
    # }

    hyperLinks = ast.literal_eval(user.outputLinks)[1:]

    if user:
        return render(request, 'map/show_op.html', {
            'user': user,
            'hyperLinks': hyperLinks,
        })
    return
