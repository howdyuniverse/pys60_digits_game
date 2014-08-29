"""
    Digits game
    based on pys60_gametemplate:
    https://github.com/howdyworld/pys60_gametemplate

    temporary all classes in one file
"""
import e32
import appuifw
import graphics
import random
import key_codes
import base64

# http://www.mobilenin.com/pys60/resources/ex_use_of_keys_descr.py
class Keyboard(object):

    def __init__(self, onevent=lambda:None):
        self._keyboard_state = {}
        self._downs = {}
        self._onevent = onevent

    def handle_event(self, event):
        if event['type'] == appuifw.EEventKeyDown:
            code = event['scancode']
            if not self.is_down(code):
                self._downs[code]=self._downs.get(code, 0) + 1
            self._keyboard_state[code] = 1

        elif event['type'] == appuifw.EEventKeyUp:
            self._keyboard_state[event['scancode']] = 0

        self._onevent()

    def is_down(self, scancode):
        return self._keyboard_state.get(scancode, 0)

    def pressed(self, scancode):
        if self._downs.get(scancode, 0):
            self._downs[scancode] -= 1
            return True
        return False

    def flush(self):
        for key in self._downs:
            self._downs[key] = 0


class GraphicBase(object):

    def __init__(self, handle_event, bg_color=(0, 0, 0)):
        """ Constructor

        Args:
            redraw (func): function for redrawing game scene
            handle_event (func): keyboard handler
            bg_color (tuple): RGB color
        """

        self.bg_color = bg_color
        #
        self.old_body = appuifw.app.body
        self.canvas = appuifw.Canvas(redraw_callback=self.redraw,
                                     event_callback=handle_event)
        # phone screen width / height
        self.screen_w = self.canvas.size[0]
        self.screen_h = self.canvas.size[1]

        #self.draw = graphics.Draw(self.canvas)
        self.draw = graphics.Image.new(self.canvas.size)
        appuifw.app.body = self.canvas

    def clear_buf(self):
        self.draw.clear(self.bg_color)

    def redraw(self, rect=()):
        if self.draw:
            self.canvas.blit(self.draw)

    def close_canvas(self):
        """ Return old body and destroy drawing objects """

        appuifw.app.body = self.old_body
        #self.canvas = None
        #self.draw = None


class Graphics(GraphicBase):
    """ All drawing logic here """

    RGB_BLACK = (0,0,0)
    RGB_YELLOW = (255,255,0)
    RGB_RED = (255,0,0)
    RGB_ORANGE = (224, 87, 35)

    def __init__(self, keyboard_handler):
        GraphicBase.__init__(self, keyboard_handler)
        self.init_points()

    def init_points(self):
        """ Edge points for lines path that draw number """     

        x1 = 70                   # draw limit at left column
        x2 = self.screen_w - 70   # draw limit at right column
        x5 = self.screen_w / 2    # draw limit at middle column
        y1 = 70                   # draw limit at top row
        y2 = self.screen_h - 70   # draw limit at bottom row
        y5 = self.screen_h / 2    # draw limit at middle row

        self.point_top_left  = (x1, y1)
        self.point_top_right = (x2, y1)

        self.point_mid_left  = (x1, y5)
        self.point_mid_right = (x2, y5)
        
        self.point_btm_left  = (x1, y2)
        self.point_btm_right = (x2, y2)

        self.init_nums_points()

    def init_nums_points(self):
        """ Creates dict with digits as keys
        Each key contains points for drawing line path that represent number.

        Still needs reaftoring?
        """

        self.nums_points = {}
        self.nums_points[0] = [
            self.point_top_left, self.point_top_right, self.point_mid_right,
            self.point_btm_right, self.point_btm_left, self.point_mid_left,
            self.point_top_left
        ]
        self.nums_points[1] = [
            self.point_top_right, self.point_mid_right, self.point_btm_right
        ]
        self.nums_points[2] = [
            self.point_top_left, self.point_top_right, self.point_mid_right,
            self.point_mid_left, self.point_btm_left, self.point_btm_right
        ]
        self.nums_points[3] = [
            self.point_top_left, self.point_top_right, self.point_mid_right,
            self.point_mid_left, self.point_mid_right, self.point_btm_right,
            self.point_btm_left
        ]
        self.nums_points[4] = [
            self.point_top_left, self.point_mid_left, self.point_mid_right,
            self.point_top_right, self.point_btm_right
        ]
        self.nums_points[5] = [
            self.point_top_right, self.point_top_left, self.point_mid_left,
            self.point_mid_right, self.point_btm_right, self.point_btm_left
        ]
        self.nums_points[6] = [
            self.point_top_right, self.point_top_left, self.point_btm_left,
            self.point_btm_right, self.point_mid_right, self.point_mid_left
        ]
        self.nums_points[7] = [
            self.point_top_left, self.point_top_right, self.point_btm_right
        ]
        self.nums_points[8] = [
            self.point_mid_left, self.point_top_left, self.point_top_right,
            self.point_btm_right, self.point_btm_left, self.point_mid_left,
            self.point_mid_right
        ]
        self.nums_points[9] = [
            self.point_mid_right, self.point_mid_left, self.point_top_left,
            self.point_top_right, self.point_btm_right, self.point_btm_left
        ]

    def draw_num(self, number, correct=True):
        """ Drawing number on screen

        Args:
            number (int): value of pressed number 0...9
            correct (bool): flag for number color right/wrong number
        """

        if number < 0 or number > 9:
            return

        color = self.RGB_YELLOW if correct else self.RGB_RED
        self.draw.line(self.nums_points[number], width=30, outline=color)

    def draw_info(self, passed_num, dig_num, best_score, lifes, passed_digs):
        """ Drawing current game info

        Args:
            passed_num (int): passed digits number
            dig_num (int): numbers countdown
            best_score (int): best score number
            lifes (int): lifes counter
            passed_digs (list): last passed numbers, must fit in screen size
        """
        self.draw.text((5, 25),
                        u"NUMS: %s/%s" % (unicode(passed_num), unicode(dig_num)),
                        self.RGB_YELLOW,
                        font=(u'Nokia Hindi S60', 24))
        self.draw.text((5, 40),
                        u"BEST: %s" % unicode(best_score),
                        self.RGB_YELLOW,
                        font=(u'Nokia Hindi S60', 14))
        self.draw.text((self.screen_w - 80, 25),
                        u"LIFES: "+unicode(lifes),
                        self.RGB_YELLOW,
                        font=(u'Nokia Hindi S60', 24))

        # simple passed digits
        if passed_digs:
            digs_str = u""
            for digit in passed_digs[::-1]:
                digs_str += unicode(digit) + u" "
            self.draw.text((5, self.screen_h - 10),
                            digs_str,
                            self.RGB_YELLOW,
                            font=(u'Nokia Hindi S60', 24))

    def draw_gameover(self):
        self.draw.text((self.screen_w * 0.2, self.screen_h * 0.5),
                        u"GAME OVER!",
                        self.RGB_RED,
                        font=(u'Nokia Hindi S60', 32))

    def draw_ready(self):
        self.draw.text((self.screen_w * 0.3, self.screen_h * 0.5),
                        u"READY?",
                        self.RGB_YELLOW,
                        font=(u'Nokia Hindi S60', 32))

    def draw_startscreen(self):
        self.draw.text((5, 40),
                        u"Digits",
                        self.RGB_YELLOW,
                        font=(u'Nokia Hindi S60', 32))
        self.draw.text((self.screen_w * 0.14, self.screen_h * 0.3),
                        u"PRESS 5 TO START",
                        self.RGB_YELLOW,
                        font=(u'Nokia Hindi S60', 24))

    def draw_scores(self, scores):
        """ Draw tabel of best game scores
        Args:
            scores (list): list of tuples with best scores and player names
            for example:
            [(8, u"howdyworld"), (7, u"Valera"), (7, u"Homer"), (6, u"Barney"), (5, u"Ted")]
        """
        self.draw.text((self.screen_w * 0.28, self.screen_h * 0.4),
                        u"HIGHT SCORES",
                        self.RGB_ORANGE,
                        font=(u'Nokia Hindi S60', 18))
        
        pos = self.screen_h * 0.4

        if not scores:
            self.draw.text((self.screen_w * 0.28, pos+20),
                            u"0 -- None",
                            self.RGB_YELLOW,
                            font=(u'Nokia Hindi S60', 14))

        for score in scores:
            score_text = u"%d -- %s" % (score[0], score[1])
            pos += 20
            self.draw.text((self.screen_w * 0.28, pos),
                            score_text,
                            self.RGB_YELLOW,
                            font=(u'Nokia Hindi S60', 14))

class GameCore(object):
    """ All game logic here """

    KEYS = (
        key_codes.EScancode0,
        key_codes.EScancode1, key_codes.EScancode2, key_codes.EScancode3,
        key_codes.EScancode4, key_codes.EScancode5, key_codes.EScancode6,
        key_codes.EScancode7, key_codes.EScancode8, key_codes.EScancode9,
    )

    READY_INTERVAL = 1.5
    SCOREFILE_PATH = "C:\\digits_game.txt"

    def __init__(self):
        self.keyboard = Keyboard()
        self.graphics = Graphics(self.keyboard.handle_event)

        self.numbers = []
        self.start_wait = True
        self.player_wait = True
        self.best_score = 0
        self.last_playername = u"Anonym"
        self.scores = []
        self.load_scores()
        self.init_new_game()

    def tick(self):
        self.start_screen()
        self.gen_nums()
        self.show_nums()
        self.player_turn()

    def load_scores(self):
        """ Load data from file to scores list.
            All records represent as base 64 string.
            For extracting we need decode file line string.
            As result we get data in following form:
            "[score num (int)],[player name (str)]"
        """
        try:
            for line in open(self.SCOREFILE_PATH, "r"):
                score_rec = base64.b64decode(line)
                score_rec = score_rec.split(",")
                if len(score_rec) != 2:
                    continue
                try:
                    score = int(score_rec[0])
                except:
                    continue
                player = score_rec[1]
                self.scores.append((score, player))

            if self.scores:
                # assume that the list is sorted in file, and get first item
                # otherwise leave self.best_score value from constructor
                self.best_score = self.scores[0][0]
        except:
            pass

    def save_scores(self):
        fdata = open(self.SCOREFILE_PATH, "w")
        for score in self.scores:
            score_rec = u"%d,%s" % (score[0], score[1])
            fdata.write(base64.b64encode(score_rec)+"\n")
        fdata.close()

    def check_bestscore(self, score):
        """ Check if current score best than scores stored in self.scores
        Args:
            score (int): score for checking
        """
        if score == 2:
            return
        self.last_playername = appuifw.query(u"Your name", "text", self.last_playername)
        score_rec = (score, self.last_playername)
        self.scores.append(score_rec)
        self.scores.sort(key=lambda item: item[0], reverse=True)
        if len(self.scores) > 5:
            del self.scores[-1]
        self.save_scores()
        self.best_score = self.scores[-1][0]

    def cancel(self):
        self.start_wait = False
        self.player_wait = False

    def quit(self):
        """ Must be called when game ends """

        self.graphics.close_canvas()

    #
    def draw_gamefield(self):
        self.graphics.clear_buf()
        self.graphics.draw_info(self.digits_counter,
                                self.digits_num,
                                self.best_score,
                                self.lifes,
                                self.numbers[:self.digits_counter])

    def init_new_game(self):
        """ Reset all varibales that require new game (first level) """

        self.digits_num = 3
        self.digits_counter = 0
        self.lifes = 3
        self.show_interval = 1.0
        self.start_wait = True

    def start_screen(self):
        """ Display start screen (like main menu) with top 5 scores.
            User can see this screen only when game not started yet.
        """

        # if game in progress skip start screen
        if not self.start_wait:
            return

        self.graphics.clear_buf()
        self.graphics.draw_startscreen()
        self.graphics.draw_scores(self.scores)
        self.graphics.redraw()

        while self.start_wait:
            if self.keyboard.pressed(key_codes.EScancode5):
                self.start_wait = False
            e32.ao_sleep(0.001)

    def player_turn(self):
        """ Player turn loop. Wait for players key pressing. """

        self.keyboard.flush()

        while self.player_wait:
            if self.lifes == 0:
                self.draw_gamefield()
                self.graphics.draw_gameover()
                self.graphics.redraw()
                # check record
                self.check_bestscore(self.digits_num-1)
                #e32.ao_sleep(self.READY_INTERVAL)
                self.init_new_game()
                break

            # process numeric keys, in this keys index is key number 0...9
            # shorter but maybe not quite pythonic, reafactoring recommend
            for index, key in enumerate(self.KEYS):
                if self.keyboard.pressed(key):
                    self.check_num(index)

            e32.ao_sleep(0.1)

        self.player_wait = True

    def next_level(self):
        """ Re-init variables for next level """

        # wait before breaking current level loop and go to the next
        e32.ao_sleep(self.show_interval)

        self.digits_num += 1
        self.digits_counter = 0
        self.player_wait = False
        self.show_interval *= 0.8

    def check_num(self, user_num):
        """ Calls when player press key
        
        Args:
            user_num (int): 
        """

        self.draw_gamefield()
        self.graphics.redraw()
        e32.ao_sleep(0.15)

        if user_num == self.numbers[self.digits_counter]:
            self.digits_counter += 1
            self.draw_gamefield()
            self.graphics.draw_num(user_num, correct=True)
            self.graphics.redraw()

            # if user pass all numbers
            if self.digits_counter == self.digits_num:
                self.next_level()
        else:
            self.lifes -= 1
            self.draw_gamefield()
            self.graphics.draw_num(user_num, correct=False)
            self.graphics.redraw()

    def gen_nums(self):
        """ Generates random numbers 0...9 for self.numbers """

        self.numbers = []
        for i in range(self.digits_num):
            self.numbers.append(int(random.randrange(10)))

    def show_nums(self):
        """ Show numbers to user with specific interval
            
        Note:
            Needs reafactoring. When core cancels, game stucks on for loop.
            Now loop breaks before calling sleep functions. - Not good.
        """
        # check if game core is cancel and game is over
        if not self.player_wait:
            return

        # before showing nums clear display and wait few millisec
        self.draw_gamefield()
        self.graphics.draw_ready()
        self.graphics.redraw()
        e32.ao_sleep(self.READY_INTERVAL)

        for num in self.numbers:
            self.draw_gamefield()
            self.graphics.draw_num(num)
            self.graphics.redraw()

            if not self.player_wait:
                break

            e32.ao_sleep(self.show_interval)
            # show clear screen between numbers
            self.draw_gamefield()
            self.graphics.redraw()

            # wait on clear screen before showing next number
            if not self.player_wait:
                break
            e32.ao_sleep(self.show_interval * 0.25)


class Game(object):

    INTERVAL = 0.08

    def __init__(self, screen_mode="full"):
        """ Constructor

        Args:
            screen_mode (str): normal, large, full
        """

        appuifw.app.screen = screen_mode

        self.game_core = GameCore()

        appuifw.app.menu = [
            (u"Exit", self.set_exit)
        ]
        self.exit_flag = False

    def set_exit(self):
        """ Breaks game loop in self.run function """

        self.game_core.cancel()
        self.exit_flag = True

    def run(self):
        """ Main game loop """

        appuifw.app.exit_key_handler = self.set_exit
        
        while not self.exit_flag:
            self.game_core.tick()
            e32.ao_sleep(self.INTERVAL)

        self.game_core.quit()


if __name__ == "__main__":
    try:
        app = Game()
    except Exception, e:
        appuifw.note(u"Exception: %s" % (e))
    else:
        app.run()
        del app
