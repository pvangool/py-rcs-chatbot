import json
import logging
import requests
from enum import Enum

class CardOrientation(Enum):
  VERTICAL = "VERTICAL"
  HORIZONTAL = "HORIZONTAL"

  def __str__(self):
    return self.value

class CardWidth(Enum):
  SMALL = "SMALL_WIDTH"
  MEDIUM = "MEDIUM_WIDTH"

  def __str__(self):
    return self.value

class MediaHeight(Enum):
  SHORT = "SHORT_HEIGHT"
  MEDIUM = "MEDIUM_HEIGHT"
  TALL = "TALL_HEIGHT"

  def __str__(self):
    return self.value

class ImageAlignment(Enum):
  LEFT = "LEFT"
  RIGHT = "RIGHT"

  def __str__(self):
    return self.value

class EventType(Enum):
  MESSAGE = "message"
  ISTYPING = "isTyping"
  MESSAGESTATUS = "messageStatus"
  FILESTATUS = "fileStatus"
  RESPONSE = "response"
  ALIAS = "alias"
  NEWUSER = "newUser"

class DialType(Enum):
  PHONE = "dialPhoneNumber"
  ENRICHED = "dialEnrichedCall"
  VIDEO = "dialVideoCall"

class SettingsType(Enum):
  DISABLEANONYMIZATION = "disableAnonymization"
  ENABLEDISPLAYEDNOTIFICATIONS = "enableDisplayedNotifications"

class MessageContact:
  def __init__(self, userContact, chatId):
    self.userContact = userContact
    self.chatId = chatId

  def generate(self):
    return {
      "userContact": self.userContact,
      "chatId": self.chatId
    }

class Suggestions:
  def __init__(self):
    self.suggestions = []

  def addReply(self, displayText, postbackData):
    suggestion = {
      "reply": {
        "displayText": displayText,
        "postback": {
          "data": postbackData
        }
      }
    }

    self.suggestions.append(suggestion)

  def addUrlAction(self, displayText, postbackData, url):
    suggestion = {
      "action": {
        "urlAction": {
          "openUrl": {
            "url": url
          }
        },
        "displayText": displayText,
        "postback": {
          "data": postbackData
        }
      }
    }

    self.suggestions.append(suggestion)

  def addDialerAction(self, displayText, postbackData, dialType, phoneNumber, fallbackUrl, subject = None):
    suggestion = {
      "action": {
        "dialerAction": {},
        "displayText": displayText,
        "postback": {
          "data": postbackData
        }
      }
    }

    if dialType is DialType.PHONE:
        suggestion["dialerAction"] = {
          "dialPhoneNumber": {
            "phoneNumber": phoneNumber,
            "fallbackUrl": fallbackUrl
          }
        }
    elif dialType is DialType.ENRICHED:
        suggestion["dialerAction"] = {
          "dialEnrichedCall": {
            "phoneNumber": phoneNumber,
            "fallbackUrl": fallbackUrl,
            "subject": subject,
          }
        }
    elif dialType is DialType.VIDEO:
        suggestion["dialerAction"] = {
          "dialVideoNumber": {
            "phoneNumber": phoneNumber,
            "fallbackUrl": fallbackUrl
          }
        }
    else:
      raise TypeError("Unknown dialType")

    self.suggestions.append(suggestion)

  def addRequestLocationPushMapAction(self, displayText, postbackData):
    suggestion = {
      "action": {
        "mapAction": {
          "requestLocationPush": {}
        },
        "displayText": displayText,
        "postback": {
          "data": postbackData
        }
      }
    }

    self.suggestions.append(suggestion)

  def addShowLocationMapAction(self, displayText, postbackData, latitude, longitude, label, query, fallbackUrl):
    suggestion = {
      "action": {
        "mapAction": {
          "showLocation": {
            "location": {
              "latitude": latitude,
              "longitude": longitude,
              "label": label,
              "query": query
            },
            "fallbackUrl": fallbackUrl
          }
        },
        "displayText": displayText,
        "postback": {
          "data": postbackData
        }
      }
    }

    self.suggestions.append(suggestion)

  def addCalendarAction(self, displayText, postbackData, startTime, endTime, title, description, fallbackUrl):
    suggestion = {
      "action": {
        "calendarAction": {
          "createCalendarEvent": {
            "startTime": startTime,
            "endTime": endTime,
            "title": title,
            "description": description,
            "fallbackUrl": fallbackUrl
          }
        },
        "displayText": displayText,
        "postback": {
          "data": postbackData
        }
      }
    }

    self.suggestions.append(suggestion)

  def addTextComposeAction(self, displayText, postbackData, phoneNumber, text):
    suggestion = {
      "action": {
        "composeAction": {
          "composeTextMessage": {
            "phoneNumber": phoneNumber,
            "text": text
          }
        },
        "displayText": displayText,
        "postback": {
          "data": postbackData
        }
      }
    }

    self.suggestions.append(suggestion)

  def addRecordingComposeAction(self, displayText, postbackData, phoneNumber, type):
    suggestion = {
      "action": {
        "composeAction": {
          "composeRecordingMessage": {
            "phoneNumber": phoneNumber,
            "type": type
          }
        },
        "displayText": displayText,
        "postback": {
          "data": postbackData
        }
      }
    }

    self.suggestions.append(suggestion)

  def addDeviceAction(self, displayText, postbackData):
    suggestion = {
      "action": {
        "deviceAction": {
          "requestDeviceSpecifics": {}
        },
        "displayText": displayText,
        "postback": {
          "data": postbackData
        }
      }
    }

    self.suggestions.append(suggestion)

  def addSettingsAction(self, displayText, postbackData, settingsType):
    suggestion = {
      "action": {
        "settingsAction": {},
        "displayText": displayText,
        "postback": {
          "data": postbackData
        }
      }
    }

    if settingsType is SettingsType.DISABLEANONYMIZATION:
        suggestion["settingsAction"] = {
          "disableAnonymization": {}
        }
    elif settingsType is SettingsType.ENABLEDISPLAYEDNOTIFICATION:
        suggestion["settingsAction"] = {
          "enableDisplayedNotifications": {}
        }
    else:
      raise TypeError("Unknown settingsType")

    self.suggestions.append(suggestion)

  def generate(self):
    return self.suggestions

class FileMessage:
  def __init__(self, fileUrl):
    self.fileUrl = fileUrl
    self.fileName = None
    self.fileMIMEType = None
    self.fileSize = None
    self.thumbnailUrl = None
    self.thumbnailFileName = None
    self.thumbnailMIMEType = None
    self.thumbnailFileSize = None

  def setFileName(self, fileName):
    self.fileName = fileName

  def setFileMIMEType(self, fileMIMEType):
    self.fileMIMEType = fileMIMEType

  def setFileSize(self, fileSize):
    self.fileSize = fileSize

  def setThumbnailUrl(self, thumbnailUrl):
    self.thumbnailUrl = thumbnailUrl

  def setThumbnailFileName(self, thumbnailFileName):
    self.thumbnailFileName = thumbnailFileName

  def setThumbnailMIMEType(self, thumbnailMIMEType):
    self.thumbnailMIMEType = thumbnailMIMEType

  def setThumbnailFileSize(self, thumbnailFileSize):
    self.thumbnailFileSize = thumbnailFileSize

  def generate(self):
    return {
      "fileUrl": self.fileUrl,
      "fileName": self.fileName,
      "fileMIMEType": self.fileMIMEType,
      "fileSize": self.fileSize,
      "thumbnailUrl": self.thumbnailUrl,
      "thumbnailFileName": self.thumbnailFileName,
      "thumbnailMIMEType": self.thumbnailMIMEType,
      "thumbnailFileSize": self.thumbnailFileSize
    }

class AudioMessage:
  def __init__(self, fileUrl):
    self.fileUrl = fileUrl
    self.fileName = None
    self.fileMIMEType = None
    self.fileSize = None
    self.playingLength = None

  def setFileName(self, fileName):
    self.fileName = fileName

  def setFileMIMEType(self, fileMIMEType):
    self.fileMIMEType = fileMIMEType

  def setFileSize(self, fileSize):
    self.fileSize = fileSize

  def setPlayingLength(self, playingLength):
    self.playingLength = playingLength

  def generate(self):
    return {
      "fileUrl": self.fileUrl,
      "fileName": self.fileName,
      "fileMIMEType": self.fileMIMEType,
      "fileSize": self.fileSize,
      "playingLength": self.playingLength
    }

class GeolocationPushMessage:
  def __init__(self, pos):
    self.pos = pos
    self.label = None
    self.timestamp = None
    self.expiry = None
    self.timeOffset = None
    self.radius = None

  def setLabel(self, label):
    self.label = label

  def setTimestamp(self, timestamp):
    self.timestamp = timestamp

  def setExpiry(self, expiry):
    self.expiry = expiry

  def setTimeOffset(self, timeOffset):
    self.timeOffset = timeOffset

  def setRadius(self, radius):
    self.radius = radius

  def generate(self):
    return {
      "pos": self.pos,
      "label": self.label,
      "timestamp": self.timestamp,
      "expiry": self.expiry,
      "timeOffset": self.timeOffset,
      "radius": self.radius
    }

class Richcard:
  def __init__(self):
    self.cardOrientation = CardOrientation.VERTICAL
    self.imageAlignment = None
    self.media = None
    self.title = None
    self.description = None
    self.suggestions = None

  def setCardOrientation(self, cardOrientation):
    self.cardOrientation = cardOrientation

  def setImageAlignment(self, imageAlignment):
    self.imageAlignment = imageAlignment

  def setMedia(self, mediaUrl, mediaContentType, mediaFileSize, height, thumbnailUrl, thumbnailContentType, thumbnailFileSize, contentDescription):
    self.media = {
      "mediaUrl": mediaUrl,
      "mediaContentType": mediaContentType,
      "mediaFileSize": mediaFileSize,
      "height": height,
      "thumbnailUrl": thumbnailUrl,
      "thumbnailContentType": thumbnailContentType,
      "thumbnailFileSize": thumbnailFileSize,
      "contentDescription": contentDescription
    }

  def setTitle(self, title):
    self.title = title

  def setDescription(self, description):
    self.description = description

  def setSuggestions(self, suggestions):
    self.suggestions = suggestions

  def generate (self):
    richcard = {
      "message": {
        "generalPurposeCard": {
          "layout": {
            "cardOrientation": str(self.cardOrientation)
          },
          "content": self.generateContent()
        }
      }
    }

    if (self.cardOrientation == CardOrientation.HORIZONTAL):
      richcard["message"]["generalPurposeCard"]["layout"]["imageAlignment"] = str(self.imageAlignment)

    return richcard

  def generateContent(self):
    content = {}

    if self.media != None:
      content["media"] = self.media
    if self.title != None:
      content["title"] = self.title
    if self.description != None:
      content["description"] = self.description
    if self.suggestions != None:
      content["suggestions"] = self.suggestions.generate()

    return content

class RichcardCarousel:
  def __init__(self):
    self.cardWidth = CardWidth.SMALL
    self.richcards = []

  def setCardWidth(self, cardWidth):
    self.cardWidth = cardWidth

  def addRichcard(self, richcard):
    self.richcards.append(richcard)

  def generate(self):
    richcardcarousel = {
      "message": {
        "generalPurposeCardCarousel": {
          "layout": {
            "cardWidth": str(self.cardWidth)
          },
          "content": []
        }
      }
    }

    i = 0
    while i < len(self.richcards):
      richcardcarousel["message"]["generalPurposeCardCarousel"]["content"].append(self.richcards[i].generateContent())
      i += 1

    return richcardcarousel

class Chatbot:
  eventHandlers = {}

  def __init__(self, apiUrl, botId, accessToken, logger=None, logger_level=None):
    self.apiUrl = apiUrl
    self.botId = botId
    self.accessToken = accessToken

    if logger is not None:
      self.logger = logger
    else:
      logging.basicConfig()
      self.logger = logging.getLogger(__name__)
      self.logger.setLevel(logging.INFO)

    if logger_level is not None:
      self.logger.setLevel(logger_level)

  def registerEventHandler(self, eventType):
    def decorator(function):
      if eventType not in EventType:
        self.logger.warn("{} is not event type".format(eventType))
        return function

      self.logger.info("{} event handler has been added".format(eventType))
      self.eventHandlers[eventType] = function
      return function

    return decorator

  def processEvent(self, body):
    self.logger.debug(body)

    if body is None:
      self.logger.warn("Empty POST body")
      raise Exception("Empty POST body")
    if "event" not in body:
      self.logger.warn("Invalid POST body")
      raise Exception("Invalid POST body")

    event = body["event"]
    eventType = None
    if ("message" == event):
      eventType = EventType.MESSAGE
    elif ("isTyping" == event):
      eventType = EventType.ISTYPING
    elif ("messageStatus" == event):
      eventType = EventType.MESSAGESTATUS
    elif ("fileStatus" == event):
      eventType = EventType.FILESTATUS
    elif ("response" == event):
      eventType = EventType.RESPONSE
    elif ("alias" == event):
      eventType = EventType.ALIAS
    elif ("newUser" == event):
      eventType = EventType.NEWUSER
    else:
      self.logger.warn("Invalid event type: {}".format(event))
      raise Exception("Invalid event type")

    if eventType in self.eventHandlers:
      self.eventHandlers[eventType](body)
    else:
      self.logger.debug("No event handler register for event type: {}".format(eventType))

  def sendMessage(self, messageContact, content, suggestions = None):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " +  self.accessToken
    }

    message = {
      "RCSMessage": {},
      "messageContact": messageContact.generate()
    }

    if (type(content) == str):
      message["RCSMessage"]["textMessage"] = content
    elif (isinstance(content, Richcard)):
      message["RCSMessage"]["richcardMessage"] = content.generate()
    elif (isinstance(content, RichcardCarousel)):
      message["RCSMessage"]["richcardMessage"] = content.generate()
    elif (isinstance(content, FileMessage)):
      message["RCSMessage"]["fileMessage"] = content.generate()
    elif (isinstance(content, AudioMessage)):
      message["RCSMessage"]["audioMessage"] = content.generate()
    elif (isinstance(content, GeolocationPushMessage)):
      message["RCSMessage"]["geolocationPushMessage"] = content.generate()
    else:
      raise Exception("Unsupported content type")

    if suggestions != None:
      message["RCSMessage"]["suggestedChipList"] = {
        "suggestions": suggestions.generate()
      }

    r = requests.post(self.apiUrl + "/" + self.botId + "/messages",
        headers=headers, data=json.dumps(message))

    if r.status_code != 202:
        raise("Unexpected status code")

  def startTyping(self, messageContact):
    return

  def stopTyping(self, messageContact):
    return

  def getMessageStatus(self, messageId):
    return

  def updateMessageStatus(self, messageId, status):
    return

  def getContactCapabilities(self, userContact, chatId):
    return

  def uploadFile(self, path, url, fileType, until):
    return

  def deleteFile(self, fileId):
    return

  def getFile(self, fileId):
    return

