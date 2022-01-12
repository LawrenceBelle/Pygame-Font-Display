import pygame
from text_button import Button

class FontTest:
    def __init__(self):
        pygame.init()
        self.running = True
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 800, 400
        self.WINDOW = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Pygame SysFont Test")

        self.base_font = pygame.font.get_default_font()
        self.fonts = pygame.font.get_fonts()
        self.font_index = 0
        self.current_font = self.fonts[self.font_index]
        self.text_colour = (255, 255, 255)
        self.bg_colour = (0, 0, 0)

        self.FPS = 60

        self.input_box = self.TextBox(self.WINDOW, self.WINDOW_WIDTH, self.WINDOW_HEIGHT, self.base_font, self.text_colour)
        self.example_text_caps = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.example_text_lower = self.example_text_caps.lower()
        self.example_text_num = '0123456789'

        # Button parameters
        self.button_y = 7 * self.WINDOW_HEIGHT//8
        self.button_width = self.WINDOW_HEIGHT//8
        self.button_height = self.WINDOW_HEIGHT//8      
        self.b_width_buffer = 20
        self.l_button_pos = (self.WINDOW_WIDTH//2 - (self.button_width + self.b_width_buffer), self.button_y)
        self.r_button_pos = (self.WINDOW_WIDTH//2 + (self.button_width + self.b_width_buffer), self.button_y)
        self.button_colour = (80, 80, 80)
        self.h_button_colour = (140, 140, 140)

        self.left_button = Button(self.l_button_pos, '<', self.button_colour, self.h_button_colour, self.button_width, self.button_height, self.WINDOW, 'left')
        self.right_button = Button(self.r_button_pos, '>', self.button_colour, self.h_button_colour, self.button_width, self.button_height, self.WINDOW, 'right')
        self.buttons = [self.left_button, self.right_button]

        self.enter_button = Button((self.WINDOW_WIDTH//2, self.input_box.text_box.center[1] + self.input_box.text_box.height), '<-/', self.button_colour, self.h_button_colour, self.button_width, self.button_height//2, self.WINDOW, 'enter')
        self.buttons.append(self.enter_button)

    class TextBox:
        def __init__(self, window, window_width, window_height, font, colour):
            self.WINDOW = window
            self.WINDOW_WIDTH = window_width
            self.WINDOW_HEIGHT = window_height
            self.base_font = font
            self.font_size = self.WINDOW_HEIGHT//10
            self.text_colour = colour

            self.box_text = ''
            self.text_box = pygame.Rect(0, 0, (2 * self.WINDOW_WIDTH//3), self.WINDOW_HEIGHT//8)
            self.text_box.center = (self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT//4)
            self.active_text_box_colour = (140, 140, 140)
            self.passive_text_box_colour = (80, 80, 80)
            self.box_colour = self.passive_text_box_colour
            self.text_box_border = 5

            self.active = False

        def draw_text_box(self):
            font = pygame.font.SysFont(self.base_font, self.font_size)
            text_surface = font.render(self.box_text, True, self.text_colour)
            text_rect = text_surface.get_rect() 
            text_rect.center = self.text_box.center
            pygame.draw.rect(self.WINDOW, self.box_colour, self.text_box, self.text_box_border)
            self.WINDOW.blit(text_surface, text_rect)

        def activate(self):
            self.active = True
            self.box_colour = self.active_text_box_colour

        def deactivate(self):
            self.active = False
            self.box_colour = self.passive_text_box_colour

    def draw_text(self, size, pos, font_name, text):
        font = pygame.font.SysFont(font_name, size)
        text_surface = font.render(text, True, self.text_colour)
        text_rect = text_surface.get_rect()
        text_rect.center = pos
        self.WINDOW.blit(text_surface, text_rect)

    def check_buttons(self):
        for button in self.buttons:
            if button.check_clicked():

                if button.function == 'left':
                    self.font_index -= 1
                    self.font_index = self.font_index % len(self.fonts)
                    self.current_font = self.fonts[self.font_index]

                if button.function == 'right':
                    self.font_index += 1
                    self.font_index = self.font_index % len(self.fonts)
                    self.current_font = self.fonts[self.font_index]

                if button.function == 'enter':
                    if self.input_box.box_text in self.fonts:
                        self.current_font = self.input_box.box_text
                        self.font_index = self.fonts.index(self.current_font)
                        self.input_box.box_text = ''

    def draw_window(self):
        self.WINDOW.fill(self.bg_colour)
        self.draw_text(self.WINDOW_HEIGHT//15, (self.WINDOW_WIDTH//2, self.input_box.text_box.center[1] - self.input_box.text_box.height), self.base_font, f'Current font: {self.current_font}')
        try:
            self.draw_text(self.WINDOW_WIDTH//26, (self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT//2), self.current_font, self.example_text_caps)
            self.draw_text(self.WINDOW_WIDTH//26, (self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT//2 + 30), self.current_font, self.example_text_lower)
            self.draw_text(self.WINDOW_WIDTH//26, (self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT//2 + 60), self.current_font, self.example_text_num)
        except:
            self.draw_text(self.WINDOW_WIDTH//26, (self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT//2), self.base_font, 'Current font not found')

        self.input_box.draw_text_box()

        for button in self.buttons:
            button.draw()
        pygame.display.update()


    def run(self):
        while self.running:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_box.text_box.collidepoint(event.pos):
                        self.input_box.activate()
                    else:
                        self.input_box.deactivate()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.font_index -= 1
                        self.font_index = self.font_index % len(self.fonts)
                        self.current_font = self.fonts[self.font_index]
                    if event.key == pygame.K_RIGHT:
                        self.font_index += 1
                        self.font_index = self.font_index % len(self.fonts)
                        self.current_font = self.fonts[self.font_index]

                    if self.input_box.active:
                        if event.key == pygame.K_BACKSPACE:
                            self.input_box.box_text = self.input_box.box_text[:-1]
                        elif event.key == pygame.K_RETURN:
                            if self.input_box.box_text in self.fonts:
                                self.current_font = self.input_box.box_text
                                self.font_index = self.fonts.index(self.current_font)
                                self.input_box.box_text = ''
                        else:
                            self.input_box.box_text += event.unicode

            for button in self.buttons:
                button.update()
            self.check_buttons()
            self.draw_window()



if __name__ == '__main__':
    font_test = FontTest()
    font_test.run()



