from app_display_image import app 
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/anwesh/Desktop/webapp/")
app.secret_key = '\xcd\xf8%\x06\xbaQ\x13`\xae\x81p\xbd\xd65.\xb4\x1b\x7ft=\xf0\x10\xdet'

if __name__ == "__main__":
    app.run()

