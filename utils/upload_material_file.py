import hashlib
import os

from PIL import Image
from bson.objectid import ObjectId
from pymediainfo import MediaInfo

base_dir = '/data/wcbp/files'

material_dir = os.path.join(base_dir, 'zips')
video_dir = os.path.join(base_dir, 'mp4s')
thumb_dir = os.path.join(base_dir, 'imgs')
poster_dir = os.path.join(base_dir, 'imgs')


def save_file(file_path, file):
    if file is None:
        return None
    md5obj = hashlib.md5()
    md5obj.update(file.read())
    file_name = str(ObjectId())
    file_type = file.name.split('.')[-1].lower()
    file_name += '.' + file_type
    full_file_name = os.path.join(file_path, file_name)
    with open(full_file_name, 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)
    return file_name


def save_material_file(file):
    return 'zips/' + save_file(material_dir, file)


def save_video_file(file):
    return 'mp4s/' + save_file(video_dir, file)


def save_thumb_file(file):
    return 'imgs/' + save_file(thumb_dir, file)


def save_poster_file(file):
    return 'imgs/' + save_file(poster_dir, file)


def parse_video_info(video_file_name):
    width, height, duration, file_size = 0, 0, 0, 0
    video_file = os.path.join(video_dir, video_file_name)
    media_info = MediaInfo.parse(video_file)
    for track in media_info.tracks:
        if track.track_type == 'General':
            duration = track.duration or duration
            file_size = track.file_size or file_size
        if track.track_type == 'Video':
            height = track.height or height
            width = track.width or width
    return width, height, duration, file_size


def parse_thumb_info(thumb_file_name):
    thumb_file = os.path.join(thumb_dir, thumb_file_name)
    with open(thumb_file, 'rb') as src_file:
        im = Image.open(src_file)
        width, height = im.size[0], im.size[1]
        return width, height


def parse_material_info(material_file_name):
    material_file = os.path.join(material_dir, material_file_name)
    file_size = os.path.getsize(material_file)
    return file_size
