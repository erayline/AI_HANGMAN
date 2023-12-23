import openai
import pygame
import sys
import random

global page
page = 0
#we are loading our saved information here 


pygame.init()
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
WHITE = (225, 205, 205)
BLACK = (0, 0, 0)
GREEN = (100,50,100)



screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Team 1 - Hangingman")

resim6 = pygame.image.load("game_assets/images/life6.png")
resim5 = pygame.image.load("game_assets/images/life5.png")
resim4 = pygame.image.load("game_assets/images/life4.png")
resim3 = pygame.image.load("game_assets/images/life3.png")
resim2 = pygame.image.load("game_assets/images/life2.png")
resim1 = pygame.image.load("game_assets/images/life1.png")
resim0 = pygame.image.load("game_assets/images/life0.png")
enterance = pygame.image.load("game_assets/images/enterance.png")
hint_image = pygame.image.load("game_assets/images/hint.png")
dying =pygame.mixer.Sound("game_assets/sound_effects/dying.mp3")
thank_you = pygame.mixer.Sound("game_assets/sound_effects/thank.mp3")

background = pygame.mixer.music.load("game_assets/sound_effects/general_music.mp3")



#when you enter a difficulty level among 1-2-3 output will be a random word. this works for database.
def random_word(diff): #deiş

    easyList = ["animal.txt", "fruit.txt"]
    medList = ["items.txt", "cities.txt"]
    hardList = ["medical.txt", "disease.txt"]

    if diff == 1:
        category = random.choice(easyList)
    elif diff == 2:
        category = random.choice(medList)
    elif diff == 3:
        category = random.choice(hardList)

    with open(f"game_assets/word_database/{category}",'r',encoding='utf-8') as database:
        save_file_content = database.read()
        save_file_content = save_file_content.split(",")
        game_word = random.choice(save_file_content)

    return game_word


def generate_word_from_ai(difficulty):
    """
    hardness should be between 1-2-3
    """
    openai.api_key = "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"
    messages = [ {"role": "system", "content": "create just one random word for a hangman game.and make sure to create different, original word, just write what i want don't write your comment"} ]

    if difficulty == 1:
        message = "make it easy level"
    if difficulty == 2:
        message = "make it hard level"
    if difficulty == 3:
        message = "make it extreme level"

    if message:
        messages.append( 
            {"role": "user", "content": message}, 
        )
        chat = openai.ChatCompletion.create( 
            model="gpt-3.5-turbo", messages=messages 
        )
    reply = chat.choices[0].message.content 

    return str(reply)



save_path =""
def draw_save_screen():
    global page
    global save_path
    global current_game
    font = pygame.font.Font("game_assets/HelpMe.ttf", 56)

    box_size = SCREEN_WIDTH/3 - 200
    box_y = SCREEN_HEIGHT/2 - box_size/2 + SCREEN_HEIGHT/13
    empty_space = (SCREEN_WIDTH - box_size*3)/4 -30
    screen.blit(enterance,(0,0))


    if not save_path == "save_files/save_1.txt":
        BLACK1 = (0,0,0)
    else:
        BLACK1 = (0,50,250)
        
    if not save_path == "save_files/save_2.txt":
        BLACK2 = (0,0,0)
    else:
        BLACK2 = (0,50,250)
    
    if not save_path == "save_files/save_3.txt":
        BLACK3 = (0,0,0)
    else:
        BLACK3= (0,50,250)


    pygame.draw.rect(screen,BLACK1,(SCREEN_WIDTH/3    -box_size -empty_space  ,box_y,box_size,box_size),3,10)
    name1 = font.render(f"  {names[0]}", False, BLACK1)
    screen.blit(name1, (SCREEN_WIDTH/3    -box_size -empty_space,box_y + 30))
    TP1 = font.render(f"  {TPS[0]}", False, BLACK1)
    screen.blit(TP1, (SCREEN_WIDTH/3    -box_size -empty_space,box_y + 200))
    if (is_clicked(SCREEN_WIDTH/3    -box_size -empty_space  ,box_y,box_size,box_size)):
        current_game = load_from_save("save_files/save_1.txt")
        save_path = "save_files/save_1.txt"


    pygame.draw.rect(screen,BLACK2,((SCREEN_WIDTH/3)*2-box_size -empty_space  ,box_y,box_size,box_size),3,10)
    name2 = font.render(f"  {names[1]}", False, BLACK2)
    screen.blit(name2, (SCREEN_WIDTH/3 *2   -box_size -empty_space ,box_y + 30))
    TP2 = font.render(f"  {TPS[1]}", False, BLACK2)
    screen.blit(TP2, (SCREEN_WIDTH/3 *2    -box_size -empty_space,box_y + 200))
    if (is_clicked((SCREEN_WIDTH/3)*2-box_size -empty_space  ,box_y,box_size,box_size)):
        current_game = load_from_save("save_files/save_2.txt")
        save_path = "save_files/save_2.txt"


    pygame.draw.rect(screen,BLACK3,(SCREEN_WIDTH      -box_size -empty_space  ,box_y,box_size,box_size),3,10)
    name3 = font.render(f"  {names[2]}", False, BLACK3)
    screen.blit(name3, (SCREEN_WIDTH  -box_size -empty_space,box_y+ 30))
    TP3 = font.render(f"  {TPS[2]}", False, BLACK3)
    screen.blit(TP3, (SCREEN_WIDTH    -box_size -empty_space,box_y + 200))

    if (is_clicked(SCREEN_WIDTH-box_size -empty_space  ,box_y,box_size,box_size)):
        current_game = load_from_save("save_files/save_3.txt")
        save_path = "save_files/save_3.txt"



    text = font.render("Start the Execution", False, GREEN)
    screen.blit(text, (SCREEN_WIDTH/2 - 320,140))

    if (is_clicked(SCREEN_WIDTH/2 - 320,140,500,100) and ((save_path=="save_files/save_3.txt") or (save_path=="save_files/save_2.txt") or (save_path=="save_files/save_1.txt"))):
        page=2

def draw_player_count():
    global page
    global player_count
    global word_location
    global chosen_diff
    screen.blit(enterance,(0,0))

    RED = (30,24,250)
    kucuk = pygame.font.Font(None, 56)
    box_size = SCREEN_WIDTH/3 - 200
    box_y = SCREEN_HEIGHT/2 - box_size/2
    empty_space = (SCREEN_WIDTH - box_size*3)/4 -30
    BLACK = (0,0,0)


    font_kucuk = pygame.font.Font("game_assets/HelpMe.ttf", 106)
    # choose1 = font_kucuk.render("Choose word's domain", False, BLACK)
    # screen.blit(choose1, (SCREEN_WIDTH-box_size -empty_space*5  ,box_y-empty_space*2))


    font_orta = pygame.font.Font("game_assets/HelpMe.ttf", 30)
    choose1 = font_orta.render("Göktürk Can", False, RED)
    screen.blit(choose1, (SCREEN_WIDTH/4 - 300,SCREEN_HEIGHT - 40))
    choose1 = font_orta.render("Barkin Gümüs", False, RED)
    screen.blit(choose1, (SCREEN_WIDTH/4*2 - 300,SCREEN_HEIGHT - 40))
    choose1 = font_orta.render("Eren Bal", False, RED)
    screen.blit(choose1, (SCREEN_WIDTH/4*3 - 300,SCREEN_HEIGHT - 40 ))
    choose1 = font_orta.render("Eray Sona", False, RED)
    screen.blit(choose1, (SCREEN_WIDTH - 300,SCREEN_HEIGHT - 40))

    RED = (255,20,0)
    font_baslik_buyuk = pygame.font.Font("game_assets/HelpMe.ttf", 76)
    font_baslik_alti = pygame.font.Font("game_assets/HelpMe.ttf", 56)
    choose1 = font_baslik_buyuk.render("Hypatia", False, BLACK)
    screen.blit(choose1,(70,400))
    choose1 = font_baslik_alti.render("A Hangman Game", False, BLACK)
    screen.blit(choose1,(30,600))

    if(is_clicked(30,300,500,600) and (chosen_diff == 1 or chosen_diff == 2 or chosen_diff == 3) and (word_location=="ai" or word_location=="database")):
        page = 1



    if not chosen_diff == 1:
        easy_color = (0,100,0)
    else:
        easy_color = (0,50,250)
        
    if not chosen_diff == 2:
        mid_color = (50,50,0)
    else:
        mid_color = (0,50,250)
    
    if not chosen_diff == 3:
        hard_color = (130,0,0)
    else:
        hard_color= (0,50,250)


    diff_box_size = 100
    font_baslik_alti = pygame.font.Font("game_assets/HelpMe.ttf", 76)

    #difficulty choosing part
    pygame.draw.rect(screen,easy_color,(SCREEN_WIDTH-box_size -empty_space*5  ,box_y*2-empty_space*1.5 ,diff_box_size,diff_box_size),4,10)
    choose1 = font_baslik_alti.render("E", False, easy_color)
    screen.blit(choose1,(SCREEN_WIDTH-box_size -empty_space*5  + 20,box_y*2-empty_space*1.5+ 10))
    if is_clicked(SCREEN_WIDTH-box_size -empty_space*5  ,box_y*2-empty_space*1.5 ,diff_box_size,diff_box_size):
        chosen_diff = 1 


    choose1 = font_baslik_alti.render("M", False, mid_color)
    screen.blit(choose1,(SCREEN_WIDTH-box_size -200 + 15 ,box_y*2-empty_space*1.5+ 10))
    pygame.draw.rect(screen,mid_color,(SCREEN_WIDTH-box_size -200  ,box_y*2-empty_space*1.5 ,diff_box_size,diff_box_size),4,10)
    if is_clicked(SCREEN_WIDTH-box_size -200  ,box_y*2-empty_space*1.5 ,diff_box_size,diff_box_size):
        chosen_diff = 2


    choose1 = font_baslik_alti.render("H", False, hard_color)
    screen.blit(choose1,(SCREEN_WIDTH-box_size +empty_space + 60  + 20,box_y*2-empty_space*1.5 + 10))
    pygame.draw.rect(screen,hard_color,(SCREEN_WIDTH-box_size +empty_space + 60  ,box_y*2-empty_space*1.5 ,diff_box_size,diff_box_size),4,10)
    if is_clicked(SCREEN_WIDTH-box_size +empty_space + 60  ,box_y*2-empty_space*1.5 ,diff_box_size,diff_box_size):
        chosen_diff = 3


    if not word_location=="ai":
        BLACK = (0,0,0)
        choose1 = font_kucuk.render("AI ( beta )", False, BLACK)
    else:
        BLACK = (0,50,250)
        choose1 = font_kucuk.render("AI ( beta )", False, BLACK)


    screen.blit(choose1, (SCREEN_WIDTH-box_size -empty_space*5 + (SCREEN_WIDTH-box_size -empty_space*5)/6 ,box_y-empty_space*2 + (box_size-70)/3 + 10))
    pygame.draw.rect(screen,BLACK,(SCREEN_WIDTH-box_size -empty_space*5  ,box_y-empty_space*2 ,box_size*2,box_size-70),4,10)
    if(is_clicked(SCREEN_WIDTH-box_size -empty_space*5  ,box_y-empty_space*2 ,box_size*2,box_size-70)):
        player_count = "tek"
        word_location = "ai"


    if not word_location == "database":
        BLACK = (0,0,0)
        choose1 = font_kucuk.render("Database", False, BLACK)
    else:
        BLACK = (0,50,250)
        choose1 = font_kucuk.render("Database", False, BLACK)


    pygame.draw.rect(screen,BLACK,(SCREEN_WIDTH-box_size -empty_space*5  ,box_y*2-empty_space+50 ,box_size*2,box_size-70),4,10)
    screen.blit(choose1, (SCREEN_WIDTH-box_size -empty_space*5 +(SCREEN_WIDTH-box_size -empty_space*5)/4.5 - 20 ,box_y*2-empty_space+50+ (box_size-70)/3 + 10 ))
    if(is_clicked(SCREEN_WIDTH-box_size -empty_space*5  ,box_y*2-empty_space+50 ,box_size*2,box_size-70)):
        player_count = "tek"
        word_location = "database"

    




def set_a_game(diff,mod,word_location):
    global game_word
    global life
    global guessed_letters
    global correct_guesses
    global word_letters
    global keyboard_letter_hide
    global win_key
    global taken_hint
    taken_hint = 0
    win_key = 1

    if mod == "tek":
        if word_location == "ai":
            game_word = generate_word_from_ai(diff)
            
        elif word_location == "database":
            game_word = random_word(diff)

    game_word = game_word.upper()
    game_word = game_word.strip()


    keyboard_letter_hide = []

    # word text is -> game_word
    life = 6
    guessed_letters = []
    correct_guesses = []
    word_letters = set(list(game_word))


#we are loading our current game into save files.
def save_the_game(path,save_input):
    save_input = ",".join(save_input)

    with open(path,'w',encoding='utf-8') as save_file:
        save_file.write(save_input)

def load_from_save(path): 
    """returns save file as a list:\n
    index 0 returns save's name \n
    index 1 save's total point \n
    index 2 save's game word if there is one else returns-> 0 \n
    index 3 save's remain health if there is one else returns-> 0 \n"""
    with open(path,'r',encoding='utf-8') as save_file:
        save_file_content = save_file.read()
        save_file_content = save_file_content.split(",")
    return save_file_content


pygame.mixer.music.set_volume(0.3)
#click letter
def clicked_a_letter(letter):
    global game_word
    global life
    global guessed_letters
    global correct_guesses
    global word_letters
    global keyboard_letter_hide


    guessed_letters.append(letter)
    if letter not in word_letters:
        life -=1 # başta altı can vardı beşe düştü ilk resim beşte iken verilecek. oyun sıfır can kalındığında bitecek sıfırda tam resim çıkacak.
    if letter in word_letters:
        correct_guesses.append(letter)

    keyboard_letter_hide.append(letter)
    print(game_word)
    print("clicked: " + letter)

    
def when_win():
    global game_word
    global life
    global guessed_letters
    global correct_guesses
    global word_letters
    global keyboard_letter_hide
    global save_path
    global earniable_point
    global win_key
    global page


    word_letters_copy = word_letters
    for i in word_letters_copy:
        if i ==" ":
            word_letters_copy.remove(" ")
            break

    
    if set(correct_guesses) >= set(word_letters_copy):

        if win_key:
            thank_you.play()
            win_key = 0  
            current_game[0] = str(current_game[0])
            if earniable_point > -1:
                current_game[1] = str(int(current_game[1])+(earniable_point))
            current_game[2] = str(current_game[2]) #
            current_game[3] = str(current_game[3]) #daha bunlar eklenecek
            save_the_game(save_path,current_game)

            keyboard_letter_hide = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


        fontt = pygame.font.Font("game_assets/HelpMe.ttf", 70)
        textTRYAGAIN = fontt.render("CLICK HERE TO PLAY AGAIN", False, GREEN)
        screen.blit(textTRYAGAIN, (500,900))
        if is_clicked(500,900,800,100):
            page = 0

def when_lose():
    global game_word
    global life
    global guessed_letters
    global correct_guesses
    global word_letters
    global keyboard_letter_hide
    global save_path
    global earniable_point
    global win_key
    global page
    # pygame.mixer.music.stop()

    keyboard_letter_hide = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    correct_guesses = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    if win_key:
        dying.play()
        win_key=0

    
    fontt = pygame.font.Font("game_assets/HelpMe.ttf", 70)
    textTRYAGAIN = fontt.render("CLICK HERE TO PLAY AGAIN", False, GREEN)
    screen.blit(textTRYAGAIN, (500,900))
    if is_clicked(500,900,800,100):
        page = 0


def draw_in_game():
    global game_word
    global life
    global guessed_letters
    global correct_guesses
    global word_letters
    global keyboard_letter_hide
    global earniable_point
    global taken_hint

    # if entered_letter != "":
    if life == 6:
        screen.blit(resim6,(0,0))
    if life == 5:
        screen.blit(resim5,(0,0))
    if life == 4:
        screen.blit(resim4,(0,0))
    if life == 3:
        screen.blit(resim3,(0,0))
    if life == 2:
        screen.blit(resim2,(0,0))
    if life == 1:
        screen.blit(resim1,(0,0))
    if life <= 0:
        screen.blit(resim0,(0,0))

    #hint part
    if taken_hint < 2:
        screen.blit(hint_image,(SCREEN_WIDTH-150,10))

        if (is_clicked(SCREEN_WIDTH-150,10,150,150)):
            
            for i in game_word:
                i = random.choice(game_word)
                if i == " ":
                    continue
                if i not in correct_guesses:
                    hint_letter = i
                    break
            
            guessed_letters.append(hint_letter)
            correct_guesses.append(hint_letter)
            keyboard_letter_hide.append(hint_letter)
            taken_hint += 1



    earniable_point = 100 - (6-life)*10 - taken_hint*10

        
    fontt = pygame.font.Font("game_assets/HelpMe.ttf", 60)
    textA = fontt.render(f"Point {earniable_point}", False, BLACK)
    screen.blit(textA, (1000,10))

    when_win()

    if life <= 0:
        when_lose()

    #drawing part
    global page

    letter_row_1_y = 700
    letter_row_1_x_left = 850
    letter_row_1_x = 740
    letter_w = 80
    letter_h = 60

    draw_sub(game_word,correct_guesses)
    font = pygame.font.Font("game_assets/HelpMe.ttf",50)
    if (1):
        
        if ("A" not in keyboard_letter_hide):    
            textA = font.render("A", False, GREEN)
            screen.blit(textA, (letter_row_1_x_left,letter_row_1_y))
            if(is_clicked(letter_row_1_x_left,letter_row_1_y,letter_w,letter_h)):
                clicked_a_letter("A")

        if ("B" not in keyboard_letter_hide):    
            textB = font.render("B", False, GREEN)
            screen.blit(textB, (letter_row_1_x_left + letter_w,letter_row_1_y))
            if(is_clicked(letter_row_1_x_left + letter_w,letter_row_1_y,letter_w,letter_h)):
                clicked_a_letter("B")
                
                

        if ("C" not in keyboard_letter_hide):    
            textC = font.render("C", False, GREEN)
            screen.blit(textC, (letter_row_1_x_left + letter_w*2,letter_row_1_y))
            if(is_clicked(letter_row_1_x_left + letter_w*2,letter_row_1_y,letter_w,letter_h)):
                clicked_a_letter("C")
                
            
        if ("D" not in keyboard_letter_hide):    
            textD = font.render("D", False, GREEN)
            screen.blit(textD, (letter_row_1_x_left + letter_w*3,letter_row_1_y))
            if(is_clicked(letter_row_1_x_left + letter_w*3,letter_row_1_y,letter_w,letter_h)):
                clicked_a_letter("D")
                

        if ("E" not in keyboard_letter_hide):    
            textE = font.render("E", False, GREEN)
            screen.blit(textE, (letter_row_1_x_left + letter_w*4,letter_row_1_y))
            if(is_clicked(letter_row_1_x_left + letter_w*4,letter_row_1_y,letter_w,letter_h)):
                clicked_a_letter("E")
                
            
        if ("F" not in keyboard_letter_hide):    
            textF = font.render("F", False, GREEN)
            screen.blit(textF, (letter_row_1_x_left + letter_w*5,letter_row_1_y))
            if(is_clicked(letter_row_1_x_left + letter_w*5,letter_row_1_y,letter_w,letter_h)):
                clicked_a_letter("F")
                
            
        if ("G" not in keyboard_letter_hide):    
            textG = font.render("G", False, GREEN)
            screen.blit(textG, (letter_row_1_x_left + letter_w*6,letter_row_1_y))
            if(is_clicked(letter_row_1_x_left + letter_w*6,letter_row_1_y,letter_w,letter_h)):
                clicked_a_letter("G")
                pass
            
        if ("H" not in keyboard_letter_hide):    
            textH = font.render("H", False, GREEN)
            screen.blit(textH, (letter_row_1_x_left + letter_w*7,letter_row_1_y))
            if(is_clicked(letter_row_1_x_left + letter_w*7,letter_row_1_y,letter_w,letter_h)):
                clicked_a_letter("H")
                
            
        if ("I" not in keyboard_letter_hide):    
            textI = font.render("I", False, GREEN)
            screen.blit(textI, (letter_row_1_x_left + letter_w*8,letter_row_1_y))
            if(is_clicked(letter_row_1_x_left + letter_w*8,letter_row_1_y,letter_w,letter_h)):
                clicked_a_letter("I")
                
            
        if ("J" not in keyboard_letter_hide):    
            textJ = font.render("J", False, GREEN)
            screen.blit(textJ, (letter_row_1_x_left + letter_w*9,letter_row_1_y))
            if(is_clicked(letter_row_1_x_left + letter_w*9,letter_row_1_y,letter_w,letter_h)):
                clicked_a_letter("J")
                
            
        if ("K" not in keyboard_letter_hide):    
            textK = font.render("K", False, GREEN)
            screen.blit(textK, (letter_row_1_x_left + letter_w*10,letter_row_1_y))
            if(is_clicked(letter_row_1_x_left + letter_w*10,letter_row_1_y,letter_w,letter_h)):
                clicked_a_letter("K")
                


            
        if ("L" not in keyboard_letter_hide):    
            textL = font.render("L", False, GREEN)
            screen.blit(textL, (letter_row_1_x,letter_row_1_y +  letter_h *2))
            if(is_clicked(letter_row_1_x,letter_row_1_y +  letter_h *2,letter_w,letter_h)):
                clicked_a_letter("L")
                
            
        if ("M" not in keyboard_letter_hide):    
            textM = font.render("M", False, GREEN)
            screen.blit(textM, (letter_row_1_x + letter_w,letter_row_1_y +  letter_h *2 ))
            if(is_clicked(letter_row_1_x + letter_w,letter_row_1_y +  letter_h *2 ,letter_w,letter_h)):
                clicked_a_letter("M")
                
            
        if ("N" not in keyboard_letter_hide):    
            textN = font.render("N", False, GREEN)
            screen.blit(textN, (letter_row_1_x + letter_w *2,letter_row_1_y + letter_h *2))
            if(is_clicked(letter_row_1_x + letter_w *2,letter_row_1_y + letter_h *2,letter_w,letter_h)):
                clicked_a_letter("N")
                
            
        if ("O" not in keyboard_letter_hide):    
            textO = font.render("O", False, GREEN)
            screen.blit(textO, (letter_row_1_x + letter_w *3,letter_row_1_y + letter_h *2))
            if(is_clicked(letter_row_1_x + letter_w *3,letter_row_1_y + letter_h *2,letter_w,letter_h)):
                clicked_a_letter("O")
                
            
        if ("P" not in keyboard_letter_hide):    
            textP = font.render("P", False, GREEN)
            screen.blit(textP, (letter_row_1_x + letter_w *4,letter_row_1_y + letter_h *2))
            if(is_clicked(letter_row_1_x + letter_w *4,letter_row_1_y + letter_h *2,letter_w,letter_h)):
                clicked_a_letter("P")
                
            
        if ("Q" not in keyboard_letter_hide):    
            textQ = font.render("Q", False, GREEN)
            screen.blit(textQ, (letter_row_1_x + letter_w *5,letter_row_1_y + letter_h *2))
            if(is_clicked(letter_row_1_x + letter_w *5,letter_row_1_y + letter_h *2,letter_w,letter_h)):
                clicked_a_letter("Q")
                
            
        if ("R" not in keyboard_letter_hide):    
            textR = font.render("R", False, GREEN)
            screen.blit(textR, (letter_row_1_x + letter_w*6,letter_row_1_y + letter_h *2))
            if(is_clicked(letter_row_1_x + letter_w*6,letter_row_1_y + letter_h *2,letter_w,letter_h)):
                clicked_a_letter("R")
                
            
        if ("S" not in keyboard_letter_hide):    
            textS = font.render("S", False, GREEN)
            screen.blit(textS, (letter_row_1_x + letter_w*7,letter_row_1_y + letter_h *2))
            if(is_clicked(letter_row_1_x + letter_w*7,letter_row_1_y + letter_h *2,letter_w,letter_h)):
                clicked_a_letter("S")
                
            
        if ("T" not in keyboard_letter_hide):    
            textT = font.render("T", False, GREEN)
            screen.blit(textT, (letter_row_1_x + letter_w*8,letter_row_1_y + letter_h *2))
            if(is_clicked(letter_row_1_x + letter_w*8,letter_row_1_y + letter_h *2,letter_w,letter_h)):
                clicked_a_letter("T")
                
            
        if ("U" not in keyboard_letter_hide):    
            textU = font.render("U", False, GREEN)
            screen.blit(textU, (letter_row_1_x + letter_w*9,letter_row_1_y + letter_h *2))
            if(is_clicked(letter_row_1_x + letter_w*9,letter_row_1_y + letter_h *2,letter_w,letter_h)):
                clicked_a_letter("U")
                
            
        if ("V" not in keyboard_letter_hide):    
            textV = font.render("V", False, GREEN)
            screen.blit(textV, (letter_row_1_x + letter_w*10,letter_row_1_y + letter_h *2))
            if(is_clicked(letter_row_1_x + letter_w*10,letter_row_1_y + letter_h *2,letter_w,letter_h)):
                clicked_a_letter("V")
                
            
        if ("W" not in keyboard_letter_hide):    
            textW = font.render("W", False, GREEN)
            screen.blit(textW, (letter_row_1_x + letter_w*11,letter_row_1_y + letter_h *2))
            if(is_clicked(letter_row_1_x + letter_w*11,letter_row_1_y + letter_h *2,letter_w,letter_h)):
                clicked_a_letter("W")
                
            
        if ("X" not in keyboard_letter_hide):    
            textX = font.render("X", False, GREEN)
            screen.blit(textX, (letter_row_1_x + letter_w*12,letter_row_1_y + letter_h *2))
            if(is_clicked(letter_row_1_x + letter_w*12,letter_row_1_y + letter_h *2,letter_w,letter_h)):
                clicked_a_letter("X")
                
            
        if ("Y" not in keyboard_letter_hide):    
            textY = font.render("Y", False, GREEN)
            screen.blit(textY, (letter_row_1_x + letter_w*13,letter_row_1_y + letter_h *2))
            if(is_clicked(letter_row_1_x + letter_w*13,letter_row_1_y + letter_h *2,letter_w,letter_h)):
                clicked_a_letter("Y")
                
            
        if ("Z" not in keyboard_letter_hide):    
            textZ = font.render("Z", False, GREEN)
            screen.blit(textZ, (letter_row_1_x + letter_w*14,letter_row_1_y + letter_h *2))
            if(is_clicked(letter_row_1_x + letter_w*14,letter_row_1_y + letter_h *2,letter_w,letter_h)):
                clicked_a_letter("Z")
          
    fontt = pygame.font.Font("game_assets/HelpMe.ttf", 30)
    textA = fontt.render(f"Total Point on this save: {current_game[1]}", False, BLACK)
    screen.blit(textA, (10,10))


def is_clicked(bx_l,by_u,bw,bh):
    global clicked_1
    bx_r = bx_l + bw
    by_b = by_u + bh
    mouse_pos = pygame.mouse.get_pos()
    x = mouse_pos[0]
    y = mouse_pos[1]
    
    if((bx_l< x and bx_r >x) and (by_u<y and by_b > y)):
        if(clicked_1 == 1):
            clicked_1 = 0
            return 1
    else:
        return 0
    

def draw_sub (kelime, correct_guess):
    text = str(kelime)
    sub_y = 360
    sub_x = 800
    if " " in text:
        text_splitted = text.split(" ") # iki kelimelik liste yaptık
        first_word = text_splitted[0] # atamalar yaptık
        second_word = text_splitted[1] # atamalar yaptık



        text1_len = len(first_word)
        text1_size = int(1000/text1_len)
        if text1_size>200:
            text1_size = 200
        font = pygame.font.Font("game_assets/HelpMe.ttf", text1_size)


        space = 0
        for i in first_word:
            if i in correct_guess:
                word_text_1 = font.render(i, False, GREEN)
            else:
                word_text_1 = font.render("_", False, GREEN)

            space_prot = space
            space = space*text1_size
            screen.blit(word_text_1,(sub_x + space,sub_y - text1_size))
            space = space_prot
            space+=1
        space = 0



        text2_len = len(second_word)
        text2_size = int(1000/text2_len)
        if text2_size>200:
            text2_size = 200
        font = pygame.font.Font("game_assets/HelpMe.ttf", text2_size)


        space = 0
        for i in second_word:
            if i in correct_guess:
                word_text_2 = font.render(i, False, GREEN)
            else:
                word_text_2 = font.render("_", False, GREEN)

            space_prot = space
            space = space*text2_size
            screen.blit(word_text_2,(sub_x+ space,sub_y))
            space = space_prot
            space+=1 
        space = 0

            
    else:
        text3_len = len(text)
        text3_size = int(1000/text3_len)
        if text3_size>200:
            text3_size = 200
        font = pygame.font.Font("game_assets/HelpMe.ttf", text3_size)


        space = 0
        for i in text:
            if i in correct_guess:
                word_text_3 = font.render(i, False, GREEN)
            else:
                word_text_3 = font.render("_", False, GREEN)

            space_prot = space
            space = space*text3_size
            screen.blit(word_text_3,(sub_x+ space,sub_y))
            space = space_prot
            space+=1 
        space = 0

    return 0


def main():
    global set_a_game_worked
    global chosen_diff
    set_a_game_worked = False
    chosen_diff = 0
    global page, names, TPS, font, clicked_1
    global word_location
    word_location =""
    clicked_1 = 0
    page = 0
    clock = pygame.time.Clock()
    names = [load_from_save("save_files/save_1.txt")[0],load_from_save("save_files/save_2.txt")[0],load_from_save("save_files/save_3.txt")[0]]
    TPS = [load_from_save("save_files/save_1.txt")[1],load_from_save("save_files/save_2.txt")[1],load_from_save("save_files/save_3.txt")[1]]

    font = pygame.font.Font("game_assets/HelpMe.ttf", 66)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_1 = 1
            elif event.type == pygame.KEYDOWN:

                if(event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_0:
                    page = 0
                if event.key == pygame.K_1:
                    page = 1
                if event.key == pygame.K_2:
                    page = 2

        screen.fill(WHITE)



        if (page == 0):
            pygame.mixer.music.stop()
            draw_player_count()
            set_a_game_worked = False
                
        if (page == 1):
            draw_save_screen()
            
        if (page == 2):
            #funtional part

            if not set_a_game_worked:
                set_a_game(chosen_diff,"tek",word_location)
                set_a_game_worked = True
                pygame.mixer.music.play(-1)

            draw_in_game()
            
        pygame.display.flip()
        clock.tick(1000)

main()