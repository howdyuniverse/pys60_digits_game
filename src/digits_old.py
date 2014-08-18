import e32
import appuifw
import graphics
import key_codes
import random

class Draw:

  RGB_BLACK = (0,0,0)
  RGB_YELLOW = (255,255,0)
  RGB_RED = (255,0,0)

  def __init__(self, key_callback):
    self.old_screen = appuifw.app.screen
    appuifw.app.screen = "full"
    self.canvas = None
    self.img = None
    self.canvas = appuifw.Canvas(
                    resize_callback = self.cb_handle_resize,
                    redraw_callback = self.cb_handle_redraw,
                    event_callback = key_callback)
    self.init_graphics()
    self.old_body = appuifw.app.body
    appuifw.app.body = self.canvas

  def init_graphics(self):
    #appuifw.note(u"in init", "info")
    self.img = graphics.Image.new(self.canvas.size)
    # Speed up drawing by calculating points beforehands
    #   a1 a2
    #   b1 b2
    #   c1 c2
    self.gPointA1 = (0,0)
    self.gPointA2 = (0,0)
    self.gPointB1 = (0,0)
    self.gPointB2 = (0,0)
    self.gPointC1 = (0,0)
    self.gPointC2 = (0,0)

  def cb_handle_resize(self, aSize=(0,0,0,0)):
    if not self.canvas: return

    if self.img: del self.img
    self.img = graphics.Image.new(self.canvas.size)

    x,y = self.canvas.size
    x1 = 40       # my draw limit at left column
    x2 = x - 40   # my draw limit at right column
    x5 = x/2      # my draw limit at middle column
    y1 = 40       # my draw limit at top row
    y2 = y - 40   # my draw limit at bottom row
    y5 = y/2      # my draw limit at middle row

    self.gPointA1 = (x1, y1)
    self.gPointA2 = (x2, y1)
    self.gPointB1 = (x1, y5)
    self.gPointB2 = (x2, y5)
    self.gPointC1 = (x1, y2)
    self.gPointC2 = (x2, y2)

    self.cb_handle_redraw()

  def cb_handle_redraw(self, aRect=(0,0,0,0)):
    if not self.canvas: return
    if self.img: self.canvas.blit(self.img)

  def clear_display(self):
    self.img.clear(Draw.RGB_BLACK)

  def draw_num(self, aValue, colortype="correct"):
    # Draw a number, stop at negative values
    if aValue < 0: return

    # Set coordinates for drawing new number
    points = []
    if aValue == 0:
      points += self.gPointA1 + self.gPointA2 + self.gPointB2 + self.gPointC2
      points += self.gPointC1 + self.gPointB1 + self.gPointA1
    elif aValue == 1:
      points += self.gPointA2 + self.gPointB2 + self.gPointC2
    elif aValue == 2:
      points += self.gPointA1 + self.gPointA2 + self.gPointB2 + self.gPointB1
      points += self.gPointC1 + self.gPointC2
    elif aValue == 3:
      points += self.gPointA1 + self.gPointA2 + self.gPointB2 + self.gPointB1
      points += self.gPointB2 + self.gPointC2 + self.gPointC1
    elif aValue == 4:
      points += self.gPointA1 + self.gPointB1 + self.gPointB2 + self.gPointA2
      points += self.gPointC2
    elif aValue == 5:
      points += self.gPointA2 + self.gPointA1 + self.gPointB1 + self.gPointB2
      points += self.gPointC2 + self.gPointC1
    elif aValue == 6:
      points += self.gPointA2 + self.gPointA1 + self.gPointC1 + self.gPointC2
      points += self.gPointB2 + self.gPointB1
    elif aValue == 7:
      points += self.gPointA1 + self.gPointA2 + self.gPointC2
    elif aValue == 8:
      points += self.gPointB1 + self.gPointA1 + self.gPointA2 + self.gPointC2
      points += self.gPointC1 + self.gPointB1 + self.gPointB2
    elif aValue == 9:
      points += self.gPointB2 + self.gPointB1 + self.gPointA1 + self.gPointA2
      points += self.gPointC2 + self.gPointC1
    else:
      # Should never get here, but avoid problems anyway
      aValue = 0
      points = self.gPointA1

    color = Draw.RGB_YELLOW
    if colortype == "incorrect":
      color = Draw.RGB_RED
    # Remove old and draw new number
    self.clear_display()
    self.img.line(points, width=40, outline=color)
    self.canvas.blit(self.img)


class Digits(Draw):

  def __init__(self):
    self.numbers = []
    self.alive = 3
    self.curr_numindex = 0
    self.wait = True

    appuifw.app.exit_key_handler = self.quit_game
    appuifw.app.menu = [
      (u"Start", self.start_game),
      (u"Exit", self.quit_game)
    ]

    # init draw class
    Draw.__init__(self, key_callback=self.key_callback)
    #
    self.timer = e32.Ao_timer()
    self.app_lock = e32.Ao_lock()
    self.app_lock.wait()

  def quit_game(self):
    appuifw.app.body = self.old_body
    appuifw.app.screen = self.old_screen
    appuifw.app.exit_key_handler = None
    # interupt timer
    self.timer.cancel()
    self.app_lock.signal()

  def check_num(self, num):
    if num != self.numbers[self.curr_numindex]:
      self.draw_num(num, 'incorrect')
    else:
      self.draw_num(num)
      self.curr_numindex += 1
      # if user finish current number set
      if self.curr_numindex == len(self.numbers)-1:
        self.curr_numindex = 0
        self.wait = False

  def key_callback(self, event):
    if event['keycode'] == key_codes.EKey0:
      self.check_num(0)

    elif event['keycode'] == key_codes.EKey1:
      self.check_num(1)

    elif event['keycode'] == key_codes.EKey2:
      self.check_num(2)

    elif event['keycode'] == key_codes.EKey3:
      self.check_num(3)

    elif event['keycode'] == key_codes.EKey4:
      self.check_num(4)

    elif event['keycode'] == key_codes.EKey5:
      self.check_num(5)

    elif event['keycode'] == key_codes.EKey6:
      self.check_num(6)

    elif event['keycode'] == key_codes.EKey7:
      self.check_num(7)

    elif event['keycode'] == key_codes.EKey8:
      self.check_num(8)

    elif event['keycode'] == key_codes.EKey9:
      self.check_num(9)

  def gen_numbers(self, digitnum):
    #del self.numbers
    self.numbers = []
    for i in range(digitnum+1):
      self.numbers.append(int(random.randrange(10)))

  def show_nums(self, interval):
    """ Show numbers to user with specific interval
    Args:
        interval (float): interval between each showing number
    Return:
        None
    """
    #self.clear_display()
    for num in self.numbers:
      self.timer.after(interval)
      self.clear_display()
      self.timer.after(interval)
      self.draw_num(num)

  def player_turn(self):
    """ Function wait for a user input
    and check if his num is corrent
    """
    self.wait = True
    self.clear_display()
    while self.wait:
      e32.ao_sleep(0.1)

  def set_exit(self):
    self.alive = False

  def start_game(self):
    dig_num = 3
    interval = 1
    while self.alive:
      self.gen_numbers(dig_num)
      self.show_nums(interval)
      self.player_turn()
      dig_num += 1

if __name__ == "__main__":
  digits_game = Digits()
  digits_game.start_game()
  del digits_game