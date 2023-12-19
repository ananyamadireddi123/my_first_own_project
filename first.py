import pygame

pygame.init()

screen_width=800
screen_height=600

screen=pygame.display.set_mode((screen_width,screen_height)) # to display a screen of required width and height

player=pygame.Rect((0,0,20,20))  # (distance from top, distance from left, width, height) 

cond=True

while cond:
    screen.fill((0,0,0))  # for the rectange not to remember its past, i.e. it fills the past of that rectangle with backgound color
    pygame.draw.rect(screen,(255,200,200),player)  # (255,200,200) this is a color code for the rectangle
    
    key=pygame.key.get_pressed()
    if key[pygame.K_a] == True:
        player.move_ip(-0.5,0)
    elif key[pygame.K_s] == True:
        player.move_ip(0,0.5)
    elif key[pygame.K_d] == True:
        player.move_ip(0.5,0)
    elif key[pygame.K_w] == True:
        player.move_ip(0,-0.5)
                    
    
    for x in pygame.event.get():
        if x.type == pygame.QUIT:
            cond=False
        # elif x.type == pygame.KEYDOWN:
        #     print("Key is pressed")
        # elif x.type == pygame.KEYUP:
        #     print("Key is released")        
            
    pygame.display.update()     # necessary to update the changes caused in the screen   

pygame.quit()            