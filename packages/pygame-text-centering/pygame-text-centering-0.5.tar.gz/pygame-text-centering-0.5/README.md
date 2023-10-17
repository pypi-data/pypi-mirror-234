![Pygame](https://www.pygame.org/docs/_images/pygame_logo.png)

# PYGAME WITH TRUE CENTERING

### Shell
```
pip install pygame-text-centering
```

### Python
```
#example.py

import pygame
from pgcentering import Button, BadButton, Text, TextButton

if __name__ == "__main__":
    
    pygame.init()
    clock = pygame.time.Clock()

    screen_dim = (800, 400)
    screen = pygame.display.set_mode(screen_dim)
    button_color = (200, 200, 200)
    button_dim = (300, 100)

    good_button_center = (screen_dim[0]//4, screen_dim[1]//4)
    good_button = Button(
        screen = screen,
        text = 'GOOD', 
        color = button_color, 
        center = good_button_center, 
        dim = button_dim)
    good_button.draw()

    bad_button_center = (screen_dim[0]*3//4, screen_dim[1]//4)
    bad_button = BadButton(
        screen = screen, 
        text = 'BAD', 
        color = button_color, 
        center = bad_button_center, 
        dim = button_dim)
    bad_button.draw()

    plain_text_center = (screen_dim[0]//4, screen_dim[1]*3//4)
    plain_text = Text(
        screen = screen,
        text = 'BUTTON',
        color = button_color,
        center = plain_text_center,
        font_size = 70)
    plain_text.draw()
    
    text_button_center = (screen_dim[0]*3//4, screen_dim[1]*3//4)
    text_button = TextButton(
        screen = screen,
        text = 'TEXT',
        color = button_color,
        center = text_button_center,
        font_size = 70)
    text_button.draw()

    while True:

        if good_button.is_clicked():
            print("I am a good button")

        if bad_button.is_clicked():
            print("I am a bad button")

        if text_button.is_clicked():
            print("I am a text button")
            text_button.erase_button()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
        clock.tick(60)
        pygame.display.update()
```

# WHAT A DIFFERENCE!
![Button Demo](https://i.imgur.com/glxJul9.png)
