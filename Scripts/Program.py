import pygame, os
import GridSystem as grid
import UI as uIScript

# Initialize Pygame
pygame.init()
# Initialize the mixer
pygame.mixer.init()
FPS = 60
infoObject = pygame.display.Info()
screenWidth = infoObject.current_w; screenHeight = infoObject.current_h
SIZE = min(screenWidth, screenHeight)
#17x17 grid(diameter = size/divisions)
gridDiameter = (SIZE-1/10**10)/15
inputDelay = 0.01
win = pygame.display.set_mode((SIZE,SIZE), pygame.FULLSCREEN)
pygame.display.set_caption("STH")
#No of nodes = size/diameter
grid.Initialize(SIZE, (screenWidth, screenHeight), gridDiameter)
#Creating GameObjects
import GameObjects as gObj
player = gObj.player = gObj.CreatePlayer()
gObj.CreateBoundaries()
uI = uIScript.UI(win, gObj)

background = gObj.sprites.AnimatedSprite("Background/", 1800, _scale = (SIZE, SIZE))
background.RandomizeSprites(); background.randomizeOnEnd = True
gObj.animations.append(background)
gObj.highScore = gObj.load_high_score()

# Load and play background music
musicFiles = [gObj.sprites.resourcePath("Data/Music/cyberpunk-music-277931.mp3"),
              gObj.sprites.resourcePath("Data/Music/dark-synthwave-spectral-251688.mp3")]

def Main():
    #?Game loop
    clock = pygame.time.Clock()
    player.WaitForInput()
    run = True; num = 0; t = 0; a=3*FPS
    PlayRandomTrack()

    while(run):
        if(player.health <= 0): ResetGame() #?Game Over
        clock.tick(FPS)
        num+=1
        for event in pygame.event.get():
            if(event.type == pygame.QUIT): run = False #?Game is trying to close
            if(event.type == pygame.KEYDOWN and num > FPS*inputDelay):
                num = 0
                if(gObj.shake_duration <= 0):
                    gObj.trigger_screen_shake(0.5, 1)
                player.Input(event)
                
        #?SpawnEnemy
        if(len(gObj.enemies) < 4):
            if(len(gObj.enemies)<=2): t-=1
            t-=1
            if(t < 0):
                gObj.SpawnEnemies.SpawnRandEnemy()
                t = gObj.random.randrange(1, 5)*FPS
        #?Main logic
        player.Movement()
        #?Animation
        a-=1
        if(a < 0 and player.parts[0].animatedSprite == player.defAnim):
            player.SwitchToIdleAnim()
            a = gObj.random.randrange(3, 8)*FPS
        for animation in gObj.animations:
            animation.Update()
        #?Collision Delay
        if(player.damageDelay > 0):
            head = player.parts[0]
            player.damageDelay -= 1
            if(player.damageDelay <= 0 and head.position == head.target):
                player.Collision()

        #?Drawing
        DrawWindow()
        uI.draw()
        pygame.display.update()
    pygame.quit()

def DrawWindow():
    win.fill((0, 0, 0))
    shakeX, shakeY = gObj.apply_screen_shake()
    pos = grid.wTopLeft.wPosition
    rect = pygame.Rect(pos[0], pos[1], SIZE, SIZE)
    win.blit(background.curSprite, (rect.x + shakeX, rect.y + shakeY))
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
        win.blit(enemy.animatedSprite.curSprite, (enemy.rect.x + shakeX, enemy.rect.y + shakeY))
    #Player
    for part in player.parts:
        sprite = part.animatedSprite
        if(sprite.orientation != part.orientation):
            sprite.CorrectSpriteRotation()
        win.blit(sprite.curSprite, (part.rect.x + shakeX, part.rect.y + shakeY))
    
    for fx in gObj.specialFx:
        win.blit(fx.curSprite, (fx.pos[0] + shakeX, fx.pos[1] + shakeY))
    '''pos = grid.NodeFromPos(player.parts[0].target).wPosition
    rect = pygame.Rect(pos[0], pos[1], gridDiameter, gridDiameter)
    pygame.draw.rect(win, (235, 82, 52), rect)'''
    #Unwakable Nodes
    '''for node in grid.nodes:
        if(node.walkable == True): continue
        rect = pygame.Rect(node.wPosition[0], node.wPosition[1], gridDiameter/1.01, gridDiameter/1.01)
        pygame.draw.rect(win, (168, 50, 60), rect)'''

def ResetGame():
    global player, gObj, uI
    player = gObj.player = gObj.CreatePlayer()  # Reinitialize player
    uI = uIScript.UI(win, gObj)  # Reinitialize UI
    gObj.enemies.clear()
    gObj.update_high_score()
    gObj.score = 0
    pygame.mixer.music.stop()
    PlayRandomTrack()
    Main()  # Restart the main game loop


def PlayRandomTrack():
    pygame.mixer.music.load(gObj.random.choice(musicFiles))
    pygame.mixer.music.set_volume(0.07)
    pygame.mixer.music.play(-1)

Main()