from bingapi import BingAPI


if __name__ == '__main__':
    api = BingAPI()
    images = api.create_images("Blue screen of windows")
    for index, image in enumerate(images):
        image.save(f'image-{index}.jpg')