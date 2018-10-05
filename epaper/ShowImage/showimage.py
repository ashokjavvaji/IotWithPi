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
    image = Image.open('tajmahal.bmp')
    epd.display_frame(epd.get_frame_buffer(image))

if __name__ == '__main__':
    main()
