![](https://mr-insane.net/wp-content/uploads/2023/10/NoteClient.png)

Note Client can automate the posting of articles on note. The content of the articles is written using Markdown notation.  

We are currently releasing a beta version. In the beta version, you can use major headings, minor headings, bullet points, paragraph numbers, and horizontal lines. With future updates, customization such as bold text and quotations as well as the insertion of tables of contents will be available.

Note Client's source code is made available under the [MIT license](https://github.com/Mr-SuperInsane/NoteClient/blob/main/LICENSE).

## Documentation

=-=-=in preparation=-=-=

## Requirements

- Python >= 3.7

## Installation

```
pip install note-client
```

## Quick Example

```
from  client.note_client import Note

EMAIL = "Your Email"
PASSWORD = "Your Password"
USER_ID = "Your UserID"

client = Note(email=EMAIL, password=PASSWORD, user_id=USER_ID)

TITLE = "Article title"
FILE_NAME = "Path to the text file containing the article content."
TAG_LIST = ["tag1", "tag2"]

response = client.create_article(title=TITLE, file_name=FILE_NAME, input_tag_list=TAG_LIST)
if response == "success":
    print("Posted successfully")
else:
    print("Error")
```

## Help

For inquiries regarding Note Client, please contact [info@mr-insane.net](info@mr-insane.net)
