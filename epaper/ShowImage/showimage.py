import epd4in2
import Image
import ImageDraw
import ImageFont

EPD_WIDTH = 400
EPD_HEIGHT = 300

def main():
    epd = epd4in2.EPD()
    epd.init()

    # For simplicity, the arguments are explicit numerical coordinates
    #image = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 1)    # 1: clear the frame
    image = Image.open('image3.bmp')
    img = Image.open('hearts1.bmp')
    img_w, img_h = img.size
    bg_w, bg_h = image.size
    #offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    offset = (0,0)
    image.paste(img, offset)
    epd.display_frame(epd.get_frame_buffer(image))


if __name__ == '__main__':
    main()


