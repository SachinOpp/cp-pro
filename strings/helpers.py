HELP_1 = """
<b>Admin Commands:</b>

Just add <b>c</b> in the starting of the commands to use them for the channel.

/pause: Pause the current playing stream.

/resume: Resume the paused stream.

/skip: Skip the current playing stream and start streaming the next track in queue.

/end or /stop: Clears the queue and end the current playing stream.

/player: Get an interactive player panel.

/queue: Shows the queued tracks list.
"""

HELP_2 = """
<b>Auth Users:</b>

Auth users can use admin rights in the bot without admin rights in the chat.

/auth [username/user_id]: Add a user to the auth list of the bot.

/unauth [username/user_id]: Remove an auth user from the auth users list.

/authusers: Shows the list of auth users of the group.
"""

HELP_3 = """
<b>Broadcast Feature [Only for Sudoers]:</b>

/broadcast [message or reply to a message]: Broadcast a message to served chats of the bot.

Broadcasting Modes:
- <code>-pin</code> : Pins your broadcasted messages in served chats.
- <code>-pinloud</code> : Pins your broadcasted message in served chats and sends notifications to the members.
- <code>-user</code> : Broadcasts the message to the users who have started your bot.
- <code>-assistant</code> : Broadcast your message from the assistant account of the bot.
- <code>-nobot</code> : Forces the bot to not broadcast the message.

Example: <code>/broadcast -user -assistant -pin testing broadcast</code>
"""

HELP_4 = """
<b>Chat Blacklist Feature [Only for Sudoers]:</b>

Restrict shit chats to use our precious bot.

/blacklistchat [chat id]: Blacklist a chat from using the bot.

/whitelistchat [chat id]: Whitelist the blacklisted chat.

/blacklistedchat: Shows the list of blacklisted chats.
"""

HELP_5 = """
<b>BLOCK USERS:</b> [ONLY FOR sudoers]

starts ignoring the blacklisted user, so that he can't use bot commands.

/block [username or reply to a user] : block the user from our bot.
/unblock [username or reply to a user] : unblocks the blocked user.
/blockedusers : shows the list of blocked users.
"""

HELP_6 = """
<b>CHANNEL PLAY COMMANDS:</b>

You can stream audio/video in channel.

/cplay : starts streaming the requested audio track on channel's videochat.
/cvplay : starts streaming the requested video track on channel's videochat.
/cplayforce or /cvplayforce : stops the ongoing stream and starts streaming the requested track.

/channelplay [chat username or id] or [disable] : connect channel to a group and starts streaming tracks by the help of commands sent in group.
"""

HELP_7 = """
<b>GLOBAL BAN FEATURE</b> [ONLY FOR sudoers] :

/gban [username or reply to a user] : globally bans the user from all the served chats and blacklists him from using the bot.
/ungban [username or reply to a user] : globally unbans the globally banned user.
/gbannedusers : shows the list of globally banned users.
"""

HELP_8 = """
<b>LOOP STREAM :</b>

starts streaming the ongoing stream in loop

/loop [enable/disable] : enables/disables loop for the ongoing stream
/loop [1, 2, 3, ...] : enables the loop for the given value.
"""

HELP_9 = """
<b>MAINTENANCE MODE</b> [ONLY FOR sudoers] :

/logs : get logs of the bot.

/logger [enable/disable] : bot will start logging the activities happen on bot.

/maintenance [enable/disable] : enable or disable the maintenance mode of your bot.
"""

HELP_10 = """
<b>PING & STATS :</b>

/start : starts the music bot.
/help : get help menu with explanation of commands.

/ping : shows the ping and system stats of the bot.

/stats : shows the overall stats of the bot.
"""

HELP_11 = """
<b>Play Commands:</b>

v: stands for video play.
force: stands for force play.

/play or /vplay: starts streaming the requested track on video chat.

/playforce or /vplayforce: stops the ongoing stream and starts streaming the requested track.
"""

HELP_12 = """
<b>Shuffle Queue:</b>

/shuffle: shuffles the queue.
 
/queue: shows the shuffled queue.
"""

HELP_13 = """
<b>Seek Stream:</b>

/seek [duration in seconds]: seek the stream to the given duration.

/seekback [duration in seconds]: backward seek the stream to the given duration.
"""

HELP_14 = """
<b>Song Download:</b>

/song [song name/yt url]: download any track from YouTube in mp3 or mp4 formats.
"""

HELP_15 = """
<b>Speed Commands:</b>

You can control the playback speed of the ongoing stream. [Admins only]

/speed or /playback: for adjusting the audio playback speed in group.

/cspeed or /cplayback: for adjusting the audio playback speed in channel.
"""
