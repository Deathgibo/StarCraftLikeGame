import pygame
import os

class Overlay:

    def __init__(self):
        self._cwdpath = None    #Same path as in main
        self.start_time = 0     #Used to keep track of when game started AFTER menu (milliseconds)
        self.printMinutes = 0   #Keep Track of minutes played in-game,

    def load_media(self, cwdpath):
        self._cwdpath = cwdpath

        #Overlay
        self.overlayimage = pygame.image.load(
            os.path.join(self._cwdpath, "Images/Overlay", "CleanBottomOverlay.png")).convert_alpha()

        #Resource Icons
        self.mineralOverlay = pygame.image.load(
            os.path.join(self._cwdpath,"Images/Overlay","Mineral_Overlay.png")).convert_alpha()
        self.vespeneOverlay = pygame.image.load(
            os.path.join(self._cwdpath,"Images/Overlay","Vespene_Overlay.png")).convert_alpha()
        self.populationOverlay = pygame.image.load(
            os.path.join(self._cwdpath,"Images/Overlay","Population_Overlay.png")).convert_alpha()

        #Green Holograms
        #####Troops
        self.marineHolo = pygame.image.load(
            os.path.join(self._cwdpath,"Images/Overlay","Marine_Holo.png")).convert_alpha()
        self.workerHolo = pygame.image.load(
            os.path.join(self._cwdpath,"Images/Overlay","Worker_Holo.png")).convert_alpha()
        ######Buildings
        self.commandCenterHolo = pygame.image.load(
            os.path.join(self._cwdpath,"Images/Overlay","CommandCenter_Holo.png")).convert_alpha()

        #Profiles
        self.marineProfile = pygame.image.load(
            os.path.join(self._cwdpath,"Images/Overlay","Marine_Profile.png")).convert_alpha()
        self.robotProfile = pygame.image.load(
            os.path.join(self._cwdpath,"Images/Overlay","Robot_Profile.png")).convert_alpha()
        self.workerProfile = pygame.image.load(
            os.path.join(self._cwdpath,"Images/Overlay","Worker_Profile.png")).convert_alpha()
        
    def renderBottomOverlay(self, displaysurf):
        # Bottom_Overlay (Height is random - just looks nice)
        overlay_height = int(displaysurf.get_height() / 3)  # Take up bottom 1/3 of screen
        overlay_width = displaysurf.get_width()  # Screen Width
        self.overlayimg = pygame.transform.scale(self.overlayimage, (overlay_width, overlay_height))
        displaysurf.blit(self.overlayimg, (0, displaysurf.get_height() - overlay_height))

    #Render game clock in left hand corner of screen
    def renderGameClock(self, displaysurf):
        # Set-up dimensions for other items based on screen size
        if displaysurf.get_rect().size == (800, 600):
            #Get start time of game
            if self.start_time == 0:
                self.start_time = pygame.time.get_ticks()
            else:
                #Subtract start time of game from ticks to get actual game time
                self.gameTime = pygame.time.get_ticks() - self.start_time
                self.gameSeconds = int(self.gameTime/1000)

                #Calculating times (Just doing seconds and minutes)
                self.printSeconds = self.gameSeconds % 60
                if self.gameSeconds % 60 == 0 and self.gameSeconds != 0:
                    self.printMinutes = int(self.gameSeconds / 60)

                #Create string for time (zfill is just padding 0's in front)
                self.time = str(self.printMinutes).zfill(2) + ":" + str(self.printSeconds).zfill(2)
                font = pygame.font.SysFont(None, 14)
                img = font.render(self.time, True, (255, 255, 255))
                displaysurf.blit(img, (114, 421))

    #Render items in the top right of screen
    def renderResources(self, displaysurf, playerinfo):
        # Set-up dimensions for other items based on screen size
        if displaysurf.get_rect().size == (800, 600):
            # Mineral Sprite (Yellow)
            self.mineralOverlay_trans = pygame.transform.scale(self.mineralOverlay,(20, 20))
            displaysurf.blit(self.mineralOverlay_trans, (530, 20))
            
            # Mineral Amount (Orange)
            font = pygame.font.SysFont(None, 26)
            img = font.render(str(playerinfo.resources), True, (0, 0, 0))
            displaysurf.blit(img, (555, 20))
            font = pygame.font.SysFont(None, 24)
            img = font.render(str(playerinfo.resources), True, (255, 255, 255))
            displaysurf.blit(img, (556, 21))
        
            # Vespene Sprite (blue)
            self.vespeneOverlay_trans = pygame.transform.scale(self.vespeneOverlay,(20, 20))
            displaysurf.blit(self.vespeneOverlay_trans, (615, 20))

            # Vespene Amount (teal)
            font = pygame.font.SysFont(None, 26)
            img = font.render(str(playerinfo.supply), True, (0, 0, 0))
            displaysurf.blit(img, (640, 20))
            font = pygame.font.SysFont(None, 24)
            img = font.render(str(playerinfo.supply), True, (255, 255, 255))
            displaysurf.blit(img, (641, 21))

            # Population Sprite (pink)
            self.populationOverlay_trans = pygame.transform.scale(self.populationOverlay,(20, 20))
            displaysurf.blit(self.populationOverlay_trans, (700, 20))

            # Population Amount (dark pink)
            font = pygame.font.SysFont(None, 26)
            img = font.render(str(playerinfo.population), True, (0, 0, 0))
            displaysurf.blit(img, (725, 20))
            font = pygame.font.SysFont(None, 24)
            img = font.render(str(playerinfo.population), True, (255, 255, 255))
            displaysurf.blit(img, (726, 21))

    def renderSelectedItem(self, displaysurf, selectedEntityList, selectedBuildingList):    
        # Set-up dimensions for other items based on screen size
        if displaysurf.get_rect().size == (800, 600):

            #Nothing chosen
            if len(selectedEntityList) == 0 and len(selectedBuildingList) == 0:
                #Profile Area (Unit Chose Image)
                self.robotProfile_trans = pygame.transform.scale(self.robotProfile,(50, 115))
                displaysurf.blit(self.robotProfile_trans, (579, 480))
                return

            #Selected one entity (troop) 
            #Right now multiple due to selectedEntityList bug 
            elif len(selectedEntityList) != 0 and len(selectedBuildingList) == 0:
                #Grab first item in list as the figure-head stat to show
                classSelected = selectedEntityList[0].__class__.__name__

                #Hit Points Area (In Middle below hologram)
                font = pygame.font.SysFont(None, 26)
                printHitpoints = str(selectedEntityList[0].health) + "/" + str(selectedEntityList[0].maxhealth)
                img = font.render(printHitpoints, True, (255, 255, 255))
                displaysurf.blit(img, (250, 569))
                
                # Selectable Name Area (In Middle to right of hologram)
                font = pygame.font.SysFont(None, 26)
                img = font.render(classSelected, True, (255, 255, 255))
                displaysurf.blit(img, (318, 494))
                
                #Listed Alphabetically (Unit Specific items like Hologram, Profiles, and Buttons(eventually!))
                #####Entities
                if classSelected == "Marauder":
                    #I'll get it later, I made all holo's and button sizes the same
                    pass

                elif classSelected == "Marine":
                    # Hologram Area (Unit Chose Green Image in Middle)
                    self.marineHolo_trans = pygame.transform.scale(self.marineHolo,(70, 70))
                    displaysurf.blit(self.marineHolo_trans, (233, 494))

                    #Profile Area (Unit Chose Image)
                    self.marineProfile_trans = pygame.transform.scale(self.marineProfile,(50, 115))
                    displaysurf.blit(self.marineProfile_trans, (579, 480))

                elif classSelected == "Worker":
                    # Hologram Area (Unit Chose Green Image in Middle)
                    self.workerHolo_trans = pygame.transform.scale(self.workerHolo,(70, 70))
                    displaysurf.blit(self.workerHolo_trans, (233, 494))

                    #Profile Area (Unit Chose Image)
                    self.workerProfile_trans = pygame.transform.scale(self.workerProfile,(50, 115))
                    displaysurf.blit(self.workerProfile_trans, (579, 480))
                return

            #Selected one building
            elif len(selectedEntityList) == 0 and len(selectedBuildingList) == 1:
                #Grab first item in list as the figure-head stat to show
                classSelected = selectedBuildingList[0].__class__.__name__

                #Grab first item in list as the figure-head stat to show
                classSelected = selectedBuildingList[0].__class__.__name__

                #Hit Points Area (In Middle below hologram)
                font = pygame.font.SysFont(None, 26)
                printHitpoints = str(selectedBuildingList[0].health) + "/" + str(selectedBuildingList[0].maxhealth)
                img = font.render(printHitpoints, True, (255, 255, 255))
                displaysurf.blit(img, (250, 569))
                
                # Selectable Name Area (In Middle to right of hologram)
                font = pygame.font.SysFont(None, 26)
                img = font.render(classSelected, True, (255, 255, 255))
                displaysurf.blit(img, (318, 494))

                if classSelected == "CommandCenter":
                    # Hologram Area (Unit Chose Green Image in Middle)
                    self.commandCenterHolo_trans = pygame.transform.scale(self.commandCenterHolo,(70, 70))
                    displaysurf.blit(self.commandCenterHolo_trans, (233, 494))

                    #Profile Area (Unit Chose Image)
                    self.robotProfile_trans = pygame.transform.scale(self.robotProfile,(50, 115))
                    displaysurf.blit(self.robotProfile_trans, (579, 480))

    def renderTemplate(self, displaysurf):
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

