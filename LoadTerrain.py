import Image
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from RenderTexture import RenderTexture

class LoadTerrain:
    X_FACTOR = 1
    Y_FACTOR = 25
    Z_FACTOR = 1
    MAP_SIZE = 100
    counter = 1

    def __init__(self, filename):
        self.im = Image.open(filename)
        self.width = self.im.size[0]
        self.height = self.im.size[1]
        self.images = []
	self.center = 0    	

    def load(self):
        '''Load a heightmap bitmap file into the Terrain.
        Store the terrain as a list of triangle strips.
        '''      
        heights = []
        
        # Down the rows
        for y in range(self.height):
            row = []

            # Across the columns
            for x in range(self.width):
                try:
                    pix = (self.im.getpixel((y, x)) / 255.) * self.Y_FACTOR
                except:
                    pass
                row.append(pix)
            heights.append(row)

        return heights

    def createRenderList(self, heights, offsetx, offsetz, textname, textid):
        rend = RenderTexture(heights, (self.X_FACTOR,self.Y_FACTOR,self.Z_FACTOR))
        self.texture = self.loadTexture(rend.run(heights,textname), textid)
        index = glGenLists(1)
        glNewList(index, GL_COMPILE)
        self.applyTexture(self.texture)
	
	z_incr = self.Z_FACTOR/float(len(heights))
	x_incr = self.X_FACTOR/float(len(heights[0]))

        for y in range(1, len(heights)):
            glBegin(GL_TRIANGLE_STRIP)
            for x in range(len(heights[y])):
	
		glTexCoord2f((len(heights)- y) * z_incr,-(x) * x_incr)

	        glVertex3f((x+offsetx)*self.X_FACTOR, heights[x][-y], -(y-1 + offsetz)*self.Z_FACTOR)

	        glTexCoord2f((len(heights)- y-1) * z_incr,-(x) * x_incr)

	        glVertex3f((x+offsetx)*self.X_FACTOR, heights[x][-y-1], -(y + offsetz)*self.Z_FACTOR)

            glEnd()
        glEndList()
        return index

    def loadTexture(self, filenames, texId):
        glGenTextures(1, texId)
        glBindTexture(GL_TEXTURE_2D, texId)
	print filenames
        self.images.append(Image.open(filenames))
        glTexImage2D(GL_TEXTURE_2D, 0, 3, self.images[-1].size[0], self.images[-1].size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, self.images[-1].tostring("raw","RGBX",0,-1))
        return texId

    def applyTexture(self, tex_id):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        #glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        '''glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)'''
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        #glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)


    def newTexture(self, altitude, percip):
        d_temp = altitude / 6.5
        temp = 20 - d_temp
        if temp <= 18:
            self.applyTexture(self.tex_list[0])
        elif temp < 20:
            self.applyTexture(self.tex_list[1])
        else:
            self.applyTexture(self.tex_list[2])
