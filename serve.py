from core.bots.music import MusicBot

if __name__ == "__main__":
    bot = MusicBot()

    while True:
        time.sleep(1.0)
        bot.run()