#!/usr/bin/env python

import Skype4Py
import time
import json
import re
import subprocess
import sys
from MusicPlayer import MusicPlayerObject
from db import MongoConnection
from music import MusicManager

class SkypeBot(object):
    def __init__(self):

        self.music_manager = MusicManager(MongoConnection(db="skype_music"))
        self.skype = Skype4Py.Skype(Events=self)
        self.skype.FriendlyName = "Skype Bot"
        self.skype.Attach()

        self.musicPlayer = MusicPlayerObject()

        print "*** Started!"

    def MessageStatus(self, msg, status):
        if status == Skype4Py.cmsReceived:
            for regexp, target in self.commands.items():
                match = re.match(regexp, msg.Body, re.IGNORECASE)
                if match:
                    msg.MarkAsSeen()
                    reply = target(self, *match.groups())

                    if reply:
                        msg.Chat.SendMessage(reply)
                    break

    def cmd_status(self):
        return "bot is doing well"

    def cmd_help(self):
        return "tc music bot, supported commands:\nhelp - this message\nstop - stop the music\nskip - skip the current track\nlist - list the current queue\nqueue {search term}, {optional index}"

    def cmd_stop(self):
        self.musicPlayer.stop()

    def cmd_skip(self):
        self.musicPlayer.stop()
        song = self.music_manager.play_next()

        if song:
            self.musicPlayer.play(song)

        return "skipping the track"

    def cmd_list(self):
        return [song.name for song in json.loads(self.music_manager.get_queue())].join("\n")

    def cmd_play(self, song):
        params = song.split(',')

        if len(params) == 1:
            self.musicPlayer.play(song, 1)
        elif len(params) == 2:
            self.musicPlayer.play(params[0], int(params[1].strip()))

    def cmd_play_next(self):
        playing = self.musicPlayer.is_playing()
        print playing
        if playing == False:
            song = self.music_manager.play_next()
            if song:
                self.cmd_play(song)

    def cmd_search(self, search):
        return self.musicPlayer.find(search)

    def cmd_queue(self, search):
        self.music_manager.queue(search)

    commands = {
        "@musicbot$" : cmd_help,
        "@musicbot help$" : cmd_help,
        "@musicbot stop$" : cmd_stop,
        "@musicbot skip$" : cmd_skip,
        "@musicbot list$" : cmd_list,
        "@musicbot search *(.*)" : cmd_search,
        "@musicbot queue *(.*)" : cmd_queue,
    }


if __name__ == "__main__":
    bot = SkypeBot()

    while True:
        time.sleep(1.0)
        bot.cmd_play_next()