#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Strube: add youtube and vlc
# pip3 install youtube_dl
# pip3 install python_vlc
# Volume control: sudo apt-get install python3-alsaaudio

"""Run a recognizer using the Google Assistant Library.

The Google Assistant Library has direct access to the audio API, so this Python
code doesn't need to record audio. Hot word detection "OK, Google" is supported.

It is available for Raspberry Pi 2/3 only; Pi Zero is not supported.
"""

import logging
import platform
import subprocess
import sys
import re

from google.assistant.library.event import EventType

from aiy.assistant import auth_helpers
from aiy.assistant.library import Assistant
from aiy.board import Board, Led
from aiy.voice import tts


import vlc
import youtube_dl
import alsaaudio

ydl_opts = {
    'default_search': 'ytsearch1:',
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True
}
vlc_instance = vlc.get_default_instance()
vlc_player = vlc_instance.media_player_new()

def power_off_pi():
    tts.say("Good bye, but I won\'t turn it off!")
    #subprocess.call('sudo shutdown now', shell=True)


def reboot_pi():
    tts.say('See you in a bit, but no way I will reboot!')
    #subprocess.call('sudo reboot', shell=True)


def say_ip():
    ip_address = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True)
    tts.say('My IP address is %s' % ip_address.decode('utf-8'))

def play_music(name):
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(name, download=False)
    except Exception:
        tts.say('Sorry, I can\'t find that song.')
        return

    if meta:
        info = meta['entries'][0]
        vlc_player.set_media(vlc_instance.media_new(info['url']))
        tts.say('Playing ' + re.sub(r'[^\s\w]', '', info['title']))
        vlc_player.play()

def lower_volume():
    m = alsaaudio.Mixer()
    current_volume = m.getvolume()
    print("Current volume is ",current_volume)
    next_volume=(current_volume[0]-25) if current_volume[0] > 30 else 0
    m.setvolume(next_volume)

def raise_volume():
    m = alsaaudio.Mixer()
    current_volume = m.getvolume()
    print("Current volume is ", current_volume)
    next_volume=current_volume[0]+25 if current_volume[0] < 70 else 100
    print("Next volume is ",next_volume)
    m.setvolume(next_volume)

def process_event(assistant, led, event):
    logging.info(event)
    if event.type == EventType.ON_START_FINISHED:
        led.state = Led.BEACON_DARK  # Ready.
        print('Say "OK, Google" then speak, or press Ctrl+C to quit...')
    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        led.state = Led.ON  # Listening.
    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
        print('You said:', event.args['text'])
        text = event.args['text'].lower()
        if text == 'power off':
            assistant.stop_conversation()
            power_off_pi()
        elif text == 'reboot':
            assistant.stop_conversation()
            reboot_pi()
        elif text == 'ip address' or text == 'my ip':
            assistant.stop_conversation()
            say_ip()
        elif text == 'pause':
            assistant.stop_conversation()
            vlc_player.set_pause(True)
        elif text == 'stop':
            assistant.stop_conversation()
            vlc_player.stop()
        elif text == 'resume':
            assistant.stop_conversation()
            vlc_player.set_pause(False)
        elif text.startswith('play '):
            assistant.stop_conversation()
            play_music(text[5:])
        elif text == 'raise volume' or text == 'louder':
            assistant.stop_conversation()
            raise_volume()
        elif text == 'lower volume' or text == 'quieter':
            assistant.stop_conversation()
            lower_volume()

    elif event.type == EventType.ON_END_OF_UTTERANCE:
        led.state = Led.PULSE_QUICK  # Thinking.
    elif (event.type == EventType.ON_CONVERSATION_TURN_FINISHED
          or event.type == EventType.ON_CONVERSATION_TURN_TIMEOUT
          or event.type == EventType.ON_NO_RESPONSE):
        led.state = Led.BEACON_DARK  # Ready.
    elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
        sys.exit(1)


def main():
    logging.basicConfig(level=logging.INFO)

    credentials = auth_helpers.get_assistant_credentials()
    with Board() as board, Assistant(credentials) as assistant:
        for event in assistant.start():
            process_event(assistant, board.led, event)


if __name__ == '__main__':
    main()
