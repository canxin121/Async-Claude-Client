# Claude Client

# 目录

[一.Claude.ai](#claude-ai)

- [1]. [初始化client](#1-初始化client)
- [2]. [获取所有的聊天窗口](#2获取所有的聊天窗口)
- [3]. [获取某个聊天窗口的聊天记录](#3获取某个聊天窗口的聊天记录)
- [4]. [创建一个新的聊天窗口](#4创建一个新的聊天窗口)
- [5]. [删除一个聊天窗口](#5删除一个聊天窗口)
- [6]. [重命名聊天窗口的名称](#6重命名聊天窗口的名称)
- [7]. [流式询问claude](#7流式询问claude)

[二.Slack Claude](#slack-claude)

- [1]. [创建client](#1-创建client)
- [2]. [创建一个新的对话信息dict](#2创建一个新的对话信息dict)
- [3]. [流式询问claude](#3流式询问claude)

# Claude Ai

## 1. 初始化client

函数:  
ClaudeAiClient(cookie).init()  
参数:  
cookie:`str | Path | list[dict]` - 可以是str或者Path的路径,也可以是直接的json  
获取的方式是 通过浏览器插件 cookie-editor 提取claude.ai的cookie为json格式  

```python
from async_claude_client import ClaudeAiClient

claude_ai_client = await ClaudeAiClient(cookie="cookies.json").init()
```

## 2.获取所有的聊天窗口

函数:  
get_all_chats()  
返回值:  
一个包含所有的chat聊天窗口的dict  

```python

chats = await claude_ai_client.get_all_chats()

```

## 3.获取某个聊天窗口的聊天记录

函数:  
get_chat_history()  
参数:  
chat_id:`str` - 聊天窗口的chat_id, 获取方式是在聊天窗口的连接中提取最后一个uuid,
或者是提取create_new_chat函数的返回值data的data['uuid']  
返回值:  
一个包含所有的聊天记录的dict  

```python
history = await claude_ai_client.get_chat_history(chat_id)
```

## 4.创建一个新的聊天窗口

函数:  
create_new_chat()  
返回值:  
一个包含新的聊天窗口的信息的dict,其中的键'uuid'对应的值为新的窗口的chat_id

```python
new_chat = await claude_ai_client.create_new_chat()
```

## 5.删除一个聊天窗口

函数:  
delete_chat()  
参数:  
chat_id:`str` - 聊天窗口的chat_id, 获取方式是在聊天窗口的连接中提取最后一个uuid,
或者是提取create_new_chat函数的返回值data的data['uuid']  

```python
await claude_ai_client.delete_chat(chat_id)
```

## 6.重命名聊天窗口的名称

函数:  
rename_chat()  
参数:  
title:`str` - 新的聊天窗口的名称  
chat_id:`str` - 聊天窗口的chat_id, 获取方式是在聊天窗口的连接中提取最后一个uuid,
或者是提取create_new_chat函数的返回值data的data['uuid']  

```python
await claude_ai_client.rename_chat(title, chat_id)
```

## 7.流式询问claude

函数:  
异步生成器 ask_stream()  
参数:  
question:`str` - 要询问的问题  
chat_id:`str` - 聊天窗口的chat_id, 获取方式是在聊天窗口的连接中提取最后一个uuid,
或者是提取create_new_chat函数的返回值data的data['uuid']  
attachment:`str | Path` - 要上传的文件附件的地址字符串或者地址Path  

```python
new_chat = await claude_ai_client.create_new_chat()
async for text in claude_ai_client.ask_stream("在吗", new_chat["uuid"]):
    print(text, end="")
```

# Slack Claude

## 1. 创建client

函数:  
ClaudeAiClient(cookie).init()  
参数:  
slack_user_token:`str` - slack官方api的用户的token,获取方法请看[如何获取slack_user_token](#1如何获取slack_user_token)  
claude_id:`str` - slack中添加的应用Claude的成员ID,获取方法是在应用中打开Claude,然后点击claude的头像,即可开到成员ID  
channel_id:`str` - 要用做client与claude交流的频道id,获取方法是打开对应频道之后,在链接中提取/thread/前面的一个拼接地址字符串,通常以C开头,如C0579MZR3LH  
pre_msg:`str` - 发送给claude的消息的前缀,这是一个妥协的举动,因为slack在频道中发送给claude的消息会带有'@claude'
这个信息,需要让claude忽略这个'@claude'  

```python
from async_claude_client import Slack_Claude_Client, Text, ChatUpdate

slack_claude_client = Slack_Claude_Client(
    slack_user_token,
    claude_id,
    channel_id,
    "<忽略'@Claude',不说没看到也不说看到>"
)
```

## 2.创建一个新的对话信息dict

函数:  
create_new_chat()  
返回值:  
一个新的会话消息的dict  

```python
chat = slack_claude_client.create_new_chat()
```

## 3.流式询问claude

函数:  
ask_stream_raw()  
参数:  
question: `str` - 询问的问题  
chat: `dict` - 会话消息dict  
返回值类型:  
`ChatUpdate`: 更新后的会话消息dict  
`Text`: 文本回复消息  

注意:
每次询问之后chat这个会话消息dict都会更新,下次使用时应该使用更新后的chat: dict

```python
chat = slack_claude_client.create_new_chat()
async for data in client.ask_stream_raw("在吗", chat):
    if isinstance(data, Text):
        print(data.content, end="")
    elif isinstance(data, ChatUpdate):
        # 这里把新的chat赋值给了原来的chat
        chat = data.content

async for data in client.ask_stream_raw("你说谁?", chat):
    if isinstance(data, Text):
        print(data.content, end="")
    elif isinstance(data, ChatUpdate):
        chat = data.content
```

# QA

## 1.如何获取slack_user_token?:

```md
进入 https://api.slack.com  
创建一个bot的api  
进入选项  

OAuth & Permissions添加如下权限  

Bot Token Scopes 需要安装如下权限  
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

User Token Scopes 需要安装如下权限
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

将所有权限添加完毕后选择Install App进行安装

安装完成后可以获得 xoxp 开头的一个token极为slack_user_token
```

## 2.为什么Slack Claude不回复?:

    应该是slack 服务器自己的问题, 开发者无法解决, 可以尝试创建新的chat聊天窗口
