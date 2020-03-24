import pygame
import os  # When testing images


class Overlay:

    def __init__(self):
        self._cwdpath = os.getcwd()
        self.overlayimage = None  # Bottom Overlay

    def render(self, displaysurf):
        # Bottom_Overlay (Height is random - just looks nice)
        overlay_height = int(displaysurf.get_height() / 3)  # Take up bottom 1/3 of screen
        overlay_width = displaysurf.get_width()  # Screen Width
        self.overlayimg = pygame.transform.scale(self.overlayimage, (overlay_width, overlay_height))
        displaysurf.blit(self.overlayimg, (0, displaysurf.get_height() - overlay_height))

        # print(pygame.mouse.get_pos())

        # Set-up dimensions for other items based on screen size
        if displaysurf.get_rect().size == (800, 600):

            # LEFT OF SCREEN######################################################################################

            # Game Clock Area (In Middle to right of hologram) (red)
            clockHeight = 12
            clockWidth = 24
            pygame.draw.rect(displaysurf, (0, 0, 0), (114, 421, clockWidth, clockHeight))

            # MIDDLE OF SCREEN#####################################################################################

            # Hologram Area (Unit Chose Green Image in Middle)
            hologramHeight = 70
            hologramWidth = 70
            pygame.draw.rect(displaysurf, (255, 0, 0), (233, 494, hologramWidth, hologramHeight))

            # Hit Points Area (In Middle below hologram) (green)
            hitPointsHeight = 20
            hitPointsWidth = 70
            pygame.draw.rect(displaysurf, (0, 255, 0), (233, 569, hitPointsWidth, hitPointsHeight))

            # Selectable Name Area (In Middle to right of hologram) (blue)
            nameHeight = 20
            nameWidth = 140
            pygame.draw.rect(displaysurf, (0, 0, 255), (308, 494, nameWidth, nameHeight))

            # Profile Area (Unit Chose Image) (magenta)
            profileHeight = 115
            profileWidth = 50
            pygame.draw.rect(displaysurf, (255, 0, 255), (579, 480, profileWidth, profileHeight))

            # RIGHT SIDE OF SCREEN (BOTTOM)########################################################################################

            # Menu Button (Red)
            menuButtonHeight = 18
            menuButtonWidth = 26
            pygame.draw.rect(displaysurf, (255, 0, 0), (771, 433, menuButtonWidth, menuButtonHeight))

            # ROW 1 #########################
            # BUTTON is eventualy going to be its own class, and you'll use one of these dimensions to draw the button.

            # #Button1 (White)
            genericButtonHeight = 26
            genericButtonWidth = 26
            pygame.draw.rect(displaysurf, (255, 255, 255), (643, 467, genericButtonWidth, genericButtonHeight))

            # #IMAGE TEST
            # self.button1 = pygame.image.load(os.path.join(self._cwdpath,"Images/Overlay","Barracks_Button_BuildMarine.png")).convert_alpha()
            # self.button1_trans = pygame.transform.scale(self.button1,(26, 26))
            # displaysurf.blit(self.button1_trans, (643, 467))

            # Button2
            pygame.draw.rect(displaysurf, (255, 0, 0), (672, 467, genericButtonWidth, genericButtonHeight))

            # Button3
            pygame.draw.rect(displaysurf, (0, 255, 0), (701, 467, genericButtonWidth, genericButtonHeight))

            # Button4
            pygame.draw.rect(displaysurf, (0, 0, 255), (730, 467, genericButtonWidth, genericButtonHeight))

            # Button5
            pygame.draw.rect(displaysurf, (255, 255, 0), (759, 467, genericButtonWidth, genericButtonHeight))

            # ROW 2 #################################################################################################

            # Button6 (Yellow)
            pygame.draw.rect(displaysurf, (255, 255, 0), (643, 507, genericButtonWidth, genericButtonHeight))

            # Button7
            pygame.draw.rect(displaysurf, (0, 0, 255), (672, 507, genericButtonWidth, genericButtonHeight))

            # Button8
            pygame.draw.rect(displaysurf, (128, 128, 128), (701, 507, genericButtonWidth, genericButtonHeight))

            # Button9
            pygame.draw.rect(displaysurf, (255, 0, 0), (730, 507, genericButtonWidth, genericButtonHeight))

            # Button10
            pygame.draw.rect(displaysurf, (255, 255, 255), (759, 507, genericButtonWidth, genericButtonHeight))

            # ROW 3 #############################################################################################

            # Button11 (White)
            pygame.draw.rect(displaysurf, (255, 255, 255), (643, 550, genericButtonWidth, genericButtonHeight))

            # Button12
            pygame.draw.rect(displaysurf, (255, 0, 0), (672, 550, genericButtonWidth, genericButtonHeight))

            # Button13
            pygame.draw.rect(displaysurf, (0, 255, 0), (701, 550, genericButtonWidth, genericButtonHeight))

            # Button14
            pygame.draw.rect(displaysurf, (0, 0, 255), (730, 550, genericButtonWidth, genericButtonHeight))

            # Button15
            pygame.draw.rect(displaysurf, (255, 255, 0), (759, 550, genericButtonWidth, genericButtonHeight))

            # RIGHT SIDE OF SCREEN (TOP)########################################################################################

            # Mineral Sprite (Yellow)
            mineralSpriteHeight = 20
            mineralSpriteWidth = 20
            pygame.draw.rect(displaysurf, (255, 255, 0), (530, 20, mineralSpriteWidth, mineralSpriteHeight))

            # Mineral Amount (Orange)
            mineralAmtHeight = 20
            mineralAmtWidth = 40
            pygame.draw.rect(displaysurf, (255, 155, 0), (555, 20, mineralAmtWidth, mineralAmtHeight))

            # Vespene Sprite (blue)
            vespeneSpriteHeight = 20
            vespeneSpriteWidth = 20
            pygame.draw.rect(displaysurf, (0, 255, 255), (615, 20, vespeneSpriteWidth, vespeneSpriteHeight))

            # Vespene Amount (teal)
            vespeneAmtHeight = 20
            vespeneAmtWidth = 40
            pygame.draw.rect(displaysurf, (0, 255, 155), (640, 20, vespeneAmtWidth, vespeneAmtHeight))

            # Population Sprite (pink)
            popSpriteHeight = 20
            popSpriteWidth = 20
            pygame.draw.rect(displaysurf, (255, 0, 255), (700, 20, popSpriteWidth, popSpriteHeight))

            # Population Amount (dark pink)
            popAmtHeight = 20
            popAmtWidth = 40
            pygame.draw.rect(displaysurf, (255, 0, 155), (725, 20, popAmtWidth, popAmtHeight))

        elif displaysurf.get_rect().size == (1350, 750):

            # BoxAroundMini
            genericButtonHeight = 180
            genericButtonWidth = 180
            pygame.draw.rect(displaysurf, (255, 0, 0), (
            22, displaysurf.get_height() - genericButtonHeight - 12, genericButtonWidth, genericButtonHeight))

    def renderGameClock(self, displaysurf):

        # Set-up dimensions for other items based on screen size
        if displaysurf.get_rect().size == (800, 600):
            # print(pygame.time.get_ticks())
            font = pygame.font.SysFont(None, 14)
            img = font.render('12:44', True, (255, 255, 255))
            displaysurf.blit(img, (114, 421))
