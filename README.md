# rcs_chatbot

A Python SDK for [RCS MaaP chatbots](https://www.gsma.com/futurenetworks/wp-content/uploads/2017/11/FNW.11_v1.0.pdf).

## Installation

```bash
pip install rcs_chatbot
```

## Example

See more examples in [the example folder](https://github.com/pvangool/py-rcs-chatbot/tree/master/example).

```python
import flask
import rcs_chatbot

chatbot = rcs_chatbot.Chatbot(
  "API_URL",
  "BOT_ID",
  "TOKEN"
)

app = flask.Flask(__name__)

@app.route('/', methods=['POST'])
def event():
  try:
    chatbot.processEvent(flask.request.get_json())
    return "ok", 200
  except:
    pass

@chatbot.registerEventHandler(rcs_chatbot.EventType.MESSAGE)
def messageHandler(event):
  userContact = None
  chatId = None

  if "userContact" in event["messageContact"]:
    userContact = event["messageContact"]["userContact"]
  if "chatId" in event["messageContact"]:
    chatId = event["messageContact"]["chatId"]

  contact = rcs_chatbot.MessageContact(userContact, chatId)

  suggestions = rcs_chatbot.Suggestions()
  suggestions.addReply("reply", "reply")
  suggestions.addUrlAction("url", "url", "http://example.com")

  chatbot.sendMessage(
    contact,
    "You wrote: " + event["RCSMessage"]["textMessage"],
    suggestions
  )

@chatbot.registerEventHandler(rcs_chatbot.EventType.ISTYPING)
def isTypingHandler(event):
  print("isTypingHandler")

@chatbot.registerEventHandler(rcs_chatbot.EventType.MESSAGESTATUS)
def messageStatusHandler(event):
  print("messageStatusHandler")

@chatbot.registerEventHandler(rcs_chatbot.EventType.FILESTATUS)
def fileStatusHandler(event):
  print("fileStatusHandler")

@chatbot.registerEventHandler(rcs_chatbot.EventType.RESPONSE)
def responseHandler(event):
  print("responseHandler")

@chatbot.registerEventHandler(rcs_chatbot.EventType.ALIAS)
def aliasHandler(event):
  print("aliasHandler")

@chatbot.registerEventHandler(rcs_chatbot.EventType.NEWUSER)
def newUserHandler(event):
  print("newUserHandler")

if __name__ == '__main__':
    app.run(port=5000, debug=False)
```

Instead of a simple message, you can also use `sendMessage` to send an `AudioMessage`, etc. Show below is
how to send a `RichcardCarousel` message.

```python
@chatbot.registerEventHandler(maap.EventType.MESSAGE)
def messageHandler(event):
  userContact = None
  chatId = None

  if "userContact" in event["messageContact"]:
    userContact = event["messageContact"]["userContact"]
  if "chatId" in event["messageContact"]:
    chatId = event["messageContact"]["chatId"]

  contact = maap.MessageContact(userContact, chatId)

  card1 = maap.Richcard()
  card1.setTitle("title")

  card2 = maap.Richcard()
  card2.setTitle("title")

  carousel = maap.RichcardCarousel()
  carousel.addRichcard(card1)
  carousel.addRichcard(card2)

  chatbot.sendMessage(
    contact,
    carousel
  )
```

## Usage

### Chatbot Functions

#### constructor

#### sendMessage(recipient, content, suggestions = None)

Sends a message with `content` and optional `suggestions` to the target `recipient`.

* `recipient` - Object: A `MessageContact` object.
* `content` - Object: The message payload. Either a string, an `AudioMessage` object, a `FileMessage` object, a `GeolocationPushMessage` object, a `Richcard` object, or a `RichcardCarousel` object.
* `suggestions` - (Optional) Object: A `Suggestions` object.

#### getMessageStatus(messageId)

Gets the status of a message with `messageId`.

* `messageId` - String: The message identifier.

#### updateMessageStatus(messageId, status)

Updates the status of a message with `messageId` to `status`.

* `messageId` - String: The message identifier.
* `status` - String: The requested status. Needs to be either `rcs_chatbot.MessageStatus.CANCELLED` or `rcs_chatbot.MessageStatus.DISPLAYED`.

#### getContactCapabilities(userContact, chatId)

Gets the capabilities for a subscriber. Either `userContact` or `chatId` needs to be specified.

* `userContact` - String: The subscriber's MSISDN.
* `chatId` - String: The user's anonymous token.

#### uploadFile(path, url, fileType, until)

Uploads a file of type `fileType` to the MaaP content storage until it expires at date `until`Either `path` or `url` needs to be specified.

* `path` - String: The path to the file.
* `url` - String: The URL to the file.
* `fileType` - String: The file's content type.
* `until` - Date: The date at which time the content should be expired.

#### deleteFile(fileId, [cb])

Deletes a file with identifier `fileId` from the MaaP content storage.

* `fileId` - String: The file identifier.

#### getFile(fileId, [cb])

Gets info for a file with identifier `fileId` from the MaaP content storage.

* `fileId` - String: The file identifier.

#### startTyping(recipient)

Starts the 'is typing' indicator for the target `recipient`.

* `recipient` - Object: A `MessageContact` object.

#### stopTyping(recipient, [cb])

Stops the 'is typing' indicator for the target `recipient`.

* `recipient` - Object: A `MessageContact` object.

#### processEvent(json)

The main middleware for your bot's webhook. It parses the message payload, and fire the appropriate event.

### FileMessage Functions

An `FileMessage` object representes a file and has the following properties:

| Property | Type | Mandatory | Description |
| --- | --- | --- | --- |
| `fileUrl` | String | Yes | The URL of the file. |
| `fileName` | String | No | The file name. |
| `fileMIMEType` | String | No | The MIME type of the file. |
| `fileSize` | Number | No | The size of the file. |
| `thumbnailUrl` | String | No | The URL of the thumbnail. |
| `thumbnailFileName` | String | No | The file name of the thumbnail. |
| `thumbnailMIMEType` | String | No | The MIME type of the thumbnail. |
| `thumbnailFileSize` | Number | No | The size of the thumbnail. |

#### constructor(fileUrl)

Returns a new `FileMessage` instance.

* `fileUrl` - String: The URL of the file.

#### setFileName(fileName)

Set the `fileName` property.

* `fileName` - String: The file name.

#### setFileMIMEType(fileMIMEType)

Set the `fileMIMEType` property.

* `fileMIMEType` - String: The MIME type of the file.

#### setFileSize(fileSize)

Set the `fileSize` property.

* `fileSize` - Number: The size of the file.

#### setThumbnailUrl(thumbnailUrl)

Set the `thumbnailUrl` property.

* `thumbnailUrl` - String: The URL of the thumbnail.

#### setThumbnailFileName(thumbnailFileName)

et the `thumbnailFileName` property.

* `thumbnailFileName` - String: The file name of the thumbnail.

#### setThumbnailMIMEType(thumbnailMIMEType)

Set the `thumbnailMIMEType` property.

* `thumbnailMIMEType` - String: The MIME type of the thumbnail.

#### setThumbnailFileSize(thumbnailFileSize)

Set the `thumbnailFileSize` property.

* `thumbnailFileSize` - Number: The size of the thumbnail.

### AudioMessage Functions

An `AudioMessage` object representes an audio file and has the following properties:

| Property | Type | Mandatory | Description |
| --- | --- | --- | --- |
| `fileUrl` | String | Yes | The URL of the file. |
| `fileName` | String | No | The file name. |
| `fileMIMEType` | String | No | The MIME type of the file. |
| `fileSize` | Number | No | The size of the file. |
| `playingLength` | Number | No | The playing length of the audio. |

#### constructor(fileUrl)

Returns a new `AudioMessage` instance.

* `fileUrl` - String: The URL of the file.

#### setFileName(fileName)

Set the `fileName` property.

* `fileName` - String: The file name.

#### setFileMIMEType(fileMIMEType)

Set the `fileMIMEType` property.

* `fileMIMEType` - String: The MIME type of the file.

#### setFileSize(fileSize)

Set the `fileSize` property.

* `fileSize` - Number: The size of the file.

#### setPlayingLength(playingLength)

Set the `playingLength` property.

* `playingLength` - Number: The playing length of the audio.

### GeolocationPushMessage

 Property | Type | Mandatory | Description |
| --- | --- | --- | --- |
| `pos` | String | Yes | This are the coordinates in WGS 84 (latitude, longitude) decimal notation. Example "26.118 1289 - 80.1283921" |
| `label` | String | No | This can be used to tag the nature of the location. |
| `timestamp` | String | No | This is the time when the location information was pushed. |
| `expiry` | String | No | This is an absolute date at which time the recipient is no longer permitted to possess the location information. |
| `timeOffset` | Number | No | This is the time zone where the location information was pushed, expressed as the number of minutes away from UTC. |
| `radius` | Number | No | The radius of the circle will be represented in meters. |

#### constructor(pos)

Returns a new `GeolocationPushMessage` instance. This is a geolocation push to be sent via RCS Geolocation Push.

* `pos` - String: This are the coordinates in WGS 84 (latitude, longitude) decimal notation.

#### setLabel(label)

Set the `label` property.

* `label` - String: This can be used to tag the nature of the location.

#### setTimestamp(timestamp)

Set the `timestamp` property.

* `timestamp` - String: This is the time when the location information was pushed.

#### setExpiry(expiry)

Set the `expiry` property.

* `expiry` - String: This is an absolute date at which time the recipient is no longer permitted to possess the location information.

#### setTimeOffset(timeOffset)

Set the `timeOffset` property.

* `timeOffset` - Number: This is the time zone where the location information was pushed, expressed as the number of minutes away from UTC.

#### setRadius(radius)

Set the `radius` property.

* `radius` - Number: The radius of the circle will be represented in meters.

### Richcard Functions

#### constructor()

Returns a new `Richcard` instance.

Returns a new `Richcard` instance.

#### setCardOrientation(cardOrientation)

Set the orientation of the card.

* `cardOrientation` - String: Either `rcs_chatbot.CardOrientation.HORIZONTAL` or `rcs_chatbot.CardOrientation.VERTICAL`.

#### setImageAlignment(imageAlignment)

Set the alignment of the image on the card.

* `imageAlignment` - String: Either `rcs_chatbot.ImageAlignment.LEFT` or `rcs_chatbot.ImageAlignment.RIGHT`.

#### setMedia(mediaUrl, mediaContentType, mediaFileSize, height, [thumbnailUrl], [thumbnailContentType], [thumbnailFileSize], [contentDescription])

Set the media (image) to be displayed on the richcard.

* `mediaUrl` - String: The URL to the image.
* `mediaContentType` - String: The content type of the image.
* `mediaFileSize` - Number: The size of the image.
* `height` - String: Either `rcs_chatbot.MediaHeight.SHORT` or `rcs_chatbot.MediaHeight.MEDIUM` or `rcs_chatbot.MediaHeight.TALL`.
* `thumbnailUrl` - (Optional) String: The URL to the thumbnail for the image.
* `thumbnailContentType` - (Optional) String: The content type of the thumbnail.
* `thumbnailFileSize` - (Optional) Number: The size of the thumbnail.
* `contentDescription` - (Optional) String: Textual description of media content.

The `thumbnailUrl` property is optional, but if used, `thumbnailContentType` and `thumbnailFileSize` must be provided as well.

#### setTitle(title)

Set the title of the card.

* `title` - String: The title.

#### setDescription(description)

Set the description of the card.

* `description` - String: The description.

#### setSuggestions(suggestions)

Add suggestions to the card.

* `suggestions` - Suggestions: The suggestions.

### RichcardCarousel Functions

#### constructor()

Returns a new `RichcardCarousel` instance.

#### setCardWidth(cardWidth)

Set the width of the cards in the carousel.

* `cardWidth` - String: Either `rcs_chatbot.CardWidth.SMALL` or `rcs_chatbot.CardWidth.MEDIUM`.

#### addRichcard(richcard)

Add a card to the carousel.

* `richcard` - Richcard: The `Richcard` object.

### Suggestions Functions

Suggested Replies consist of a display text and a set of postback data.

Suggested Actions are grouped into seven different categories supporting a total of twelve different suggested actions:

* urlAction:
  * openUrl - Opens a web site or app via deep linking.
* dialerAction:
  * dialPhoneNumber - Calls a phone number via the user's dialer app.
  * dialEnrichedCall - Start an Enriched Call via the user’s dialer app.
  * dialVideoCall - Start a video call via the user’s dialer app.
* mapAction:
  * showLocation - Show location(s) on a map for given coordinates or search query.
  * requestLocationPush - Request for a one-time geo location push.
* calendarAction:
  * createCalendarEvent - Creates a new event on the user's calendar.
* composeAction:
  * composeTextMessage - Compose a draft text message.
  * composeRecordingMessage - Compose a draft message and start recording audio or video.
* deviceAction:
  * requestDeviceSpecifics - Request for a one-time share of device specifics (device model, operating system version, messaging client identifier and version, and remaining battery charge in minutes).
* settingsAction:
  * disableAnonymization - Ask the user to disable the anonymization setting.
  * enableDisplayedNotifications - Ask the user to enable sending displayed notifications.

Most actions allow fallback URLs in case a user does not have any app of the required type installed. Chatbot platforms can use the fallback URL to suggest an appropriate app to the user.

#### constructor()

Returns a new `Suggestions` instance.

#### addReply(displayText, postbackData)

On-the-wire example:

```json
{
  "reply": {
    "displayText": "Yes",
    "postback": {
      "data": "set_by_chatbot_reply_yes"
    }
  }
}
```

#### addUrlAction(displayText, postbackData, url)

On-the-wire example:

```json
{
  "action": {
    "urlAction": {
      "openUrl": {
        "url": "https://www.google.com"
      }
    },
    "displayText": "Open website or deep link",
    "postback": {
      "data": "set_by_chatbot_open_url"
    }
  }
}
```

#### addDialerAction(displayText, postbackData, dialType, phoneNumber, fallbackUrl, subject = None)

On-the-wire example:

```json
{
  "action": {
    "dialerAction": {
      "dialPhoneNumber": {
        "phoneNumber": "+1650253000"
      }
    },
    "displayText": "Call a phone number",
    "postback": {
      "data": "set_by_chatbot_dial_phone_number"
    }
  }
},
{
  "action": {
    "dialerAction": {
      "dialEnrichedCall": {
        "phoneNumber": "+1650253000",
        "subject": "The optional subject for the enriched call"
      }
    },
    "displayText": "Start enriched call",
    "postback": {
      "data": "set_by_chatbot_dial_enriched_call"
    }
  }
},
{
  "action": {
    "dialerAction": {
      "dialVideoCall": {
        "phoneNumber": "+1650253000"
      }
    },
    "displayText": "Start video call",
    "postback": {
      "data": "set_by_chatbot_dial_video_call"
    }
  }
}
```

#### addRequestLocationPushMapAction(displayText, postbackData)

On-the-wire example:

```json
{
  "action": {
    "mapAction": {
      "requestLocationPush": {}
    },
    "displayText": "Request a geo location",
    "postback": {
      "data": "set_by_chatbot_request_location_push"
    }
  }
}
```

#### addShowLocationMapAction(displayText, postbackData, latitude, longitude, label, query, fallbackUrl)

On-the-wire example:

```json
{
  "action": {
    "mapAction": {
      "showLocation": {
        "location": {
          "latitude": 37.4220041,
          "longitude": -122.0862515,
          "label": "Googleplex"
        },
        "fallbackUrl": "https://www.google.com/maps/@37.4219162,-122.078063,15z"
      }
    },
    "displayText": "Show location on a map",
    "postback": {
      "data": "set_by_chatbot_show_location"
    }
  }
},
{
  "action": {
    "mapAction": {
      "showLocation": {
        "location": {
          "query": "restaurants"
        },
        "fallbackUrl": "https://www.google.com/maps/search/restaurants"
      }
    },
    "displayText": "Search location(s) on map",
    "postback": {
      "data": "set_by_chatbot_search_locations"
    }
  }
}
```

#### addCalendarAction(displayText, postbackData, startTime, endTime, title, description, fallbackUrl)

On-the-wire example:

```json
{
  "action": {
    "calendarAction": {
      "createCalendarEvent": {
        "startTime": "2017-03-14T00:00:00Z",
        "endTime": "2017-03-14T23:59:59Z",
        "title": "Meeting",
        "description": "GSG review meeting"
      }
    },
    "displayText": "Schedule Meeting",
    "postback": {
      "data": "set_by_chatbot_create_calendar_event"
    }
  }
}
```

#### addTextComposeAction(displayText, postbackData, phoneNumber, text)

On-the-wire example:

```json
{
  "action": {
    "composeAction": {
      "composeTextMessage": {
        "phoneNumber": "+1650253000",
        "text": "Draft to go into the send message text field."
      }
    },
    "displayText": "Draft a text message",
    "postback": {
      "data": "set_by_chatbot_compose_text_message"
    }
  }
}
```

#### addRecordingComposeAction(displayText, postbackData, phoneNumber, type)

On-the-wire example:

```json
{
  "action": {
    "composeAction": {
      "composeRecordingMessage": {
        "phoneNumber": "+1650253000",
        "type": "VIDEO"
      }
    },
    "displayText": "Record audio or video",
    "postback": {
      "data": "set_by_chatbot_compose_recording_message"
    }
  }
}
```

#### addDeviceAction(displayText, postbackData)

On-the-wire example:

```json
{
  "action": {
    "deviceAction": {
      "requestDeviceSpecifics": {}
    },
    "displayText": "Request device specifics",
    "postback": {
      "data": "set_by_chatbot_request_device_specifics"
    }
  }
}
```

#### addSettingsAction(displayText, postbackData, settingsType)

On-the-wire example:

```json
{
  "action": {
    "settingsAction": {
      "disableAnonymization": {}
    },
    "displayText": "Share your phone number",
    "postback": {
      "data": "set_by_chatbot_disable_anonymization"
    }
  }
},
{
  "action": {
    "settingsAction": {
      "enableDisplayedNotifications": {}
    },
    "displayText": "Send read receipts",
    "postback": {
      "data": "set_by_chatbot_enable_displayed_notifications"
    }
  }
}
```

### Events

A different event is triggered for each type of event an RCS chatbot can receive. Below are all
the possible events with an example of the payload they provide.

#### EventType.MESSAGE

Triggered when a 'message' event is sent to the bot.

* `event` - Object: An object containing the 'message' event payload.

Example usage:

```python
@chatbot.registerEventHandler(rcs_chatbot.EventType.MESSAGE)
def messageHandler(event):
  print("messageHandler")
```

Sample payload:

```json
{
  "RCSMessage": {
    "msgId": "Xs8CI3tdf",
    "textMessage": "hello world",
    "timestamp": "2017-09-26T01:33:20.315Z"
  },
  "messageContact": {
    "userContact": "+14251234567"
  },
  "event": "message"
}
```

#### EventType.ISTYPING

Triggered when an 'isTyping' event is sent to the bot.

* `event` - Object: An object containing the 'isTyping' event payload.

Example usage:

```python
@chatbot.registerEventHandler(rcs_chatbot.EventType.ISTYPING)
def isTypingHandler(event):
  print("isTypingHandler")
```

Sample payload:

```json
{
  "RCSMessage": {
    "msgId": "Xs8CI3tdf",
    "isTyping": "active",
    "timestamp": "2017-09-26T01:33:20.315Z"
  },
  "messageContact": {
    "userContact": "+14251234567"
  },
  "event": "isTyping"
}
```

#### EventType.MESSAGESTATUS

Triggered when a 'messageStatus' event is sent to the bot.

* `event` - Object: An object containing the 'messageStatus' event payload.

Example usage:

```python
@chatbot.registerEventHandler(rcs_chatbot.EventType.MESSAGESTATUS)
def messageStatusHandler(event):
  print("messageStatusHandler")
```

Sample payload:

```json
{
  "RCSMessage": {
    "msgId": "MzJmajlmamVzZGZ8bmk5MHNlbmRmZTAz",
    "status": "displayed",
    "timestamp": "2017-09-26T01:33:20.315Z"
  },
  "messageContact": {
    "userContact": "+14251234567"
  },
  "event": "messageStatus"
}
```

#### EventType.FILESTATUS

Triggered when a 'fileStatus' event is sent to the bot.

* `event` - Object: An object containing the 'fileStatus' event payload.

Example usage:

```python
@chatbot.registerEventHandler(rcs_chatbot.EventType.FILESTATUS)
def fileStatusHandler(event):
  print("fileStatusHandler")
```

Sample payload:

```json
{
  "file": {
    "fileId": "MzJmajlmamVzZGZ8bmk5MHNlbmRmZTAz",
    "fileUrl": "http://www.example.com/files/f.jpg",
    "fileSize": 123456,
    "status": "ready",
    "validity": "2017-10-03T22:31:00.597Z"
  },
  "event": "fileStatus"
}
```

#### EventType.RESPONSE

Triggered when a 'response' event is sent to the bot.

* `event` - Object: An object containing the 'response' event payload.

Example usage:

```python
@chatbot.registerEventHandler(rcs_chatbot.EventType.RESPONSE)
def responseHandler(event):
  print("responseHandler")
```

Sample payload:

```json
{
  "RCSMessage": {
    "msgId": "MzJmajlmamVzZGZ8bmk5MHNlbmRmZTAz",
    "suggestedResponse": {
      "response": {
        "action": {
          "displayText": "Visit Website",
          "postback": {
            "data": "set_by_chatbot_reply_yes"
          }
        }
      }
    },
    "timestamp": "2017-09-26T01:33:20.315Z"
  },
  "messageContact": {
    "userContact": "+14251234567"
  },
  "event": "response"
}
```

#### EventType.ALIAS

Triggered when a 'alias' event is sent to the bot.

* `event` - Object: An object containing the 'alias' event payload.

Example usage:

```python
@chatbot.registerEventHandler(rcs_chatbot.EventType.ALIAS)
def aliasHandler(event):
  print("aliasHandler")
```

Sample payload:

```json
{
  "RCSMessage": {
    "msgId": "MzJmajlmamVzZGZ8bmk5MHNlbmRmZTAz",
    "timestamp": "2017-09-26T01:33:20.315Z"
  },
  "messageContact": {
    "userContact": "+14251234567",
    "chatId": "93JF93SEIJFE"
  },
  "event": "alias"
}
```

#### EventType.NEWUSER

Triggered when a 'newUser' event is sent to the bot.

* `event` - Object: An object containing the 'newUser' event payload.

Example usage:

```python
@chatbot.registerEventHandler(rcs_chatbot.EventType.NEWUSER)
def newUserHandler(event):
  print("newUserHandler")
```

Sample payload:

```json
{
  "RCSMessage": {
    "msgId": "MzJmajlmamVzZGZ8bmk5MHNlbmRmZTAz",
    "suggestedResponse": {
      "response": {
        "reply": {
          "displayText": "Start Chat",
          "postback": {
            "data": "new_bot_user_initiation"
          }
        }
      }
    },
    "timestamp": "2017-09-26T01:33:20.315Z"
  },
  "messageContact": {
    "userContact": "+14251234567"
  },
  "event": "newUser"
}
```

## To Do

* Verify constraints before sending
* Look for missing fields like trafficType (there may be more)

