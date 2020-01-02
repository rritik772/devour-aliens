import sys
import pygame
from time import sleep
from settings import Settings
from ship import Ship
from game_stats import GameStats
from bullet import Bullet
from alien import Alien



class AlienInvasion: 


    def __init__(self):
        pygame.init() 
        self.settings =Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.ship=Ship(self)
        self.bullets =pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()
        self._create_fleet()
        self.stats=GameStats(self)
        self.game_active=True
                


    def run_game(self):        
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            
            
    def _check_events(self):
        """Respond to keypresses and mouse events"""

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)

                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                
                
    def _check_keydown_events(self,event):
        if event.key ==pygame.K_RIGHT:
            self.ship.moving_right=True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left=True
        elif event.key ==pygame.K_q:
            sys.exit()
        elif event.key==pygame.K_SPACE:
            self._fire_bullet()

    
    
    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right=False
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=False

    def _fire_bullet(self):
        if len(self.bullets)<self.settings.bullet_allowed:
            new_bullet =Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
                if bullet.rect.bottom<=0:
                    self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """responds to any bullet collision"""
        #remove any bullet collion
        collisions =pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            
                    
    def _update_screen(self):
        pygame.display.flip()
        self.screen.fill(self.settings.bgcolor)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
    
    def _create_fleet(self):
        alien = Alien(self)
        alien_width,alien_height=alien.rect.size

        #determine the number of columns of alien that fit on the screen
        avaliable_space_x=self.settings.screen_width-(2*alien_width)
        number_aliens_x=avaliable_space_x //(2*alien_width)

        #deterine the number of rows of aliend that fit on the screen
        ship_height=self.ship.rect.height
        avaliable_space_y =(self.settings.screen_height-(3*alien_height)-ship_height)
        number_row =avaliable_space_y//(2*alien_height)

        for row_number in range (number_row):
            for alien_number in range (number_aliens_x):
                self._create_alien(alien_number,row_number)

    def _create_alien(self,alien_number,row_number):
        '''Create an alien and place it in a row'''
        alien=Alien(self)
        alien_width, alien_hight =alien.rect.size
        alien.x =alien_width+2*alien_width*alien_number
        alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
        alien.rect.x=alien.x
        self.aliens.add(alien)

    def _update_aliens(self):
        
        """check if the fleet is at the edge,
        then update the position of all the alien in the fleet"""
        self._check_fleet_edge()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        
        self._check_aliens_bottom()


    def _check_fleet_edge(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """drop the entire fleet and change the fleet direction"""
        for alien in self.aliens.sprites():
            alien.rect.y+=self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        if self.stats.ships_left>0:
            self.stats.ship_left=-1

            self.aliens.empty()
            self.bullets.empty

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        
        else:
            self.stats.game_active =False
    
    def _check_aliens_bottom(self):
        screen_rect=self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom>=screen_rect.bottom:
                self._ship_hit()
                break

        

            

if __name__=="__main__":
    ai=AlienInvasion()
    ai.run_game()
