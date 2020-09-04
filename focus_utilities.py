import pygame
import math
import time

 
from enum import Enum
class Status(Enum):
    INACTIVE = 1
    HOVER = 2
    PUSHED = 3
        



class GButton:
    
    
    def __init__(self, rect, colors, text = None, index = None, value = None, image = None, action = None):

        self.rect = pygame.Rect(rect)
        self.colors = colors
        self.text = text
        self.value = value
        self.index = index
        self.image = image
        self.status = Status.INACTIVE
        self.action = action
         

    def text_button(self):
       
        font = pygame.font.Font(None, self.rect[3]//2)
        text_but = font.render(self.text, True, (0,0,0))
        text_but_rect = text_but.get_rect(center = self.rect.center)

        return text_but, text_but_rect

    def get_text(self):
        return self.text
    def get_value(self):
        return self.value
    def get_index(self):
        return self.index
    

    def add_image(self):
        if self.image:
            return  pygame.image.load(self.image)
        
  
    def button_check(self, event):        
  
        if event.type == pygame.MOUSEMOTION:
               
            if self.status is not Status.PUSHED:
                if self.rect.collidepoint(event.pos):
                    self.status = Status.HOVER
                else:
                    self.status = Status.INACTIVE
     

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.status is Status.PUSHED:
                    self.status = Status.HOVER
                else:
                    self.status = Status.PUSHED
                    if callable(self.action):
                        self.action()

    def release_button(self):
        self.status = Status.INACTIVE
                        
        
            


    def button_draw(self, surface):
  
        inactive_color, hover_color, pushed_color = self.colors
  
        color = inactive_color
  

        if self.status is Status.HOVER:
            color = hover_color
        
        elif self.status is Status.PUSHED:
  
            color = pushed_color

        pygame.draw.rect(surface, color, self.rect)
        
        if self.image:
            
            
            img = self.add_image()
            img_rect = img.get_rect(center = self.rect.center)
            surface.blit(img,img_rect)
        if self.text:
            text, text_rect = self.text_button()
            surface.blit(text, text_rect)

    def __repr__(self):
        x, y, w, h = self.rect
        return 'Button:' + str(self.index) + ',' + str(self.value) + ','+str(x) +','+str(y)+','+str(w)+','+str(h)

     
 




class GroupButton:

    VAL = 500
    
    def __init__(self, group_rect, rows, cols,  buttons_number, 
                marge, colors, text = None, images = None, values = None, action = None):

        self.group_rect = group_rect
        self.marge = marge
        self.cols, self.rows = cols, rows
        self.buttons_number = buttons_number
        self.text = text
        self.colors = colors
        self.values = values
        self.images = images
        self.action = action
        self.buttons = []
        self.already_pushed = GroupButton.VAL

    def getButDimensions(self):
        _, _, width, height = self.group_rect
              
        but_width = (width - self.marge*(self.cols+1)) // self.cols
        but_height = (height - self.marge*(self.rows + 1)) // self.rows
        return but_width, but_height
        

    def set_group(self):
        x, y, _, _ = self.group_rect
        but_width, but_height = self.getButDimensions()
        bx, by = x + self.marge, y + self.marge
        button_colors = self.colors[1:]
        for i in range(self.buttons_number):

            but_rect = pygame.Rect(bx, by, but_width, but_height)
            button = GButton(but_rect, button_colors,index = i,
                             value = self.values[i] if self.values else None,
                             text = self.text[i] if self.text else None,
                             image = self.images[i] if self.images else None,
                             action = self.action if self.action else None)
            self.buttons.append(button)
            if not (i + 1) % self.cols:
                bx, by = x + self.marge, by + but_height + self.marge
            else:
                bx = bx + but_width + self.marge
            


    def check_group(self,event):
        i = 0
        
        while True:
            if i == len(self.buttons):
                break
            self.buttons[i].button_check(event)
 
            #print( i , ':already_pushed = ', self.already_pushed)

            if self.buttons[i].status is Status.PUSHED and i != self.already_pushed:
                if self.already_pushed in range(self.buttons_number):
                    self.buttons[self.already_pushed].status = Status.INACTIVE
                self.already_pushed = i
                
                    

                    
                    
            if self.buttons[i].status is Status.INACTIVE and self.already_pushed == i:
                self.already_pushed = GroupButton.VAL
            
            i += 1
    def get_choice(self, default_value):
        if self.already_pushed != GroupButton.VAL:
            return self.buttons[self.already_pushed].value
        return default_value
            

    def display_group(self, surface):
        marge_col = self.colors[0]
        pygame.draw.rect(surface, marge_col, self.group_rect)

        for button in self.buttons:
  
            button.button_draw(surface)
     



class Message:
    def __init__(self, surface, msg, font, font_size, msg_center, color, background_color = None):
        
        self.surface = surface
        text_font = pygame.font.Font(font, font_size)
        self.textSurface = text_font.render(msg, True, color, background_color)
        self.textRect = self.textSurface.get_rect(center = msg_center)

    def display_msg(self):
        
        self.surface.blit(self.textSurface, self.textRect)
  
        
    def clear_msg(self):
        clean_surf = self.textRect.inflate(20,0)
        clean_surf = self.surface.subsurface(clean_surf)
        
        if self.background_color:
            clean_surf.fill(self.bacground_color)
        else:
            clean_surf.fill((255,255,255))



        
            
