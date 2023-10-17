import pygame
import os

def generate_offset_data(params = None):
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,-1000"
    pygame.init()
    dim = (1000, 600)
    screen = pygame.display.set_mode((dim[0], dim[1]))
    screen.fill((0, 0, 0))

    real_rect = pygame.rect.Rect((0 , 0), dim)
    real_rect.center = screen.get_rect().center

    COLOR = (255, 255, 255)

    font_list = []
    offset_list = []
    for font_size in range(5, 800):
        
        screen.fill((0, 0, 0))
        
        font = pygame.font.Font(None, font_size)
        render = font.render('T', True, COLOR)
        font_rect = render.get_rect(center = real_rect.center)
        if params:
            font_rect.centery = font_rect.centery+font_size*params['coef']+params['intercept']
        screen.blit(render, font_rect)
        pygame.draw.rect(screen, COLOR, real_rect, 1)

        ##initial value
        text_top = -1 
        text_bot = -1

        rect_centery = dim[1]//2+1
        
        #0 and height-1 are the rectangle border
        i = 0
        while text_top < 0 or text_bot < 0:
            
            for y in range(1,dim[1]//2):
                pos = (dim[0]//2+i,y)
                color = screen.get_at(pos)[1]

                #get center of text and and size of text
                #offset -> move down the difference in pixels between text center and rectangle center for each font_size
                if color > 0:
                    text_top = y

                    break

            for y in range(dim[1]-2,dim[1]//2,-1):
                pos = (dim[0]//2+i,y)
                color = screen.get_at(pos)[1]

                #get center of text and and size of text
                #offset -> move down the difference in pixels between text center and rectangle center for each font_size
                if color > 0:
                    text_bot = y
                    break
            
            i = i+1

        letter_height = text_bot-text_top+1
        letter_centery = text_top + letter_height//2 + 1

        offset = rect_centery - letter_centery

        font_list.append(font_size)
        offset_list.append(offset)

        pygame.display.update()

    pygame.quit()

    data = {'font_size_list': font_list, 'offset_list': offset_list}
    del os.environ['SDL_VIDEO_WINDOW_POS']
    return data
    

