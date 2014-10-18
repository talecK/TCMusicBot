##TCMusicBot

TCMusicBot provides an abstract way to use the deprecated Skype API to build chat bots that interact and perform services.

###Disclaimer

Because the Skype API is deprecated and no longer supported in any official capacity, this package will cease to work with the newer
chats which are provided by Skype. This will only work with older chats not hosted in the cloud. Any future support for even the older chats
may one day cease to exist as well. Upon that time this package will be rendered unusable.

###Setup

To begin using or developing more bots using this package, clone the repo and run ./setup.sh in the root of the directory.
This will create a python virtual environment to work within and pull down all the dependencies required.

###Run

Once installed, its simple to begin using the package. By running ./run.sh, this will enable the virtualenvironment and launch the included musicbot which
will attach itself to Skype and listen for incoming chat requests.
It will also launch a micro API server built on Flask to provide web endpoints to control the music streaming service which musicbot
hooks into.

###Develop

Creating new bots is simple. Begin by creating a class which inherits from core.bots.base.SkypeBot. There are 4 abstract methods which
are required to be implemented: run, register, register_delimiter, register_owner.

Following the example musicbot which is provided, implement these methods to register how the bot will interact with chat commands by
identifying the names of the commands and the classes or functions which will be called when they are encountered. You are able to provide
the callback functions within the bot class itself, or by creating an external command class (see core.commands.music.MusicCommand as an example),
which is just a standard python class holding the functions which describe and implement the bot's command interactions.

###Test

Tests are provided for the core classes and functions. To run the tests just run the tests file python tests.py. Add any of your own tests to this file,
to test that any added functionality continues to operate as expected.

###That's it!

This is a really simple package, hope you enjoy.
