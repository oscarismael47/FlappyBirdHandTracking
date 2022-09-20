from email import message
from ursina import *
import numpy as np
import zmq

class Bird(Animation):
    def __init__(self):
        super().__init__("images/bird.gif")
        #self.collider = "box"
        self.collider = BoxCollider(self, center=Vec3(0,0,0), size=Vec3(0.5,0.5,1)) 
        self.scale = 1
        self.z=0

    def update(self):
        self.y = self.y - 0.75*time.dt
        intersection = self.intersects()
        if intersection.hit is True or self.y<-4: 
            print("intersection" )
            quit()
    def up(self):
        self.y =self.y +0.75

    def input(self,key):
        if key == "space":
            self.up()


class Pipe(Entity):
    def __init__(self,x = 10):
        y_rand = np.random.uniform(-3,3,1)[0]
        super().__init__(x=x,y=y_rand,z=0)
        self.p_a = Entity(model ="cube",y = -5.5,scale =(0.8,7.1,0.001),texture =load_texture("images/pipe_a.png"),collider ="box",parent = self)
        self.p_b = Entity(model ="cube",y = 5.5,scale =(0.8,7.1,0.001),texture =load_texture("images/pipe_b.png"),collider ="box",parent = self) 
    def update(self):
        self.x = self.x - 1*time.dt

class Score(Text):
    def __init__(self):
        super().__init__()
        self.color = color.black
        self.scale = 2
        self.position = (-0.6,0.45)
        self.value = 0
        self.text = "Score: " + str(self.value).zfill(3)
        self.update_score()

    def update_score(self):
        self.value+=1
        self.text = "Score: " + str(self.value).zfill(3)
        invoke(self.update_score,delay=1)

class ControlPanel(Entity):
    def __init__(self,x = 10):
        super().__init__(position=(-5.25,-3.5,-1))
        self.panel = Entity(model='quad', color=color.black, scale=(3,3),parent=self)
        self.h_line = Entity(model='line', color=color.white, scale=(3,1),parent=self)
        self.point = Entity(model='circle', color=color.red,position=(0,0,-0.1), scale=0.3,parent=self)
        self.point_value = 0
    def update(self):
        #self.point_value  = np.random.uniform(-1.5,1.5,1)[0]
        self.point.position = (0,self.point_value,-0.1)



def newPipe():
    Pipe()
    invoke(newPipe,delay=6)

def update():    
    message = socket.recv_string()
    state,value = message.split(',')
    if state == '1':
        bird_1.up()
    value = np.interp(float(value),[0,1],[1.5,-1.5])
    cp.point_value = value




context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.connect("tcp://localhost:5555")

app = Ursina()
window.borderless = False
window.windowed_size = (0.3,0.6)
window.update_aspect_ratio()
window.late_init()


Sky()
bird_1 = Bird()
newPipe()
score = Score()
cp=ControlPanel()


app.run()