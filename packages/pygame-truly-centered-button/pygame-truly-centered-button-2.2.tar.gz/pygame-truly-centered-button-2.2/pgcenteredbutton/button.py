import pygame
from pgcenteredbutton.offset_linear_regression import params


class Button:
    def __init__(self, screen: pygame.Surface, text: str, color: tuple, center: tuple, dim: tuple, thickness = 1, radius = -1, font_size = 0, adjusted = True):
        self.screen = screen
        self.screen_color = screen.get_at(center)
        self.color = color
        self.font_size = font_size or int(dim[1]/.9) 
        self.render = pygame.font.Font(None, self.font_size).render(text, True, color)
        self.radius = radius
        self.thickness = thickness
        self.dim = dim #(w, h)

        self.real_rect = pygame.Rect(0, 0, dim[0], dim[1]) #(left, top, width, height)
        self.real_rect.center = center
        self.font_rect = self.render.get_rect(center=center)
        while self.font_rect.w > dim[0] or self.font_rect.h > dim[1]:
            self.font_size -= 1
            font = pygame.font.Font(None, self.font_size)
            self.render = font.render(text, True, color)
            self.font_rect = self.render.get_rect(center=center)

        if adjusted:
            self.font_rect.centery = self.font_rect.centery+self.font_size*params['coef']+params['intercept'] #adjust text to center

        self.was_hovered = False
        self.clicked = False

    def __draw_text(self):
        self.screen.blit(self.render, self.font_rect)

    def __draw_border(self, extra = 0, color = None):
        color = color or self.color
        pygame.draw.rect(self.screen, color, self.real_rect, self.thickness + extra, self.radius)

    def __draw_hovered(self, color = (255, 255, 255)):
        self.__draw_border(3, color)

    def erase_button(self):
        self.__draw_border(-self.thickness, self.screen_color)

    def __handle_unhovered(self):
        self.__draw_hovered(self.screen_color)
        self.__draw_border()
    
    def __handle_click_down(self):
        brighter_color = tuple([value+(255-value)*0.2 for value in self.screen_color.normalize()[:3]])
        self.__draw_border(-self.thickness, brighter_color)
        self.__draw_text()
        self.__draw_hovered()

    def __handle_click_up(self):
        self.erase_button()
        self.screen.blit(self.render, self.font_rect)
        self.__draw_hovered()
        self.clicked = True

    #Public methods

    def draw(self):
        self.__draw_text()
        self.__draw_border()

    def is_hovered(self):
        return self.real_rect.collidepoint(pygame.mouse.get_pos())

    def is_clicked(self, event: pygame.event):
        if self.was_hovered is False:
            if self.is_hovered() is True:
                self.was_hovered = True
                self.__draw_hovered()
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                pygame.display.update()
            
        else:
            if self.is_hovered() is True:     
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.__handle_click_down()
                    pygame.display.update()
                
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.__handle_click_up()
                    pygame.display.update()
                    return True

            else:
                self.was_hovered = False
                self.__handle_unhovered()
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                pygame.display.update()
                
        return False

            
class BadButton(Button):
    def __init__(self, screen: pygame.Surface, text: str, color: tuple, center: tuple, dim: tuple, thickness = 1, radius = -1, font_size = 0):
        super().__init__(screen, text, color, center, dim, thickness, radius, font_size, adjusted = False)        
        

