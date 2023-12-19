import os
import pygame as pg

if not pg.font:
    print("Warning, fonts disabled")
if not pg.mixer:
    print("Warning, sound disabled")

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

def load_image(name, colorkey=None, scale=1):
    fullname = os.path.join(data_dir, name)
    image = pg.image.load(fullname)

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self):
            pass

    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()

    fullname = os.path.join(data_dir, name)
    sound = pg.mixer.Sound(fullname)

    return sound

class Fist(pg.sprite.Sprite):
    """moves a clenched fist on the screen, following the mouse"""

    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image("fist.png", -1,0.2)
        self.fist_offset = (-235, -80)
        self.punching = False

    def update(self):
        """move the fist based on the mouse position"""
        pos = pg.mouse.get_pos()
        self.rect.topleft = pos
        self.rect.move_ip(self.fist_offset)
        if self.punching:
            self.rect.move_ip(15, 25)

    def punch(self, target):
        """returns true if the fist collides with the target"""
        if not self.punching:
            hitbox_width = 30
            hitbox_height = 30
            hitbox = pg.Rect(self.rect.x, self.rect.y, hitbox_width, hitbox_height)
            return hitbox.colliderect(target.rect)

    def unpunch(self):
        """called to pull the fist back"""
        self.punching = False
        
class Chimp(pg.sprite.Sprite):
    """moves a monkey critter across the screen. it can spin the
    monkey when it is punched."""

    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image("chimp.png", -1, 0.3)
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 90
        self.move = 18
        self.dizzy = False

    def update(self):
        """walk or spin, depending on the monkeys state"""
        if self.dizzy:
            self._spin()
        else:
            self._walk()

    def _walk(self):
        """move the monkey across the screen, and turn at the ends"""
        newpos = self.rect.move((self.move, 0))
        if not self.area.contains(newpos):
            if self.rect.left < self.area.left or self.rect.right > self.area.right:
                self.move = -self.move
                newpos = self.rect.move((self.move, 0))
                self.image = pg.transform.flip(self.image, True, False)
        self.rect = newpos

    def _spin(self):
        """spin the monkey image"""
        center = self.rect.center
        self.dizzy = self.dizzy + 12
        if self.dizzy >= 360:
            self.dizzy = False
            self.image = self.original
        else:
            rotate = pg.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center=center)

    def punched(self):
        """this will cause the monkey to start spinning"""
        if not self.dizzy:
            self.dizzy = True
            self.original = self.image        
def main_function():
    pg.init()
    score=0
    screen = pg.display.set_mode((1500, 600), pg.SCALED)
    pg.display.set_caption("Monkey Fever")
    pg.mouse.set_visible(False)

    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 200, 200))

# to put text on the background
    if pg.font:
        font = pg.font.Font(None, 64)
        text = font.render("Hit The Monkey, And Win!!!", True, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width() / 2, y=10)
        background.blit(text, textpos)
        text1 = font.render("Points:",True,(5,5,5))
        textpos1=text.get_rect(centerx=background.get_width() / 2, y=55)
        background.blit(text1, textpos1)
        
    
    screen.blit(background, (0, 0))
    pg.display.flip()    
    
    whiff_sound = load_sound("whiff.wav")
    punch_sound = load_sound("punch.wav")
    clap_sound=load_sound("claps.wav")
    
    chimp = Chimp()
    fist = Fist()
    allsprites = pg.sprite.Group()
    allsprites.add(chimp)
    allsprites.add(fist)
    clock = pg.time.Clock()
    flag=0
    going = True
    while going:
        clock.tick(60)
        if pg.font:
            background.fill((255, 200, 200))
            font = pg.font.Font(None, 64)
            text = font.render("Hit The Monkey, And Win!!!", True, (10, 10, 10))
            textpos = text.get_rect(centerx=background.get_width() / 2, y=10)
            background.blit(text, textpos)
            text1 = font.render("Points:",True,(5,5,5))
            textpos1=text.get_rect(centerx=background.get_width() / 2, y=55)
            background.blit(text1, textpos1)
            score_text = font.render(str(score), True, (5, 5, 5))
            scorepos = textpos.move(text1.get_width() + 10,50)  # Adjust the position as needed
            background.blit(score_text, scorepos)
            pg.display.update()
            
        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                going = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if fist.punch(chimp):
                    punch_sound.play()  # punch
                    chimp.punched()
                    score=score+20
                else:
                    whiff_sound.play()  # miss
                    score=score-10
            elif event.type == pg.MOUSEBUTTONUP:
                fist.unpunch()
        if score>1000==0 and score != 0 and flag==0:
            clap_sound.play() 
            flag=1   
        allsprites.update()
        # print(f"Fist position: {fist.rect.topleft}")
        # print(f"Chimp position: {chimp.rect.topleft}")
  
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pg.display.flip()   
        
    pg.quit()
    
if __name__ == "__main__":
    main_function()    
