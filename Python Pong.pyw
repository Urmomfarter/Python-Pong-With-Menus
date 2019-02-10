import pygame, sys, time, math, os
import random
from random import randint as rand
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()
pygame.font.init()

gameIcon = pygame.image.load(r"C:\Users\urmom\Pictures\Python Pong Icon.ico")
pygame.display.set_icon(gameIcon)

WelcomeTitle = pygame.image.load(r"C:\Users\urmom\Pictures\Python Pong.png")
StartButton = pygame.image.load(r"C:\Users\urmom\Pictures\Retro Start.png")
SettingsButton = pygame.image.load(r"C:\Users\urmom\Pictures\Retro Settings.png")
BackButton = pygame.image.load(r"C:\Users\urmom\Pictures\Retro Back.png")
DiffButton = pygame.image.load(r"C:\Users\urmom\Pictures\Retro Difficulty.png")
ExitButtonInMenu = pygame.image.load(r"C:\Users\urmom\Pictures\Retro exit.png")
ExitBox = pygame.image.load(r"C:\Users\urmom\Pictures\Retro AreYouSure.png")
GoToMenu = pygame.image.load(r"C:\Users\urmom\Pictures\Retro Go To Menu.png")
YouLose = pygame.image.load(r"C:\Users\urmom\Pictures\Retro You Lose.png")
YouWin = pygame.image.load(r"C:\Users\urmom\Pictures\Retro You Win.png")
PlayAgain = pygame.image.load(r"C:\Users\urmom\Pictures\Retro Play Again.png")
GamePaused = pygame.image.load(r"C:\Users\urmom\Pictures\Retro Game Paused.png")

#800x600 looks good
fps = 600
fullscreen = 0
if not fullscreen:
    display_width = 800
    display_height = 600
else:
    display_width = 1600
    display_height = 900
####
Difficulty = 0 #Will be used later
os.environ['SDL_VIDEO_CENTERED'] = '1'
DISPLAY = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Python Pong")
clock = pygame.time.Clock()

ButtonScale = int((math.sqrt(display_width ** 2 + display_height ** 2) / 11)/5)

startTime = time.time()


startupMusic = pygame.mixer.Sound(r"C:\Users\urmom\Music\8 bit Gamecube startup.wav")
BlipSound = pygame.mixer.Sound(r"C:\Users\urmom\Music\Pong Blip.wav")
MissSound = pygame.mixer.Sound(r"C:\Users\urmom\Music\Pong Miss Hum.wav")

if fullscreen:
    DISPLAYSURF = pygame.display.set_mode((1600, 900), pygame.FULLSCREEN)

#####
p_score = 0
b_score = 0
#####
def chooseFont(a,b):
    return pygame.font.SysFont(str(a), int(b))
class userRectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

isClick = 0
paddleH = int(display_height / 20 + 40.5) * 1
x_start, y_start, x, y,x_stop,y_stop = (),(),(),(),(),()
botMult = 1
GoToGame = 0

def centerX(width):
    global display_width
    return int(display_width/2 - width/2)

def withinCenter(Box_x,Box_y,Box_w,Box_h): #Assuming button is centered
    global x_start,y_start,x_stop,y_stop,display_width,display_height
    
    if x_start >= Box_x and x_stop >= Box_x and x_start <= Box_x + Box_w and  x_stop <= Box_x + Box_w: #Click within x
        if y_start >= Box_y and y_stop >= Box_y and y_start <= Box_y + Box_h and  y_stop <= Box_y + Box_h:
            return 1
    return 0

def startMenu(a):
    global isClick, x_start, y_start, x, y,x_stop,y_stop,WelcomeTitle,StartButton,SettingsButton,ExitButtonInMenu
    pygame.mouse.set_visible(1)
    isClick = 0
    WTW = int(51 * ButtonScale / 2) #Welcome Title Width
    WTH = int(25 * ButtonScale / 2)
    WT_x = centerX(WTW)
    WT_y = display_height / 10
    WelcomeTitle = pygame.transform.scale(WelcomeTitle, (WTW, WTH))
    
    SBW = int(36 * ButtonScale / 5)
    SBH = int(11 * ButtonScale / 5)
    SB_x = centerX(SBW)
    SB_y = (display_height + (WTH+WT_y)) / 2 - SBH/2 - 44
    StartButton = pygame.transform.scale(StartButton, (SBW, SBH))
    
    SeBW = int(59 * ButtonScale / 5)
    SeBH = int(11 * ButtonScale / 5)
    SeB_x = centerX(SeBW)
    SeB_y = SB_y + 2 * SBH
    SettingsButton = pygame.transform.scale(SettingsButton, (SeBW, SeBH))
    
    ExBW = int(31 * ButtonScale / 5)
    ExBH = int(11 * ButtonScale / 5)
    ExB_x = centerX(ExBW)
    ExB_y = SB_y + 4 * SBH
    ExitButtonInMenu = pygame.transform.scale(ExitButtonInMenu, (ExBW, ExBH))
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            x,y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not isClick:       
                    if pygame.mouse.get_pressed()[0]:
                        isClick = 1
                        x_start,y_start = x,y
            elif event.type == pygame.MOUSEBUTTONUP:
                if isClick:
                    if not pygame.mouse.get_pressed()[0]:
                        isClick = 0
                    x_stop,y_stop = x,y
                    if withinCenter(SB_x,SB_y,SBW,SBH):
                        return 0
                    elif withinCenter(SeB_x,SeB_y,SeBW,SeBH):
                            BlipSound.play()
                            Settings(1)
                    elif withinCenter(ExB_x,ExB_y,ExBW,ExBH):
                            BlipSound.play()
                            ExitScreen(1)
        DISPLAY.fill((0,0,0))
        DISPLAY.blit(WelcomeTitle,(WT_x,WT_y))
        DISPLAY.blit(StartButton,(SB_x,SB_y))
        DISPLAY.blit(SettingsButton,(SeB_x,SeB_y))
        DISPLAY.blit(ExitButtonInMenu,(ExB_x,ExB_y))
        
        pygame.display.update()
        clock.tick(fps)

def Settings(a):
    global isClick, x_start, y_start, x, y,x_stop,y_stop,BackButton,DiffButton,Difficulty,ButtonScale,botMult
    pygame.mouse.set_visible(1)
    isClick = 0
    
    DBW = int(98 * ButtonScale / 5)
    DBH = int(11 * ButtonScale / 5)
    DB_x = centerX(DBW)
    DB_y = display_height/2
    DiffButton = pygame.transform.scale(DiffButton, (DBW, DBH))
    
    BBW = int(29 * ButtonScale / 5)
    BBH = int(11 * ButtonScale / 5)
    BB_x = centerX(BBW)
    BB_y = DB_y + 2 * DBH
    BackButton = pygame.transform.scale(BackButton, (BBW, BBH))
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            x,y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not isClick:       
                    if pygame.mouse.get_pressed()[0]:
                        isClick = 1
                        x_start,y_start = x,y
            elif event.type == pygame.MOUSEBUTTONUP:
                if isClick:
                    if not pygame.mouse.get_pressed()[0]:
                        isClick = 0
                    x_stop,y_stop = x,y
                    if y_start >= DB_y and y_stop >= DB_y and y_start <= DB_y + DBH and  y_stop <= DB_y + DBH:
                        if x_start >= DB_x+76*ButtonScale/5 and x_stop >= DB_x+76*ButtonScale/5 and x_start <= DB_x + DBW-12*ButtonScale/5 and  x_stop <= DB_x + DBW - 12*ButtonScale/5: #Click within x
                            BlipSound.play()
                            botMult *= 1.1
                        if x_start >= DB_x+88*ButtonScale/5 and x_stop >= DB_x+88*ButtonScale/5 and x_start <= DB_x + DBW and  x_stop <= DB_x + DBW: #Click within x
                            BlipSound.play()
                            botMult /= 1.1
                    elif withinCenter(BB_x,BB_y,BBW,BBH):
                            BlipSound.play()
                            return 0
        DISPLAY.fill((0,0,0))
        DISPLAY.blit(DiffButton,(DB_x,DB_y))
        DISPLAY.blit(BackButton,(BB_x,BB_y))
        
        pygame.display.update()
        clock.tick(60)

def ExitScreen(a):
    global isClick, x_start, y_start, x, y,x_stop,y_stop,ExitBox,ButtonScale
    pygame.mouse.set_visible(1)
    isClick = 0
    
    EBW = int(108 * ButtonScale / 5)
    EBH = int(45 * ButtonScale / 5)
    EB_x = centerX(EBW)
    EB_y = display_height/2 - EBH/2
    ExitBox = pygame.transform.scale(ExitBox, (EBW, EBH))
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            x,y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not isClick:       
                    if pygame.mouse.get_pressed()[0]:
                        isClick = 1
                        x_start,y_start = x,y
            elif event.type == pygame.MOUSEBUTTONUP:
                if isClick:
                    if not pygame.mouse.get_pressed()[0]:
                        isClick = 0
                    x_stop,y_stop = x,y
                    if y_start >= EB_y+31*ButtonScale/5 and y_stop >= EB_y+31*ButtonScale/5 and y_start <= EB_y + EBH-3*ButtonScale/5 and  y_stop <= EB_y + EBH-3*ButtonScale/5:
                        if x_start >= EB_x+8*ButtonScale/5 and x_stop >= EB_x+8*ButtonScale/5 and x_start <= EB_x + EBW-77*ButtonScale/5 and  x_stop <= EB_x + EBW - 77*ButtonScale/5: #Click within "YES" x
                            pygame.quit()
                        elif x_start >= EB_x+81*ButtonScale/5 and x_stop >= EB_x+81*ButtonScale/5 and x_start <= EB_x + EBW-8*ButtonScale/5 and  x_stop <= EB_x + EBW - 8*ButtonScale/5: #Click within "NO" x
                            BlipSound.play()
                            return 0
        DISPLAY.fill((0,0,0))
        DISPLAY.blit(ExitBox,(EB_x,EB_y))
        
        pygame.display.update()
        clock.tick(60)

def ScoreScreen(a):
    global p_score,b_score,display_width,display_height,isClick, x_start, y_start, x, y,x_stop,y_stop,ButtonScale,YouLose,YouWin,GoToMenu,ExitButtonInMenu,PlayAgain,GoToGame
    pygame.mouse.set_visible(1)
    isClick = 0

    playerWins = 0
    if p_score > b_score:
        playerWins = 1
    
    if playerWins:
        TVW = int(58 * ButtonScale / 3) #The victory width
    else:
         TVW = int(56 * ButtonScale / 3)
    TVH = int(11 * ButtonScale / 3)
    TV_x = centerX(TVW)
    TV_y = display_height/4 - TVH/2
    if playerWins:
        VictoryBox = pygame.transform.scale(YouWin, (TVW, TVH))
    else:
        VictoryBox = pygame.transform.scale(YouLose, (TVW, TVH))

    PAW = int(72 * ButtonScale / 5)
    PAH = int(11 * ButtonScale / 5)
    PA_x = centerX(PAW)
    PA_y = display_height / 2 + PAH
    PlayAgain = pygame.transform.scale(PlayAgain, (PAW, PAH))

    GTMW = int(76 * ButtonScale / 5)
    GTMH = int(11 * ButtonScale / 5)
    GTM_x = centerX(GTMW)
    GTM_y = PA_y + 2*PAH
    GoToMenu = pygame.transform.scale(GoToMenu, (GTMW, GTMH))
    
    ExBW = int(31 * ButtonScale / 5)
    ExBH = int(11 * ButtonScale / 5)
    ExB_x = centerX(ExBW)
    ExB_y = GTM_y + 2*GTMH
    ExitButtonInMenu = pygame.transform.scale(ExitButtonInMenu, (ExBW, ExBH))
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            x,y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not isClick:       
                    if pygame.mouse.get_pressed()[0]:
                        isClick = 1
                        x_start,y_start = x,y
            elif event.type == pygame.MOUSEBUTTONUP:
                if isClick:
                    if not pygame.mouse.get_pressed()[0]:
                        isClick = 0
                    x_stop,y_stop = x,y
                    if y_start >= DB_y and y_stop >= DB_y and y_start <= DB_y + DBH and  y_stop <= DB_y + DBH:
                        if x_start >= DB_x+76*ButtonScale/5 and x_stop >= DB_x+76*ButtonScale/5 and x_start <= DB_x + DBW-12*ButtonScale/5 and  x_stop <= DB_x + DBW - 12*ButtonScale/5: #Click within x
                            BlipSound.play()
                            botMult *= 1.1
                        if x_start >= DB_x+88*ButtonScale/5 and x_stop >= DB_x+88*ButtonScale/5 and x_start <= DB_x + DBW and  x_stop <= DB_x + DBW: #Click within x
                            BlipSound.play()
                            botMult /= 1.1
        DISPLAY.fill((0,0,0))
        DISPLAY.blit(VictoryBox,(TV_x,TV_y))
        DISPLAY.blit(PlayAgain,(PA_x,PA_y))
        DISPLAY.blit(GoToMenu,(GTM_x,GTM_y))
        DISPLAY.blit(ExitButtonInMenu,(ExB_x,ExB_y))
        
        pygame.display.update()
        clock.tick(60)

def PauseScreen(a):
    global display_width,display_height,isClick, x_start, y_start, x, y,x_stop,y_stop,ButtonScale,GamePaused,DiffButton,botMult
    pygame.mouse.set_visible(1)
    isClick = 0


    GPW = int(77 * ButtonScale / 4)
    GPH = int(11 * ButtonScale / 4)
    GP_x = centerX(GPW)
    GP_y = display_height / 2 - GPH/2
    GamePaused = pygame.transform.scale(GamePaused, (GPW, GPH))

    DBW = int(98 * ButtonScale / 5)
    DBH = int(11 * ButtonScale / 5)
    DB_x = centerX(DBW)
    DB_y = GP_y + GPH *2
    DiffButton = pygame.transform.scale(DiffButton, (DBW, DBH))

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            x,y = pygame.mouse.get_pos()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not isClick:       
                    if pygame.mouse.get_pressed()[0]:
                        isClick = 1
                        x_start,y_start = x,y
            elif event.type == pygame.MOUSEBUTTONUP:
                if isClick:
                    if not pygame.mouse.get_pressed()[0]:
                        isClick = 0
                    x_stop,y_stop = x,y
                    if y_start >= DB_y and y_stop >= DB_y and y_start <= DB_y + DBH and  y_stop <= DB_y + DBH:
                        if x_start >= DB_x+76*ButtonScale/5 and x_stop >= DB_x+76*ButtonScale/5 and x_start <= DB_x + DBW-12*ButtonScale/5 and  x_stop <= DB_x + DBW - 12*ButtonScale/5: #Click within x
                            BlipSound.play()
                            botMult *= 1.1
                        if x_start >= DB_x+88*ButtonScale/5 and x_stop >= DB_x+88*ButtonScale/5 and x_start <= DB_x + DBW and  x_stop <= DB_x + DBW: #Click within x
                            BlipSound.play()
                            botMult /= 1.1
                            
        DISPLAY.fill((0,0,0))
        DISPLAY.blit(GamePaused,(GP_x,GP_y))
        DISPLAY.blit(DiffButton,(DB_x,DB_y))
        
        pygame.display.update()
        clock.tick(60)

def game_loop(a):
    global p_score,b_score,paddleH,display_width,display_height,startTime,fps
    pygame.mouse.set_visible(0)
    startTime = time.time()

    
    upBool,downBool = 0,0
    DISPLAY.fill((0,0,0))
    
    movementPx = int((display_height / 60 + .5) * 1.5)
    paddleW = int(display_width / 200 + 5.5)
    ball_w = 10
    
    player = userRectangle(20,display_height/2 - paddleH/2,paddleW,paddleH)
    bot = userRectangle(display_width-20-paddleW,display_height/2-paddleH/2,paddleW,paddleH)
    ball = userRectangle(centerX(ball_w),display_height/2-ball_w/2-3,ball_w,ball_w)

    ballSlope = ()
    ballSpeed = display_width / fps
    ballDeltaX = random.uniform(-ballSpeed,-ballSpeed / 2)/2
    ballDeltaY = (ballSpeed - abs(ballDeltaX*2))*.5
    if rand(0,1):
        ballDeltaX *= -1
    if rand(0,1):
        ballDeltaY *= -1

    totalDistance = display_height/2

    altkey = 0
    f4key = 0
    
    roundOver = 0
    while 1:
        if roundOver:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                
                if event.key==pygame.K_RALT or event.key==pygame.K_LALT:
                    altkey=1
                elif event.key==pygame.K_F4:
                    f4key=1
                elif event.key == pygame.K_DOWN:
                    downBool = 1
                elif event.key == pygame.K_UP:
                    upBool = 1
                if event.key == pygame.K_ESCAPE:
                    PauseScreen(1)
                if f4key and altkey:
                    pygame.quit()
            if event.type == pygame.KEYUP:
                downBool,upBool,altkey,f4key = 0,0,0,0
        #Any of the code that runs during the program goes here
        if not player.y + player.height + 1 < display_height:
            downBool = 0
            player.y = display_height - player.height - 1
        if not player.y > 1:
            upBool = 0
            player.y = 1
        if upBool:
            player.y -= movementPx * (60 / fps)
        elif downBool:
            player.y += movementPx* (60 / fps)
        if time.time() - startTime > 1: #move ball, bot
            if ball.x > 1 and ball.x + ball.width < display_width: #On the stage
                if ball.y > 1 and ball.y + ball.height < display_height - 1: #Within stage vertically
                    if player.x  <= ball.x <= player.x + player.width: #If ball_x is within player x
                        bC_Y = ball.y + ball.height/2 #Ball center Y
                        if player.y <= bC_Y <= player.y + player.height: #If bLC_Y within player y
                            BlipSound.play()
                            ballSlope = ((player.y + player.height / 2) - bC_Y) / ((player.x + player.width - player.height/2) - ball.x)
                            z = ballSpeed
                            s = ballSlope
                            ballDeltaY = math.sqrt(abs(z**2*(-4/s**2-4)))/(2*((1/s**2)+1))
                            ballDeltaX = math.sqrt(abs(ballSpeed ** 2 - ballDeltaY ** 2))
                            ball.x += player.width
                            if bC_Y < player.y + player.height/2:
                                ballDeltaY *= -1
                            ballSpeed *= 1.05
                            ###############
                            #Bot AI
                            ###############
                    elif bot.x  <= ball.x + ball.width <= bot.x + bot.width: #If ball_x is within bot x:
                        bC_Y = ball.y + ball.height/2 #Ball center Y
                        if bot.x  <= ball.x + ball.width <= bot.x + bot.width: #If ball_x is within bot x
                            if bot.y <= bC_Y <= bot.y + bot.height: #If bLC_Y within bot y
                                BlipSound.play()
                                ballSlope = ((bot.y + bot.height / 2) - bC_Y) / ((bot.x + bot.height / 2) - (ball.x + ball.width))
                                z = ballSpeed
                                s = ballSlope
                                ballDeltaY = math.sqrt(abs(z**2*(-4/s**2-4)))/(2*((1/s**2)+1))
                                ballDeltaX = math.sqrt(ballSpeed ** 2 - ballDeltaY ** 2)
                                ball.x -= bot.width
                                if bC_Y < bot.y + bot.height/2:
                                    ballDeltaY *= -1
                                ballDeltaX *= -1
                                ballSpeed *= 1.05
                        
                else:
                    ballDeltaY *= -1
            else:
                if ball.x < display_width/2:
                    b_score += 1
                else:
                    p_score += 1
                return 0
            ball.y += ballDeltaY
            ball.x += ballDeltaX
        #Bot movement
        if ballDeltaX > 0:
            totalDistance = ball.y + ball.height/2
            distToPrediction = abs(bot.y + bot.height/2 - totalDistance)
            isAbleToMove = 1
            botSlowDown = 1
            if distToPrediction <= 1:
                isAbleToMove = 0
            elif distToPrediction <= movementPx * (60 / fps):
                botSlowdown = 2
            if isAbleToMove:
                if bot.y + bot.height/2 < totalDistance:
                    if bot.y + bot.height < display_height - 1:
                        bot.y += movementPx * (60 / fps) / botSlowDown * botMult
                else:
                    if bot.y > 1:
                        bot.y -= movementPx * (60 / fps) / botSlowDown * botMult
        TextToRender = ""
        if p_score < 10:
            TextToRender += "0"
        TextToRender += (str(p_score) + " - ")
        if b_score < 10:
            TextToRender += '0'
        TextToRender += str(b_score)
        
        DISPLAY.fill((0,0,0))

        netw=10
        neth = 30
        net = pygame.Surface((netw,neth))
        net.set_alpha(128)
        net.fill((255,255,255))
        for i in range(int(display_height / (neth))):
            DISPLAY.blit(net, (centerX(netw),2 * neth * i))
            
        pygame.draw.rect(DISPLAY, (255,255,255), (player.x,player.y,player.width,player.height), 0)
        pygame.draw.rect(DISPLAY, (255,255,255), (bot.x,bot.y,bot.width,bot.height), 0)
        pygame.draw.rect(DISPLAY, (255,255,255), (ball.x,ball.y,ball.width,ball.height), 0)
        textsurface = (chooseFont("monospace",50)).render(TextToRender,1,(255,255,255))
        DISPLAY.blit(textsurface,(display_width/2 - 2 * 50 - 5,20))
        pygame.display.update()
        clock.tick(fps)

def wait(Time):
    global startTime
    while time.time() - startTime < Time:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        clock.tick(15)

while 1:
    if not GoToGame:
        startupMusic.play()
        startMenu(1)
        pygame.mixer.stop()
        BlipSound.play()
    GoToGame = 0
    while 1:
        game_loop(1)
        MissSound.play()
        startTime = time.time()
        wait(2.5)
        if p_score >= 10 or b_score >= 10:
            ScoreScreen(1)
            break
    p_score = 0
    b_score = 0
