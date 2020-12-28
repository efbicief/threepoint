import pygame
import numpy as np
 
class Point:
	def __init__(self):
		self.loc = (0,0)
		self.selected = False
	def getLoc(self):
		return self.loc
	def getx(self):
		return self.loc[0]
	def gety(self):
		return self.loc[1]
	def setLoc(self, x, y):
		self.loc = (x,y)
	def setLocTup(self, location):
		self.loc = location
		
class Button:
	def __init__(self, text, x1, y1, x2, y2):
		self.x1 = x1
		self.x2 = x2
		self.y1 = y1
		self.y2 = y2
		self.topleft = (x1, y1)
		self.topright = (x2, y1)
		self.botleft = (x1, y2)
		self.botright = (x2, y2)
		self.text = text
	def draw(self, colour): #colour in form (128,0,255)
		pygame.draw.line(screen, colour, self.topleft, self.topright, 1)
		pygame.draw.line(screen, colour, self.topleft, self.botleft, 1)
		pygame.draw.line(screen, colour, self.botleft, self.botright, 1)
		pygame.draw.line(screen, colour, self.topright, self.botright, 1)
		screen.blit(myfont.render(self.text, False, colour), self.topleft)
	def clicked(self):
		return (pygame.mouse.get_pressed()[0] and (self.x1 < pygame.mouse.get_pos()[0] <= self.x2) and (self.y1 < pygame.mouse.get_pos()[1] <= self.y2))

def calculateMidpoint(loc1, loc2):
	return ( ((loc1[0] + loc2[0])/2), ((loc1[1] + loc2[1])/2) )

#https://rosettacode.org
def line_intersect(Ax1, Ay1, Ax2, Ay2, Bx1, By1, Bx2, By2):
    """ returns a (x, y) tuple or None if there is no intersection """
    d = (By2 - By1) * (Ax2 - Ax1) - (Bx2 - Bx1) * (Ay2 - Ay1)
    if d:
        uA = ((Bx2 - Bx1) * (Ay1 - By1) - (By2 - By1) * (Ax1 - Bx1)) / d
        uB = ((Ax2 - Ax1) * (Ay1 - By1) - (Ay2 - Ay1) * (Ax1 - Bx1)) / d
    else:
        return
    if not(0 <= uA <= 1 and 0 <= uB <= 1):
        return
    x = Ax1 + uA * (Ax2 - Ax1)
    y = Ay1 + uA * (Ay2 - Ay1)
    return x, y

pygame.init()
screen = pygame.display.set_mode((1000, 800))
done = False
myfont = pygame.font.SysFont(None, 30)

points = []
for i in range(11):
	points.append(Point())
	
buttons = [Button("origin", 0,0,200,40), Button("C1", 0,41,67,80), Button("C2", 68,41,133,80), Button("C3", 134,41,200,80), Button("M1", 0,80,67,120), Button("M2", 68,80,133,120), Button("M3", 134,80,200,120)]
#buttons=[Button("C2", 68,41,133,80)]
selectedbtn = 0

drawConsLines = False
drawCube = True

consToggle = Button("No Construction Lines", 0,721, 200,760)
cubeToggle = Button("Drawing Cube", 0,761, 200,800)
drawarea = Button("", 201,0, 1000,800) #treat drawing area as button for clicks

while not done:
	mouseclick = False
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
	screen.fill( (255,255,255) )
	
	#basic stuff to draw!
	pygame.draw.line(screen, (0,0,0), (200,0), (200, 800), 2)
	#pygame.draw.line(screen, (0,0,0), (0, 40), (200, 40), 1)
	#pygame.draw.line(screen, (0,0,0), (0, 40), (200, 40), 1)
	for i in range(7):
		if i == selectedbtn:
			buttons[i].draw((200,0,0))
		else:
			buttons[i].draw((0,0,0))
		
		if buttons[i].clicked():
			selectedbtn = i
	#print("Button " + str(selectedbtn) + "(" + buttons[selectedbtn].text + ") selected")
	
	#extra buttons!
	
	if consToggle.clicked():
		if drawConsLines:
			drawConsLines = False
			consToggle.text = "No Construction Lines"
		else:
			drawConsLines = True
			consToggle.text = "Drawing Construction Lines"
	consToggle.draw((0,0,0))
	
	if cubeToggle.clicked():
		if drawCube:
			drawCube = False
			cubeToggle.text = "No Cube"
		else:
			drawCube = True
			cubeToggle.text = "Drawing Cube"
	cubeToggle.draw((0,0,0))
	
	if drawarea.clicked(): #if screen clicked
		points[selectedbtn].setLoc(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
		
	#calculate locations of midpoints
	points[4].setLoc( calculateMidpoint(points[0].getLoc(), points[1].getLoc())[0], calculateMidpoint(points[0].getLoc(), points[1].getLoc())[1] )
	points[5].setLoc( calculateMidpoint(points[0].getLoc(), points[2].getLoc())[0], calculateMidpoint(points[0].getLoc(), points[2].getLoc())[1] )
	points[6].setLoc( calculateMidpoint(points[0].getLoc(), points[3].getLoc())[0], calculateMidpoint(points[0].getLoc(), points[3].getLoc())[1] )
	
	#calculate lineints
	points[7].setLocTup( line_intersect(points[1].getx(), points[1].gety(), points[6].getx(), points[6].gety(), points[3].getx(), points[3].gety(), points[4].getx(), points[4].gety()) )
	points[8].setLocTup( line_intersect(points[1].getx(), points[1].gety(), points[5].getx(), points[5].gety(), points[2].getx(), points[2].gety(), points[4].getx(), points[4].gety()) )
	points[9].setLocTup( line_intersect(points[2].getx(), points[2].gety(), points[6].getx(), points[6].gety(), points[3].getx(), points[3].gety(), points[5].getx(), points[5].gety()) )
	
	#calculate point behind
	try:
		points[10].setLocTup( line_intersect(points[7].getx(), points[7].gety(), points[2].getx(), points[2].gety(), points[8].getx(), points[8].gety(), points[3].getx(), points[3].gety()) )
	except:
		pass
	
	#now, draw the cube
	#origin to perspective points
	if drawConsLines:
		pygame.draw.line(screen, (50,50,50), points[0].getLoc(), points[1].getLoc(), 1)
		pygame.draw.line(screen, (50,50,50), points[0].getLoc(), points[2].getLoc(), 1)
		pygame.draw.line(screen, (50,50,50), points[0].getLoc(), points[3].getLoc(), 1)
	
		#perspective points to midpoints
		pygame.draw.line(screen, (100,100,100), points[1].getLoc(), points[5].getLoc(), 2)
		pygame.draw.line(screen, (100,100,100), points[1].getLoc(), points[6].getLoc(), 2)
		pygame.draw.line(screen, (100,100,100), points[2].getLoc(), points[4].getLoc(), 2)
		pygame.draw.line(screen, (100,100,100), points[2].getLoc(), points[6].getLoc(), 2)
		pygame.draw.line(screen, (100,100,100), points[3].getLoc(), points[4].getLoc(), 2)
		pygame.draw.line(screen, (100,100,100), points[3].getLoc(), points[5].getLoc(), 2)
	
	if drawCube:
		#behind lines
		try:
			pygame.draw.line(screen, (150,150,250), points[10].getLoc(), points[7].getLoc(), 3)
			pygame.draw.line(screen, (150,150,250), points[10].getLoc(), points[8].getLoc(), 3)
			pygame.draw.line(screen, (150,150,250), points[10].getLoc(), points[9].getLoc(), 3)
		except:
			pass
		#origin to midpoints
		pygame.draw.line(screen, (0,0,0), points[0].getLoc(), points[4].getLoc(), 4)
		pygame.draw.line(screen, (0,0,0), points[0].getLoc(), points[5].getLoc(), 4)
		pygame.draw.line(screen, (0,0,0), points[0].getLoc(), points[6].getLoc(), 4)
	
		#midpoints to lineints
		#print(points[8].getLoc())
		try:
			pygame.draw.line(screen, (0,0,0), points[4].getLoc(), points[8].getLoc(), 4)
			pygame.draw.line(screen, (0,0,0), points[8].getLoc(), points[5].getLoc(), 4)
			pygame.draw.line(screen, (0,0,0), points[5].getLoc(), points[9].getLoc(), 4)
			pygame.draw.line(screen, (0,0,0), points[9].getLoc(), points[6].getLoc(), 4)
			pygame.draw.line(screen, (0,0,0), points[6].getLoc(), points[7].getLoc(), 4)
			pygame.draw.line(screen, (0,0,0), points[7].getLoc(), points[4].getLoc(), 4)
		except:
			pass
	
	#draw perspective points
	pygame.draw.circle(screen, (255,0,0), points[1].getLoc(), 5, 1)
	pygame.draw.circle(screen, (0,255,0), points[2].getLoc(), 5, 1)
	pygame.draw.circle(screen, (0,0,255), points[3].getLoc(), 5, 1)
	
	pygame.display.flip()
	pygame.time.delay(round(1000/30)) #30fps
