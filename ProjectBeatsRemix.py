import sys, pygame, math, random, os

#initialize program
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Project Beats Remix")

#GUI and related
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)
fps = pygame.time.Clock()
player = pygame.rect.Rect(width/2-10, height/2-10, 20, 20)
screenNumber = 2

#Music and related
activeMusic = None
busyFading = False
fading = True
fade_speed = 0.05
volume = 1.0
pygame.mixer.music.set_volume(volume)
RectLobbyMusic = 'StartTheStars.mp3'

#Text and related
font = pygame.font.Font(None, 40)

#Screen 2
RectLevelSelect = [pygame.rect.Rect(width/4, height/3, 2*width/4, height/3),
                   pygame.rect.Rect(0, 0, width/4, height/3),
                   pygame.rect.Rect(3*width/4, height/3, width/4, height/3),
                   pygame.rect.Rect(0, 2*height/3, width / 4, height / 3),
                   pygame.rect.Rect(width / 4, 2*height/3, width / 4, height / 3),
                   pygame.rect.Rect(width / 2, 2*height/3, width / 4, height / 3),
                   pygame.rect.Rect(3 * width / 4, 2*height/3, width / 4, height / 3)]
RectLevelMusic = [[pygame.rect.Rect(0, 0, width/4, height/3), 'CoconutMall.mp3'],
             [pygame.rect.Rect(width/4, 0, width/4, height/3), 'Focus.mp3'],
             [pygame.rect.Rect(width/2, 0, width/4, height/3), 'MilkyWays.mp3'],
             [pygame.rect.Rect(3*width/4, 0, width/4, height/3), 'Sevcon.mp3'],
             [pygame.rect.Rect(0, height/3, width/4, height/3), 'Chronos.mp3']]

Gvx, Gvy = 0, 0
speed = 5

def drawText(font, text, color, x, y, alpha):
    surface = font.render(text, True, color).convert_alpha()
    surface.set_alpha(alpha)
    screen.blit(surface, (x, y))

def movePlayer(player):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player.y > 0: player.y -= speed
    if keys[pygame.K_a] and player.x > 0: player.x -= speed
    if keys[pygame.K_s] and player.y < 700: player.y += speed
    if keys[pygame.K_d] and player.x < 1260: player.x += speed
    if player.x>0 and player.x<1260: player.x += Gvx
    if player.y>0 and player.y<700: player.y -= Gvy

def moveObject(rect, vx, vy):
    rect.x += vx
    rect.y -= vy
    return rect

#Generates a basic enemy
def generateBasic(x, y, w, h, vx, vy):
    return [pygame.rect.Rect(x, y, w, h), vx, vy]

#Generates an enemy for a certain time
#Can also start with a warning
#Also useful for stationary enemies
def generateLaser(x, y, w, h, LT, t, warn):
    return [pygame.rect.Rect(x, y, w, h), LT, t, warn, False]

#Generates an exploding enemy into n different enemies
def generateExploding(x, y, w, h, vx, vy, LT, ew, eh, ev, n):
    return [pygame.rect.Rect(x, y, w, h), vx, vy, LT, (ew, eh, ev, n)]


def level_1():
    pygame.mixer.music.stop()
    gameOver=False
    RectEnemies = []
    volume = 0.0
    bpm = 132
    activeMusic = False
    start = 260

    # When running, set LT = 0
    # When debugging, set LT >= 0
    LT = 0

    INVT = 0
    fading = False
    vx, vy = 0, 0
    fpb = 3600/bpm
    lives=3
    inv = False
    paused = False

    #Use aprox values
    beats1 = [i for i in range(0, 50, 10)]
    beats1.extend([round(i) for i in range(round(2 * fpb), 50 + round(2 * fpb), 10)])
    beats1.extend([round(i) for i in range(round(4 * fpb), 50 + round(4 * fpb), 10)])
    beats1.extend([round(i) for i in range(round(6 * fpb), 50 + round(6 * fpb), 10)])
    pos1 = [i for i in range(0, 720, 144)]
    pos1.extend([i for i in range(36, 720, 144)])
    pos1.extend([i for i in range(72, 720, 144)])
    pos1.extend([i for i in range(108, 720, 144)])
    beats2 = [round(i * fpb) for i in range(28)]
    beats3 = [round(i * fpb / 2) for i in range(12 * 2)]  # half-beats
    beats4 = [round(i * fpb) for i in range(12)]  # full beats
    beats5 = [round(i * fpb / 2) for i in range(4 * 2)]  # half-beats, 4 beats long
    beats6 = [round(i * fpb * 2) for i in range(28 // 2)]  # every 2 beats
    beats7 = [round(i * fpb / 4) for i in range(36 * 4)]  # quarter-beats

    #Use precise values
    refBeat = [start, start+round(16*3600/bpm), start+round(32*fpb), start+round(48*3600/bpm),
               start+round(56*fpb), start+round(64*fpb), start+round(96*fpb)]

    while not gameOver:
        #Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_p:
                    if paused:
                        paused = False
                        pygame.mixer.music.unpause()
                    else:
                        paused = True
                        pygame.mixer.music.pause()
                        drawText(font, "Game Paused", "white", 550, 340, 255)
                        pygame.display.flip()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print("Frame #: " + str(LT))

        #Core game code

        if not paused:
            screen.fill("black")
            #Fading text
            if LT<=240:
                fs, fe = 180, 240
                if fs <= LT <= fe:
                    alpha = 255 * (1 - (LT - fs) / (fe - fs))
                    drawText(font, "Coconut Mall", "white", 830, 600, alpha)
                    drawText(font, "Ryu Nagamatsu & Asuka Ohta", "white", 830, 650, alpha)
                elif LT < fs:
                    drawText(font, "Coconut Mall", "white", 830, 600, 255)
                    drawText(font, "Ryu Nagamatsu & Asuka Ohta", "white", 830, 650, 255)
            if LT >= start-20 and not fading:
                if not activeMusic:
                    pygame.mixer.music.load('CoconutMall.mp3')
                    pygame.mixer.music.play(0)
                    #Debug set song position
                    #Remove/Comment below two lines when running
                    #pygame.mixer.music.set_pos((LT-start)/60)
                    #volume = 1.0
                volume = min(1.0, volume + 0.05)
                pygame.mixer.music.set_volume(volume)
                if volume >= 1.0:
                    fading = True
            i = 0
            while i < len(RectEnemies):
                RectEnemies[i][0] = moveObject(RectEnemies[i][0], RectEnemies[i][1], RectEnemies[i][2])
                if RectEnemies[i][0].x < 0 - RectEnemies[i][0].width or RectEnemies[i][0].x > 1280:
                    RectEnemies.pop(i)
                    continue
                pygame.draw.rect(screen, "red", RectEnemies[i][0])
                i += 1

            # Enemies start here
            for i, j in zip(beats1, pos1):
                if LT == refBeat[0] + i:
                    RectEnemies.append(generateBasic(1280, j, 36, 36, -7, 0))
            for i in beats2:
                if LT == refBeat[1] + i:
                    RectEnemies.append(generateBasic(1280, random.randint(0, 620), 100, 100, -10, 0))
            for i in beats3:
                if LT == refBeat[2] + i:
                    RectEnemies.append(generateBasic(1280, random.randint(0, 688), 32, 32, -15, 0))
            for i in beats4:
                if LT == refBeat[3] + i:
                    RectEnemies.append(generateBasic(-100, random.randint(0, 620), 100, 100, 10, 0))
            for i in beats5:
                if LT == refBeat[4] + i:
                    RectEnemies.append(generateBasic(-32, random.randint(0, 688), 32, 32, 15, 0))
            for i in beats6:
                if LT == refBeat[5] + i:
                    top = random.randint(120, 600)
                    RectEnemies.append(generateBasic(1280, 0, 50, top, -10, 0))
                    RectEnemies.append(generateBasic(1280, top+80, 50, 720-top-80, -10, 0))
            for i in beats7:
                if LT == refBeat[6] + i:
                    if LT%4==0:
                        RectEnemies.append(generateBasic(1280, random.randint(0, 710), 15, 15, -10, 0))
                    else:
                        RectEnemies.append(generateBasic(-15, random.randint(0, 710), 15, 15, 10, 0))
            # Enemies end here

            #Player movement
            if 0 < player.x < 1260: player.x += vx
            if 0 < player.y < 700: player.y -= vy
            movePlayer(player)

            #I frames
            if INVT <= LT:
                inv = False
            for i in RectEnemies:
                if player.colliderect(i[0]) and not inv:
                    lives-=1
                    inv = True
                    INVT = LT+120

            #End of level
            if(LT>=start+round(144*fpb)):
                player.centerx = width / 2
                player.centery = height / 2
                gameOver=True
                print("You win")

            #Damage taken
            if lives==3:
                pygame.draw.rect(screen, "blue", player)
            elif lives==2:
                pygame.draw.rect(screen, "yellow", player)
            elif lives==1:
                pygame.draw.rect(screen, "dark red", player)
            else:
                player.centerx=width/2
                player.centery=height/2
                gameOver = True
                print("You died")

            #Ticks and Display
            pygame.display.flip()
            fps.tick(60)
            LT += 1

def level_2():
    pygame.mixer.music.stop()
    gameOver = False
    RectEnemies = []
    ExplodeEnemies = []
    volume = 0.0
    bpm = 174
    activeMusic = False
    start = 260
    switch = True
    switch2 = True

    # When running, set LT = 0
    # When debugging, set LT >= 0
    LT = 0

    INVT = 0
    fading = False
    vx, vy = 0, 0
    fpb = 3600 / bpm
    lives = 3
    inv = False
    paused = False

    # Use aprox values
    beats1 = [round(i*fpb*4) for i in range(60//4)]
    beats2 = [round(i*fpb) for i in range(52)]
    beats3 = [round(i*fpb*4) for i in range(28//4)]
    beats4 = [round(i*fpb) for i in range(12)]
    beats5 = [round(i*fpb) for i in range(12)]
    beats6 = [round(i*fpb) for i in range(12)]
    beats7 = [round(i*fpb/2) for i in range(2*2)]
    beats7.extend([round(i*fpb/2) for i in range(4*2, 6*2)])
    beats7.extend([round(i*fpb/2) for i in range(8*2, 10*2)])
    beats8 = [round(i * fpb / 2) for i in range(2 * 2, 4*2)]
    beats8.extend([round(i * fpb / 2) for i in range(6 * 2, 8*2)])
    beats8.extend([round(i * fpb / 2) for i in range(10 * 2, 12*2)])
    beats9 = [round(i*fpb*4) for i in range(28//4)]
    beats10 = [round(i*fpb*4) for i in range(28//4)]
    beats11 = [round(i*fpb) for i in range(60)]
    beats12 = [round(i*fpb*4) for i in range(60//4)]

    # Use precise values
    refBeat = [start, start + round(64*fpb), start + round(96*fpb), start + round(128*fpb),
               start + round(144*fpb), start + round(160*fpb), start + round(176*fpb), start + round(192*fpb),
               start + round(224*fpb), start + round(272*fpb)]

    while not gameOver:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_p:
                    if paused:
                        paused = False
                        pygame.mixer.music.unpause()
                    else:
                        paused = True
                        pygame.mixer.music.pause()
                        drawText(font, "Game Paused", "white", 550, 340, 255)
                        pygame.display.flip()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print("Frame #: " + str(LT))

        # Core game code

        if not paused:
            screen.fill("black")

            # Fading text
            if LT <= 240:
                fs, fe = 180, 240
                if fs <= LT <= fe:
                    alpha = 255 * (1 - (LT - fs) / (fe - fs))
                    drawText(font, "Focus", "white", 830, 600, alpha)
                    drawText(font, "Chipzel", "white", 830, 650, alpha)
                elif LT < fs:
                    drawText(font, "Focus", "white", 830, 600, 255)
                    drawText(font, "Chipzel", "white", 830, 650, 255)
            if LT >= start - 25 and not fading:
                if not activeMusic:
                    pygame.mixer.music.load('Focus.mp3')
                    pygame.mixer.music.play(0)
                    # Debug set song position
                    # Remove/Comment below two lines when running
                    #pygame.mixer.music.set_pos((LT-start)/60)
                    #volume = 1.0
                volume = min(1.0, volume + 0.05)
                pygame.mixer.music.set_volume(volume)
                if volume >= 1.0:
                    fading = True
            i = 0
            while i < len(RectEnemies):
                RectEnemies[i][0] = moveObject(RectEnemies[i][0], RectEnemies[i][1], RectEnemies[i][2])
                if RectEnemies[i][0].x < 0 - RectEnemies[i][0].width or RectEnemies[i][0].x > 1280 or RectEnemies[i][0].y < 0 - RectEnemies[i][0].height or RectEnemies[i][0].y > 720 :
                    RectEnemies.pop(i)
                    continue
                pygame.draw.rect(screen, "red", RectEnemies[i][0])
                i += 1
            i=0
            while i < len(ExplodeEnemies):
                ExplodeEnemies[i][0] = moveObject(ExplodeEnemies[i][0], ExplodeEnemies[i][1], ExplodeEnemies[i][2])
                if ExplodeEnemies[i][3]==LT:
                    for j in range(1, ExplodeEnemies[i][4][3]+1):
                        RectEnemies.append(generateBasic(ExplodeEnemies[i][0].centerx, ExplodeEnemies[i][0].centery,
                                                         ExplodeEnemies[i][4][0], ExplodeEnemies[i][4][1],
                                                         round(ExplodeEnemies[i][4][2]*math.cos(2*math.pi*j/ExplodeEnemies[i][4][3])),
                                                         round(ExplodeEnemies[i][4][2]*math.sin(2*math.pi*j/ExplodeEnemies[i][4][3]))))
                    ExplodeEnemies.pop(i)
                    continue
                pygame.draw.rect(screen, "orange", ExplodeEnemies[i][0])
                i += 1
            # Enemies start here
            for i in beats1:
                if LT == refBeat[0] + i:
                    ExplodeEnemies.append(generateExploding(1280, random.randint(0, 670), 50, 50, -10, 0, LT + int(2*fpb), 10, 10, 15, 16))
            for i in beats2:
                if LT == refBeat[1] + i:
                    if switch:
                        RectEnemies.append(generateBasic(1280, random.randint(0, 620), 10, 100, -5, 0))
                    else:
                        RectEnemies.append(generateBasic(-10, random.randint(0, 620), 10, 100, 5, 0))
                    switch = not switch
            for i in beats3:
                if LT == refBeat[2] + i:
                    ExplodeEnemies.append(generateExploding(1280, random.randint(0, 695), 50, 50, -10, 0, LT + int(2*fpb), 10, 10, 15, 16))
            for i in beats4:
                if LT == refBeat[3] + i:
                    ExplodeEnemies.append(generateExploding(1280, random.randint(0, 695), 25, 25, -10, 0, LT + int(2 * fpb), 5, 5,10, 12))
            for i in beats5:
                if LT == refBeat[4] + i:
                    ExplodeEnemies.append(generateExploding(-25, random.randint(0, 695), 25, 25, 10, 0, LT + int(2 * fpb), 5, 5,10, 12))
            for i in beats6:
                if LT == refBeat[5] + i:
                    ExplodeEnemies.append(generateExploding(1280, random.randint(0, 695), 25, 25, -10, 0, LT + int(2 * fpb), 5, 5,10, 12))
            for i in beats7:
                if LT == refBeat[6] + i:
                    if switch:
                        ExplodeEnemies.append(generateExploding(1280, random.randint(0, 695), 25, 25, -10, 0, LT + int(2 * fpb), 5, 5,10, 8))
                    else:
                        ExplodeEnemies.append(generateExploding(-25, random.randint(0, 695), 25, 25, 10, 0, LT + int(2 * fpb), 5, 5,10, 8))
                    switch = not switch
            for i in beats8:
                if LT == refBeat[6] + i:
                    if switch2:
                        RectEnemies.append(generateBasic(1280, random.randint(0, 670), 50, 50, -15, 0))
                    else:
                        RectEnemies.append(generateBasic(-50, random.randint(0, 670), 50, 50, 15, 0))
                    switch2 = not switch2
            for i in beats9:
                if LT == refBeat[7] + i:
                    if switch:
                        RectEnemies.append(generateBasic(0, -20, 800, 20, 0, -5))
                    else:
                        RectEnemies.append(generateBasic(480, -20, 800, 20, 0, -5))
                    switch = not switch
            for i in beats10:
                if LT == refBeat[8] + i:
                    if switch:
                        RectEnemies.append(generateBasic(0, 720, 800, 20, 0, 5))
                    else:
                        RectEnemies.append(generateBasic(480, 720, 800, 20, 0, 5))
                    switch = not switch
            for i in beats11:
                if LT == refBeat[9] + i:
                    RectEnemies.append(generateBasic(random.randint(0, 1230), -50, 50, 50, 0, -10))
            for i in beats12:
                if LT == refBeat[9] + i:
                    if switch:
                        ExplodeEnemies.append(
                            generateExploding(1280, random.randint(0, 670), 50, 50, -10, 0, LT + int(2 * fpb), 10, 10, 10,12))
                    else:
                        ExplodeEnemies.append(
                            generateExploding(-25, random.randint(0, 670), 50, 50, 10, 0, LT + int(2 * fpb), 10, 10, 10,12))
                    switch = not switch
            # Enemies end here

            # Player movement
            if player.x > 0 and player.x < 1260: player.x += vx
            if player.y > 0 and player.y < 700: player.y -= vy
            movePlayer(player)

            # I frames
            if INVT <= LT:
                inv = False
            for i in RectEnemies:
                if player.colliderect(i[0]) and not inv:
                    lives -= 1
                    inv = True
                    INVT = LT + 120
            for i in ExplodeEnemies:
                if player.colliderect(i[0]) and not inv:
                    lives -= 1
                    inv = True
                    INVT = LT + 120

            # End of level
            if LT >= start + round(340 * fpb):
                player.centerx = width / 2
                player.centery = height / 2
                gameOver = True
                print("You win")

            # Damage taken
            if lives == 3:
                pygame.draw.rect(screen, "blue", player)
            elif lives == 2:
                pygame.draw.rect(screen, "yellow", player)
            elif lives == 1:
                pygame.draw.rect(screen, "dark red", player)
            else:
                player.centerx = width / 2
                player.centery = height / 2
                gameOver = True
                print("You died")

            # Ticks and Display
            pygame.display.flip()
            fps.tick(60)
            LT += 1

def level_3():
    pygame.mixer.music.stop()
    gameOver = False
    RectEnemies = []
    ExplodeEnemies = []
    LaserEnemies = []
    volume = 0.0
    bpm = 183
    activeMusic = False
    start = 260
    switch = True
    switch2 = True

    # When running, set LT = 0
    # When debugging, set LT >= 0
    LT = 0

    INVT = 0
    fading = False
    vx, vy = 0, 0
    fpb = 3600 / bpm
    lives = 3
    inv = False
    paused = False

    # Use aprox values
    beats1 = [round(i * fpb/2) for i in range(44*2)]
    beats2 = [round(i * fpb) for i in range(0, 28)]
    beats3 = [round(i * fpb) for i in range(0, 28)]
    beats4 = [round(i * fpb) for i in range(0, 28)]
    beats5 = [round(i * fpb) for i in range(0, 28)]
    beats6 = [round(i * fpb) for i in range(0, 28)]
    beats7 = [round(i * fpb) for i in range(0, 28)]
    beats8 = [round(i * fpb/2) for i in range(0, 48)]
    beats9 = [round(i * fpb*2) for i in range(0, 14)]
    beats10 = [round(i * fpb*2) for i in range(0, 14)]


    # Use precise values
    refBeat = [start, start + round(16*fpb), start + round(48*fpb), start + round(80*fpb), start + round(112*fpb),
               start + round(144*fpb), start + round(176*fpb), start + round(212*fpb), start + round(244*fpb),
               start + round(276*fpb)]

    while not gameOver:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_p:
                    if paused:
                        paused = False
                        pygame.mixer.music.unpause()
                    else:
                        paused = True
                        pygame.mixer.music.pause()
                        drawText(font, "Game Paused", "white", 550, 340, 255)
                        pygame.display.flip()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print("Frame #: " + str(LT))

        # Core game code

        if not paused:
            screen.fill("black")

            # Fading text
            if LT <= 240:
                fs, fe = 180, 240
                if fs <= LT <= fe:
                    alpha = 255 * (1 - (LT - fs) / (fe - fs))
                    drawText(font, "Milky Ways", "white", 830, 600, alpha)
                    drawText(font, "Bossfight", "white", 830, 650, alpha)
                elif LT < fs:
                    drawText(font, "Milky Ways", "white", 830, 600, 255)
                    drawText(font, "Bossfight", "white", 830, 650, 255)
            if LT >= start - 25 and not fading:
                if not activeMusic:
                    pygame.mixer.music.load('MilkyWays.mp3')
                    pygame.mixer.music.play(0)
                    # Debug set song position
                    # Remove/Comment below two lines when running
                    #pygame.mixer.music.set_pos((LT-start)/60)
                    #volume = 1.0
                volume = min(1.0, volume + 0.05)
                pygame.mixer.music.set_volume(volume)
                if volume >= 1.0:
                    fading = True

            #Enemies logic start
            i = 0
            while i < len(RectEnemies):
                RectEnemies[i][0] = moveObject(RectEnemies[i][0], RectEnemies[i][1], RectEnemies[i][2])
                if (RectEnemies[i][0].x < 0 - RectEnemies[i][0].width and RectEnemies[i][1]<0 or
                    RectEnemies[i][0].x > 1280 and RectEnemies[i][1]>0 or
                    RectEnemies[i][0].y < 0 - RectEnemies[i][0].height and RectEnemies[i][2]>0 or
                    RectEnemies[i][0].y > 720 and RectEnemies[i][2]<0):
                    RectEnemies.pop(i)
                    continue
                pygame.draw.rect(screen, "red", RectEnemies[i][0])
                i += 1
            i = 0
            while i < len(ExplodeEnemies):
                ExplodeEnemies[i][0] = moveObject(ExplodeEnemies[i][0], ExplodeEnemies[i][1], ExplodeEnemies[i][2])
                if ExplodeEnemies[i][3] == LT:
                    for j in range(1, ExplodeEnemies[i][4][3] + 1):
                        RectEnemies.append(generateBasic(ExplodeEnemies[i][0].centerx, ExplodeEnemies[i][0].centery,
                                                         ExplodeEnemies[i][4][0], ExplodeEnemies[i][4][1],
                                                         round(ExplodeEnemies[i][4][2] * math.cos(
                                                             2 * math.pi * j / ExplodeEnemies[i][4][3])),
                                                         round(ExplodeEnemies[i][4][2] * math.sin(
                                                             2 * math.pi * j / ExplodeEnemies[i][4][3]))))
                    ExplodeEnemies.pop(i)
                    continue
                pygame.draw.rect(screen, "orange", ExplodeEnemies[i][0])
                i += 1
            i=0
            while i < len(LaserEnemies):
                if LaserEnemies[i][1] == LT:
                    LaserEnemies[i][4] = True
                elif LaserEnemies[i][1] + LaserEnemies[i][2] == LT:
                    LaserEnemies.pop(i)
                    continue
                if LT < LaserEnemies[i][1]:
                    pygame.draw.rect(screen, "pink", LaserEnemies[i][0])
                else:
                    pygame.draw.rect(screen, "red", LaserEnemies[i][0])
                i += 1
            #Enemies logic ends

            # Enemies start here
            for i in beats1:
                if LT == refBeat[0] + i:
                    RectEnemies.append(generateBasic(random.randint(0, 1260), -20, 20, 20, 0, -15))
            for i in beats2:
                if LT == refBeat[1] + i:
                    if switch:
                        a = random.randint(0, 590)
                    else:
                        a = random.randint(591, 1180)
                    RectEnemies.append(generateBasic(a, -100, 100, 100, 0, -10))
                    for j in range(1, 4):
                        RectEnemies.append(generateBasic(a+25, -100-60*j, 50, 50, 0, -10))
                    switch = not switch
            if LT == refBeat[2] - round(4*fpb):
                for i in range(1, 6):
                    ExplodeEnemies.append(
                        generateExploding(1280, 120*i, 50, 50, -2, 0, LT + round(4 * fpb), 5, 5, 8,24))
            for i in beats3:
                if LT == refBeat[2] + i:
                    ExplodeEnemies.append(generateExploding(1280, random.randint(0, 670), 50, 50, -10, 0, LT + round(fpb), 10, 10, 15, 16))
            if LT == refBeat[3] - round(4*fpb):
                for i in range(1, 6):
                    ExplodeEnemies.append(
                        generateExploding(-50, 120*i, 50, 50, 2, 0, LT + round(4 * fpb), 5, 5, 8,24))
            for i in beats4:
                if LT == refBeat[3] + i:
                    ExplodeEnemies.append(generateExploding(-50, random.randint(0, 670), 50, 50, 10, 0, LT + round(fpb), 10, 10, 15, 16))
            for i in beats5:
                if LT == refBeat[4] + i:
                    a = random.randint(0, 680)
                    if switch:
                        RectEnemies.append(generateBasic(1280, a, 40, 40, -15, 0))
                        for j in range(1, 6):
                            RectEnemies.append(generateBasic(1300+30*j, a+10, 20, 20, -15, 0))
                    else:
                        RectEnemies.append(generateBasic(-40, a, 40, 40, 15, 0))
                        for j in range(1, 6):
                            RectEnemies.append(generateBasic(-40 - 30 * j, a+10, 20, 20, 15, 0))
                    switch = not switch
            if LT == refBeat[5] - round(4 * fpb):
                ExplodeEnemies.append(generateExploding(1280, 110, 100, 100, -3, 0, LT + round(4 * fpb), 10, 10, 7, 16))
                ExplodeEnemies.append(generateExploding(1280, 430, 100, 100, -3, 0, LT + round(4 * fpb), 10, 10, 7, 16))
                ExplodeEnemies.append(generateExploding(-100, 110, 100, 100, 2, 0, LT + round(4 * fpb), 10, 10, 7, 16))
                ExplodeEnemies.append(generateExploding(-100, 430, 100, 100, 2, 0, LT + round(4 * fpb), 10, 10, 7, 16))
            for i in beats6:
                if LT == refBeat[5] + i:
                    a = random.randint(0, 1240)
                    if switch:
                        RectEnemies.append(generateBasic(a, -40, 40, 40, 0, -10))
                        for j in range(1, 6):
                            RectEnemies.append(generateBasic(a+10, -40-30*j, 20, 20, 0, -10))
                    else:
                        RectEnemies.append(generateBasic(a, 720, 40, 40, 0, 10))
                        for j in range(1, 6):
                            RectEnemies.append(generateBasic(a+10, 740+30*j, 20, 20, 0, 10))
                    switch = not switch
            for i in beats7:
                if LT == refBeat[6] + i:
                    LaserEnemies.append(generateLaser(random.randint(0, 1180), 0, 100, 720, LT + round(2*fpb), round(fpb), round(2*fpb)))
            for i in beats8:
                if LT == refBeat[7] + i:
                    LaserEnemies.append(generateLaser(random.randint(0, 1230), 0, 50, 720, LT + round(2*fpb), round(fpb), round(2*fpb)))
            if LT == refBeat[8] - round(4*fpb):
                for i in range(1, 6):
                    ExplodeEnemies.append(generateExploding(1280, 120*i, 50, 50, -2, 0, LT + round(4 * fpb), 5, 5, 8,24))
            for i in beats9:
                if LT == refBeat[8] + i:
                    ExplodeEnemies.append(generateExploding(1280, random.randint(0, 670), 50, 50, -10, 0, LT + round(fpb), 10, 10, 15,16))
                    LaserEnemies.append(generateLaser(random.randint(0, 1200), 0, 80, 720, LT + round(2*fpb), round(fpb), round(2*fpb)))
            if LT == refBeat[9] - round(4*fpb):
                for i in range(1, 6):
                    ExplodeEnemies.append(generateExploding(-50, 120*i, 50, 50, 2, 0, LT + round(4 * fpb), 5, 5, 8,24))
            for i in beats10:
                if LT == refBeat[9] + i:
                    ExplodeEnemies.append(generateExploding(-50, random.randint(0, 670), 50, 50, 10, 0, LT + round(fpb), 10, 10, 15,16))
                    LaserEnemies.append(generateLaser(random.randint(0, 1200), 0, 80, 720, LT + round(2*fpb), round(fpb), round(2*fpb)))
            # Enemies end here
            # Player movement
            if player.x > 0 and player.x < 1260: player.x += vx
            if player.y > 0 and player.y < 700: player.y -= vy
            movePlayer(player)

            # I frames
            if INVT <= LT:
                inv = False
            for i in RectEnemies:
                if player.colliderect(i[0]) and not inv:
                    lives -= 1
                    inv = True
                    INVT = LT + 120
            for i in ExplodeEnemies:
                if player.colliderect(i[0]) and not inv:
                    lives -= 1
                    inv = True
                    INVT = LT + 120
            for i in LaserEnemies:
                if player.colliderect(i[0]) and i[4] and not inv:
                    lives -= 1
                    inv = True
                    INVT = LT + 120

            # End of level
            if LT >= start + round(316 * fpb):
                player.centerx = width / 2
                player.centery = height / 2
                gameOver = True
                print("You win")

            # Damage taken
            if lives == 3:
                pygame.draw.rect(screen, "blue", player)
            elif lives == 2:
                pygame.draw.rect(screen, "yellow", player)
            elif lives == 1:
                pygame.draw.rect(screen, "dark red", player)
            else:
                player.centerx = width / 2
                player.centery = height / 2
                gameOver = True
                print("You died")

            # Ticks and Display
            pygame.display.flip()
            fps.tick(60)
            LT += 1

def level_4():
    pygame.mixer.music.load('Sevcon.mp3')
    pygame.mixer.music.play(0)

def level_5():
    pygame.mixer.music.load('Chronos.mp3')
    pygame.mixer.music.play(0)

pygame.mixer.music.load(RectLobbyMusic)
pygame.mixer.music.play(0)

#Main condition
while True:
    screen.fill("black")
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_RETURN:
                if screenNumber==2 and not activeMusic is None and not busyFading:
                    if activeMusic==0:
                        level_1()
                        fading = True
                    elif activeMusic == 1:
                        level_2()
                        fading = True
                    elif activeMusic == 2:
                        level_3()
                    elif activeMusic == 3:
                        level_4()
                    elif activeMusic == 4:
                        level_5()
    movePlayer(player)

    for i in range(len(RectLevelSelect)):
        pygame.draw.rect(screen, "black", RectLevelSelect[i])
    pygame.draw.rect(screen, "yellow", RectLevelMusic[0][0])
    pygame.draw.rect(screen, "purple", RectLevelMusic[1][0])
    pygame.draw.rect(screen, "navy", RectLevelMusic[2][0])
    pygame.draw.rect(screen, "pink", RectLevelMusic[3][0])
    pygame.draw.rect(screen, "red", RectLevelMusic[4][0])
    drawText(font, "Welcome to Project Beats Remix", "white", 430, 300, 255)
    drawText(font, "Go to a level and hit 'Enter' to play", "white", 420, 400, 255)
    drawText(font, "Level 1: Coconut Mall", "purple", 15, 100, 255)
    drawText(font, "level 2: Focus", "yellow", 380, 100, 255)
    drawText(font, "level 3: Milky Ways", "orange", 670, 100, 255)
    drawText(font, "level 4: WIP", "dark green", 1020, 100, 255)
    drawText(font, "level 5: WIP", "cyan", 20, 340, 255)
    drawText(font, "level 6: ???", "white", 1020, 340, 255)
    drawText(font, "level 7: ???", "white", 20, 580, 255)
    drawText(font, "level 8: ???", "white", 380, 580, 255)
    drawText(font, "level 9: ???", "white", 670, 580, 255)
    drawText(font, "level 10: ???", "white", 1020, 580, 255)
    pygame.draw.rect(screen, "blue", player)

    musicIndex = None
    for i in range(len(RectLevelMusic)):
        if RectLevelMusic[i][0].collidepoint(player.center):
            musicIndex = i
            break
    if musicIndex != activeMusic or busyFading:
        if musicIndex is None and musicIndex != activeMusic and not fading:
            pygame.mixer.music.load(RectLobbyMusic)
            pygame.mixer.music.play(0)
        elif musicIndex != activeMusic and not fading:
            pygame.mixer.music.load(RectLevelMusic[musicIndex][1])
            pygame.mixer.music.play(0)
        if fading:
            busyFading = True
            volume = max(0.0, volume - fade_speed)
            pygame.mixer.music.set_volume(volume)
            if volume <= 0.0:
                fading = False
        else:
            activeMusic = musicIndex
            volume = min(1.0, volume + fade_speed)
            pygame.mixer.music.set_volume(volume)
            if volume >= 1.0:
                fading = True
                busyFading = False
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(0)
    pygame.display.flip()
    fps.tick(60)
