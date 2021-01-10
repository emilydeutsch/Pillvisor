import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

lcd_rs = digitalio.DigitalInOut(board.D5)
lcd_en = digitalio.DigitalInOut(board.D6)
lcd_d4 = digitalio.DigitalInOut(board.D12)
lcd_d5 = digitalio.DigitalInOut(board.D13)
lcd_d6 = digitalio.DigitalInOut(board.D19)
lcd_d7 = digitalio.DigitalInOut(board.D16)
lcd_columns = 16
lcd_rows = 2

lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6,
                                      lcd_d7, lcd_columns, lcd_rows)
while True:
    lcd.message = "hello"


# import Adafruit_CharLCD as LCD
# 
# #16x2 LCD display
# lcd_rs        = 5 
# lcd_en        = 6
# lcd_d4        = 12
# lcd_d5        = 13
# lcd_d6        = 19
# lcd_d7        = 26
# lcd_backlight = 4
# lcd_columns = 16
# lcd_rows = 2
# lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
# 
# # writing to the LCD display
# lcd.message('Motrin')