# -*- coding: utf-8 -*-

import random

import env
import dynamo

from flask import Flask
from flask_sslify import SSLify



app = Flask(__name__)
sslify = SSLify(app)


denv = env.prefix('dynamo_')
table = dynamo.table(denv['table'], (denv['access_key'], denv['secret_access_key']))

set_one = [
    'chaos', 'tasty', 'fruity', 'nice', 'swell', 'flying', 'loud', 'wet',
    'bitter', 'good', 'sweet', 'friendly', 'sad', 'flat', 'sharp', 'bright'
]

set_two = [
    'monkey', 'penguin', 'pizza', 'taco', 'fajita', 'synthesizer', 'iphone',
    'beer', 'wine', 'apple', 'chip', 'book', 'kindle', 'lens', 'camera', 'dog',
    'puppy', 'bunny', 'speaker', 'car'
]


def generate_slug():
    a = random.choice(set_one)
    b = random.choice(set_two)
    c = random.randint(0,10000)

    return '{0}-{1}-{2}'.format(a, b, c)


def fresh_slug():
    slug = generate_slug()


    s = table[slug]

    if 'taken' not in s:
        s['taken'] = 1
        return slug

    # Recursion.
    return fresh_slug()



@app.route('/')
def slug():
    return fresh_slug()