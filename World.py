#class to control background

XFACTOR = 1
YFACTOR = 25
ZFACTOR = 1

FACTOR = 1
OFFSET = 128
from DiamondSquare import DiamondSquare
from LoadTerrain import LoadTerrain
import threading
import Queue
import time
#from RenderThread import RenderThread

PATH = ""

class World:

	def __init__(self, rw, transaction):
		self.rw = rw
		self.size = 3
		self.curr_x = 0
		self.curr_y = 0
		self.diamonds = {}
		self.index_list = []
		self.pos_list = []
		self.total_terr = 1
		self.trans = transaction
		
		
	#used to create the inital world
	def create_world(self):
		self.init_world()
		self.rw.index_list = []
		nlist = self.create_lists()	
		self.rw.lock.acquire()
		self.rw.index_list = nlist
		self.rw.lock.release()
		

	def start(self):	
		while True:
			self.update_loc(self.rw.camera.pos_X, self.rw.camera.pos_Y, self.rw.camera.pos_Z)
			#print "inside thread"
			time.sleep(1)
	#Used to create the inital world
	def init_world(self):
		for y in range(-FACTOR, self.size-FACTOR):
			for x in range(-FACTOR, self.size-FACTOR):
				#print "POS:",x,y
				self.pos_list.append((x,y))				
				ds = DiamondSquare((x, y))
				ds.diamond_square_tile(self.diamonds)
				self.diamonds[(x,y)] = ds
				#if (not x == 0 and not y == -1) or (not x == 0 and not y == 0):# or (x != 0 and y != -1):
				ds.save(PATH+str(x)+"_"+str(y)+".bmp")
	
	#Used to update camera location
	def update_loc(self,x,y,z):
		#print str(x),",",str(y)+",", str(z)
		x = int(x)
		z = int(z)
		if not self.is_in_tile(x,z,self.curr_x, self.curr_y):		
			newloc = self.get_tile(x,y,z)			
			self.curr_x = newloc[0]
			self.curr_y = newloc[1]
			print "NEWLOC:", newloc
			self.update_diamonds(newloc)

	def get_tile(self, x,y,z):
		x=int(x)
		y=int(y)
		z=int(z)
		for loc in self.pos_list:
				posx, posy = loc
				#print "POS:", posx, posy
				#print "stuff:",x,z,posx,posy
				if self.is_in_tile(x,z,posx,posy):
					return loc

	def is_in_tile(self,x,z,posx, posy):
	
		if posy < 0:
			if x in range(posx*OFFSET, (posx+1)*(OFFSET)) and z in range((posy)*(OFFSET), (posy-1)*OFFSET, -1):
				return True
			else:
				return False
		else:
			if x in range(posx*OFFSET, (posx+1)*(OFFSET)) and z in range((posy-1)*(OFFSET), (posy)*OFFSET):
				return True
			else:
				return False
		
	#Used to update the world list
	def update_diamonds(self, new_loc):
		x,y = new_loc
		self.pos_list = []
		for newy in range(y-1, y+2):
			for newx in range(x-1, x+2):
				self.pos_list.append((newx,newy))
				if not (newx, newy) in self.diamonds:
					ds = DiamondSquare((newx,newy))
					ds.diamond_square_tile(self.diamonds)
					self.diamonds[(newx,newy)] = ds
					ds.save(PATH+str(newx)+"_"+str(newy)+".bmp")
					print "done updating diamonds"
		
		self.rw.lock.acquire()
		new_list = self.create_lists()
		
		#set new index list

		print new_list
		self.rw.index_list = new_list
		self.rw.lock.release()
		'''
		def create_stuff(lock):
			new_list = self.create_lists()
			print new_list			
			lock.acquire()
			self.index_list = new_list
		w = World(r, trans)	lock.release()		
		#print self.pos_list

		print "making a thread"
		lock = threading.RLock()
		t = threading.Thread(target=create_stuff, args=(lock,))#thread.start_new_thread(self.create_lists, (lock))
		t.start()
		t.join()	'''	
		
		
		
	#Used to create the call lists
	def create_lists(self):
		#new_list = []
		#queue = Queue.Queue()
		
		def render_thing(location):
			print location
			#loc = queue.get()		
			x,y = location
			
			load = LoadTerrain(PATH+str(x)+"_"+str(y)+".bmp", (XFACTOR, YFACTOR, ZFACTOR))
			heights = load.load()
			
			face_norms, vert_norms = load.createRenderList(heights,str(x)+"_"+str(y))
			
			self.trans.location_var[location] = (face_norms, vert_norms, heights, x*OFFSET, -y*OFFSET, str(x)+"_"+str(y), self.pos_list.index(location))
			
			#nlist.append(index)
			
			
		'''
		for i in range(9):
			t = threading.Thread(target=render_thing, args=(new_list,))
			t.setDaemon(True)
              		t.start()

		for location in self.pos_list:
			queue.put(location)

		queue.join()
		
		self.index_list = new_list
		
					
		'''
		for location in self.pos_list:
			#nlock = threading.RLock()
			#render_thread = threading.Thread(target=render_thing, args=(location, new_list, nlock))
			#render_thread.start()
			#render_thread.join()
			render_thing(location)
		
		self.rw.need_lists = True
		#return new_list


if __name__ == "__main__":
	w = World()
