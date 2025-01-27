import pygame
import time
import GridSystem as grid
import UI as uIScript

# Initialize Pygame
pygame.init()
# Initialize the mixer
pygame.mixer.init()
FPS = 60
FIXED_TIME_STEP = 1 / FPS *2
infoObject = pygame.display.Info()
screenWidth = infoObject.current_w; screenHeight = infoObject.current_h
SIZE = min(screenWidth, screenHeight)
#17x17 grid(diameter = size/divisions)
gridDiameter = (SIZE-1/10**10)/15
inputDelay = 0.01
win = pygame.display.set_mode((screenWidth, screenHeight), pygame.FULLSCREEN, pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption("STH")
#No of nodes = size/diameter
grid.Initialize(SIZE, (screenWidth, screenHeight), gridDiameter)
#Creating GameObjects
import GameObjects as gObj
player = gObj.player = gObj.CreatePlayer()
gObj.CreateBoundaries()
sprites = gObj.sprites
uI = uIScript.UI(win, gObj)
showInfo = False

background = sprites.AnimatedSprite("Background/", 1800, _scale = (SIZE, SIZE))
background.RandomizeSprites(); background.randomizeOnEnd = True
gObj.animations.append(background)
gObj.highScore = gObj.load_high_score()

# Load and play background music
musicFiles = [sprites.resourcePath("Data/Music/cyberpunk-music-277931.mp3"),
              sprites.resourcePath("Data/Music/dark-synthwave-spectral-251688.mp3")]

def Main():
    #?Game loop
    global showInfo
    clock = pygame.time.Clock()
    player.WaitForInput()
    run = True; num = 0; t = 0; a=1*FPS
    accumulator = 0.0
    last_time = time.time()
    ZoomedBack = False

    while(run):
        if(player.health <= 0): ResetGame() #?Game Over
        current_time = time.time()
        frame_time = current_time - last_time
        last_time = current_time
        accumulator += frame_time
        num+=1

        for event in pygame.event.get():
            if(event.type == pygame.QUIT): run = False #?Game is trying to close
            if(event.type == pygame.KEYDOWN and num > FPS*inputDelay):
                num = 0
                if(event.key == pygame.K_k): run = False #?quit Game key
                player.Input(event)
                
                if(gObj.shake_duration <= 0):
                    gObj.trigger_screen_shake(0.5, 1)
                if not ZoomedBack:
                    #?Game has Started
                    PlayRandomTrack()
                    gObj.SmoothZoom(target_in=1.5, target_out=1.0, speed=0.02)
                    ZoomedBack = True
                if(event.key == pygame.K_h): showInfo = True

            if(event.type == pygame.KEYUP):
                if(event.key == pygame.K_h): showInfo = False
        
        while accumulator >= FIXED_TIME_STEP:
            #?Main logic
            player.Movement()
            #?Animation
            a-=1
            if(a < 0 and player.parts[0].animatedSprite == player.defAnim):
                player.SwitchToIdleAnim()
                a = gObj.random.randrange(3, 8)*FPS
            for animation in gObj.animations:
                animation.Update()
            # Update zoom factor
            if gObj.zoom_triggered: gObj.UpdateZoom()
            gObj.apply_screen_shake()
            accumulator -= FIXED_TIME_STEP
        #?Collision Delay
        if(player.damageDelay > 0):
            head = player.parts[0]
            player.damageDelay -= 1
            if(player.damageDelay <= 0 and head.position == head.target):
                player.Collision()
        #?SpawnEnemy
        if(len(gObj.enemies) < 4):
            if(len(gObj.enemies)<=2): t-=1
            t-=1
            if(t < 0):
                gObj.SpawnEnemies.SpawnRandEnemy()
                t = gObj.random.randrange(1, 5)*FPS
        #?Drawing
        DrawWindow()
        uI.draw()
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()

def DrawWindow():
    win.fill((0, 0, 0))
    shakeX, shakeY = gObj.shake_x, gObj.shake_y
    wTopL = grid.wTopLeft.wPosition
    rect = pygame.Rect(wTopL[0], wTopL[1], SIZE, SIZE)
    # Draw background
    scaled_sprite, offset_x, offset_y = gObj.ScaleSpriteToZoom(background.curSprite)
    background_center_x = rect.x + shakeX - offset_x + scaled_sprite.get_width() // 2
    background_center_y = rect.y + shakeY - offset_y + scaled_sprite.get_height() // 2
    win.blit(scaled_sprite, (rect.x + shakeX - offset_x, rect.y + shakeY - offset_y))

    '''#Grid System
    for node in grid.nodes:
        rect = pygame.Rect(node.wPosition[0], node.wPosition[1], gridDiameter/1.01, gridDiameter/1.01)
        pygame.draw.rect(win, (150, 150, 150), rect)'''
    #Boundary
    #for bound in gObj.boundaries:
    #    win.blit(bound.sprite, (bound.rect.x + shakeX, bound.rect.y + shakeY))
    #BlockedDir
    '''for enemy in gObj.enemies:
        for dir in enemy.blocksFromDir:
            if(dir == (0, 0)): continue
            rect = pygame.Rect(enemy.wPosition[0] + dir[0]*gridDiameter, enemy.wPosition[1] + dir[1]*gridDiameter, gridDiameter/2, gridDiameter/2)
            rect.center = grid.NodeFromPos(rect.center).position
            pygame.draw.rect(win, (235, 82, 52), rect)'''
    #Enemies
    for enemy in gObj.enemies:
        scaled_sprite, offset_x, offset_y = gObj.ScaleSpriteToZoom(enemy.animatedSprite.curSprite)
        enemy_center_x = enemy.rect.x + shakeX - offset_x + scaled_sprite.get_width() // 2
        enemy_center_y = enemy.rect.y + shakeY - offset_y + scaled_sprite.get_height() // 2
        win.blit(scaled_sprite, (background_center_x + (enemy_center_x - background_center_x) * gObj.zoom_factor - scaled_sprite.get_width() // 2,
                                 background_center_y + (enemy_center_y - background_center_y) * gObj.zoom_factor - scaled_sprite.get_height() // 2))
    #Player
    parts = [player.parts[0], player.parts[-1]]
    for part in parts:
        sprite = part.animatedSprite
        if sprite.orientation != part.orientation:
            sprite.CorrectSpriteRotation()
        scaled_sprite, offset_x, offset_y = gObj.ScaleSpriteToZoom(sprite.curSprite)
        part_center_x = part.rect.x + shakeX - offset_x + scaled_sprite.get_width() // 2
        part_center_y = part.rect.y + shakeY - offset_y + scaled_sprite.get_height() // 2
        win.blit(scaled_sprite, (background_center_x + (part_center_x - background_center_x) * gObj.zoom_factor - scaled_sprite.get_width() // 2,
                                 background_center_y + (part_center_y - background_center_y) * gObj.zoom_factor - scaled_sprite.get_height() // 2))
    
    for part in player.parts[1:-1]:
        sprite = part.animatedSprite
        if sprite.orientation != part.orientation:
            sprite.CorrectSpriteRotation()
        scaled_sprite, offset_x, offset_y = gObj.ScaleSpriteToZoom(sprite.curSprite)
        part_center_x = part.rect.x + shakeX - offset_x + scaled_sprite.get_width() // 2
        part_center_y = part.rect.y + shakeY - offset_y + scaled_sprite.get_height() // 2
        win.blit(scaled_sprite, (background_center_x + (part_center_x - background_center_x) * gObj.zoom_factor - scaled_sprite.get_width() // 2,
                                 background_center_y + (part_center_y - background_center_y) * gObj.zoom_factor - scaled_sprite.get_height() // 2))
    
    for fx in gObj.specialFx:
        win.blit(fx.curSprite, (fx.pos[0] + shakeX, fx.pos[1] + shakeY))

    # Draw the info text
    global showInfo
    if(showInfo):
        win.blit(gObj.infoSprite, (wTopL[0] + shakeX, wTopL[1] + shakeY))
    '''pos = grid.NodeFromPos(player.parts[0].target).wPosition
    rect = pygame.Rect(pos[0], pos[1], gridDiameter, gridDiameter)
    pygame.draw.rect(win, (235, 82, 52), rect)'''
    #Unwakable Nodes
    '''for node in grid.nodes:
        if(node.walkable == True): continue
        rect = pygame.Rect(node.wPosition[0], node.wPosition[1], gridDiameter/1.01, gridDiameter/1.01)
        pygame.draw.rect(win, (168, 50, 60), rect)'''

def ResetGame():
    global player, gObj, uI, ZoomedBack
    player = gObj.player = gObj.CreatePlayer()  # Reinitialize player
    uI = uIScript.UI(win, gObj)  # Reinitialize UI
    gObj.enemies.clear()
    gObj.update_high_score()
    gObj.score = 0
    pygame.mixer.music.stop()
    gObj.SmoothZoom(target_in=1.49, target_out=1.5, speed=100)
    Main()  # Restart the main game loop


def PlayRandomTrack():
    pygame.mixer.music.load(gObj.random.choice(musicFiles))
    pygame.mixer.music.set_volume(0.07)
    pygame.mixer.music.play(-1)

Main()