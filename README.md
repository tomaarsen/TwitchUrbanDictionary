# TwitchUrbanDictionary
Twitch Bot to look up urban dictionary definitions and examples. 

---
# Explanation

When the bot has started, it will start listening to chat messages in the channel listed in the settings.txt file. Whenever a user types `!urban <term>` in chat, the bot will respond with top Urban Dictionary's definition of that word. Similarly, whenever a user types `!example <term>` in chat, the bot will respond with the example shown in the top example as displayed on Urban Dictionary.

Because both the definitions and examples can be quite long, it is possible to set a max character count. The bot will cleverly cut off separate sentences rather than cutting off right at the character limit. This does mean that the bot always shows at least one sentence, which may cross the character count limit.

The bot has a configurable cooldown attached, to prevent spam in chat.

# Usage
Command:
<pre><b>!urban &lt;term&gt;</b></pre>
For example:
<pre><b>!urban hello<br>Hello: a very offensive curse word.</pre></b>
Anyone can use this command.

---

Command:
<pre><b>!example &lt;term&gt;</b></pre>
For example:
<pre><b>!example hello<br>What the hello.</pre></b>
Anyone can use this command.

---

# Settings
This bot is controlled by a settings.txt file, which looks like:
```
{
    "Host": "irc.chat.twitch.tv",
    "Port": 6667,
    "Channel": "#<channel>",
    "Nickname": "<name>",
    "Authentication": "oauth:<auth>",
    "MaxCharacters": 150,
    "Cooldown": 30
}
```

| **Parameter**        | **Meaning** | **Example** |
| -------------------- | ----------- | ----------- |
| Host                 | The URL that will be used. Do not change.                         | "irc.chat.twitch.tv" |
| Port                 | The Port that will be used. Do not change.                        | 6667 |
| Channel              | The Channel that will be connected to.                            | "#CubieDev" |
| Nickname             | The Username of the bot account.                                  | "CubieB0T" |
| Authentication       | The OAuth token for the bot account.                              | "oauth:pivogip8ybletucqdz4pkhag6itbax" |
| MaxCharacters | The maximum amount of characters the bot should aim to make the results. Might cross this amount if the first sentence is already longer than this amount. | 150 | 
| Cooldown | Cooldown in seconds between uses of the bot, to prevent spam in chat. | 30 |

*Note that the example OAuth token is not an actual token, nor is the OWMKey an actual API key, but merely a generated string to give an indication what it might look like.*

I got my real OAuth token from https://twitchapps.com/tmi/.

---

# Requirements
* [Python 3.6+](https://www.python.org/downloads/)
* [Module requirements](requirements.txt)<br>
Install these modules using `pip install -r requirements.txt`

Among these modules is my own [TwitchWebsocket](https://github.com/CubieDev/TwitchWebsocket) wrapper, which makes making a Twitch chat bot a lot easier.
This repository can be seen as an implementation using this wrapper.

---

# Other Twitch Bots

* [TwitchMarkovChain](https://github.com/CubieDev/TwitchMarkovChain)
* [TwitchAIDungeon](https://github.com/CubieDev/TwitchAIDungeon)
* [TwitchGoogleTranslate](https://github.com/CubieDev/TwitchGoogleTranslate)
* [TwitchCubieBotGUI](https://github.com/CubieDev/TwitchCubieBotGUI)
* [TwitchCubieBot](https://github.com/CubieDev/TwitchCubieBot)
* [TwitchRandomRecipe](https://github.com/CubieDev/TwitchRandomRecipe)
* [TwitchUrbanDictionary](https://github.com/CubieDev/TwitchUrbanDictionary)
* [TwitchRhymeBot](https://github.com/CubieDev/TwitchRhymeBot)
* [TwitchWeather](https://github.com/CubieDev/TwitchWeather)
* [TwitchDeathCounter](https://github.com/CubieDev/TwitchDeathCounter)
* [TwitchSuggestDinner](https://github.com/CubieDev/TwitchSuggestDinner)
* [TwitchPickUser](https://github.com/CubieDev/TwitchPickUser)
* [TwitchSaveMessages](https://github.com/CubieDev/TwitchSaveMessages)
* [TwitchMMLevelPickerGUI](https://github.com/CubieDev/TwitchMMLevelPickerGUI) (Mario Maker 2 specific bot)
* [TwitchMMLevelQueueGUI](https://github.com/CubieDev/TwitchMMLevelQueueGUI) (Mario Maker 2 specific bot)
* [TwitchPackCounter](https://github.com/CubieDev/TwitchPackCounter) (Streamer specific bot)
* [TwitchDialCheck](https://github.com/CubieDev/TwitchDialCheck) (Streamer specific bot)
* [TwitchSendMessage](https://github.com/CubieDev/TwitchSendMessage) (Meant for debugging purposes)

