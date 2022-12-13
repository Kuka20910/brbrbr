#Создай собственный Шутер!
from pygame import*
from random import*
from  time import time as timer
w_h = 700
w_v = 500
monsters = sprite.Group()
assters = sprite.Group()
bulls = sprite.Group()
lost = 0
score = 0
font.init()
class GS(sprite.Sprite):
    def __init__ (self,p_i,p_x,p_y,p_s,size_x,size_y):
        super().__init__()
        self.image = transform.scale(image.load(p_i),(size_x,size_y))
        self.speed = p_s
        self.rect = self.image.get_rect()
        self.rect.x = p_x
        self.rect.y = p_y
        self.directs = 'right'
    def reset(self):
        win.blit(self.image,(self.rect.x ,self.rect.y ))
class Player(GS):
    def update(self):
        key_p = key.get_pressed()
        if key_p[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if key_p[K_d] and self.rect.x < 650:
            self.rect.x += self.speed
    def fire(self):
        Bullet = bull('bullet.png', self.rect.centerx,self.rect.top,15,15,20)
        bulls.add(Bullet)
class Enemy(GS):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 690:
            self.rect.y = 0
            self.rect.x = randint(50,450)
            lost = lost+1
class bull(GS):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()
    
    

        
win = display.set_mode((w_h,w_v))
back = transform.scale(image.load('galaxy.jpg'),(700,500))
display.set_caption('Шутер')
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
pl = Player('rocket.png',350,400,10,80,100)
tex_l = font.SysFont(None,36)
tex_f = font.SysFont(None,70)
for i in range(5):
    monster = Enemy('ufo.png',randint(50,450),randint(-40,-5),randint(2,3),100,70)
    monsters.add(monster)
for i in range(3):
    asster = Enemy('asteroid.png',randint(50,450),randint(-40,-5),2,100,70)
    assters.add(asster)
clock = time.Clock()
tex1f = tex_f.render('You lose',1,(255,0,0))
tex2f = tex_f.render('You win',1,(0,255,0))

FPS = 30
no_f = 0
rec = False
game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if no_f < 5 and rec == False:
                    no_f += 1
                    pl.fire()
                if no_f >= 5 and rec == False:
                    l = timer()
                    rec = True


                

    if finish != True:
        win.blit(back,(0, 0))
        pl.reset()
        pl.update()
        monsters.update()
        monsters.draw(win)
        assters.update()
        assters.draw(win)
        if rec == True:
            l1 = timer()
            if l1 - l < 1:
                tex2 = tex_f.render('Rel',1,(0,255,0))
                win.blit(tex2,(250,450))
            else:
                no_f = 0
                rec = False
        tex = tex_l.render('Пропущено:' + str(lost),1,(255,255,255))
        tex1 = tex_l.render('Счет:' + str(score),1,(255,255,255))
        win.blit(tex,(10,30))
        win.blit(tex1,(10,10))
        bulls.draw(win)
        bulls.update()

        spr_list = sprite.groupcollide(monsters,bulls,True,True)
        for i in spr_list:
            score += 1
            monster = Enemy('ufo.png',randint(50,450),randint(-40,-5),randint(2,5),100,70)
            monsters.add(monster)
        if sprite.spritecollide(pl,monsters,False) or sprite.spritecollide(pl,assters,False) or lost >= 3:
            finish = True
            win.blit(tex1f,(250,200))
        if score >= 10:
            finish = True
            win.blit(tex2f,(250,200))
        
        



    display.update()
    clock.tick(FPS)