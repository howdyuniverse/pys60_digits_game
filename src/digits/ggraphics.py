import appuifw
import graphics

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
