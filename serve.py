# from core.bots.music import MusicBot
from api import api_v1

if __name__ == "__main__":
    api_v1.run(debug=True)
    # bot = MusicBot()

    # while True:
    #     time.sleep(1.0)
    #     bot.run()