import e32
import appuifw
import key_codes
import random
import base64

import ggraphics
import keyboard

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
        self.keyboard = keyboard.Keyboard()
        self.graphics = ggraphics.Graphics(self.keyboard.handle_event)

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
