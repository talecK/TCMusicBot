# from core.bots.music import MusicBot
from api import api_v1

if __name__ == "__main__":

    # This runs the api on a flask server
    api_v1.run(debug=True)

    # Uncomment the following lines to enable the bot
    # bot = MusicBot()
    # bot.run()
