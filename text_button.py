import pygame

# Creates a rectangular button you can fill the center with text
class Button:
    def __init__(self, pos, text, colour, hover_colour, width, height, window, function):
        self.function = function    # To be paired with a function in the mainloop which decides how to handle it
        self.window = window
        self.base_font = pygame.font.get_default_font()

        self.text = text
        self.colour = colour
        self.hover_colour = hover_colour
        self.width = width
        self.height = height
        self.border = 5

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = pos  # pos will be a tuple of (x_position, y_position)
        self.hovering = False
        
        self.clicked = True     # Starting on true stops the button being pressed immediately

    # Sees if button has been pressed
    def check_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                return True

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        return False

    def update(self):
        # Swaps colours if cursor is over the button
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if not self.hovering:
                self.hovering = True
                self.colour, self.hover_colour = self.hover_colour, self.colour

        elif self.hovering:
            self.hovering = False
            self.colour, self.hover_colour = self.hover_colour, self.colour

    def draw_text(self, size, pos, font_name, text):
        font = pygame.font.SysFont(font_name, size)
        text_surface = font.render(text, True, self.colour)
        text_rect = text_surface.get_rect()
        text_rect.center = pos
        self.window.blit(text_surface, text_rect)

    # Draws entire button
    def draw(self):
        pygame.draw.rect(self.window, self.colour, self.rect, self.border)
        self.draw_text(self.rect.height//2, self.rect.center, self.base_font, self.text)