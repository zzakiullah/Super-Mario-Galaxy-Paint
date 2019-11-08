# SMG_Paint.py

# Zulaikha Zakiullah

# Although the title is "Super Mario Galaxy Paint", this program also has
# aspects of the sequel Super Mario Galaxy 2, so it's more of a paint
# program of the Galaxy Series.

from pygame import *
from tkinter import *
from tkinter.colorchooser import *
import tkinter.messagebox as messagebox
from random import *
from math import *
import os

font.init()
init()

root = Tk()
root.withdraw() 

# font for labels
calibriSmall = font.SysFont("Calibri", 14)
calibriNorm = font.SysFont("Calibri", 16)
calibriBig = font.SysFont("Calibri", 18)
calibriBold = font.SysFont("Calibri", 18, True)

# displaying the paint screen in the middle of the computer screen
inf = display.Info()
windowWth, windowHt = inf.current_w, inf.current_h
windowPos = str((windowWth-1200)//2)+", "+str((windowHt-700)//2)
os.environ['SDL_VIDEO_WINDOW_POS'] = windowPos
screen = display.set_mode((1200, 700))

# the top bar display
display.set_caption('Untitled - Super Mario Galaxy Paint')
mushroom = image.load("Pictures/Other/mushroom.png")
mushroom = transform.scale(mushroom, (32, 32))
display.set_icon(mushroom)

mx, my = mouse.get_pos()  # to prevent from crashing if someone decides to
mxStart = mx              # hold down on the mouse button before the program
myStart = my              # even starts

# background and title
spacePic = image.load("Pictures/Backgrounds/Screen-background.jpg")
origSmgLogo = image.load("Pictures/Other/SMG-logo.png")
paintPic = image.load("Pictures/Other/Paint-logo.png")
# NOTE FOR paintPic ^
# I couldn't load this font even after downloading it, so I just did the "Paint"
# title separately on PowerPoint and saved it as a picture

orig_mario_paint = image.load("Pictures/Other/Mario-painting.png")
orig_babyLuma_paint = image.load("Pictures/Other/Luma-painting.png")

spacePic = transform.scale(spacePic, (1200, 700))
smgLogo = transform.scale(origSmgLogo, (137, 80))
paintPic = transform.scale(paintPic, (241, 70))
mario_paint = transform.scale(orig_mario_paint, (118, 150))
babyLuma_paint = transform.scale(orig_babyLuma_paint, (90, 60))

screen.blit(spacePic, (0, 0))
screen.blit(smgLogo, (400, 5))
screen.blit(paintPic, (559, 10))
screen.blit(mario_paint, (280, -35))
screen.blit(babyLuma_paint, (802, 15))

# drawing surface
canvas = Rect(120, 90, 960, 500)
draw.rect(screen, (255, 255, 255), (canvas))
draw.rect(screen, (0), (119, 89, 962, 502), 1)

# undo/redo lists
undoScreens = []
redoScreens = []

add = True  # flag used when adding canvases to undoScreens
            # used to prevent the program from crashing when copying and adding
            # too many canvases to the undoScreens list
clearAdd = True  # flag used when adding canvases after using the clear button
take = True # flag used when clicking the undo or redo button

cutting = False  # flags for cut and copy tool (cutting is only used in cut tool,
copying = False  # as copying is only used in copy tool; pasting is used in both  
pasting = False

# loading command buttons
saveAsIcon = image.load("Pictures/Commands/save-as.png")
undoIcon = image.load("Pictures/Commands/undo.png")
redoIcon = image.load("Pictures/Commands/redo.png")
newIcon = image.load("Pictures/Commands/new.png")
openIcon = image.load("Pictures/Commands/open.png")
loadIcon = image.load("Pictures/Commands/load.png")
cutIcon = image.load("Pictures/Commands/cut.png")
copyIcon = image.load("Pictures/Commands/copy.png")
clearIcon = image.load("Pictures/Commands/clear.png")

# loading the tool icons
pencilIcon = image.load("Pictures/Tools/pencil.png")
markerIcon = image.load("Pictures/Tools/marker.png")
eraserIcon = image.load("Pictures/Tools/eraser.png")
dropperIcon = image.load("Pictures/Tools/dropper.png")
bucketIcon = image.load("Pictures/Tools/paint-bucket.png")
sprayPaintIcon = image.load("Pictures/Tools/spray-paint.png")
calligraphyIcon = image.load("Pictures/Tools/calligraphy-pen.png")

# undo, redo, save, and loading image Rects
saveRect = Rect(7, 92, 33, 33)
undoRect = Rect(43, 92, 33, 33)
redoRect = Rect(79, 92, 33, 33)
newRect = Rect(7, 130, 33, 33)
openRect = Rect(43, 130, 33, 33)
loadRect = Rect(79, 130, 33, 33)
cutRect = Rect(7, 168, 33, 33)
copyRect = Rect(43, 168, 33, 33)
clearRect = Rect(79, 168, 33, 33)

# tool Rects and icons
pencilRect = Rect(14, 236, 43, 43)
markerRect = Rect(62, 236, 43, 43)
eraserRect = Rect(14, 282, 43, 43)
dropperRect = Rect(62, 282, 43, 43)
bucketRect = Rect(14, 328, 43, 43)
sprayPaintRect = Rect(62, 328, 43, 43)
textRect = Rect(14, 374, 43, 43)
calligraphyRect = Rect(62, 374, 43, 43)

# shape Rects, along with the fill/no fill toggler
fillRect = Rect(13, 453, 93, 38)
fillToggler = Rect(14, 454, 46, 36)
lineRect = Rect(14, 497, 43, 43)
rectRect = Rect(62, 497, 43, 43)
ellipseRect = Rect(14, 547, 43, 43)
polygonRect = Rect(62, 547, 43, 43)

# scaling the commands and tools together and blitting them as well
icons = [saveAsIcon, undoIcon, redoIcon, newIcon, openIcon, loadIcon,
         cutIcon, copyIcon, clearIcon, pencilIcon, markerIcon, eraserIcon,
         dropperIcon, bucketIcon, sprayPaintIcon, calligraphyIcon]
iconScales = [(27, 26), (29, 28), (29, 28), (28, 28), (27, 27), (28, 28),
              (33, 33), (23, 27), (30, 30), (40, 40), (40, 40), (40, 40),
              (38, 42), (40, 40), (40, 40), (43, 43)]
blitIcons = [(10, 95), (45, 96), (80, 96), (9, 132), (46, 132), (81, 133),
             (6, 167), (48, 171), (81, 169), (17, 236), (65, 236), (17, 282),
             (66, 282), (15, 329), (64, 328), (62, 374)]
iconRects = [saveRect, undoRect, redoRect, newRect, openRect, loadRect,
             cutRect, copyRect, clearRect, pencilRect, markerRect, eraserRect,
             dropperRect, bucketRect, sprayPaintRect, calligraphyRect,
             lineRect, rectRect, ellipseRect, polygonRect]
for i in icons:
    a = icons.index(i)
    i = transform.scale(i, (iconScales[a]))
    icons[a] = i
    screen.blit(i, (blitIcons[a]))

# text icon is an exception to the list
arialBig = font.SysFont("Arial", 40)
textPic = arialBig.render("A", True, (255, 255, 255))
screen.blit(textPic, (24, 372))

# command Rect copies
# I loaded the save button ahead of time and saved a copy of the Rect it took up
# (hence why the saveRectCopy is being loaded and not copied). 
saveAsRectCopy = screen.subsurface(saveRect).copy()
saveRectCopy = image.load("Pictures/Commands/saveRectCopy.png")
undoRectCopy = screen.subsurface(undoRect).copy()
redoRectCopy = screen.subsurface(redoRect).copy()
newRectCopy = screen.subsurface(newRect).copy()
openRectCopy = screen.subsurface(openRect).copy()
loadRectCopy = screen.subsurface(loadRect).copy()
cutRectCopy = screen.subsurface(cutRect).copy()
copyRectCopy = screen.subsurface(copyRect).copy()
clearRectCopy = screen.subsurface(clearRect).copy()

# tool Rect copies
pencilRectCopy = screen.subsurface(pencilRect).copy()
markerRectCopy = screen.subsurface(markerRect).copy()
eraserRectCopy = screen.subsurface(eraserRect).copy()
dropperRectCopy = screen.subsurface(dropperRect).copy()
bucketRectCopy = screen.subsurface(bucketRect).copy()
sprayPaintRectCopy = screen.subsurface(sprayPaintRect).copy()
textRectCopy = screen.subsurface(textRect).copy()
calligraphyRectCopy = screen.subsurface(calligraphyRect).copy()

# shape Rect copies
draw.line(screen, (255, 0, 0), (18, 533), (52, 502), 2)
draw.rect(screen, (0, 255, 255), (68, 505, 30, 26), 2)
draw.ellipse(screen, (255, 255, 0), (18, 553, 36, 31), 2)
draw.polygon(screen, (0, 255, 0), ((68, 554), (88, 554), (98, 567), (98, 581), (68, 581), (74, 571)), 2)

lineCopy = screen.subsurface(lineRect).copy()
rectEmptyCopy = screen.subsurface(rectRect).copy()
ellipseEmptyCopy = screen.subsurface(ellipseRect).copy()
polygonEmptyCopy = screen.subsurface(polygonRect).copy() 

draw.rect(screen, (0, 255, 255), (68, 505, 30, 26), 0)
draw.ellipse(screen, (255, 255, 0), (18, 553, 36, 31), 0)
draw.polygon(screen, (0, 255, 0), ((68, 554), (88, 554), (98, 567), (98, 581), (68, 581), (74, 571)), 0)

rectFillCopy = screen.subsurface(rectRect).copy()
ellipseFillCopy = screen.subsurface(ellipseRect).copy()
polygonFillCopy = screen.subsurface(polygonRect).copy()

# fill/no fill toggler
draw.rect(screen, (255, 255, 255), (fillRect))
fillTxt = calibriBold.render("Fill", True, (0, 0, 0))
noTxt = calibriBold.render("No", True, (0, 0, 0))
screen.blit(fillTxt, (26, 464))
screen.blit(noTxt, (72, 456))
screen.blit(fillTxt, (73, 472))
fillRectCopy = screen.subsurface(fillRect).copy()
draw.rect(screen, (0), (fillToggler))

# tool thicknesses
pencilSize = 4
markerSize = 20
eraserSize = 20
sprayPaintSize = 30
textSize = 18
calligraphySize = 10
shapeSize = 2
lineSize = shapeSize  # except when shapes are filled (at that point shapeSize
                      # would be zero and lineSize would hold the last value of
                      # shapeSize that was not zero)

sizes = [pencilSize, markerSize, eraserSize, sprayPaintSize, calligraphySize,   
         lineSize, textSize, shapeSize]
tools = ["pencil", "marker", "eraser", "spray paint", "calligraphy", "line", "text", 
         "rectangle", "ellipse", "stamp", "picture", "cut", "copy", 
         "choose background", "polygon", "dropper", "bucket"]
toolLabels = ["Pencil Thickness: ", "Marker Thickness: ", "Eraser Thickness: ",
              "Spray Paint Radius: ", "Calligraphy Pen Thickness: ", "Line Thickness: ", 
              "Font Size: ", "Rectangle Size: ", "Ellipse Size: ",
              "Stamp Size: ", "Picture Size: ", "Selected Size: ", "Selected Size: ",
              "Background: ",  "Number of Sides: ", "Dropper", "Fill Bucket"]
toolLabelRect = Rect(780, 592, 300, 20)
labelRectCopy = screen.subsurface(toolLabelRect).copy()

tool = "pencil"
shapeFormat = "no fill"
command = ""

# so many flags

saveAs = True # flag for program to know when to save as and when to just save
filepath = "Untitled"  # default filepath/filename
saved = False  # flag for when the canvas has been saved
loaded = False  # flag for when an image has been loaded

fill = False # flag for fill bucket tool

signs = [-1, 1] # for spray paint
sp = 0 # spray paint counter

calibriTxt = font.SysFont("Calibri", textSize)
txt = ""  # text that the user types (using the text tool)
newTxt = ""
txtBox = False
drewBox = False

useOld = True  # flag for shape tools

clickPt = True  # flag for polygon function, so the program records the
                # coordinates of a point once
starting = True  # another flag for polygon function, so the program knows
                 # when to record the first point of the polygon
drawing = False  # yet another polygon function flag, used to let the program
                 # know when the user is beginning to draw his/her shape
pts = []  # list of points in polygon
sides = 0  # number of sides in the polygon

oldCanvas = screen.subsurface(canvas).copy()

pt = (0, 0)               # point in polygon (used in polygon function)

# loading stamps (and up and down arrows for stamps)
upArrow = image.load("Pictures/Other/up-arrow.png")
downArrow = image.load("Pictures/Other/down-arrow.png")

upArrow = transform.scale(upArrow, (73, 20))
downArrow = transform.scale(downArrow, (73, 20))

upRect = Rect(1100, 90, 79, 20)
downRect = Rect(1100, 550, 79, 20)

screen.blit(upArrow, (1102, 90))
screen.blit(downArrow, (1102, 550))
upArrowCopy = screen.subsurface(upRect).copy()
downArrowCopy = screen.subsurface(downRect).copy()

# loading all the stamps -- perhaps I went *a little* overboard

# section 1
origMario = image.load("Pictures/Stamps/Mario.png") 
origLuigi = image.load("Pictures/Stamps/Luigi.png")
origPeach = image.load("Pictures/Stamps/Princess-Peach.png")
origBowser = image.load("Pictures/Stamps/Bowser.png")
origRosalina = image.load("Pictures/Stamps/Rosalina.png")

mario = transform.scale(origMario, (150, 200))
luigi = transform.scale(origLuigi, (101, 200))
peach = transform.scale(origPeach, (107, 200))
bowser = transform.scale(origBowser, (200, 200))
rosalina = transform.scale(origRosalina, (155, 200))

# section 2
origYoshi = image.load("Pictures/Stamps/Yoshi.png")
origBowserJr = image.load("Pictures/Stamps/Bowser-Jr.png")
origPolari = image.load("Pictures/Stamps/Polari.png")
origBabyLuma = image.load("Pictures/Stamps/Baby-Luma.png")
origLubba = image.load("Pictures/Stamps/Lubba.png")

yoshi = transform.scale(origYoshi, (133, 200))
bowserJr = transform.scale(origBowserJr, (129, 200))
polari = transform.scale(origPolari, (106, 100))
babyLuma = transform.scale(origBabyLuma, (98, 90))
lubba = transform.scale(origLubba, (181, 200))

# section 3
origCaptainToad = image.load("Pictures/Stamps/Captain-Toad.png") # technically the picture is from a different video game
origBlueToad = image.load("Pictures/Stamps/Blue-Toad.png")
origYellowToad = image.load("Pictures/Stamps/Yellow-Toad.png")
origBankToad = image.load("Pictures/Stamps/Banktoad.png") # this was fun to photoshop
origMailToad = image.load("Pictures/Stamps/Mailtoad.png")

captainToad = transform.scale(origCaptainToad, (102, 102))
blueToad = transform.scale(origBlueToad, (58, 100))
yellowToad = transform.scale(origYellowToad, (82, 104))
bankToad = transform.scale(origBankToad, (120, 104))
mailToad = transform.scale(origMailToad, (67, 102))

# section 4
origPowerStar = image.load("Pictures/Stamps/Power-Star.png")
origGrandStar = image.load("Pictures/Stamps/Grand-Star.png")
origGreenStar = image.load("Pictures/Stamps/Green-Star.png")
origRedStar = image.load("Pictures/Stamps/Red-Star.png")
origBronzeStar = image.load("Pictures/Stamps/Bronze-Star.png")

powerStar = transform.scale(origPowerStar, (100, 100))
grandStar = transform.scale(origGrandStar, (117, 120))
greenStar = transform.scale(origGreenStar, (101, 100))
redStar = transform.scale(origRedStar, (100, 100))
bronzeStar = transform.scale(origBronzeStar, (100, 100))

# section 5
origYellowLuma = image.load("Pictures/Stamps/Yellow-Luma.png")
origBlueLuma = image.load("Pictures/Stamps/Blue-Luma.png")
origCoStarLuma = image.load("Pictures/Stamps/Co-Star-Luma.png")
origRedLuma = image.load("Pictures/Stamps/Red-Luma.png")
origGreenLuma = image.load("Pictures/Stamps/Green-Luma.png")

yellowLuma = transform.scale(origYellowLuma, (100, 100))
blueLuma = transform.scale(origBlueLuma, (100, 100))
coStarLuma = transform.scale(origCoStarLuma, (100, 100))
redLuma = transform.scale(origRedLuma, (100, 100))
greenLuma = transform.scale(origGreenLuma, (100, 100))

# section 6
origSilverStar = image.load("Pictures/Stamps/Silver-Star.png")
origMarioSpinning = image.load("Pictures/Stamps/Mario-spinning.png")
origMarioFlying = image.load("Pictures/Stamps/Mario-flying.png")
origMarioYoshiLuma = image.load("Pictures/Stamps/Mario-Yoshi-Luma-flying.png")
origFaceship = image.load("Pictures/Stamps/Mario-faceship.png")

silverStar = transform.scale(origSilverStar, (80, 80))
marioSpinning = transform.scale(origMarioSpinning, (204, 170))
marioFlying = transform.scale(origMarioFlying, (180, 150))
marioYoshiLuma = transform.scale(origMarioYoshiLuma, (206, 200))
faceship = transform.scale(origFaceship, (212, 220))

# the copies of every stamp surface

# section 1
marioCopy = image.load("Pictures/Stamp Surfaces/Mario-copy.png")
luigiCopy = image.load("Pictures/Stamp Surfaces/Luigi-copy.png")
peachCopy = image.load("Pictures/Stamp Surfaces/Peach-copy.png")
bowserCopy = image.load("Pictures/Stamp Surfaces/Bowser-copy.png")
rosalinaCopy = image.load("Pictures/Stamp Surfaces/Rosalina-copy.png")

# section 2
yoshiCopy = image.load("Pictures/Stamp Surfaces/Yoshi-copy.png")
bowserJrCopy = image.load("Pictures/Stamp Surfaces/Bowser_Jr-copy.png")
polariCopy = image.load("Pictures/Stamp Surfaces/Polari-copy.png")
babyLumaCopy = image.load("Pictures/Stamp Surfaces/Baby_Luma-copy.png")
lubbaCopy = image.load("Pictures/Stamp Surfaces/Lubba-copy.png")

# section 3
captainToadCopy = image.load("Pictures/Stamp Surfaces/Captain_Toad-copy.png")
blueToadCopy = image.load("Pictures/Stamp Surfaces/Blue_Toad-copy.png")
yellowToadCopy = image.load("Pictures/Stamp Surfaces/Yellow_Toad-copy.png")
bankToadCopy = image.load("Pictures/Stamp Surfaces/Bank_Toad-copy.png")
mailToadCopy = image.load("Pictures/Stamp Surfaces/Mail_Toad-copy.png")

# section 4
powerStarCopy = image.load("Pictures/Stamp Surfaces/Power_Star-copy.png")
grandStarCopy = image.load("Pictures/Stamp Surfaces/Grand_Star-copy.png")
greenStarCopy = image.load("Pictures/Stamp Surfaces/Green_Star-copy.png")
redStarCopy = image.load("Pictures/Stamp Surfaces/Red_Star-copy.png")
bronzeStarCopy = image.load("Pictures/Stamp Surfaces/Bronze_Star-copy.png")

# section 5
yellowLumaCopy = image.load("Pictures/Stamp Surfaces/Yellow_Luma-copy.png")
blueLumaCopy = image.load("Pictures/Stamp Surfaces/Blue_Luma-copy.png")
coStarLumaCopy = image.load("Pictures/Stamp Surfaces/Co-Star_Luma-copy.png")
redLumaCopy = image.load("Pictures/Stamp Surfaces/Red_Luma-copy.png")
greenLumaCopy = image.load("Pictures/Stamp Surfaces/Green_Luma-copy.png")

# section 6
silverStarCopy = image.load("Pictures/Stamp Surfaces/Silver_Star-copy.png")
marioSpinningCopy = image.load("Pictures/Stamp Surfaces/Mario_spinning-copy.png")
marioFlyingCopy = image.load("Pictures/Stamp Surfaces/Mario_flying-copy.png")
marioYoshiLumaCopy = image.load("Pictures/Stamp Surfaces/Mario_Yoshi_Luma-copy.png")
faceshipCopy = image.load("Pictures/Stamp Surfaces/faceship-copy.png")

# stamps after will not be displayed on screen (can be attained in special
# cases
origMarioYoshi = image.load("Pictures/Upgrades/Mario-on-Yoshi.png")
origLuigiYoshi = image.load("Pictures/Upgrades/Luigi-on-Yoshi.png")

marioYoshi = transform.scale(origMarioYoshi, (201, 200))
luigiYoshi = transform.scale(origLuigiYoshi, (185, 200))

# upgraded versions of Mario or Yoshi after consuming one of the power-ups
origDashYoshi = image.load("Pictures/Upgrades/Dash-Yoshi.png")
origBeeMario = image.load("Pictures/Upgrades/Bee-Mario.png")
origBooMario = image.load("Pictures/Upgrades/Boo-Mario.png")
origRockMario = image.load("Pictures/Upgrades/Rock-Mario.png")
origSpringMario = image.load("Pictures/Upgrades/Spring-Mario.png")
origRainbowMario = image.load("Pictures/Upgrades/Rainbow-Mario.png")
origBlimpYoshi = image.load("Pictures/Upgrades/Blimp-Yoshi.png")
origBulbYoshi = image.load("Pictures/Upgrades/Bulb-Yoshi.jpg")
origFireMario = image.load("Pictures/Upgrades/Fire-Mario.png")
origIceMario = image.load("Pictures/Upgrades/Ice-Mario.png")
origCloudMario = image.load("Pictures/Upgrades/Cloud-Mario.png")
origSpinMario = image.load("Pictures/Upgrades/Spin-Mario.png")
origFlyMario = image.load("Pictures/Upgrades/Flying-Mario.png")

dashYoshi = transform.scale(origDashYoshi, (300, 201))
beeMario = transform.scale(origBeeMario, (150, 200))
booMario = transform.scale(origBooMario, (200, 200))
rockMario = transform.scale(origRockMario, (220, 200))
springMario = transform.scale(origSpringMario, (200, 200))
rainbowMario = transform.scale(origRainbowMario, (253, 200))
blimpYoshi = transform.scale(origBlimpYoshi, (214, 270))
bulbYoshi = transform.scale(origBulbYoshi, (238, 200))
fireMario = transform.scale(origFireMario, (254, 200))
iceMario = transform.scale(origIceMario, (174, 200))
cloudMario = transform.scale(origCloudMario, (189, 250))
spinMario = transform.scale(origSpinMario, (169, 250))
flyMario = transform.scale(origFlyMario, (190, 172))

# each row in the stamps list corresponds to when each stamp appears (the first 5 in row 1
# appear first; when the user clicks the down button, the 5 in the second row appear, and
# so on; however, anything after faceship are bonus stamps
stamps = [mario, luigi, peach, bowser, rosalina,    
          yoshi, bowserJr, polari, babyLuma, lubba,
          captainToad, blueToad, yellowToad, bankToad, mailToad,
          powerStar, grandStar, greenStar, redStar, bronzeStar,
          yellowLuma, blueLuma, coStarLuma, redLuma, greenLuma,
          silverStar, marioSpinning, marioFlying, marioYoshiLuma, faceship,
          marioYoshi, luigiYoshi,
          blimpYoshi, beeMario, booMario, rockMario, springMario, rainbowMario,
          dashYoshi, bulbYoshi, fireMario, iceMario, cloudMario, spinMario,
          flyMario]

# original pictures; used when resizing pictures in the program, or else (I
# learned) you end up getting deformed pixelated pictures if you keep 
# resizing already resized photos
originals = [origMario, origLuigi, origPeach, origBowser, origRosalina,    
             origYoshi, origBowserJr, origPolari, origBabyLuma, origLubba,
             origCaptainToad, origBlueToad, origYellowToad, origBankToad, origMailToad,
             origPowerStar, origGrandStar, origGreenStar, origRedStar, origBronzeStar,
             origYellowLuma, origBlueLuma, origCoStarLuma, origRedLuma, origGreenLuma,
             origSilverStar, origMarioSpinning, origMarioFlying, origMarioYoshiLuma,
             origFaceship,
             origMarioYoshi, origLuigiYoshi,
             origBlimpYoshi, origBeeMario, origBooMario, origRockMario, 
             origSpringMario, origRainbowMario, origDashYoshi, origBulbYoshi,
             origFireMario, origIceMario, origCloudMario, origSpinMario,
             origFlyMario]

# each stamp button/icon (along with the space background)
stampSurfaces = [marioCopy, luigiCopy, peachCopy, bowserCopy, rosalinaCopy,    
                 yoshiCopy, bowserJrCopy, polariCopy, babyLumaCopy, lubbaCopy,
                 captainToadCopy, blueToadCopy, yellowToadCopy, bankToadCopy, mailToadCopy,
                 powerStarCopy, grandStarCopy, greenStarCopy, redStarCopy, bronzeStarCopy,
                 yellowLumaCopy, blueLumaCopy, coStarLumaCopy, redLumaCopy, greenLumaCopy,
                 silverStarCopy, marioSpinningCopy, marioFlyingCopy, marioYoshiLumaCopy, faceshipCopy,]
stampSection = 1  # using stampRow or stampColumn would be confusing; in the 
                  # list, rows are used, but in the program, the stamps are  
                  # displayed in a column


stampTxtAreaCopy = screen.subsurface(1089, 574, 111, 20).copy()
stampTxt = calibriNorm.render("Stamp: None", True, (255, 255, 255))
stpWidth = stampTxt.get_width()
screen.blit(stampTxt, (1140-stpWidth//2, 574))
                  
click = True  # flag used when changing stampSection  
sizeUp = False  # both used with MOUSEBUTTONDOWN
sizeDown = False
divide = True  # flag used when resizing pictures

# square area for each stamp button/icon
firstSqr = Rect(1099, 115, 82, 82)
secondSqr = Rect(1099, 202, 82, 82)
thirdSqr = Rect(1099, 289, 82, 82)
fourthSqr = Rect(1099, 376, 82, 82)
fifthSqr = Rect(1099, 463, 82, 82)

squares = [firstSqr, secondSqr, thirdSqr, fourthSqr, fifthSqr]

# loading the power-ups (the images along the bottom of the canvas)
resetIcon = image.load("Pictures/Power-Ups/reset.png")
dashPepper = image.load("Pictures/Power-Ups/Dash-pepper.png")
beeMushroom = image.load("Pictures/Power-Ups/Bee-mushroom.png")
booMushroom = image.load("Pictures/Power-Ups/Boo-mushroom.png")
rockMushroom = image.load("Pictures/Power-Ups/Rock-mushroom.png")
springMushroom = image.load("Pictures/Power-Ups/Spring-mushroom.png")
rainbowStar = image.load("Pictures/Power-Ups/Rainbow-star.png")
blimpFruit = image.load("Pictures/Power-Ups/Blimp-fruit.png")
bulbBerry = image.load("Pictures/Power-Ups/Bulb-berry.png")
fireFlower = image.load("Pictures/Power-Ups/Fire-flower.png")
iceFlower = image.load("Pictures/Power-Ups/Ice-flower.png")
cloudFlower = image.load("Pictures/Power-Ups/Cloud-flower.png")
spinDrill = image.load("Pictures/Power-Ups/Spin-drill.png")
redFlyStar = image.load("Pictures/Power-Ups/Red-powerup-star.png")

powerUps = [resetIcon, blimpFruit, beeMushroom, booMushroom, rockMushroom,
            springMushroom, rainbowStar, dashPepper, bulbBerry, fireFlower,
            iceFlower, cloudFlower, spinDrill, redFlyStar]
powerUpScales = [(26, 26), (26, 26), (30, 31), (26, 26), (29, 30), (28, 28),
                 (26, 26), (19, 32), (18, 30), (28, 28), (28, 28),
                 (28, 28), (30, 23), (32, 32)]
powerUpBlit = [(851, 625), (884, 625), (915, 622), (950, 625), (982, 623),
               (1015, 624), (1049, 625), (855, 655), (888, 656), (916, 657),
               (949, 657), (982, 657), (1014, 660), (1046, 655)]
for pU in powerUps:
    a = powerUps.index(pU)
    pU = transform.scale(pU, (powerUpScales[a]))
    screen.blit(pU, (powerUpBlit[a]))

powerUpRect = Rect(848, 622, 231, 66)

powerUpRectCopy = screen.subsurface(powerUpRect).copy()

riding = False  # flag to see whether Mario is riding Yoshi or not
                # **In order for the dashPepper, blimpFruit, and bulbBerry to 
                # work, Mario must be riding Yoshi as Yoshi consumes those
                # power-ups. 



# choosing a background
backgroundIcon = image.load("Pictures/Other/Background.png")
backgroundIcon = transform.scale(backgroundIcon, (54, 54))
screen.blit(backgroundIcon,(1112, 602))
chooseTxt = calibriNorm.render("Choose", True, (255, 255, 255))
backgroundTxt = calibriNorm.render("Background", True, (255, 255, 255))
screen.blit(chooseTxt, (1114, 656))
screen.blit(backgroundTxt, (1102, 670))

backgroundRect = Rect(1099, 602, 82, 86)
backgroundRectCopy = screen.subsurface(backgroundRect).copy()

choosing = False  # flag to let program know when user is choosing a background

# loading the possible backgrounds
marioFloating = image.load("Pictures/Backgrounds/Mario-floating.jpg")
marioInSpace = image.load("Pictures/Backgrounds/mario-in-space.jpg")
marioRidingSeed = image.load("Pictures/Backgrounds/mario-riding-seed.jpg")
gatewayGalaxy = image.load("Pictures/Backgrounds/Gateway-Galaxy.jpg")
gatewayScene = image.load("Pictures/Backgrounds/gateway-scene.jpg")
toyTime = image.load("Pictures/Backgrounds/toy-time-galaxy.png")
airshipArmada = image.load("Pictures/Backgrounds/bowser-jr-armada.jpg")
bowserCastle = image.load("Pictures/Backgrounds/bowser-throne.jpg")
spaceClouds = image.load("Pictures/Backgrounds/space-clouds.jpg")
blueGalaxy = image.load("Pictures/Backgrounds/galaxy-hd.jpg")
redGalaxy = image.load("Pictures/Backgrounds/red-galaxy.jpg")
purplishGalaxy = image.load("Pictures/Backgrounds/purplish-galaxy.jpg")
spiralGalaxy = image.load("Pictures/Backgrounds/space-scenery.jpg")
spaceMountains = image.load("Pictures/Backgrounds/space-rocks.jpg")
fireIceEarth = image.load("Pictures/Backgrounds/fire-ice-earth.jpg")

backgrounds = [marioFloating, marioInSpace, marioRidingSeed, gatewayGalaxy,
               gatewayScene, toyTime, airshipArmada, bowserCastle,
               spaceClouds, blueGalaxy, redGalaxy, purplishGalaxy, spiralGalaxy,
               spaceMountains, fireIceEarth]

for b in backgrounds:
    a = backgrounds.index(b)
    b = transform.scale(b, (960, 500))
    backgrounds[a] = b

leftArrow = image.load("Pictures/Other/left-arrow.png")
rightArrow = image.load("Pictures/Other/right-arrow.png")
checkmark = image.load("Pictures/Other/checkmark.png")
cancel = image.load("Pictures/Other/cancel.png")

leftArrow = transform.scale(leftArrow, (36, 36))
rightArrow = transform.scale(rightArrow, (36, 36))
checkmark = transform.scale(checkmark, (32, 31))
cancel = transform.scale(cancel, (32, 32))

nxtBkrdRect = Rect(1025, 535, 40, 40)
checkRect = Rect(980, 535, 40, 40)
cancelRect = Rect(935, 535, 40, 40)
prvBkrdRect = Rect(890, 535, 40, 40)

bRects = [nxtBkrdRect, checkRect, cancelRect, prvBkrdRect]

oldTool = ""

# colours
colour = (0, 0, 0)
paletteRect = Rect(121, 622, 220, 66)
# colours in the palette Rect
palette = [(0, 0, 0), (127, 127, 127), (100, 0, 0), (255, 0, 0), (255, 128, 0),  
           (255, 255, 0), (0, 128, 0), (0, 0, 255), (75, 0, 130), (163, 73, 164),  
           (255, 255, 255), (195, 195, 195), (128, 64, 0), (255, 128, 192),     
           (255, 201, 14), (255, 255, 153),(0, 255, 0), (0, 255, 255), 
           (147, 112, 219), (216, 191, 216)]

# the button that says "More..." to give you more colour options 
customClrRect = Rect(343, 622, 45, 66)  # custom colour button Rect
spectrum = image.load("Pictures/Other/spectrum.jpg")
spectrum = transform.scale(spectrum, (45, 50))
screen.blit(spectrum, (344, 623))
moreTxt = calibriNorm.render("More", True, (255, 255, 255))
screen.blit(moreTxt, (348, 674))
clrRectCopy = screen.subsurface(customClrRect).copy()

# area below the canvas where it displays the RGB value of either the colour
# the user is using or (when using the dropper) what colour their mouse is
# hovering over
rgbIcon = image.load("Pictures/Other/rgb.png")
rgbIcon = transform.scale(rgbIcon, (16, 16))
rgbAreaCopy = screen.subsurface(507, 592, 186, 18).copy()

# area below the canvas that gives the mouse position
posIcon = image.load("Pictures/Other/Position.png")
posIcon = transform.scale(posIcon, (9, 16))
screen.blit(posIcon, (120, 592))
posAreaCopy = screen.subsurface(120, 592, 200, 18).copy()


p = -1 # position of colour in palette counter


def paint_bucket(x, y, newClr, oldClr):
    finding = True
    neighbours = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    newPts = [(x, y)]
    if newClr == oldClr:
        finding = False
    while finding:
        f = 0 # paint bucket (aka fill) counter
        if len(newPts) != 0:
            for p in newPts:
                for n in neighbours:
                    np = (p[0] + n[0], p[1] + n[1]) # np for new point
                    if screen.get_at(np) == oldClr:
                        f += 1
                        newPts.append(np)
                        screen.set_at(np, newClr)
            deleting = len(newPts) - f # delete the old points that have been used
            del newPts[:deleting]      # to keep the program's memory from filling 
        else:
            finding = False


# loading the star that shows the colour the user is using
star = image.load("Pictures/Other/star.png")
# because it wouldn't be a Mario star without the eyes:
starEye = image.load("Pictures/Other/star-eye.png") 
star = transform.scale(star, (88, 84))
starEye = transform.scale(starEye, (6, 19))
fillStar = False  # flag for when to fill the star

screen.blit(star, (16, 600))
paint_bucket(60, 650, colour, (255, 255, 255))
screen.blit(starEye, (49, 630))
screen.blit(starEye, (64, 630))

# music that will be played, as well as play button, pause button, volume, etc.

songs = ["Gateway", "StarshipMario", "World1&2", "World3", "World4", "World5",
         "World6", "WorldS", "CosmicCove", "SpaceJunk", "SweetMystery",
         "DripDrop", "SpaceFantasy", "FlipSwap", "Interlude", "Luma", "SadGirl",
         "GalaxyReactor", "GalaxyGenerator", "Wish", "Birth", "Credits1",
         "Credits2", "Family", "Ending"]

songNames = ["Gateway Galaxy", "Starship Mario", "Worlds 1 & 2", "World 3",
             "World 4", "World 5", "World 6", "World S", "Cosmic Cove Galaxy",
             "Space Junk Galaxy", "Sweet Mystery Galaxy", "Drip Drop Galaxy",
             "Space Fantasy", "Flip Swap Galaxy", "Interlude", "Luma",
             "Sad Girl", "Bowser's Galaxy Reactor", "Bowser's Galaxy Generator",
             "A Wish", "Birth", "SMG Credits", "SMG2 Credits", "Family", "Ending"]

songPos = 0
playing = True  # flag for when music is playing (as opposed being paused)
mute = False

mixer.music.load("Music/"+songs[songPos]+".ogg")
mixer.music.play()


click = False  # flag for clicking play previous or play next button

playIcon = image.load("Pictures/Music Buttons/play.png")
pauseIcon = image.load("Pictures/Music Buttons/pause.png")
playNextIcon = image.load("Pictures/Music Buttons/play-next.png")
playPreviousIcon = image.load("Pictures/Music Buttons/play-previous.png")
muteIcon = image.load("Pictures/Music Buttons/mute.png")
vlmIcon = image.load("Pictures/Music Buttons/volume.png") 
speakerIcon = image.load("Pictures/Music Buttons/speaker.png") 

playIcon = transform.scale(playIcon, (21, 21))
pauseIcon = transform.scale(pauseIcon, (23, 23))
playNextIcon = transform.scale(playNextIcon, (21, 21))
playPreviousIcon = transform.scale(playPreviousIcon, (21, 21))
muteIcon = transform.scale(muteIcon, (19, 23))
highVlmIcon = transform.scale(vlmIcon, (5, 55))
mediumVlmIcon = transform.scale(vlmIcon, (5, 39))
lowVlmIcon = transform.scale(vlmIcon, (4, 25))
speakerIcon = transform.scale(speakerIcon, (10, 21))

speakerRect = Rect(533, 664, 23, 21)
speakerRectEmpty = screen.subsurface(speakerRect).copy()
screen.blit(speakerIcon, (533, 664))
speakerRectCopy = screen.subsurface(speakerRect).copy()

screen.blit(highVlmIcon, (551, 647))
screen.blit(mediumVlmIcon, (549, 655))
screen.blit(lowVlmIcon, (546, 662))

draw.line(screen, (255, 255, 255), (565, 675), (665, 675), 1)
for i in range(565, 666, 50):
    draw.line(screen, (255, 255, 255), (i, 678), (i, 672))

vlm = 50
vlmTxtRect = Rect(675, 664, 30, 24)
vlmTxtRectCopy = screen.subsurface(vlmTxtRect).copy()

vlmTxt = calibriBig.render(str(vlm), True, (255, 255, 255))
screen.blit(vlmTxt, (677, 667))

playPreviousRect = Rect(558, 638, 24, 24)
playRect = Rect(603, 638, 24, 24)
playNextRect = Rect(648, 638, 24, 24)
vlmRect = Rect(559, 664, 114, 24)

screen.blit(playPreviousIcon, (559, 639))
screen.blit(pauseIcon, (603, 638))
screen.blit(playNextIcon, (649, 639))

playPreviousRectCopy = screen.subsurface(playPreviousRect).copy()
playRectCopy = image.load("Pictures/Music Buttons/playRectCopy.png") 
playNextRectCopy = screen.subsurface(playNextRect).copy()
vlmRectCopy = screen.subsurface(vlmRect).copy()
songTitleRectCopy = screen.subsurface(516, 622, 198, 16).copy()
pauseRectCopy = screen.subsurface(playRect).copy()

vlmTab = Rect(610, 665, 10, 21)
draw.rect(screen, (120, 120, 120), (vlmTab))

# speech bubbles for Mario and the Luma
marioSpeech = image.load("Pictures/Other/Mario-speech.png")
lumaSpeech = image.load("Pictures/Other/Luma-speech.png")
speechBubble = image.load("Pictures/Other/speech-bubble.png")

marioSpeech = transform.scale(marioSpeech, (55, 10))
lumaSpeech = transform.scale(lumaSpeech, (55, 10))
speechBubble = transform.scale(speechBubble, (250, 60))

noLumaSpeech = screen.subsurface(905, 15, 280, 60).copy()

screen.blit(speechBubble, (15, 15))
screen.blit(speechBubble, (935, 15))
screen.blit(marioSpeech, (240, 50))
screen.blit(lumaSpeech, (905, 50))

marioSpeechCopy = screen.subsurface(15, 15, 280, 60).copy()
lumaSpeechCopy = screen.subsurface(905, 15, 280, 60).copy()

# things Mario and the Baby Luma will be saying

toolNames = ["Pencil", "Marker", "Eraser", "Spray Paint", "Calligraphy Pen",
             "Line", "Text", "Rectangle", "Ellipse", "Stamp", "Picture",
             "Cut", "Copy", "Choose Background", "Polygon", "Eyedropper",
             "Fill Bucket"]

marioToolInfo = ["Click to draw on the canvas.",
		 "Click to draw on the canvas.",
		 "Click to erase part of the canvas.",
		 "Click to spray paint on the canvas.",
		 "Click to draw on the canvas.",
		 "Click to draw a line on the canvas.",
		 "Type to insert text and click to paste it onto the canvas.",
		 "Click to draw a rectangle on the canvas.",
		 "Click to draw an ellipse on the canvas.",
                 "Click to paste the stamp onto the canvas.",
                 "Click to paste your picture onto the canvas.",
		 "Click to select a part of the canvas to cut. Click to paste it elsewhere.",
		 "Click to select a part of the canvas to copy. Click to paste it elsewhere.",
		 "Use the arrows to choose a background.",
		 "Click to draw each point of your polygon.",
		 "Click to select the colour the mouse is currently hovering over.",
		 "Click to fill a portion of the canvas with the selected colour."]

stampNames = ["Mario", "Luigi", "Princess Peach", "Bowser", "Rosalina",
              "Yoshi", "Bowser Jr.", "Polari", "Baby Luma", "Lubba",
              "Captain Toad", "Blue Toad", "Yellow Toad", "Banktoad", "Mailtoad",
              "Power Star", "Grand Star", "Green Power Star", "Red Power Star", "Bronze Power Star",
              "Yellow Luma", "Blue Luma", "Co-Star Luma", "Red Luma", "Green Luma",
              "Silver Star", "Mario spinning", "Mario flying", "Mario with Yoshi and Luma", "Starship Mario",
              "Mario on Yoshi", "Luigi on Yoshi",
              "Blimp Yoshi", "Bee Mario", "Boo Mario", "Rock Mario", "Spring Mario", "Rainbow Mario",
              "Dash Yoshi", "Bulb Yoshi", "Fire Mario", "Ice Mario", "Cloud Mario", "Drill Mario"]
                
lumaSpeechInfo = ["pencil thickness", "marker thickness", "eraser thickness",
                  "spray paint radius", "calligraphy pen thickness", "line thickness",
                  "font size", "rectangle thickness", "ellipse thickness", "stamp size",
                  "picture size", "cut size", "copied size",
                  "polygon thickness", "Draw each point of the polygon",
                  None, None]
                  
running = True
starting = True

# MAY CHANGE
# The code in the while running loop is (mainly) split up into 2 parts, the 
# first being the section with screen.set_clip(None) and the second being the 
# section with screen.set_clip(canvas).

while running:
    for e in event.get(): 
        if e.type == KEYDOWN:  # had to put this in more than once throughout the
            if tool == "text":   # program or it wouldn't catch every key pressed 
                if e.key == 8 and len(txt) != 0:
                    txt = txt[:-1]
                elif e.key != 8 and len(txt) < 201:
                    mx, my = mx, my
                    newTxt = e.unicode
                    txt += newTxt
                txtPic = calibriTxt.render(txt, True, (colour))
                txtW = txtPic.get_width()
                txtH = txtPic.get_height()
                screen.blit(oldCanvas, (120, 90))
                screen.blit(txtPic, (mx-txtW//2, my-txtH//2))

        if e.type == MOUSEBUTTONDOWN:
            if e.button == 4:
                sizeUp = True
            elif e.button == 5:
                sizeDown = True
        
        if e.type == QUIT:
            running = False
            answer = messagebox.askyesno(title = 'Super Mario Galaxy Paint',
            message = 'Do you want to save changes to '+filepath+'?')
            if answer:
                if saveAs:
                    filepath = filedialog.asksaveasfilename(defaultextension = '.png', initialfile = 'Untitled')
                    if len(filepath) != 0:
                        if click:
                            mixer.Sound("Sounds/okie-dokie.ogg").play()
                        click = False                                            
                        slashPos = filepath.rfind("/")
                        if slashPos != len(filepath) - 1:
                            dot = filepath.rfind(".")
                            name = filepath[slashPos+1:dot]
                            display.set_caption(name+" - Super Mario Galaxy Paint")
                            oldCanvas = screen.subsurface(canvas).copy()
                            image.save(screen.subsurface(canvas), filepath)
                        saveAs = False
                else:
                    image.save(screen.subsurface(canvas), filepath)


    mx, my = mouse.get_pos()
    mb = mouse.get_pressed()

    # click flag is used so the mb[0] only equals 1 once and not multiple times
    # in one click

    if mb[0] == 0 and tool != "line" and tool != "rectangle" and tool != "ellipse" and tool != "polygon":
        click = True
        if add:
            undoScreens.append(oldCanvas)
        add = False
    elif mb[0] == 0 and tool != "polygon":
        if useOld:
            screen.blit(oldCanvas, (120, 90))
            oldCanvas = screen.subsurface(canvas).copy()
        elif drawing:
            oldCanvas = screen.subsurface(canvas).copy()
        click = True
        if add:
            undoScreens.append(oldCanvas)
        add = False
    elif mb[0] == 0:
        if sides > 0:
            click = True
            if add:
                undoScreens.append(oldCanvas)
            add = False
    elif mb[0] == 1:
        if canvas.collidepoint(mx, my) and choosing == False:
            add = True
            redoScreens = []
            
    calibriTxt = font.SysFont("Calibri", textSize)
    
# Beginning of section 1
    for e in event.get():
        if e.type == KEYDOWN and tool == "text":
            screen.set_clip(canvas)
            if e.key == 8 and len(txt) != 0:
                    txt = txt[:-1]
            elif e.key != 8 and len(txt) < 201:
                mx, my = mx, my
                newTxt = e.unicode
                txt += newTxt
            txtPic = calibriTxt.render(txt, True, (colour))
            txtW = txtPic.get_width()
            txtH = txtPic.get_height()
            screen.blit(oldCanvas, (120, 90))
            screen.blit(txtPic, (mx-txtW//2, my-txtH//2))
        if e.type == MOUSEBUTTONDOWN:
            screen.set_clip(None)
            if e.button == 4:
                sizeUp = True
            elif e.button == 5:
                sizeDown = True

        if e.type == QUIT:
            running = False
            answer = messagebox.askyesno(title = 'Super Mario Galaxy Paint',
            message = 'Do you want to save changes to '+filepath+'?')
            if answer:
                if saveAs:
                    filepath = filedialog.asksaveasfilename(defaultextension = '.png', initialfile = 'Untitled')
                    if len(filepath) != 0:
                        if click:
                            mixer.Sound("Sounds/okie-dokie.ogg").play()
                        click = False                                            
                        slashPos = filepath.rfind("/")
                        if slashPos != len(filepath) - 1:
                            dot = filepath.rfind(".")
                            name = filepath[slashPos+1:dot]
                            display.set_caption(name+" - Super Mario Galaxy Paint")
                            oldCanvas = screen.subsurface(canvas).copy()
                            image.save(screen.subsurface(canvas), filepath)
                        saveAs = False
                else:
                    image.save(screen.subsurface(canvas), filepath)

            
    screen.set_clip(None)
    

    # info on each tool (or help) that the Baby Luma (the puffy star beside the
    # word "PAINT"

    # Mario text:
    screen.blit(marioSpeechCopy, (15, 15))
    if tool != "stamp":
        marioIntroTalk = calibriSmall.render(toolNames[tools.index(tool)], True, (0, 0, 0))
    else:
        marioIntroTalk = calibriSmall.render(stampNames[stamps.index(stamp)], True, (0, 0, 0))        
    toolInfo = calibriSmall.render(marioToolInfo[tools.index(tool)], True, (0, 0, 0))
    if tool == "stamp" and stamp == stamps[0]:
        toolInfo = calibriSmall.render(marioToolInfo[tools.index("stamp")], True, (0, 0, 0))        
        rideYoshi = calibriSmall.render("Right click on Yoshi to ride him.", True, (0, 0, 0))
        upgradeMario = calibriSmall.render("Click on the power ups to upgrade Mario.", True,(0, 0, 0))
        screen.blit(marioIntroTalk, (15+(250-marioIntroTalk.get_width())//2, 17))
        screen.blit(toolInfo, (15+(250-toolInfo.get_width())//2, 31))
        screen.blit(rideYoshi, (15+(250-rideYoshi.get_width())//2, 46))
        screen.blit(upgradeMario, (15+(250-upgradeMario.get_width())//2, 60))
    elif tool == "stamp" and stamp == stamps[1]:
        toolInfo = calibriSmall.render(marioToolInfo[tools.index("stamp")], True, (0, 0, 0))
        rideYoshi = calibriSmall.render("Right click on Yoshi to ride him.", True, (0, 0, 0))
        screen.blit(marioIntroTalk, (15+(250-marioIntroTalk.get_width())//2, 19))
        screen.blit(toolInfo, (15+(250-marioIntroTalk.get_width())//2, 37))
        screen.blit(rideYoshi, (15+(250-rideYoshi.get_width())//2, 55))
    elif toolInfo.get_width() > 250:
        toolInfo = marioToolInfo[tools.index(tool)]
        half = len(toolInfo)//2
        partInfo = toolInfo[:half]
        space = partInfo.rfind(" ")  # must find a space and not just split
                                     # the string in half or else some words
                                     # will be cut off at the end
        toolInfo1 = calibriSmall.render(toolInfo[:space], True, (0, 0, 0))
        toolInfo2 = calibriSmall.render(toolInfo[space:], True, (0, 0, 0))
        screen.blit(marioIntroTalk, (15+(250-marioIntroTalk.get_width())//2, 19))
        screen.blit(toolInfo1, (15+(250-toolInfo1.get_width())//2, 37)) 
        screen.blit(toolInfo2, (15+(250-toolInfo2.get_width())//2, 55))
    else:        
        screen.blit(marioIntroTalk, (15+(250-marioIntroTalk.get_width())//2, 30))
        screen.blit(toolInfo, (15+(250-toolInfo.get_width())//2, 46))

    # Baby Luma text:
    screen.blit(lumaSpeechCopy, (905, 15))
    if tools.index(tool) < 13:   
        lumaIntroTalk = calibriSmall.render("Scroll up or down to change", True, (0, 0, 0))
        lumaToolTalk = calibriSmall.render("the "+lumaSpeechInfo[tools.index(tool)]+".", True, (0, 0, 0))
        screen.blit(lumaIntroTalk, (935+(250-lumaIntroTalk.get_width())//2, 30))
        screen.blit(lumaToolTalk, (935+(250-lumaToolTalk.get_width())//2, 46))
    else:
        screen.blit(noLumaSpeech, (905, 15))


    songTitle = calibriNorm.render("\""+songNames[songPos]+"\"", True, (255, 255, 255))
    nameLength = songTitle.get_width()
    screen.blit(songTitleRectCopy, (516, 622))
    screen.blit(songTitle, (615-nameLength//2, 622))

    if playRect.collidepoint(mx, my):
        if mb[0] == 0:
            click = True
        elif mb[0] == 1:
            if click:
                if playing:
                    playing = False
                    screen.blit(playRectCopy, (603, 638))
                else:
                    playing = True
                    screen.blit(pauseRectCopy, (603, 638))
            click = False

    if playing == False:
        mixer.music.pause()
    else:
        mixer.music.unpause()
    
    if mixer.music.get_busy() == False:
        if songPos < len(songs) - 1:
            songPos += 1
        else:
            songPos = 0
        mixer.music.load("Music/"+songs[songPos]+".ogg")
        mixer.music.play()

    
    if playNextRect.collidepoint(mx, my):
        if mb[0] == 0:
            click = True
        elif mb[0] == 1:
            if click:
                if songPos < len(songs) - 1:
                    songPos += 1
                else:
                    songPos = 0
                mixer.music.load("Music/"+songs[songPos]+".ogg")
                mixer.music.play()
            click = False

    if playPreviousRect.collidepoint(mx, my):
        if mb[0] == 0:
            click = True
        elif mb[0] == 1:
            if click:
                if songPos > 0:
                    songPos -= 1
                else:
                    songPos = len(songs) - 1
                mixer.music.load("Music/"+songs[songPos]+".ogg")
                mixer.music.play()
            click = False
            
    if vlmTab.collidepoint(mx, my):
        draw.rect(screen, (170, 170, 170), (vlmTab))
        if mb[0] == 0:
            click = True
        if mb[0] == 1 and 565 <= mx <= 665:
            screen.blit(vlmRectCopy, (559, 664))
            vlmTab[0] = mx-5
            draw.rect(screen, (170, 170, 170), (vlmTab))
            vlm = mx - 565
            vlmTxt = calibriBig.render(str(vlm), True, (255, 255, 255))
            screen.blit(vlmTxtRectCopy, (675, 664))
            screen.blit(vlmTxt, (677, 667))
            mixer.music.set_volume(vlm/10)
    else:
        draw.rect(screen, (120, 120, 120), (vlmTab))

    mixer.music.set_volume(vlm/10)
    if vlm >= 68:
        screen.blit(speakerRectCopy,(533, 664))
        screen.blit(highVlmIcon, (551, 647))
        screen.blit(mediumVlmIcon, (547, 655))
        screen.blit(lowVlmIcon, (544, 662))
    elif 34 <= vlm <= 67:
        screen.blit(speakerRectCopy,(533, 664))
        screen.blit(mediumVlmIcon, (547, 655))
        screen.blit(lowVlmIcon, (544, 662))
    elif 1 <= vlm <= 33:
        screen.blit(speakerRectCopy,(533, 664))
        screen.blit(lowVlmIcon, (544, 662))
    else:
        screen.blit(speakerRectEmpty, (533, 664))
        screen.blit(muteIcon, (530, 663)) 

    if speakerRect.collidepoint(mx, my):
        if mb[0] == 0:
            click = True
        elif mb[0] == 1:
            if mute == False and vlm != 0:
                if click:
                    oldVlm = vlm
                    mute = True
                    screen.blit(speakerRectEmpty, (533, 664))
                    screen.blit(muteIcon, (530, 663))
                    vlm = 0
                click = False
            elif mute:
                if click:
                    vlm = oldVlm
                    mute = False
                click = False

        
    if upRect.collidepoint(mx, my) and stampSection != 1:
        draw.rect(screen, (255, 255, 255), (upRect), 1)
        if mb[0] == 0:
            click = True
        if mb[0] == 1:    
            if click:             # click flag is used to prevent stampSection 
                stampSection -= 1 # from adding/subtracting more than 1 in    
            click = False         # one click (e.g. if someone held down on the 
                                  # mouse button for too long)
    else:
        screen.blit(upArrowCopy, (1100, 90))

    if downRect.collidepoint(mx, my) and stampSection != 6:
        draw.rect(screen, (255, 255, 255), (downRect), 1)
        if mb[0] == 0:
            click = True
        if mb[0] == 1:
            if click:
                stampSection += 1
            click = False
    else:
        screen.blit(downArrowCopy, (1100, 550))
        
    for e in event.get():
        if e.type == KEYDOWN and tool == "text":
            screen.set_clip(canvas)
            if e.key == 8 and len(txt) != 0:
                    txt = txt[:-1]
            elif e.key != 8 and len(txt) < 201:
                mx, my = mx, my
                newTxt = e.unicode
                txt += newTxt
            txtPic = calibriTxt.render(txt, True, (colour))
            txtW = txtPic.get_width()
            txtH = txtPic.get_height()
            screen.blit(oldCanvas, (120, 90))
            screen.blit(txtPic, (mx-txtW//2, my-txtH//2))

        if e.type == MOUSEBUTTONDOWN:
            screen.set_clip(None)
            if e.button == 4:
                sizeUp = True
            elif e.button == 5:
                sizeDown = True

        if e.type == QUIT:
            running = False
            answer = messagebox.askyesno(title = 'Super Mario Galaxy Paint',
            message = 'Do you want to save changes to '+filepath+'?')
            if answer:
                if saveAs:
                    filepath = filedialog.asksaveasfilename(defaultextension = '.png', initialfile = 'Untitled')
                    if len(filepath) != 0:
                        if click:
                            mixer.Sound("Sounds/okie-dokie.ogg").play()
                        click = False                                            
                        slashPos = filepath.rfind("/")
                        if slashPos != len(filepath) - 1:
                            dot = filepath.rfind(".")
                            name = filepath[slashPos+1:dot]
                            display.set_caption(name+" - Super Mario Galaxy Paint")
                            oldCanvas = screen.subsurface(canvas).copy()
                            image.save(screen.subsurface(canvas), filepath)
                        saveAs = False
                else:
                    image.save(screen.subsurface(canvas), filepath)

            
    # displaying the stamps
    stampPos = -1  # counter used to position each stamp surface/icon
    for s in stampSurfaces:
        if stampSurfaces.index(s)//5 == stampSection-1:
            stampPos += 1
            screen.blit(stampSurfaces[stampSurfaces.index(s)], (1099, stampPos*87+115))
                                        # each square is 87 px tall, and you must
                                        # add 115 to compensate for the gap at the
                                        # top of the screen between the top display
                                        # bar and first square

    for sq in squares:
        if sq.collidepoint(mx, my):
            screen.blit(marioSpeechCopy, (15, 15))
            toolInfo = calibriSmall.render("Stamp", True, (0, 0, 0))
            screen.blit(toolInfo, (15+(250-toolInfo.get_width())//2, 38))
            screen.blit(noLumaSpeech, (905, 15))
            draw.rect(screen, (255, 255, 255), (sq), 1)
            if mb[0] == 1:
                tool = "stamp"
    if tool == "stamp":
        for sq in squares:
            if mb[0] == 1 and sq.collidepoint(mx, my):
                stamp = stamps[(my-115)//87 + (stampSection-1)*5]
                # (my - 115) // 87  -->  my-115 gives the y-pos rekative to
                # the squares and not the whole canvas
                # // 87 gives what square because each square is 87 px by 87 px
                # * 5 because the module is *technically* 5
                # e.g. stamps 0, 5, 10, etc. share the same square, 3, 8, 13 do, and so on 
                divide = True
        if stamps.index(stamp) < 30 and stampSection-1 == stamps.index(stamp)//5:
            draw.rect(screen, (255, 255, 255), (1099, (stamps.index(stamp))%5*87+115, 82, 82), 1)
        screen.blit(stampTxtAreaCopy, (1089, 574))
        if stamps.index(stamp) > 29:
            stampTxt = calibriNorm.render("Stamp: Bonus", True, (255, 255, 255))                    
            divide = True
        else:
            stampTxt = calibriNorm.render("Stamp: "+str(stamps.index(stamp)+1)+" of 30", True, (255, 255, 255))        
        stpWidth = stampTxt.get_width()
        screen.blit(stampTxt, (1140-stpWidth//2, 574))
        if stamp == stamps[0] or stamp == stamps[1]:  # identifying Mario/Luigi to ride Yoshi
            if firstSqr.collidepoint(mx, my) and stampSection == 2 and mb[2] == 1:
                stamp = stamps[stamps.index(stamp)+30]
        elif stamp == stamps[5]:  # identifying Yoshi
            if (firstSqr.collidepoint(mx, my) or secondSqr.collidepoint(mx, my)) and stampSection == 1 and mb[2] == 1:
                stamp = stamps[(my-115)//87 + (stampSection-1)*5 + 30]
    else:
        screen.blit(stampTxtAreaCopy, (1089, 574))
        stampTxt = calibriNorm.render("Stamp: None", True, (255, 255, 255))
        stpWidth = stampTxt.get_width()
        screen.blit(stampTxt, (1140-stpWidth//2, 574))
    
    # power up area
    if powerUpRect.collidepoint(mx, my):
        screen.blit(marioSpeechCopy, (15, 15))
        powerUpTxt = calibriSmall.render("Power ups can be used by Mario or Yoshi.", True, (0, 0, 0))
        screen.blit(powerUpTxt, (15+(250-powerUpTxt.get_width())//2, 38))
        screen.blit(noLumaSpeech, (905, 15))
    if powerUpRect.collidepoint(mx, my) and tool == "stamp":
        screen.blit(powerUpRectCopy, (848, 622))
        pColumn = (mx-848)//33
        pRow = (my-622)//33
        uPos = pColumn+7*pRow
        if stamp == stamps[0] or stamp == stamps[30]:
            oldStamp = stamp
        if stamp == stamps[0] or stamp == stamps[30] or stamps.index(stamp) > 31:            
            if mb[0] == 0:
                if uPos == 0 and stamps.index(stamp) > 31:
                    draw.rect(screen, (255, 255, 255), (848+pColumn*33, 622+pRow*33, 33, 33), 1)                    
                elif (uPos == 1 or uPos == 7 or uPos == 8) and (stamp == stamps[30] or stamp == stamps[30] or stamp == stamps[38] or stamp == stamps[32] or stamp == stamps[39]):
                    draw.rect(screen, (255, 255, 255), (848+pColumn*33, 622+pRow*33, 33, 33), 1)
                elif uPos != 0 and uPos != 1 and uPos != 7 and uPos != 8 and (stamp == stamps[0] or stamps.index(stamp) > 31):
                    draw.rect(screen, (255, 255, 255), (848+pColumn*33, 622+pRow*33, 33, 33), 1)                    
            if mb[0] == 1:
                if uPos == 0:
                    stamp = oldStamp
                elif (uPos == 1 or uPos == 7 or uPos == 8) and (stamp == stamps[30] or stamp == stamps[38] or stamp == stamps[32] or stamp == stamps[39]):
                    stamp = stamps[uPos+31]
                elif uPos != 0 and uPos != 1 and uPos != 7 and uPos != 8 and (stamp == stamps[0] or stamps.index(stamp) > 31):
                    stamp = stamps[uPos+31]
    else:
        screen.blit(powerUpRectCopy, (848, 622))

    if tool == "picture":  # referring to load image command
        divide = True
    

    if backgroundRect.collidepoint(mx, my):
        draw.rect(screen, (255, 255, 255), (backgroundRect), 1)
        if mb[0] == 1:
            choosing = True
            if click:
                oldTool = tool
                bPos = 0
            click = False
            tool = "choose background" # this is to prevent e.g. marker tool
                                       # circle outline from showing when
                                       # choosing a background
    else:
        screen.blit(backgroundRectCopy, (1099, 602))

    for e in event.get():
        if e.type == KEYDOWN and tool == "text":
            screen.set_clip(canvas)
            if e.key == 8 and len(txt) != 0:
                    txt = txt[:-1]
            elif e.key != 8 and len(txt) < 201:
                mx, my = mx, my
                newTxt = e.unicode
                txt += newTxt
            txtPic = calibriTxt.render(txt, True, (colour))
            txtW = txtPic.get_width()
            txtH = txtPic.get_height()
            screen.blit(oldCanvas, (120, 90))
            screen.blit(txtPic, (mx-txtW//2, my-txtH//2))

        if e.type == MOUSEBUTTONDOWN:
            screen.set_clip(None)
            if e.button == 4:
                sizeUp = True
            elif e.button == 5:
                sizeDown = True

        if e.type == QUIT:
            running = False
            answer = messagebox.askyesno(title = 'Super Mario Galaxy Paint',
            message = 'Do you want to save changes to '+filepath+'?')
            if answer:
                if saveAs:
                    filepath = filedialog.asksaveasfilename(defaultextension = '.png', initialfile = 'Untitled')
                    if len(filepath) != 0:
                        if click:
                            mixer.Sound("Sounds/okie-dokie.ogg").play()
                        click = False                                            
                        slashPos = filepath.rfind("/")
                        if slashPos != len(filepath) - 1:
                            dot = filepath.rfind(".")
                            name = filepath[slashPos+1:dot]
                            display.set_caption(name+" - Super Mario Galaxy Paint")
                            oldCanvas = screen.subsurface(canvas).copy()
                            image.save(screen.subsurface(canvas), filepath)
                        saveAs = False
                else:
                    image.save(screen.subsurface(canvas), filepath)

    
    if choosing:
        screen.blit(backgrounds[bPos], (120, 90))
        screen.blit(rightArrow, (1027, 537))
        screen.blit(leftArrow, (891, 537))
        screen.blit(checkmark, (984, 539))
        screen.blit(cancel, (939, 539))
        for bR in bRects:
            if bR.collidepoint(mx, my):
                draw.rect(screen, (255, 255, 255), (bR), 1)
            else:
                draw.rect(screen, (0), (bR), 1)
        if nxtBkrdRect.collidepoint(mx, my):
            if mb[0] == 1:
                if click:
                    if bPos == len(backgrounds) - 1:
                        bPos = 0
                    else:
                        bPos += 1
                click = False
        if prvBkrdRect.collidepoint(mx, my):
            if mb[0] == 1:
                if click:
                    if bPos == 0:
                        bPos = len(backgrounds) - 1
                    else:
                        bPos -= 1
                click = False
        if checkRect.collidepoint(mx, my):
            if mb[0] == 1:
                if click:
                    screen.blit(backgrounds[bPos], (120, 90))
                    oldCanvas = screen.subsurface(canvas).copy()
                    tool = oldTool
                    choosing = False
                click = False
        if cancelRect.collidepoint(mx, my):
            if mb[0] == 1:
                if click:
                    screen.blit(oldCanvas, (120, 90))
                    tool = oldTool
                    choosing = False
                click = False

    # fill toggler, choosing whether shapes are to be drawn filled or not filled    
    if fillToggler.collidepoint(mx, my):
        if mb[0] == 0:
            draw.rect(screen, (30, 30, 30), (fillToggler))
        elif mb[0] == 1:
            if shapeFormat == "no fill":
                screen.blit(fillRectCopy, (13, 453))
                fillToggler[0] = 59
                draw.rect(screen, (0), (fillToggler))
                oldShapeSize = shapeSize
                shapeSize = 0
                screen.blit(rectFillCopy, (62, 497))
                screen.blit(ellipseFillCopy, (14, 547))
                screen.blit(polygonFillCopy, (62, 547))
                shapeFormat = "fill"
            else:
                screen.blit(fillRectCopy, (13, 453))
                fillToggler[0] = 14
                draw.rect(screen, (0), (14, 454, 46, 36))
                shapeSize = oldShapeSize
                screen.blit(rectEmptyCopy, (62, 497))
                screen.blit(ellipseEmptyCopy, (14, 547))
                screen.blit(polygonEmptyCopy, (62, 547))
                shapeFormat = "no fill"
    else:
        draw.rect(screen, (0), (fillToggler))

    # commands
    if saveRect.collidepoint(mx, my) or command == "save":
        draw.rect(screen, (255, 255, 255), (saveRect), 1)
        screen.blit(marioSpeechCopy, (15, 15))
        if saveAs:
            toolInfo = calibriSmall.render("Save your image to a file.", True, (0, 0, 0))
            screen.blit(noLumaSpeech, (905, 15))
        else:
            toolInfo = calibriSmall.render("Save your image.", True, (0, 0, 0))
        screen.blit(toolInfo, (15+(250-toolInfo.get_width())//2, 38))
        screen.blit(noLumaSpeech, (905, 15))
        if mb[0] == 1 or command == "save":
            command = "save"
            if saveAs:
                filepath = filedialog.asksaveasfilename(defaultextension = '.png', initialfile = 'Untitled')
                if len(filepath) != 0:
                    if click:
                        mixer.Sound("Sounds/okie-dokie.ogg").play()
                    click = False                                            
                    slashPos = filepath.rfind("/")
                    if slashPos != len(filepath) - 1:
                        dot = filepath.rfind(".")
                        name = filepath[slashPos+1:dot]
                        display.set_caption(name+" - Super Mario Galaxy Paint")
                        oldCanvas = screen.subsurface(canvas).copy()
                        image.save(screen.subsurface(canvas), filepath)
                    saveAs = False
            else:
                image.save(screen.subsurface(canvas), filepath)
        command = ""
    else:
        if saveAs:
            screen.blit(saveAsRectCopy, (7, 92))
        else:
            screen.blit(saveRectCopy, (7, 92))
        
    if undoRect.collidepoint(mx, my) and len(undoScreens) > 1 or command == "undo":
        draw.rect(screen, (255, 255, 255), (undoRect), 1)
        command = "undo"
        if mb[0] == 1:
            if take:
                redoScreens.append(undoScreens[-1])
                del undoScreens[-1]
                screen.blit(undoScreens[-1], (120, 90))
                oldCanvas = undoScreens[-1]
            take = False
        else:
            take = True  # flag so the program only deletes the last screen once
        command = ""
        screen.blit(marioSpeechCopy, (15, 15))
        toolInfo = calibriSmall.render("Undo", True, (0, 0, 0))
        screen.blit(toolInfo, (15+(250-toolInfo.get_width())//2, 38))
        screen.blit(noLumaSpeech, (905, 15))
    elif undoRect.collidepoint(mx, my):
        screen.blit(marioSpeechCopy, (15, 15))
        toolInfo = calibriSmall.render("Undo", True, (0, 0, 0))
        screen.blit(toolInfo, (15+(250-toolInfo.get_width())//2, 38))
        screen.blit(noLumaSpeech, (905, 15))
    else:
        screen.blit(undoRectCopy, (43, 92))

    if redoRect.collidepoint(mx, my) and len(redoScreens) != 0 or command == "redo":
        draw.rect(screen, (255, 255, 255), (redoRect), 1)
        command = "redo"
        if mb[0] == 1:
            if take:
                undoScreens.append(redoScreens[-1])
                del redoScreens[-1]
                screen.blit(undoScreens[-1], (120, 90))
                oldCanvas = undoScreens[-1]
            take = False
        else:
            take = True
        command = ""
        screen.blit(marioSpeechCopy, (15, 15))
        toolInfo = calibriSmall.render("Redo", True, (0, 0, 0))
        screen.blit(toolInfo, (15+(250-toolInfo.get_width())//2, 38))
        screen.blit(noLumaSpeech, (905, 15))
    elif redoRect.collidepoint(mx, my):
        screen.blit(marioSpeechCopy, (15, 15))
        toolInfo = calibriSmall.render("Redo", True, (0, 0, 0))
        screen.blit(toolInfo, (15+(250-toolInfo.get_width())//2, 38))
        screen.blit(noLumaSpeech, (905, 15))
    else:
        screen.blit(redoRectCopy, (79, 92))

    if newRect.collidepoint(mx, my):
        draw.rect(screen, (255, 255, 255), (newRect), 1)
        screen.blit(marioSpeechCopy, (15, 15))
        toolInfo = calibriSmall.render("Start a new picture.", True, (0, 0, 0))
        screen.blit(toolInfo, (15+(250-toolInfo.get_width())//2, 38))
        screen.blit(noLumaSpeech, (905, 15))
        if mb[0] == 1:
            answer = messagebox.askyesno(title = 'Super Mario Galaxy Paint', message = 'Do you want to save changes to '+filepath+'?')
            if answer:
                saveAs = True
                command = "save"
                screen.subsurface(canvas).fill((255, 255, 255))
                undoScreens = [screen.subsurface(canvas).copy()]
                redoScreens = []
    else:
        screen.blit(newRectCopy, (7, 130))
    
    if openRect.collidepoint(mx, my) or command == "open":
        draw.rect(screen, (255, 255, 255), (openRect), 1)
        screen.blit(marioSpeechCopy, (15, 15))
        toolInfo = calibriSmall.render("Open an image from a file.", True, (0, 0, 0))
        screen.blit(toolInfo, (15+(250-toolInfo.get_width())//2, 38))
        screen.blit(noLumaSpeech, (905, 15))
        command = "open"
        if mb[0] == 1:
            filepath = filedialog.askopenfilename(filetypes = [('PNG Files', '*.png')])
            slashPos = filepath.rfind("/")
            if slashPos != len(filepath) - 1:
                dot = filepath.rfind(".")
                name = filepath[slashPos+1:dot]
                display.set_caption(name+" - Super Mario Galaxy Paint")
                openFile = image.load(filepath)
                screen.set_clip(canvas)
                screen.blit(openFile, (200, 200))
                oldCanvas = screen.subsurface(canvas).copy()
                saveAs = False
        command = ""
    else:
        screen.blit(openRectCopy, (43, 130))

    if loadRect.collidepoint(mx, my) or command == "load":
        draw.rect(screen, (255, 255, 255), (loadRect), 1)
        screen.blit(marioSpeechCopy, (15, 15))
        toolInfo = calibriSmall.render("Load an image from a file.", True, (0, 0, 0))
        screen.blit(toolInfo, (15+(250-toolInfo.get_width())//2, 38))
        screen.blit(noLumaSpeech, (905, 15))
        command = "load"
        if mb[0] == 1:
            filepath = filedialog.askopenfilename(title = 'Insert Picture', filetypes = [('All Picture Files', '*.png;*.gif;*.jpg;*.bmp;*.dib;*.jpeg'),
                                                                                         ('PNG Files', '*.png'), ('GIF Files', '*.gif'), ('JPG Files', '*.jpg'),
                                                                                        ('Bitmap Files', '*.bmp'), ('DIB Files', '*.dib'), ('JPEG Files', '*.jpeg')])                                                                                                                  
            if click:
                mixer.Sound("Sounds/okie-dokie.ogg").play()
            click = False
            slashPos = filepath.rfind("/")
            if slashPos != len(filepath) - 1:
                dot = filepath.rfind(".")
                name = filepath[slashPos+1:dot]
                origLoadPic = image.load(filepath)
                loadPic = origLoadPic
                w = origLoadPic.get_width()
                h = origLoadPic.get_height()
                mb = (0, 0, 0)
                loaded = True
                tool = "picture"
        command = ""
    else:
        screen.blit(loadRectCopy, (79, 130))

    if cutRect.collidepoint(mx, my):
        draw.rect(screen, (255, 255, 255), (cutRect), 1)
        screen.blit(marioSpeechCopy, (15, 15))
        toolInfo = calibriSmall.render("Cut a part of the canvas.", True, (0, 0, 0))
        screen.blit(toolInfo, (15+(250-toolInfo.get_width())//2, 38))
        screen.blit(noLumaSpeech, (905, 15))
        if mb[0] == 1:
            if click:
                selectSurf = Surface((0, 0))
            click = False
            tool = "cut"   # <-- to keep any other tools from being highlighted
                           # at the same time
            pickCorner = True
            drawingCutPic = False
            cuttingPic = False
            draggingCutPic = False
            pastingCutPic = False
        command = ""
    elif tool == "cut":
        draw.rect(screen, (255, 255, 255), (cutRect), 1)
    else:
        screen.blit(cutRectCopy, (7, 168))

    if copyRect.collidepoint(mx, my):
        draw.rect(screen, (255, 255, 255), (copyRect), 1)
        screen.blit(marioSpeechCopy, (15, 15))
        toolInfo = calibriSmall.render("Copy a part of the canvas.", True, (0, 0, 0))
        screen.blit(toolInfo, (15+(250-toolInfo.get_width())//2, 38))
        screen.blit(noLumaSpeech, (905, 15))
        if mb[0] == 1:
            if click:
                selectSurf = Surface((0, 0))
            click = False
            tool = "copy"
            pickCorner = True
            drawingCutPic = False
            cuttingPic = False
            draggingCutPic = False
            pastingCutPic = False
        command = ""
    elif tool == "copy":
        draw.rect(screen, (255, 255, 255), (copyRect), 1)
    else:
        screen.blit(copyRectCopy, (43, 168))
    
    if clearRect.collidepoint(mx, my) or command == "clear":
        draw.rect(screen, (255, 255, 255), (clearRect), 1)
        screen.blit(marioSpeechCopy, (15, 15))
        toolInfo = calibriSmall.render("Clear the canvas.", True, (0, 0, 0))
        screen.blit(toolInfo, (15+(250-toolInfo.get_width())//2, 38))
        screen.blit(noLumaSpeech, (905, 15))
        if mb[0] == 0:
            clearAdd = True
        elif mb[0] == 1:
            command = "clear"
            screen.subsurface(canvas).fill((255, 255, 255))
            oldCanvas = screen.subsurface(canvas).copy()
            if clearAdd:
                undoScreens.append(oldCanvas)
            clearAdd = False
        command = ""
    else:
        screen.blit(clearRectCopy, (79, 168))

    for e in event.get():
        if e.type == KEYDOWN and tool == "text":
            screen.set_clip(canvas)
            if e.key == 8 and len(txt) != 0:
                    txt = txt[:-1]
            elif e.key != 8 and len(txt) < 201:
                mx, my = mx, my
                newTxt = e.unicode
                txt += newTxt
            txtPic = calibriTxt.render(txt, True, (colour))
            txtW = txtPic.get_width()
            txtH = txtPic.get_height()
            screen.blit(oldCanvas, (120, 90))
            screen.blit(txtPic, (mx-txtW//2, my-txtH//2))

        if e.type == MOUSEBUTTONDOWN:
            screen.set_clip(None)
            if e.button == 4:
                sizeUp = True
            elif e.button == 5:
                sizeDown = True

        if e.type == QUIT:
            running = False
            answer = messagebox.askyesno(title = 'Super Mario Galaxy Paint',
            message = 'Do you want to save changes to '+filepath+'?')
            if answer:
                if saveAs:
                    filepath = filedialog.asksaveasfilename(defaultextension = '.png', initialfile = 'Untitled')
                    if len(filepath) != 0:
                        if click:
                            mixer.Sound("Sounds/okie-dokie.ogg").play()
                        click = False                                            
                        slashPos = filepath.rfind("/")
                        if slashPos != len(filepath) - 1:
                            dot = filepath.rfind(".")
                            name = filepath[slashPos+1:dot]
                            display.set_caption(name+" - Super Mario Galaxy Paint")
                            oldCanvas = screen.subsurface(canvas).copy()
                            image.save(screen.subsurface(canvas), filepath)
                        saveAs = False
                else:
                    image.save(screen.subsurface(canvas), filepath)
                            
    # colour palette area
    
    draw.rect(screen, (240, 240, 240), (paletteRect))
    for term in range(len(palette)):
        column = term % 10
        row = term // 10 
        draw.rect(screen, (palette[term]), (column*22+121, row*22+622, 22, 22))
    for x in range(121, 341, 22):
        for y in range(622, 688, 22):
            draw.rect(screen, (0), (x, y, 22, 22), 1)
    if colour not in palette:  # applies when using colour chooser
        if len(palette) < 30:
            palette.append(colour)
        else:
            p += 1
            extraPos = p % 10   # there are 10 slots available in the last column        
            palette[extraPos+20] = colour # there were 20 colours originally in the palette; the extras are being added on       
    clrColumn = palette.index(colour) % 10   
    clrRow = palette.index(colour) // 10
    draw.rect(screen, (255, 255, 255), (clrColumn*22+121, clrRow*22+622, 22, 22), 1)
    if paletteRect.collidepoint(mx, my):
        mColumn = (mx - 121) // 22
        mRow = (my - 622) // 22
        colourBox = mColumn + mRow*10
        if colourBox < len(palette):
            if mb[0] == 1: 
                colour = palette[colourBox]
                fillStar = True
            else:
                draw.rect(screen, (255, 255, 255), (mColumn*22+121, mRow*22+622, 22, 22), 1)

    if customClrRect.collidepoint(mx, my):
        draw.rect(screen, (255, 255, 255), (customClrRect), 1)
        if mb[0] == 1:
            resultClr, clrAsString = askcolor(title = 'More Colours')
            if resultClr != None and resultClr not in palette:
                colour = resultClr
                fillStar = True
                if len(palette) < 30:
                    palette.append(colour)
                else:
                    p += 1
                    extraPos = p % 10
                    palette[extraPos+20] = colour 
            elif resultClr in palette:
                colour = palette[palette.index(resultClr)]
    else:
        screen.blit(clrRectCopy, (343, 622))

    # rgb area
    screen.blit(rgbAreaCopy, (507, 592))
    if tool != "dropper":
        rgbTxt = calibriBig.render("R: "+str(colour[0])+"  G: "+str(colour[1])+"  B: "+str(colour[2]), True, (255, 255, 255))
        if fillStar:
            screen.blit(star, (16, 600))
            paint_bucket(60, 650, colour, (255, 255, 255))
            screen.blit(starEye, (49, 630))
            screen.blit(starEye, (64, 630))
        fillStar = False
    else:
        if canvas.collidepoint(mx, my):
            clrAtMouse = screen.get_at((mx, my))
            rgbTxt = calibriBig.render("R: "+str(int(clrAtMouse[0]))+"  G: "+str(int(clrAtMouse[1]))+"  B: "+str(int(clrAtMouse[2])), True, (255, 255, 255))
            if fillStar:
                screen.blit(star, (16, 600))
                paint_bucket(60, 650, screen.get_at((mx, my)), (255, 255, 255))
                screen.blit(starEye, (49, 630))
                screen.blit(starEye, (64, 630))
            fillStar = False
        else:
            rgbTxt = calibriBig.render("R: N/A  G: N/A  B: N/A", True, (255, 255, 255))
            if fillStar:  # the star will continuously change colour depending
                          # on where the mouse is on the canvas (only if the
                          # tool selected is "dropper")
                screen.blit(star, (16, 600))
                paint_bucket(60, 650, colour, (255, 255, 255))
                screen.blit(starEye, (49, 630))
                screen.blit(starEye, (64, 630))
            fillStar = False
    # so the RGB indicator will always be centred
    lenRGB = rgbTxt.get_width() + 26 # +26 to account for the logo
    screen.blit(rgbIcon, (600-lenRGB//2, 592))
    screen.blit(rgbTxt, (626-lenRGB//2, 592))
                            
    # area where mouse pos is stated
    screen.blit(posAreaCopy, (120, 592))
    mouseX = str(mx-120)
    mouseY= str(my-90)
    if canvas.collidepoint(mx, my):
        posTxt = calibriBig.render("Position: "+mouseX+", "+mouseY+" px", True, (255, 255, 255))
        screen.blit(posTxt, (140, 592))
    else:
        posTxt = calibriBig.render("Position: Off Canvas", True, (255, 255, 255))
        screen.blit(posTxt, (140, 592))


    for e in event.get():
        if e.type == KEYDOWN and tool == "text":
            screen.set_clip(canvas)
            if e.key == 8 and len(txt) != 0:
                    txt = txt[:-1]
            elif e.key != 8 and len(txt) < 201:
                mx, my = mx, my
                newTxt = e.unicode
                txt += newTxt
            txtPic = calibriTxt.render(txt, True, (colour))
            txtW = txtPic.get_width()
            txtH = txtPic.get_height()
            screen.blit(oldCanvas, (120, 90))
            screen.blit(txtPic, (mx-txtW//2, my-txtH//2))

        if e.type == MOUSEBUTTONDOWN:
            screen.set_clip(canvas)
            if e.button == 4:
                sizeUp = True
            elif e.button == 5:
                sizeDown = True

        if e.type == QUIT:
            running = False
            answer = messagebox.askyesno(title = 'Super Mario Galaxy Paint',
            message = 'Do you want to save changes to '+filepath+'?')
            if answer:
                if saveAs:
                    filepath = filedialog.asksaveasfilename(defaultextension = '.png', initialfile = 'Untitled')
                    if len(filepath) != 0:
                        if click:
                            mixer.Sound("Sounds/okie-dokie.ogg").play()
                        click = False                                            
                        slashPos = filepath.rfind("/")
                        if slashPos != len(filepath) - 1:
                            dot = filepath.rfind(".")
                            name = filepath[slashPos+1:dot]
                            display.set_caption(name+" - Super Mario Galaxy Paint")
                            oldCanvas = screen.subsurface(canvas).copy()
                            image.save(screen.subsurface(canvas), filepath)
                        saveAs = False
                else:
                    image.save(screen.subsurface(canvas), filepath)

    # identifying each tool/shape
    if pencilRect.collidepoint(mx, my) and mb[0] == 1:
        tool = "pencil"
    elif markerRect.collidepoint(mx, my) and mb[0] == 1:
        tool = "marker"
    elif eraserRect.collidepoint(mx, my) and mb[0] == 1:
        tool = "eraser"
    elif dropperRect.collidepoint(mx, my) and mb[0] == 1:
        tool = "dropper"
    elif bucketRect.collidepoint(mx, my) and mb[0] == 1:
        tool = "bucket"
    elif sprayPaintRect.collidepoint(mx, my) and mb[0] == 1:
        tool = "spray paint"
    elif textRect.collidepoint(mx, my) and mb[0] == 1:
        tool = "text"
    elif calligraphyRect.collidepoint(mx, my) and mb[0] == 1:
        tool = "calligraphy"
    elif lineRect.collidepoint(mx, my) and mb[0] == 1:
        tool = "line"
        useOld = True
    elif rectRect.collidepoint(mx, my) and mb[0] == 1:
        tool = "rectangle"
        useOld = True
    elif ellipseRect.collidepoint(mx, my) and mb[0] == 1:
        tool = "ellipse"
        useOld = True
    elif polygonRect.collidepoint(mx, my) and mb[0] == 1:
        tool = "polygon"
        useOld = True
        starting = True
        
    for e in event.get():
        if e.type == KEYDOWN and tool == "text":
            screen.set_clip(canvas)
            if e.key == 8 and len(txt) != 0:
                    txt = txt[:-1]
            elif e.key != 8 and len(txt) < 201:
                mx, my = mx, my
                newTxt = e.unicode
                txt += newTxt
            txtPic = calibriTxt.render(txt, True, (colour))
            txtW = txtPic.get_width()
            txtH = txtPic.get_height()
            screen.blit(oldCanvas, (120, 90))
            screen.blit(txtPic, (mx-txtW//2, my-txtH//2))

        if e.type == MOUSEBUTTONDOWN:
            screen.set_clip(None)
            if e.button == 4:
                sizeUp = True
            elif e.button == 5:
                sizeDown = True

        if e.type == QUIT:
            running = False
            answer = messagebox.askyesno(title = 'Super Mario Galaxy Paint',
            message = 'Do you want to save changes to '+filepath+'?')
            if answer:
                if saveAs:
                    filepath = filedialog.asksaveasfilename(defaultextension = '.png', initialfile = 'Untitled')
                    if len(filepath) != 0:
                        if click:
                            mixer.Sound("Sounds/okie-dokie.ogg").play()
                        click = False                                            
                        slashPos = filepath.rfind("/")
                        if slashPos != len(filepath) - 1:
                            dot = filepath.rfind(".")
                            name = filepath[slashPos+1:dot]
                            display.set_caption(name+" - Super Mario Galaxy Paint")
                            oldCanvas = screen.subsurface(canvas).copy()
                            image.save(screen.subsurface(canvas), filepath)
                        saveAs = False
                else:
                    image.save(screen.subsurface(canvas), filepath)

            
    # for tools and shapes, when to outline their boxes
    if pencilRect.collidepoint(mx, my):
        screen.blit(marioSpeechCopy, (15, 15))
        toolInfo = calibriSmall.render("Pencil", True, (0, 0, 0))
        screen.blit(toolInfo, (15+(250-toolInfo.get_width())//2, 38))
        screen.blit(noLumaSpeech, (905, 15))
        draw.rect(screen, (255, 255, 255), (pencilRect), 1)
    elif tool == "pencil":
        draw.rect(screen, (255, 255, 255), (pencilRect), 1)
    else:
        screen.blit(pencilRectCopy, (14, 236))

    if markerRect.collidepoint(mx, my):
        screen.blit(marioSpeechCopy, (15, 15))
        toolInfo = calibriSmall.render("Marker", True, (0, 0, 0))
        screen.blit(toolInfo, (15+(250-toolInfo.get_width())//2, 38))
        screen.blit(noLumaSpeech, (905, 15))
        draw.rect(screen, (255, 255, 255), (markerRect), 1)
    elif tool == "marker":
        draw.rect(screen, (255, 255, 255), (markerRect), 1)
    else:
        screen.blit(markerRectCopy, (62, 236))

    if eraserRect.collidepoint(mx, my):
        screen.blit(marioSpeechCopy, (15, 15))
        toolInfo = calibriSmall.render("Eraser", True, (0, 0, 0))
        screen.blit(toolInfo, (15+(250-toolInfo.get_width())//2, 38))
        screen.blit(noLumaSpeech, (905, 15))
        draw.rect(screen, (255, 255, 255), (eraserRect), 1)
    elif tool == "eraser":
        draw.rect(screen, (255, 255, 255), (eraserRect), 1)
    else:
        screen.blit(eraserRectCopy, (14, 282))

    if dropperRect.collidepoint(mx, my):
        screen.blit(marioSpeechCopy, (15, 15))
        toolInfo = calibriSmall.render("Eyedropper", True, (0, 0, 0))
        screen.blit(toolInfo, (15+(250-toolInfo.get_width())//2, 38))
        screen.blit(noLumaSpeech, (905, 15))
        draw.rect(screen, (255, 255, 255), (dropperRect), 1)
    elif tool == "dropper":
        draw.rect(screen, (255, 255, 255), (dropperRect), 1)
    else:
        screen.blit(dropperRectCopy, (62, 282))

    if bucketRect.collidepoint(mx, my):
        screen.blit(marioSpeechCopy, (15, 15))
        toolInfo = calibriSmall.render("Fill Bucket", True, (0, 0, 0))
        screen.blit(toolInfo, (15+(250-toolInfo.get_width())//2, 38))
        screen.blit(noLumaSpeech, (905, 15))
        draw.rect(screen, (255, 255, 255), (bucketRect), 1)
    elif tool == "bucket":
        draw.rect(screen, (255, 255, 255), (bucketRect), 1)
    else:
        screen.blit(bucketRectCopy, (14, 328))

    if sprayPaintRect.collidepoint(mx, my):
        screen.blit(marioSpeechCopy, (15, 15))
        toolInfo = calibriSmall.render("Fill Bucket", True, (0, 0, 0))
        screen.blit(toolInfo, (15+(250-toolInfo.get_width())//2, 38))
        screen.blit(noLumaSpeech, (905, 15))
        draw.rect(screen, (255, 255, 255), (sprayPaintRect), 1)
    elif tool == "spray paint":
        draw.rect(screen, (255, 255, 255), (sprayPaintRect), 1)
    else:
        screen.blit(sprayPaintRectCopy, (62, 328))

    if textRect.collidepoint(mx, my):
        screen.blit(marioSpeechCopy, (15, 15))
        toolInfo = calibriSmall.render("Text", True, (0, 0, 0))
        screen.blit(toolInfo, (15+(250-toolInfo.get_width())//2, 38))
        screen.blit(noLumaSpeech, (905, 15))
        draw.rect(screen, (255, 255, 255), (textRect), 1)
    elif tool == "text":
        draw.rect(screen, (255, 255, 255), (textRect), 1)
    else:
        screen.blit(textRectCopy, (14, 374))

    if calligraphyRect.collidepoint(mx, my):
        screen.blit(marioSpeechCopy, (15, 15))
        toolInfo = calibriSmall.render("Calligraphy Pen", True, (0, 0, 0))
        screen.blit(toolInfo, (15+(250-toolInfo.get_width())//2, 38))
        screen.blit(noLumaSpeech, (905, 15))
        draw.rect(screen, (255, 255, 255), (calligraphyRect), 1)
    elif tool == "calligraphy":
        draw.rect(screen, (255, 255, 255), (calligraphyRect), 1)
    else:
        screen.blit(calligraphyRectCopy, (62, 374))

    if lineRect.collidepoint(mx, my):
        screen.blit(marioSpeechCopy, (15, 15))
        toolInfo = calibriSmall.render("Line", True, (0, 0, 0))
        screen.blit(toolInfo, (15+(250-toolInfo.get_width())//2, 38))
        screen.blit(noLumaSpeech, (905, 15))
        draw.rect(screen, (255, 255, 255), (lineRect), 1)
    elif tool == "line":
        draw.rect(screen, (255, 255, 255), (lineRect), 1)
    else:
        screen.blit(lineCopy, (14, 497))
        
    if rectRect.collidepoint(mx, my):
        screen.blit(marioSpeechCopy, (15, 15))
        toolInfo = calibriSmall.render("Rectangle", True, (0, 0, 0))
        screen.blit(toolInfo, (15+(250-toolInfo.get_width())//2, 38))
        screen.blit(noLumaSpeech, (905, 15))
        draw.rect(screen, (255, 255, 255), (rectRect), 1)
    if tool == "rectangle":
        draw.rect(screen, (255, 255, 255), (rectRect), 1)
    else:
        if shapeFormat == "no fill":
            screen.blit(rectEmptyCopy, (62, 497))
        else:
            screen.blit(rectFillCopy, (62, 497))

    if ellipseRect.collidepoint(mx, my):
        screen.blit(marioSpeechCopy, (15, 15))
        toolInfo = calibriSmall.render("Ellipse", True, (0, 0, 0))
        screen.blit(toolInfo, (15+(250-toolInfo.get_width())//2, 38))
        screen.blit(noLumaSpeech, (905, 15))
        draw.rect(screen, (255, 255, 255), (ellipseRect), 1)
    elif tool == "ellipse":
        draw.rect(screen, (255, 255, 255), (ellipseRect), 1)
    else:
        if shapeFormat == "no fill":
            screen.blit(ellipseEmptyCopy, (14, 547))
        else:
            screen.blit(ellipseFillCopy, (14, 547))

    if polygonRect.collidepoint(mx, my):
        screen.blit(marioSpeechCopy, (15, 15))
        toolInfo = calibriSmall.render("Polygon", True, (0, 0, 0))
        screen.blit(toolInfo, (15+(250-toolInfo.get_width())//2, 38))
        screen.blit(noLumaSpeech, (905, 15))
        draw.rect(screen, (255, 255, 255), (polygonRect), 1)
    elif tool == "polygon":
        draw.rect(screen, (255, 255, 255), (polygonRect), 1)
    else:
        if shapeFormat == "no fill":
            screen.blit(polygonEmptyCopy, (62, 547))
        else:
            screen.blit(polygonFillCopy, (62, 547))
        

# Beginning of section 2
    
    screen.set_clip(canvas)
    for e in event.get():
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 4:
                sizeUp = True
            elif e.button == 5:
                sizeDown = True

        if e.type == KEYDOWN and tool == "text":
            if e.key == 8 and len(txt) != 0:
                    txt = txt[:-1]
            elif e.key != 8 and len(txt) < 201:
                mx, my = mx, my
                newTxt = e.unicode
                txt += newTxt
            txtPic = calibriTxt.render(txt, True, (colour))
            txtW = txtPic.get_width()
            txtH = txtPic.get_height()
            screen.blit(oldCanvas, (120, 90))
            screen.blit(txtPic, (mx-txtW//2, my-txtH//2))

        if e.type == QUIT:
            running = False
            answer = messagebox.askyesno(title = 'Super Mario Galaxy Paint',
            message = 'Do you want to save changes to '+filepath+'?')
            if answer:
                if saveAs:
                    filepath = filedialog.asksaveasfilename(defaultextension = '.png', initialfile = 'Untitled')
                    if len(filepath) != 0:
                        if click:
                            mixer.Sound("Sounds/okie-dokie.ogg").play()
                        click = False                                            
                        slashPos = filepath.rfind("/")
                        if slashPos != len(filepath) - 1:
                            dot = filepath.rfind(".")
                            name = filepath[slashPos+1:dot]
                            display.set_caption(name+" - Super Mario Galaxy Paint")
                            oldCanvas = screen.subsurface(canvas).copy()
                            image.save(screen.subsurface(canvas), filepath)
                        saveAs = False
                else:
                    image.save(screen.subsurface(canvas), filepath)


    if tool == "cut":
        if mb[0] == 0:
            if pickCorner and mxStart == 0 and myStart == 0:
                mxStart, myStart = mx, my
                divide = True
            if drawingCutPic:
                screen.blit(oldCanvas, (120, 90))
                draw.rect(screen, (0), (mxStart, myStart, mx-mxStart, my-myStart), 1)
                cutPicRect = Rect(mxStart, myStart, mx-mxStart, my-myStart)
                cutPicRect.normalize()
                selectSurf = screen.subsurface(cutPicRect).copy()
                pickCorner = False
                cuttingPic = True
            elif draggingCutPic:
                screen.blit(oldCanvas, (120, 90))
                cutPic = transform.scale(origCutPic, (cutPicW, cutPicH))
                selectSurf = cutPic
                screen.blit(cutPic, (mx-cutPicW//2, my-cutPicH//2))
                cuttingPic = False
                pastingCutPic = True
        elif mb[0] == 1 and canvas.collidepoint(mx, my):
            if pickCorner and mxStart != 0 and myStart != 0:
                if click:
                    mxStart, myStart = mx, my
                click = False
                drawingCutPic = True
            elif cuttingPic:
                if click:
                    screen.blit(oldCanvas, (120, 90))
                    origCutPic = screen.subsurface(cutPicRect).copy()
                    cutPic = origCutPic
                    selectSurf = cutPic
                    cutPicW = cutPic.get_width()
                    cutPicH = cutPic.get_height()
                screen.subsurface(cutPicRect).fill((255, 255, 255))
                oldCanvas = screen.subsurface(canvas).copy()
                click = False
                drawingCutPic = False
                draggingCutPic = True
            elif pastingCutPic:
                if click:
                    oldCanvas = screen.subsurface(canvas).copy()
                    screen.blit(oldCanvas, (120, 90))
                click = False
                pickCorner = True
                draggingCutPic = False
                mxStart = 0
                myStart = 0
            
    elif tool == "copy":
        if mb[0] == 0:
            if pickCorner and mxStart == 0 and myStart == 0:
                mxStart, myStart = mx, my
                divide = True
            if drawingCutPic:
                screen.blit(oldCanvas, (120, 90))
                draw.rect(screen, (0), (mxStart, myStart, mx-mxStart, my-myStart), 1)
                cutPicRect = Rect(mxStart, myStart, mx-mxStart, my-myStart)
                cutPicRect.normalize()
                selectSurf = screen.subsurface(cutPicRect).copy()
                pickCorner = False
                cuttingPic = True
            elif draggingCutPic:
                screen.blit(oldCanvas, (120, 90))
                cutPic = transform.scale(origCutPic, (cutPicW, cutPicH))
                selectSurf = cutPic
                screen.blit(cutPic, (mx-cutPicW//2, my-cutPicH//2))
                cuttingPic = False
                pastingCutPic = True
        elif mb[0] == 1 and canvas.collidepoint(mx, my):
            if pickCorner and mxStart != 0 and myStart != 0:
                if click:
                    mxStart, myStart = mx, my
                click = False
                drawingCutPic = True
            elif cuttingPic:
                if click:
                    screen.blit(oldCanvas, (120, 90))
                    origCutPic = screen.subsurface(cutPicRect).copy()
                    cutPic = origCutPic
                    selectSurf = screen.subsurface(cutPicRect).copy()
                    cutPicW = cutPic.get_width()
                    cutPicH = cutPic.get_height()
                click = False
                drawingCutPic = False
                draggingCutPic = True
            elif pastingCutPic:
                if click:
                    oldCanvas = screen.subsurface(canvas).copy()
                    screen.blit(oldCanvas, (120, 90))
                click = False
                pickCorner = True
                draggingCutPic = False
                mxStart = 0
                myStart = 0

    if (tool == "cut" or tool == "copy") and draggingCutPic:
        if divide and (cutPicW != 0 or cutPicH != 0):
            ratio = cutPicW/cutPicH
        divide = False
        if sizeUp:
            cutPicH += 10
            cutPicW = int(cutPicH*ratio)
            sizeUp = False
        elif sizeDown:
            if cutPicH >= 10:
                cutPicH -= 10
            cutPicW = int(cutPicH*ratio)
            sizeDown = False
        
            
    if tool == "picture":
        if mb[0] == 0 and loaded:
            oldTool = "" 
            screen.blit(oldCanvas, (120, 90))
            screen.blit(loadPic, (mx-w//2, my-h//2))
            if divide and (w != 0 or h != 0):
                ratio = w/h
            divide = False
            if sizeUp:
                h += 10
                w = int(h*ratio)
                loadPic = transform.scale(origLoadPic, (w, h))
                screen.blit(loadPic, (mx-w//2, my-h//2))
                sizeUp = False
            if sizeDown:
                if h >= 10 and w >= 10:
                    h -= 10
                w = int(h*ratio)
                loadPic = transform.scale(origLoadPic, (w, h))
                screen.blit(loadPic, (mx-w//2, my-h//2))
                sizeDown = False
        elif mb[0] == 1 and loaded and oldTool != "picture" and choosing == False:
            loadPicX = mx-w//2
            loadPicY = my-h//2
            screen.blit(loadPic, (loadPicX, loadPicY))
            oldCanvas = screen.subsurface(canvas).copy()                   
            loaded = False
        elif mb[0] == 0 and loaded == False:
            tool = "pencil"
        selectSurf = loadPic
    
    elif tool == "stamp":
        w = stamp.get_width()
        h = stamp.get_height()
        if mb[0] == 0:
            oldTool = ""
            screen.blit(oldCanvas, (120, 90))
            if divide and (w != 0 or h != 0):
                ratio = w/h
            divide = False
            posInList = stamps.index(stamp)
            if sizeUp:
                h += 10
                w = int(h*ratio)
                stamp = transform.scale(originals[stamps.index(stamp)], (w, h))
                stamps[posInList] = stamp
                screen.blit(stamp, (mx-w//2, my-h//2))
                sizeUp = False
            if sizeDown:
                if h > 0 and w > 0:
                    h -= 10
                    w = int(h*ratio)
                stamp = transform.scale(originals[stamps.index(stamp)], (w, h))
                stamps[posInList] = stamp
                screen.blit(stamp, (mx-w//2, my-h//2))
                sizeDown = False
            else:
                screen.blit(stamp, (mx-w//2, my-h//2))
        elif mb[0] == 1 and canvas.collidepoint(mx, my) and oldTool != "stamp" and choosing == False:
            stampX = mx-w//2
            stampY = my-h//2
            screen.blit(stamp, (stampX, stampY))
            oldCanvas = screen.subsurface(canvas).copy()
        selectSurf = stamp

        
    elif tool == "pencil":
        if sizeUp:
            if pencilSize != 20:
                pencilSize += 1
            sizeUp = False
        if sizeDown:
            if pencilSize != 4: 
                pencilSize -= 1  
            sizeDown = False    
        if mb[0] == 0:           
            oldTool = ""
            screen.blit(oldCanvas, (120, 90))
            draw.circle(screen, (colour), (mx, my), pencilSize//2)
        elif mb[0] == 1 and  oldTool != "pencil" and choosing == False and 80 < my < 600:
            if click:
                mxStart = mx
                myStart = my
                screen.blit(oldCanvas, (120, 90))
                draw.circle(screen, (colour), (mx+1, my), pencilSize//2)
            click = False
            oldCanvas = screen.subsurface(canvas).copy()
            screen.blit(oldCanvas, (120, 90))
            mxEnd = mx
            myEnd = my
            draw.line(screen, (colour), (mxStart, myStart), (mxEnd, myEnd), pencilSize)
            draw.circle(screen, (colour), (mxEnd, myEnd), (pencilSize//2-2))
            mxStart = mxEnd
            myStart = myEnd
            
    elif tool == "marker": # subject to change
        if sizeUp:
            if markerSize != 40:
                markerSize += 1
            sizeUp = False
        if sizeDown:
            if markerSize != 20:
                markerSize -= 1
            sizeDown = False
        if mb[0] == 0:
            oldTool = ""
            screen.blit(oldCanvas, (120, 90))
            draw.circle(screen, (colour), (mx+1, my), markerSize//2)
        elif mb[0] == 1 and oldTool != "marker" and choosing == False and 80 < my < 600:
            if click:
                mxStart = mx
                myStart = my
                screen.blit(oldCanvas, (120, 90))
                draw.circle(screen, (colour), (mx+1, my), markerSize//2)
            click = False
            oldCanvas = screen.subsurface(canvas).copy()
            screen.blit(oldCanvas, (120, 90))
            mxEnd = mx
            myEnd = my
            draw.line(screen, (colour), (mxStart, myStart), (mxEnd, myEnd), markerSize)
            draw.circle(screen, (colour), (mxEnd+1, myEnd), markerSize//2-2)
            mxStart = mxEnd
            myStart = myEnd
            
    elif tool == "eraser":
        if sizeUp:
            if eraserSize != 40:
                eraserSize += 1
            sizeUp = False
        if sizeDown:
            if eraserSize != 2:
                eraserSize -= 1
            sizeDown = False
        if mb[0] == 0:
            oldTool = ""
            screen.blit(oldCanvas, (120, 90))
            draw.rect(screen, (255, 255, 255), (mx-eraserSize//2, my-eraserSize//2, eraserSize, eraserSize))
        elif mb[0] == 1 and oldTool != "eraser" and choosing == False  and 80 < my < 600:
            if click:
                mxStart = mx
                myStart = my
                screen.blit(oldCanvas, (120, 90))
            click = False
            oldCanvas = screen.subsurface(canvas).copy()
            screen.blit(oldCanvas, (120, 90))
            mxEnd = mx
            myEnd = my
            draw.rect(screen, (255, 255, 255), (mxStart-eraserSize//2, myStart-eraserSize//2, eraserSize, eraserSize))
            if mxEnd < mxStart and myEnd < myStart:
                draw.polygon(screen, (255, 255, 255), ((mxStart-eraserSize//2, myStart+eraserSize//2), (mxStart+eraserSize//2, myStart-eraserSize//2), (mxEnd+eraserSize//2, myEnd-eraserSize//2), (mxEnd-eraserSize//2, myEnd-eraserSize//2), (mxEnd-eraserSize//2, myEnd+eraserSize//2)))
            elif mxEnd > mxStart and myEnd > myStart:
                draw.polygon(screen, (255, 255, 255), ((mxStart-eraserSize//2, myStart+eraserSize//2), (mxStart+eraserSize//2, myStart-eraserSize//2), (mxEnd+eraserSize//2, myEnd-eraserSize//2), (mxEnd+eraserSize//2, myEnd+eraserSize//2), (mxEnd-eraserSize//2, myEnd+eraserSize//2)))             
            elif mxEnd > mxStart and myEnd < myStart:
                draw.polygon(screen, (255, 255, 255), ((mxStart-eraserSize//2, myStart-eraserSize//2), (mxStart+eraserSize//2, myStart+eraserSize//2), (mxEnd+eraserSize//2, myEnd+eraserSize//2), (mxEnd+eraserSize//2, myEnd-eraserSize//2), (mxEnd-eraserSize//2, myEnd-eraserSize//2)))             
            elif mxEnd < mxStart and myEnd > myStart:
                draw.polygon(screen, (255, 255, 255), ((mxStart-eraserSize//2, myStart-eraserSize//2), (mxStart+eraserSize//2, myStart+eraserSize//2), (mxEnd+eraserSize//2, myEnd+eraserSize//2), (mxEnd-eraserSize//2, myEnd+eraserSize//2), (mxEnd-eraserSize//2, myEnd-eraserSize//2)))
            elif mxEnd == mxStart:
                draw.polygon(screen, (255, 255, 255), ((mxStart-eraserSize//2, myStart), (mxStart+eraserSize//2, myStart), (mxEnd+eraserSize//2, myEnd), (mxEnd-eraserSize//2, myEnd)))
            elif myEnd == myStart:
                draw.polygon(screen, (255, 255, 255), ((mxStart, myStart-eraserSize//2), (mxStart, myStart+eraserSize//2), (mxEnd, myEnd+eraserSize//2), (mxEnd, myEnd-eraserSize//2)))
            draw.rect(screen, (255, 255, 255), (mx-eraserSize//2, my-eraserSize//2, eraserSize, eraserSize))
            mxStart = mxEnd
            myStart = myEnd
            
    elif tool == "dropper":
        if mb[0] == 0:
            oldTool = ""
            screen.blit(oldCanvas, (120, 90))
            fillStar = True
        elif mb[0] == 1 and canvas.collidepoint(mx, my) and oldTool != "dropper" and choosing == False:
            oldCanvas = screen.subsurface(canvas).copy()
            screen.blit(oldCanvas, (120, 90))
            colour = screen.get_at((mx, my))
            transparency = colour[3] # fix this
            tool = "pencil"
            
    elif tool == "bucket":
        if mb[0] == 0:
            oldTool = ""
            fill = True 
            screen.blit(oldCanvas, (120, 90))
        elif mb[0] == 1 and canvas.collidepoint(mx, my) and oldTool != "bucket" and choosing == False:
            if fill:
                screen.blit(oldCanvas, (120, 90))
                paint_bucket(mx, my, colour, screen.get_at((mx, my)))
            oldCanvas = screen.subsurface(canvas).copy()
            fill = False  # makes the paint bucket function only run once in one
                          # click (or else the program crashes)

    elif tool == "spray paint":
        if sizeUp:
            if sprayPaintSize != 80:
                sprayPaintSize += 1
            sizeUp = False
        if sizeDown:
            if sprayPaintSize != 10:
                sprayPaintSize -= 1
            sizeDown = False
        if mb[0] == 0:
            oldTool = ""
            screen.blit(oldCanvas, (120, 90))
            draw.circle(screen, (0), (mx, my), sprayPaintSize, 1)
            draw.line(screen, (0), (mx+sprayPaintSize-int(sprayPaintSize*0.25), my), (mx+sprayPaintSize+int(sprayPaintSize*0.25), my), 1)
            draw.line(screen, (0), (mx-sprayPaintSize-int(sprayPaintSize*0.25), my), (mx-sprayPaintSize+int(sprayPaintSize*0.25), my), 1)
            draw.line(screen, (0), (mx, my+sprayPaintSize-int(sprayPaintSize*0.25)), (mx, my+sprayPaintSize+int(sprayPaintSize*0.25)), 1)
            draw.line(screen, (0), (mx, my-sprayPaintSize-int(sprayPaintSize*0.25)), (mx, my-sprayPaintSize+int(sprayPaintSize*0.25)), 1)
            sp = 0
        elif mb[0] == 1 and canvas.collidepoint(mx, my) and oldTool != "spray paint" and choosing == False:
            if click:
                mxStart = mx
                myStart = my
                screen.blit(oldCanvas, (120, 90))
            click = False
            sp += 1
            oldCanvas = screen.subsurface(canvas).copy()
            screen.blit(oldCanvas, (120, 90))
            rad = randint(1, sprayPaintSize)
            if sp % 2 == 1:
                xPos = randint(0, rad)
                yPos = int(sqrt(rad**2 - xPos**2))
            else:
                yPos = randint(0, rad)
                xPos = int(sqrt(rad**2 - yPos**2))
            xPos *= choice(signs)
            yPos *= choice(signs)
            draw.line(screen, (colour), (mx+xPos, my+yPos), (mx+xPos, my+yPos), 1)
    
    elif tool == "text":
        if sizeUp:
            if textSize != 500:
                textSize += 1
            sizeUp = False
        if sizeDown:
            if textSize != 2:
                textSize -= 1
            sizeDown = False
        if mb[0] == 0:
            click = True
            oldTool = ""
            for e in event.get():
                if e.type == KEYDOWN:
                    if e.key == 8 and len(txt) != 0:
                        txt = txt[:-1]
                    elif e.key != 8 and len(txt) < 201:
                        newTxt = e.unicode
                        txt += newTxt
            txtPic = calibriTxt.render(txt, True, (colour))
            txtW = txtPic.get_width()
            txtH = txtPic.get_height()
            screen.blit(oldCanvas, (120, 90))
            screen.blit(txtPic, (mx-txtW//2, my-txtH//2))
        elif mb[0] == 1 and canvas.collidepoint(mx, my) and oldTool != "text" and choosing == False and len(txt) != 0:
            if click:
                oldCanvas = screen.subsurface(canvas).copy()
            txt = ""
            click = False
        
    elif tool == "calligraphy":
        if sizeUp:
            if calligraphySize != 40:
                calligraphySize += 1
            sizeUp = False
        if sizeDown:
            if calligraphySize != 2:
                calligraphySize -= 1
            sizeDown = False
        if mb[0] == 0:
            oldTool = ""
            screen.blit(oldCanvas, (120, 90))
            draw.line(screen, (colour), (mx-calligraphySize//2, my+calligraphySize//2), (mx+calligraphySize//2, my-calligraphySize//2))
        elif mb[0] == 1 and oldTool != "calligraphy" and choosing == False  and 80 < my < 600:
            if click:
                mxStart = mx
                myStart = my
                screen.blit(oldCanvas, (120, 90))
            click = False
            oldCanvas = screen.subsurface(canvas).copy()
            screen.blit(oldCanvas, (120, 90))
            mxEnd = mx
            myEnd = my
            draw.line(screen, (colour), (mxStart-calligraphySize//2, myStart+calligraphySize//2), (mxStart+calligraphySize//2, myStart-calligraphySize//2))
            draw.polygon(screen, (colour), ((mxStart-calligraphySize//2, myStart+calligraphySize//2), (mxStart+calligraphySize//2, myStart-calligraphySize//2), (mxEnd+calligraphySize//2, myEnd-calligraphySize//2), (mxEnd-calligraphySize//2, myEnd+calligraphySize//2)))
            mxStart = mxEnd
            myStart = myEnd
            
    elif tool == "line":
        if sizeUp and shapeFormat != "fill":
            if lineSize != 20:
                lineSize += 1
            sizeUp = False
        if sizeDown and shapeFormat != "fill":
            if lineSize != 2:
                lineSize -= 1
            sizeDown = False
        if mb[0] == 0:
            oldTool = ""
            if drawing:
                oldCanvas = screen.subsurface(canvas).copy()
            drawing = False
        # The useOld flag is used to fix the issue that would happen in the 
        # event that a stamp is so enlarged that when the user's mouse hovers 
        # over the shape tools, part of the stamp sticks out onto the canvas,
        # So when the user clicks on the shape tool, that part of the stamp
        # remains on the canvas (because without the useOld flag the program
        # would just copy the current canvas and continue pasting it.
            if useOld:  
                screen.blit(oldCanvas, (120, 90))
                oldCanvas = screen.subsurface(canvas).copy()
                
            useOld = False
            mxStart = mx
            myStart = my
            screen.blit(oldCanvas, (120, 90))
            draw.line(screen, (colour), (mx-lineSize//2, my), (mx+lineSize//2, my))
            draw.line(screen, (colour), (mx, my-lineSize//2), (mx, my+lineSize//2))
        elif mb[0] == 1 and canvas.collidepoint(mx, my) and oldTool != "line" and choosing == False:
            drawing = True
            if mxStart == 0 and myStart == 0:
                mxStart = mx
                myStart = my
            screen.blit(oldCanvas, (120, 90))
            draw.line(screen, (colour), (mxStart, myStart), (mx, my), lineSize)
            
            
    elif tool == "rectangle":
        if sizeUp and shapeFormat != "fill":
            if shapeSize != 20:
                shapeSize += 1
            sizeUp = False
        if sizeDown and shapeFormat != "fill":
            if shapeSize != 2:
                shapeSize -= 1
            sizeDown = False
        if mb[0] == 0:
            oldTool = ""
            if drawing:
                oldCanvas = screen.subsurface(canvas).copy()
            drawing = False
            if useOld:
                screen.blit(oldCanvas, (120, 90))
            useOld = False
            mxStart = mx
            myStart = my
            screen.blit(oldCanvas, (120, 90))
            draw.rect(screen, (colour), (mx-shapeSize//2, my-shapeSize//2, shapeSize,shapeSize))
        elif mb[0] == 1 and canvas.collidepoint(mx, my) and oldTool != "rectangle" and choosing == False:
            drawing = True
            if click:
                mxStart = mx
                myStart = my
            click = False
            screen.blit(oldCanvas, (120, 90))
            draw.rect(screen, (colour), (mxStart, myStart, mx-mxStart, my-myStart), shapeSize)
            if shapeSize % 2 == 0 and shapeFormat != "fill":
                draw.rect(screen, (colour), (mxStart-shapeSize//2+1, myStart-shapeSize//2+1, shapeSize, shapeSize))
                draw.rect(screen, (colour), (mx-shapeSize//2, myStart-shapeSize//2+1, shapeSize, shapeSize))
                draw.rect(screen, (colour), (mxStart-shapeSize//2+1, my-shapeSize//2, shapeSize, shapeSize))
                draw.rect(screen, (colour), (mx-shapeSize//2, my-shapeSize//2, shapeSize, shapeSize))
            elif shapeSize % 2 == 1 and shapeFormat != "fill":
                draw.rect(screen, (colour), (mxStart-shapeSize//2, myStart-shapeSize//2, shapeSize, shapeSize))
                draw.rect(screen, (colour), (mx-shapeSize//2-1, myStart-shapeSize//2, shapeSize, shapeSize))
                draw.rect(screen, (colour), (mxStart-shapeSize//2, my-shapeSize//2-1, shapeSize, shapeSize))
                draw.rect(screen, (colour), (mx-shapeSize//2-1, my-shapeSize//2-1, shapeSize, shapeSize))

    # fix
    elif tool == "ellipse":
        if sizeUp and shapeFormat != "fill":
            if shapeSize != 20:
                shapeSize += 1
            sizeUp = False
        if sizeDown and shapeFormat != "fill":
            if shapeSize != 2:
                shapeSize -= 1
            sizeDown = False
        if mb[0] == 0:
            oldTool = ""
            if drawing:
                oldCanvas = screen.subsurface(canvas).copy()
            drawing = False
            if useOld:
                screen.blit(oldCanvas, (120, 90))
            useOld = False
            oldCanvas = screen.subsurface(canvas).copy()
            mxStart = mx
            myStart = my
        elif mb[0] == 1 and canvas.collidepoint(mx, my) and oldTool != "ellipse" and choosing == False:
            drawing = True
            if mxStart == 0 and myStart == 0:
                mxStart = mx
                myStart = my
            screen.blit(oldCanvas, (120, 90))
            if mxStart > mx:
                cornerX = mxStart
            else:
                cornerX = mx
            if myStart > my:
                cornerY = myStart
            else:
                cornerY = my
            ellSurf = Surface((abs(mx-mxStart), abs(my-myStart)), SRCALPHA)
            draw.ellipse(ellSurf, (colour[0], colour[1], colour[2], 255), (0, 0, abs(mx-mxStart), abs(my-myStart)))
            if shapeFormat != "fill" and abs(mxStart-mx) > 2*shapeSize and abs(myStart-my) > 2*shapeSize:
                draw.ellipse(ellSurf, (0, 0, 0, 0), (shapeSize, shapeSize, abs(mx-mxStart)-shapeSize*2, abs(my-myStart)-shapeSize*2), 0)
            screen.blit(ellSurf, (cornerX-abs(mx-mxStart), cornerY-abs(my-myStart)))
            
    elif tool == "polygon":  
        if sizeUp and shapeFormat != "fill":
            if lineSize != 20:
                lineSize += 1
            sizeUp = False
        if sizeDown and shapeFormat != "fill":
            if lineSize != 2:
                lineSize -= 1
            sizeDown = False
        if mb[0] == 0:
            oldTool = ""
            clickPt = True
            if useOld:
                screen.blit(oldCanvas, (120, 90))
            useOld = False
            screen.blit(oldCanvas, (120, 90))
            if drawing:
                draw.line(screen, (colour), (pt), (mx, my), lineSize)
            if drawing == False:
                draw.line(screen, (colour), (mx-lineSize//2, my), (mx+lineSize//2, my))
                draw.line(screen, (colour), (mx, my-lineSize//2), (mx, my+lineSize//2))
            if drawing == False and starting == False:
                starting = True
        elif mb[0] == 1 and canvas.collidepoint(mx, my) and oldTool != "polygon" and choosing == False:
            if starting:
                sides = 0
                screen.blit(oldCanvas, (120, 90))
                startPt = (mx, my)
                pt = startPt
                pts.append(pt)
                drawing = True
            elif clickPt:
                if click:
                    sides += 1
                click = False
                pt = (mx, my)
                pts.append(pt)
                if int(sqrt((pt[0]-startPt[0])**2 + (pt[0]-startPt[0])**2)) <= 8 and len(pts) > 2:
                    del pts[-1]
                    screen.blit(oldCanvas, (120, 90))
                    draw.line(screen, (colour), (pts[-1]), (startPt), lineSize)
                    if shapeFormat == "fill":
                        draw.polygon(screen, (colour), (pts))
                    drawing = False
                    pts = []
            starting = False
            clickPt = False
            oldCanvas = screen.subsurface(canvas).copy()

    screen.set_clip(None)

    sizes = [pencilSize, markerSize, eraserSize, sprayPaintSize, calligraphySize,   
             lineSize, textSize, shapeSize]

    # bottom right corner of canvas, where tool thicknesses/sizes are displayed
    screen.blit(labelRectCopy, (780, 592))
    if tools.index(tool) < 6:
        if tool == "line" and mb[0] == 1:
            width = abs(mxStart-mx)
            height = abs(myStart-my)
            length = round(sqrt(width**2+height**2), 1)
            labelTxt = calibriBig.render("Line Length: "+str(length)+" px", True, (255, 255, 255))
        else:
            labelTxt = calibriBig.render(toolLabels[tools.index(tool)]+str(sizes[tools.index(tool)])+" px", True, (255, 255, 255))
            labelW = labelTxt.get_width()
        labelW = labelTxt.get_width()
        screen.blit(labelTxt, (1080-labelW, 592))
    elif tools.index(tool) == 6:
        labelTxt = calibriBig.render(toolLabels[tools.index(tool)]+str(sizes[tools.index(tool)])+" pts", True, (255, 255, 255))
        labelW = labelTxt.get_width()
        screen.blit(labelTxt, (1080-labelW, 592))
    elif 6 < tools.index(tool) < 9:
        if mb[0] == 1 and canvas.collidepoint(mx, my):
            rectW = str(abs(mx-mxStart))
            rectH = str(abs(my-myStart))
            labelTxt = calibriBig.render(toolLabels[tools.index(tool)]+rectW+" \u00d7 "+rectH+" px", True, (255, 255, 255))
        else:
            if shapeFormat == "no fill":
                labelTxt = calibriBig.render("Line Thickness: "+str(shapeSize)+" px", True, (255, 255, 255))
            else:
                labelTxt = calibriBig.render("Filled Shape", True, (255, 255, 255))
        labelW = labelTxt.get_width()
        screen.blit(labelTxt, (1080-labelW, 592))
    elif 8 < tools.index(tool) < 11:
        labelTxt = calibriBig.render(toolLabels[tools.index(tool)]+str(w)+" \u00d7 "+str(h)+" px", True, (255, 255, 255))
        labelW = labelTxt.get_width()
        screen.blit(labelTxt, (1080-labelW, 592))
    elif 10 < tools.index(tool) < 13:
        surfW = selectSurf.get_width()
        surfH = selectSurf.get_height()
        labelTxt = calibriBig.render(toolLabels[tools.index(tool)]+str(surfW)+" \u00d7 "+str(surfH)+" px", True, (255, 255, 255))
        labelW = labelTxt.get_width()
        screen.blit(labelTxt, (1080-labelW, 592))
    elif tools.index(tool) == 13:
        labelTxt = calibriBig.render(toolLabels[tools.index(tool)]+str(bPos+1)+" of "+str(len(backgrounds)), True, (255, 255, 255))
        labelW = labelTxt.get_width()
        screen.blit(labelTxt, (1080-labelW, 592))
    elif tools.index(tool) == 14:
        labelTxt = calibriBig.render(toolLabels[tools.index(tool)]+str(sides), True, (255, 255, 255))
        labelW = labelTxt.get_width()
        screen.blit(labelTxt, (1080-labelW, 592))
    else:
        labelTxt = calibriBig.render(toolLabels[tools.index(tool)], True, (255, 255, 255))
        labelW = labelTxt.get_width()
        screen.blit(labelTxt, (1080-labelW, 592))

                
    for e in event.get():
        if e.type == KEYDOWN and tool == "text":
            if e.key == 8 and len(txt) != 0:
                    txt = txt[:-1]
            elif e.key != 8 and len(txt) < 201:
                mx, my = mx, my
                newTxt = e.unicode
                txt += newTxt
            txtPic = calibriTxt.render(txt, True, (colour))
            txtW = txtPic.get_width()
            txtH = txtPic.get_height()
            screen.blit(oldCanvas, (120, 90))
            screen.blit(txtPic, (mx-txtW//2, my-txtH//2))

        if e.type == MOUSEBUTTONDOWN:
            if e.button == 4:
                sizeUp = True
            elif e.button == 5:
                sizeDown = True

        if e.type == QUIT:
            running = False
            answer = messagebox.askyesno(title = 'Super Mario Galaxy Paint',
            message = 'Do you want to save changes to '+filepath+'?')
            if answer:
                if saveAs:
                    filepath = filedialog.asksaveasfilename(defaultextension = '.png', initialfile = 'Untitled')
                    if len(filepath) != 0:
                        if click:
                            mixer.Sound("Sounds/okie-dokie.ogg").play()
                        click = False                                            
                        slashPos = filepath.rfind("/")
                        if slashPos != len(filepath) - 1:
                            dot = filepath.rfind(".")
                            name = filepath[slashPos+1:dot]
                            display.set_caption(name+" - Super Mario Galaxy Paint")
                            oldCanvas = screen.subsurface(canvas).copy()
                            image.save(screen.subsurface(canvas), filepath)
                        saveAs = False
                else:
                    image.save(screen.subsurface(canvas), filepath)

            
    display.flip()

# ending sequence...because why not?    
smgLogo = transform.scale(origSmgLogo, (687, 400))
mario_paint = transform.scale(orig_mario_paint, (337, 430))
babyLuma_paint = transform.scale(orig_babyLuma_paint, (269, 180))
screen.blit(spacePic, (0, 0))
screen.blit(smgLogo, (256, 150))
screen.blit(mario_paint, (0, 270))
screen.blit(babyLuma_paint, (890, 40))
display.flip()
mixer.Sound("Sounds/thank-you.ogg").play() # Mario normally says this at the end
                                           # of a game in the credits scene
time.wait(2800)
quit()
