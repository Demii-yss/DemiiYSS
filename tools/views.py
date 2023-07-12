import json
import random
import string

from django.http import JsonResponse, HttpResponse, FileResponse
from tools.generateGIF import generateGIF
from datetime import datetime
from django.urls import path
from django.shortcuts import render
from PIL import Image
from DemiiYSS.settings import MEDIA_ROOT
from django.views.generic import View
from io import BytesIO
import tempfile
import os
from .models import UploadImage
import base64

test_value = 0


def home(request):
    return render(request, 'tools.html')


def generateThumbnailImage(img):
    size = img.size
    max = 256
    if size[0] > size[1]:
        scale = size[1] / size[0]
        w = max
        h = int(max * scale)
    else:
        scale = size[0] / size[1]
        w = int(max * scale)
        h = max
    return img.resize((w, h))


class makegif(View):
    def get(self, request):
        context = {}
        return render(request, 'makegif.html', context)

    def post(self, request):
        context = {}
        original_image_files = []
        thumbnail_image_files = []
        response_mode = ''

        if request.method == 'POST':
            if request.FILES:
                static_folder = ''.join(random.choice(string.ascii_letters) for _ in range(20))
                if not os.path.isdir(os.path.join(MEDIA_ROOT, static_folder)):
                    os.mkdir(os.path.join(MEDIA_ROOT, static_folder))
                response_mode = 'upload_images'
                images = request.FILES.getlist('images')
                for i, image in enumerate(images):
                    if i > 100:
                        break
                    original_file_name = image.name
                    original_image = Image.open(image)
                    original_image.save(os.path.join(os.path.join(MEDIA_ROOT, static_folder), original_file_name))
                    original_image_files.append(os.path.join('media', os.path.join(static_folder, original_file_name)))

                    thumbnail_image = generateThumbnailImage(original_image.copy())
                    thumbnail_file_name = 'thumbnail' + image.name
                    thumbnail_image.save(os.path.join(os.path.join(MEDIA_ROOT, static_folder), thumbnail_file_name))
                    thumbnail_image_files.append(os.path.join('media', os.path.join(static_folder, thumbnail_file_name)))
                context = {
                    'response_mode': response_mode,
                    'original_image_files': original_image_files,
                    'thumbnail_image_file_paths': thumbnail_image_files,
                    'static_folder': static_folder
                }
                return render(request, 'makegif.html', context)

            else:
                data = json.loads(request.body)
                if data['mode'] == 'generate_gif':
                    #
                    static_folder = data['static_folder']
                    duration = [float(image_duration) * 1000 for image_duration in data['image_duration']]
                    order = [int(o) - 1 for o in data['image_order']]
                    frames = [Image.open(data['images'][i]) for i in order]
                    #
                    gif_file_name = datetime.now().strftime("%y%m%d-%H%M%S") + '.gif'
                    gif_file_path = os.path.join(os.path.join(MEDIA_ROOT, static_folder), gif_file_name)
                    #
                    generateGIF(frames, duration, gif_file_path)
                    return JsonResponse({'gif_path': os.path.join('media', os.path.join(static_folder, gif_file_name))})
                if data['mode'] == 'leave_site':
                    print('LEAVE')