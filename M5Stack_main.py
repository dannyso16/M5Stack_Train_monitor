from m5stack import *
from m5stack_ui import *
from uiflow import *
import wifiCfg
import urequests
import time
import json


wifiCfg.autoConnect(lcdShow=True)
screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0x000000)


width_text_area = None
json_data = None
current_time = None
next_time = None
condition = None



image_background = M5Img("res/temp.png", x=0, y=0, parent=None)
label0 = M5Label('label0', x=-9, y=208, color=0x000, font=FONT_MONT_14, parent=None)
label_error = M5Label('error', x=2, y=208, color=0xf30831, font=FONT_MONT_14, parent=None)
label_current_time = M5Label('yy:yy', x=230, y=149, color=0x02faa0, font=FONT_MONT_18, parent=None)
label_next_time = M5Label('xx:xx', x=230, y=67, color=0x02faa0, font=FONT_MONT_22, parent=None)
label_condition = M5Label('STATUS', x=230, y=130, color=0x02faa0, font=FONT_MONT_18, parent=None)




screen.set_screen_brightness(40)
image_background.set_pos(0, 0)
image_background.set_img_src('/sd/base.png')
label_current_time.set_text('')
label_error.set_hidden(True)
width_text_area = 82
while True:
  label_error.set_hidden(True)
  if not (wifiCfg.wlan_sta.isconnected()):
    wifiCfg.reconnect()
  try:
    req = urequests.request(method='GET', url='https://changeHere', headers={}) # TODO Change URL
    json_data = json.loads((req.text))
    current_time = json_data['current_time']
    next_time = json_data['next_time']
    condition = json_data['condition']
    label_current_time.set_text(str(current_time))
    label_next_time.set_text(str(next_time))
    label_condition.set_text(str(condition))
    label_current_time.set_pos((int(((width_text_area - (label_current_time.get_width())) / 2)) + 230), 149)
    label_next_time.set_pos((int(((width_text_area - (label_next_time.get_width())) / 2)) + 230), 67)
    label_condition.set_pos((int(((width_text_area - (label_condition.get_width())) / 2)) + 230), 130)
    gc.collect()
    req.close()
  except:
    label_error.set_hidden(False)
    label_error.set_text('Error: Check the server is running.')
  wait(60)
  wait_ms(2)
