# Claude Client
[中文文档](README_zh_cn.md)  

Table of Contents

- [Claude Client](#claude-client)
- [Claude Ai](#claude-ai)
  - [1. Initialize Client](#1-initialize-client)
  - [2. Get All Chats](#2-get-all-chats)
  - [3. Get Chat History](#3-get-chat-history)
  - [4. Create a New Chat](#4-create-a-new-chat)
  - [5. Delete a Chat](#5-delete-a-chat)
  - [6. Rename Chat](#6-rename-chat)
  - [7. Stream Ask Claude](#7-stream-ask-claude)
- [Slack Claude](#slack-claude)
  - [1. Create Client](#1-create-client)
  - [2. Create a New Chat Message dict](#2-create-a-new-chat-message-dict)
  - [3. Ask Claude in a Streaming Manner](#3-ask-claude-in-a-streaming-manner)
- [QA](#qa)
  - [1. How to Get Slack User Token?](#1-how-to-get-slack-user-token)
  - [2. Why is Slack Claude not responding?](#2-why-is-slack-claude-not-responding)

# Claude Ai

## 1. Initialize Client

Function:  
ClaudeAiClient(cookie).init()  
Parameters:  
cookie: `str | Path | list[dict]` - It can be a string or a Path to a file, or a direct json.  
The cookie can be extracted as a JSON format using a browser extension called "cookie-editor".  

```python
from async_claude_client import ClaudeAiClient

claude_ai_client = await ClaudeAiClient(cookie="cookies.json").init()
```

## 2. Get All Chats

Function:  
get_all_chats()  
Returns:  
A dictionary containing all chat windows.  

```python
chats = await claude_ai_client.get_all_chats()
```

## 3. Get Chat History

Function:  
get_chat_history()  
Parameters:  
chat_id: `str` - The chat_id of the chat window. It can be extracted from the last UUID in the chat window's link or
from the 'uuid' value in the data returned by the create_new_chat() function.  
Returns:  
A dictionary containing the chat history of the specified chat window.  

```python
history = await claude_ai_client.get_chat_history(chat_id)
```

## 4. Create a New Chat

Function:  
create_new_chat()  
Returns:  
A dictionary containing the information of the newly created chat window. The value corresponding to the key 'uuid' is
the chat_id of the new window.  

```python
new_chat = await claude_ai_client.create_new_chat()
```

## 5. Delete a Chat

Function:  
delete_chat()  
Parameters:  
chat_id: `str` - The chat_id of the chat window. It can be extracted from the last UUID in the chat window's link or
from the 'uuid' value in the data returned by the create_new_chat() function.  
  
```python
await claude_ai_client.delete_chat(chat_id)
```

## 6. Rename Chat

Function:  
rename_chat()  
Parameters:  
title: `str` - The new name for the chat window.  
chat_id: `str` - The chat_id of the chat window. It can be extracted from the last UUID in the chat window's link or
from the 'uuid' value in the data returned by the create_new_chat() function.  

```python
await claude_ai_client.rename_chat(title, chat_id)
```

## 7. Stream Ask Claude

Function:  
ask_stream()  
Parameters:  
question: `str` - The question to ask Claude.  
chat_id: `str` - The chat_id of the chat window. It can be extracted from the last UUID in the chat window's link or
from the 'uuid' value in the data returned by the create_new_chat() function.  
attachment: `str | Path` - The address string or Path of the file attachment to upload.  

```python
new_chat = await claude_ai_client.create_new_chat()
async for text in claude_ai_client.ask_stream("Are you there?", new_chat["uuid"]):
    print(text, end="")
```

# Slack Claude

## 1. Create Client

Function:  
ClaudeAiClient(cookie).init()  
Parameters:  
slack_user_token: `str` - User token for the official Slack API. Refer
to [How to Get Slack User Token](#1-how-to-get-slack-user-token) for obtaining the token.  
claude_id: `str` - Member ID of the Claude app added in Slack. To obtain the Member ID, open Claude in the app and click
on Claude's avatar.  
channel_id: `str` - ID of the channel to communicate with Claude through the client. To obtain the channel ID, open the
desired channel and extract the concatenated address string before '/thread/' in the URL. It usually starts with 'C',
for example, C0579MZR3LH.  
pre_msg: `str` - Prefix for the messages sent to Claude. This is a workaround because Slack adds '@claude' to the
messages sent to Claude in the channel. This prefix is used to make Claude ignore the '@claude' mention.  

```python
from async_claude_client import Slack_Claude_Client, Text, ChatUpdate

slack_claude_client = Slack_Claude_Client(
    slack_user_token,
    claude_id,
    channel_id,
    "<Ignore '@Claude', neither say 'not seen' nor say 'seen'>"
)
```

## 2. Create a New Chat Message dict

Function:  
create_new_chat()  
Return:  
A new dict for the chat message  

```python
chat = slack_claude_client.create_new_chat()
```

## 3. Ask Claude in a Streaming Manner

Function:  
ask_stream_raw()  
Parameters:  
question: `str` - The question to ask  
chat: `dict` - The chat message dict  
Return Types:  
`ChatUpdate`: Updated chat message dict  
`Text`: Text reply message  

Note:
After each question, the chat message dict (`chat`) will be updated. The updated `chat` should be used for the next
interaction.  

```python
chat = slack_claude_client.create_new_chat()
async for data in client.ask_stream_raw("Are you there?", chat):
    if isinstance(data, Text):
        print(data.content, end="")
    elif isinstance(data, ChatUpdate):
        # Update the chat with the new content
        chat = data.content

async for data in client.ask_stream_raw("Who are you talking about?", chat):
    if isinstance(data, Text):
        print(data.content, end="")
    elif isinstance(data, ChatUpdate):
        chat = data.content
```

# QA

## 1. How to Get Slack User Token?

```md
Go to https://api.slack.com  
Create a bot API  
Go to the Options

Add the following permissions to OAuth & Permissions

Bot Token Scopes require the following permissions:
channels:history
channels:join
channels:manage
channels:read
channels:write.invites
channels:write.topic
chat:write
chat:write.customize
chat:write.public
groups:history
groups:read
groups:write
groups:write.invites
groups:write.topic
im:history
im:read
im:write
im:write.invites
im:write.topic
usergroups:write
users:read
users:write

User Token Scopes require the following permissions:
admin
Administer a workspace
channels:history
channels:read
channels:write
channels:write.invites
channels:write.topic
chat:write
groups:history
groups:read
groups:write
groups:write.invites
groups:write.topic
im:history
im:read
im:write
im:write.invites
im:write.topic
mpim:history
mpim:read
mpim:write
usergroups:write
users:read
users:write

After adding all the permissions, select Install App to proceed with the installation.

Once installed, you will receive a token starting with 'xoxp', which is the Slack user token.
```

## 2. Why is Slack Claude not responding?

    It could be an issue with the Slack server itself, and developers cannot fix it. You can try creating a new chat window to resolve the issue.