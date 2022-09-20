from ursina import *
import numpy as np

class Bird(Animation):
    def __init__(self):
        super().__init__("images/bird.gif")
        #self.collider = "box"
        self.collider = BoxCollider(self, center=Vec3(0,0,0), size=Vec3(0.5,0.5,1)) 

        self.scale = 1
        self.z=0
       
    def update(self):
        self.y = self.y - 1*time.dt
        intersection = self.intersects()
        if intersection.hit is True or self.y<-4:
            quit()

    def input(self,key):
        if key == "space":
            self.y =self.y +0.5
    
    def gameOver(self):
        print('inter')

class Pipe(Entity):
    def __init__(self,x = 8):
        y_rand = np.random.uniform(-3,3,1)[0]
        super().__init__(x=x,y=y_rand,z=0)
        self.p_a = Entity(model ="cube",y = -4,scale =(0.8,6.1,0.001),texture =load_texture("images/pipe_a.png"),collider ="box",parent = self)
        self.p_b = Entity(model ="cube",y = 4,scale =(0.8,6.1,0.001),texture =load_texture("images/pipe_b.png"),collider ="box",parent = self) 
    def update(self):
        self.x = self.x - 1*time.dt

def newPipe():
    Pipe()
    invoke(newPipe,delay=4)

def update():
    pass

def main():
    
    app = Ursina()
    Sky()
    Bird()
    newPipe()
    app.run()

if __name__ == "__main__":
    main()