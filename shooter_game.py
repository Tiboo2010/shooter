from pygame import *
#2.hafta
from random import randint
#5.hafta
from time import time as timer #Yorumlayıcının bu işlevi pygame zaman modülünde aramasını önlemek 


#fontlar ve yazılar
font.init()
#4.hafta
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))


font2=font.Font(None,36)
#--


#Arka plan müziği
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.1)
fire_sound = mixer.Sound('fire.ogg')


#böyle resimlere ihtiyacımız var:
img_back = "galaxy.jpg" #oyunun arka planı
img_hero = "rocket.png" #kahraman
#2.hafta
img_enemy ="ufo.png" #düşman
#4.hafta
img_ast = "asteroid.png"
life = 3#yaşam puanı


score=0
lost=0
#--
#4.hafta
goal=20
#--


#3.hafta
img_bullet = "bullet.png" #mermi
max_lost = 10 #Bu kadar çok şeyi kaçırırsanız kaybettiniz.
#--


#sprite'lar için ebeveyn sınıfı
class GameSprite(sprite.Sprite):
 #Sınıf kurucusu
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #Sınıf yapıcısını (Sprite) çağırın:
        sprite.Sprite.__init__(self)


        # Her sprite image - resim özelliğini depolamalıdır
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed


        # Her sprite, içine yazıldığı dikdörtgenin  rect özelliğini saklamalıdır
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


     #pencereye kahraman çizen yöntem
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


#ana oyuncunun sınıfı
class Player(GameSprite):
   #Sprite'ı klavye oklarıyla kontrol etme yöntemi
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
 # atış yöntemi (orada bir mermi oluşturmak için oyuncunun yerini kullanırız)
    #3.hafta
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


#mermi sprite sınıfı  
class Bullet(GameSprite):
   #düşmanın hareketi
   def update(self):
       self.rect.y += self.speed
       #ekranın kenarına ulaştığında kaybolur
       if self.rect.y < 0:
           self.kill()


#2.hafta
#düşman sınıfını oluştur.
class Enemy(GameSprite):
    def update(self):
        self.rect.y +=self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y =0
            self.rect.x = randint(80, win_width-80)
            lost = lost +1
#--


#Bir pencere oluştur
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load(img_back), (win_width, win_height))


#sozdayem spraytyvolume_up16 / 5.000Çeviri sonuçları# sprite oluştur 
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)


#2.hafta
monsters = sprite.Group()
for i in range(1,6):
    monster =Enemy(img_enemy, randint(80,win_width-80),-40,80,50,randint(1, 5))
    monsters.add(monster)


#--


#5.hafta
#bir grup asteroit sprite oluşturma ()
asteroids = sprite.Group()
for i in range(1, 3):
   asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
   asteroids.add(asteroid)


bullets = sprite.Group()
#--



# "oyun bitti" değişkeni: True olduğunda, sprite ana döngüde çalışmayı durdurur
finish = False
#Ana oyun döngüsü:
run = True #bayrak pencereyi kapat düğmesiyle sıfırlanır
#5.hafta
rel_time = False#şarjdan sorumlu bayrak
num_fire = 0 #mermileri saymak için değişken   
#--
while run:
        #Kapat düğmesindeki olayı tıklayın
    for e in event.get():
        if e.type == QUIT:
            run = False


        #3.hafta
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                #5.hafta 
                #kaç atış yapıldığını ve yeniden yükleme olup olmadığını kontrol edin
                if num_fire < 5 and rel_time == False:
                       num_fire = num_fire + 1
                       fire_sound.play()
                       ship.fire()
                     
                if num_fire  >= 5 and rel_time == False : #eğer oyuncu 5 atış yaptıysa
                       last_time = timer() #bunun gerçekleştiği zamanı tespit ediyoruz
                       rel_time = True #yeniden yükleme bayrağını yerleştiriyoruz


        #--


    if not finish:
        # arka planı güncelliyoruz
        window.blit(background,(0,0))


        #sprite hareketleri üretiyoruz
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()


        ship.reset()
        monsters.draw(window)
        #3.hafta
        #5.haft
        asteroids.draw(window)
        bullets.draw(window)
        
        
        
        
        
        


         #şarj etme
        if rel_time == True:
            now_time = timer() #zamanı okuyoruz
       
            if now_time - last_time < 3:  #3 saniye geçene kadar şarj bilgilerini gösteriyoruz
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0   #mermi sayacını sıfırlıyoruz
                rel_time = False #şarj bayrağını sıfırlıyoruz


        #2.hafta
        text=font2.render("Sayı: "+str(score), True,(255,255,255))
        window.blit(text, (10,20))


        text_lose = font2.render("Iskalanan :"+str(lost),True,(0,255,255))
        window.blit(text_lose, (10,50))


       
        #--
        #4.hafta
        #mermi ve canavarların çarpışmasını kontrol etme (hem canavar hem de mermi dokunulduğunda kaybolur)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            #Bu döngü, canavarlar vurulduğu kadar tekrarlanır
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)


            #5.hafta
            #eğer sprite düşmana dokunursa, canı azalır
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life = life -1
                #--



            #Muhtemel kaybetme durumu: kahramanın ya fazla kaçırması, ya da düşmanla karşılaşmasıdır.
            #yenilgi #5.hafta
        if life == 0 or lost >= max_lost:
            finish = True #kaybettik, arka planı koyduk ve artık spriteları yönetmiyoruz.
            window.blit(lose, (200, 200))


       #kazancınızı kontrol edin: kaç puan aldınız?
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))


        # yaşam sayısına göre farklı bir renk belirliyoruz
        #5.hafta
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)


        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))


       


        display.update()
    #loop her 0,05 saniyede bir çalışır


    #bonus: otomatik oyun yeniden başlatma
    
    else:
        finish = False
        score = 0
        lost = 0
        #5.hafta
        num_fire = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
            #5.hafta
        for a in asteroids:
           a.kill()



        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
            #5.hafta
        for i in range(1, 3):
            asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
            asteroids.add(asteroid)


    #--


    time.delay(50)
