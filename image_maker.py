from PIL import Image, ImageFont, ImageDraw
import requests
import io


CONTEXT = {
    "first_name": "БИба",
    "last_name": "Боба",
    "date": "2007-11-01",
    "flight_time": "15:30",
    "flight_number": "AA11",
    "from_city": "Moscow",
    "to_city": "Helsinki",
    "photo_url": 'https://sun1-83.userapi.com/impg/0Fg-k8HMgFqcmHybvUsi15CoA92gwbxnxipHCQ/zNR32gBpZ38.jpg?size=100x0&quality=96&crop=138,190,1343,1343&sign=1cce1ca2b97dd06af446bdb25f506582&c_uniq_tag=ijpfTO8qwB9U0R0fyIBeSIIEh9m3NZ124YabnCWoBVk&ava=1'

}


class ImageMaker:
    def __init__(self, _path):
        self.image = Image.open(_path)

    def draw_postcard(self, context):
        font = ImageFont.truetype("external_data/Roboto-Regular.ttf", 28)
        d = ImageDraw.Draw(self.image)
        d.text((200, 185), context["first_name"] + ' ' + context["last_name"], fill="black", anchor="ls", font=font)
        d.text((200, 235), context["flight_number"], fill="black", anchor="ls", font=font)
        d.text((200, 285), context["from_city"], fill="black", anchor="ls", font=font)
        d.text((200, 335), context["to_city"], fill="black", anchor="ls", font=font)
        d.text((200, 385), context["date"] + ' ' + context["flight_time"], fill="black", anchor="ls", font=font)

        photo = Image.open(io.BytesIO(requests.get(context["photo_url"]).content))

        self.image.paste(im=photo, box=(20, 20, 120, 120))
        self.image.show()


if __name__ == '__main__':
    im = ImageMaker('external_data/template.png')
    im.draw_postcard(CONTEXT)
