# Seiketsu-API

## Installation

Install the library using `pip`:

```
pip install seiketsu-api
```

## Usage

First, import the `ApiSeiketsu` class from the library:

```python
from api_seiketsu import ApiSeiketsu, ApiSeiketsuImage
```

### Initialize the ApiSeiketsu object

In the token field, insert your token, or the public one: `3rnPH1ooGMjui9fwf8y4Ueta9ivDJfbae0lTNtMRGoRddzMAhKDr=dgq7yyfJR8v`

Create an instance of the `ApiSeiketsu` class:

```python
token = 'your_token'
seiketsu = ApiSeiketsu(token)

```

### Read message

To get the latest message, call the `read_message` method:

```python
sender, message_text = seiketsu.read_message()
```

`sender` contains the sender's nickname, `message_text` contains the text of the message.


If you want `read_message` to run all the time you can loop:

```python
while True:
    sender, message_text = seiketsu.read_message()
    print(f'{sender}: {message_text}')
```

### Write message

To write a new chat message, call the `write_message` method, passing `alias` and `message_text` as arguments:

```python
seiketsu.write_message(alias="John", message_text="Hello, world!")
```

### Upload image

To upload an image, call the `upload_image` method, passing the image file as an argument.

```python
seiketsuImage = ApiSeiketsuImage()
image_file = open('C:\\folder\\image.png', 'rb')   # Use the correct file path to your image
image_url = seiketsuImage.upload_image(image_file)   # Call the upload_image function to upload the image
```

To display an image in chat, use the `write_message` method.

## Example

Here is a simple example demonstrating the use of the Seiketsu-API. Reads the last message, checks if the bot wrote it himself, if not, repeats it.

```python
from api_seiketsu import ApiSeiketsu

token = '3rnPH1ooGMjui9fwf8y4Ueta9ivDJfbae0lTNtMRGoRddzMAhKDr=dgq7yyfJR8v'
seiketsu = ApiSeiketsu(token) # Initialize seiketsu API

aliasBot = "TestBot" # Name for Bot

while True:
    # Waiting for a new message
    sender, message = seiketsu.read_message()

    # Checking that this is not a message from a bot
    if sender != aliasBot + '#BOT':
        # Sending a reply message
        seiketsu.write_message(alias=aliasBot, message_text=message)

    # Message output to console
    print(f'Repeated message: {aliasBot}: {message}')
```
