import curses, random, traceback


alphabet = range(33,127)
rate     = 5    
death    = 0.07 
delay    = 90   
fade     = 10   


class gfx:
	setup = False
	def __init__(self):
		global green, white
		
		self.w = curses.initscr()
		gfx.setup = True

		curses.noecho()
		curses.cbreak()
		curses.start_color()
		curses.curs_set(0)
		
		curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
		curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
		self.green = curses.color_pair(1)
		self.white = curses.color_pair(2)
		
		self.data = []
		for i in xrange(curses.LINES):
			self.data.append( [ (0, ord(' ')) ] * curses.COLS )
		
	def set(self, (x,y), char):
		if x < 0 or x >= curses.COLS or y < 0 or y >= curses.LINES:
			return
		
		self.data[y][x] = (fade, char)
	
	def step(self):
		for i in xrange(len(self.data)):
			for j in xrange(len(self.data[i])):
				newcount, char = self.data[i][j]
				if newcount > 0:
					newcount -= 1
					self.data[i][j] = (newcount, char)
	
	def draw(self):
		for i in xrange(len(self.data)):
			for j in xrange(len(self.data[i])):
				count, char = self.data[i][j]
				
				char = ord(' ') if count<=0 else char
				color = self.green if count<fade else self.white
				
				try: self.w.addch(i, j, char, color)
				except: pass
				

class glyph:
	def __init__(self, x):
		self.x, self.y = x, -1
		self.alive = True
		self.newchar()
	
	def newchar(self):
		self.char = random.choice("01")
	
	def move(self):
		if not self.alive:
			return
		
		if random.random() < death:
			self.alive = False
			return
		
		self.y += 1
	
	def step(self, g):
		if not self.alive:
			return
		self.move()
		self.newchar()
		g.set((self.x,self.y), self.char)

def main():
	g = gfx()
	items = []
	while True:
		for i in xrange(rate):
			items.append(glyph(random.randint(0, curses.COLS)))
		
		g.step()
		
		for i in items:
			i.step(g)
			if not i.alive:
				del i
			
		g.draw()
		g.w.refresh()
		curses.napms(delay)

if __name__ == "__main__":
	try:
		main()
	except:
		if gfx.setup:
			curses.nocbreak()
			curses.echo()
			curses.endwin()
		traceback.print_exc()