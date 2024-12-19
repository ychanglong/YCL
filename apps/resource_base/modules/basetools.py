import hashlib
import random
import time
from django.conf import settings


def md5(password):
    hash_object = hashlib.md5(settings.SECRET_KEY.encode("utf-8"))
    hash_object.update(password.encode("utf-8"))
    return hash_object.hexdigest()


def random_str():
    num_set = [chr(i) for i in range(48, 58)]
    char_set = [chr(i) for i in range(97, 123)]
    total_set = num_set + char_set
    bits = 14
    value_set = "".join(random.sample(total_set, bits))
    return value_set + str(int(time.time()))


def custom_file_name(file_name):
    file_type = str(file_name).split(".")[-1]
    new_file_name = random_str().upper()
    return ".".join([new_file_name, file_type])
