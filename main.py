import os
import random

BASE_DIR =  os.getcwd()
PATHS = {
    'data': os.path.join(BASE_DIR, 'data'),
    'views': os.path.join(BASE_DIR, 'views'),
    'screens': os.path.join(BASE_DIR, 'views', 'screens'),
    'components': os.path.join(BASE_DIR, 'views', 'components')
}
for p in PATHS.keys():
    if not os.path.exists(PATHS[p]):
        os.mkdir(PATHS[p])
        
imgs = [f for f in os.listdir(PATHS['data']) if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png')]
#for img in imgs:
    #os.rename(f'{PATHS["data"]}/{img}', f'{PATHS["data"]}/img0{imgs.index(img)}.{img.split(".")[-1]}')

import kivy
kivy.require('2.0.0')    
from kivy.animation import Animation
from kivy.clock import Clock 
from kivy.core.image import Image as CoreImage
from kivy.lang import Builder
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.camera import Camera
from kivy.uix.image import Image

from kivymd.app import MDApp
from kivymd.uix.behaviors import MagicBehavior, CircularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton, MDRectangleFlatButton, MDFloatingActionButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivymd.uix.templates import RotateWidget
print(dir(Image))


class ImgCard(MDCard, ButtonBehavior):
    '''Class emplements image card with button behaviour'''
    source = StringProperty()
    text = StringProperty()
    img_width = NumericProperty(0)
    img_height = NumericProperty(0)


class MagicIcoButton(MagicBehavior, MDFloatingActionButton):
    '''Class emplements Action Button widget with some Magic behavior'''


class Cam(CircularElevationBehavior, Camera, RotateWidget):
    '''Class emplements Camera widget with simple rotation property'''
    burst_timestop = NumericProperty(1)
    quantity = NumericProperty(3)
    rotate_value_angle = NumericProperty(-90)
    t = int(0)
    
    @property
    def get_angle_value(self):
        return self.rotate_value_angle
        
    @property
    def get_texture(self):
        return self.texture
    
    def show(self):
        print(self.burst_timestop)
        print(self.quantity)
        
    def burst(self, dt):
        self.t += round(dt)
        print(self.t)
        if self.t <= self.quantity:
            app = MDApp.get_running_app()
            self.take_pic()
            app.root.ids.burst_btn.wobble()
        else: 
            Clock.unschedule(self.burst)
        
    def take_pic(self):
        pics = [f for f in os.listdir(f'{PATHS["data"]}') if f.startswith("img")]
        index= len(pics)+1
        img = CoreImage(self.get_texture)
        img.save(f'{PATHS["data"]}/img{index}.jpg')
    

class InScreen(MDScreen):
    '''Emplements Root intro screen'''
    dialog =None
    cam = ObjectProperty()
    img_list = None
    
    def __init__(self, **kwargs):
        super(InScreen, self).__init__(**kwargs)
        
    def read_storage_data(self):
        self.img_list = [f for f in os.listdir(PATHS['data']) if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png')]
        self.ids.bakground.source = f'data/{random.choice(self.img_list)}'
        Animation(opacity=1).start(self.ids.work_lay)
     
    def settings_dialog(self):
        self.dialog = MDDialog(
            title='Settings',
            type='custom',
            #content_cls
            buttons=[
                MDRectangleFlatButton(
                    text='CANCEL',
                ),
                MDRaisedButton(
                    text='CONFIRM',
                )
            ]
        )
        self.dialog.open()
    
    
class DataAccumulatorApp(MDApp):
    title = 'Accumulating Data Camera'
    
    def build(self):
        self.theme_cls.material_style = 'M3'
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Lime'
        self.root = InScreen()
        return self.root
        
    def on_stop(self):
        pass
        
    def on_start(self):
        self.root.read_storage_data()
        for img in self.root.img_list:
            self.root.ids.grid.add_widget(ImgCard(
                source=f'{PATHS["data"]}/{img}',
                text = f'{img}',
            ))
            
            self.root.ids.grid.children[-1].img_width = Image(source=f'{PATHS["data"]}/{img}').texture_size[0]
            self.root.ids.grid.children[-1].img_height = Image(source=f'{PATHS["data"]}/{img}').texture_size[1]
        

if __name__ == '__main__':
    DataAccumulatorApp().run()