import pygame
import os
from state import State
from settings import * 

class ScoreEntry:
    def __init__(self, name, score):
        self.name = str(name).strip()[:Score.MAX_NAME_LENGTH] if name else Score.DEFAULT_NAME
        try:
            self.score = int(score)
        except (ValueError, TypeError):
            self.score = 0 
    def __lt__(self, other):
        if not isinstance(other, ScoreEntry):
            return NotImplemented 
        if self.score == other.score:
            return self.name.lower() < other.name.lower() 
        return self.score > other.score 

class Score(State):
    SCORE_FILE      = os.path.join("data", "score", "score.txt") 
    MAX_SCORES      = 6
    DEFAULT_NAME    = "---" 
    MAX_NAME_LENGTH = 10 
    _font_title     = None
    _font_list      = None
    _font_input     = None
    def __init__(self):
        super().__init__()
        self.font_title = None
        self.font_list  = None
        self.font_input = None
        self._load_assets() 
        self.high_scores        = [] 
        self.player_score_entry = None 
        self.is_editing         = False 
        self.input_name         = "" 
        self.cursor_timer       = 0.0
        self.show_cursor        = True
        self._ensure_score_file_exists()
        self._load_scores() 
    def _load_assets(self):
         if Score._font_title is None:
             try:
                 Score._font_title = pygame.font.Font("data/font/fsex2p00_public.ttf", 40)
                 Score._font_list  = pygame.font.Font("data/font/fsex2p00_public.ttf", 30)
                 Score._font_input = pygame.font.Font("data/font/fsex2p00_public.ttf", 15)
                 print("Score fonts loaded.")
             except pygame.error as e:
                 print(f"Error loading font for Score state: {e}")
                 Score._font_title = pygame.font.Font(None, 50)
                 Score._font_list  = pygame.font.Font(None, 35)
                 Score._font_input = pygame.font.Font(None, 40) 
         self.font_title = Score._font_title
         self.font_list  = Score._font_list
         self.font_input = Score._font_input
    def _ensure_score_file_exists(self):
        score_dir = os.path.dirname(self.SCORE_FILE)
        try:
            if not os.path.exists(score_dir):
                os.makedirs(score_dir, exist_ok=True)
                print(f"Created score directory: {score_dir}")
            if not os.path.exists(self.SCORE_FILE):
                print(f"Score file '{self.SCORE_FILE}' not found, creating default.")
                with open(self.SCORE_FILE, 'w', encoding='utf-8') as f:
                    for i in range(self.MAX_SCORES):
                        default_score = max(0, (self.MAX_SCORES - i -1) * 10)
                        f.write(f"{self.DEFAULT_NAME} {default_score}\n")
        except IOError as e:
            print(f"Error creating default score file '{self.SCORE_FILE}': {e}")
        except Exception as e:
             print(f"Unexpected error ensuring score file exists: {e}")
    def _load_scores(self):
        self.high_scores = []
        try:
            with open(self.SCORE_FILE, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            for line_num, line in enumerate(lines):
                 parts = line.strip().split(maxsplit=1)
                 name  = self.DEFAULT_NAME
                 score = 0
                 if len(parts) == 2:
                     name = parts[0]
                     try:
                         score = int(parts[1])
                     except ValueError:
                         print(f"Warning: Invalid score format on line {line_num+1}: '{line.strip()}'")
                         score = 0 
                 elif len(parts) == 1:
                      name = parts[0] if parts[0] else self.DEFAULT_NAME
                      print(f"Warning: Missing score on line {line_num+1}: '{line.strip()}' - Assuming 0.")
                 else:
                      continue 
                 self.high_scores.append(ScoreEntry(name, score))
            self.high_scores.sort()
            if len(self.high_scores) > self.MAX_SCORES:
                self.high_scores = self.high_scores[:self.MAX_SCORES]
            else:
                while len(self.high_scores) < self.MAX_SCORES:
                    self.high_scores.append(ScoreEntry(self.DEFAULT_NAME, 0))
            print(f"Loaded {len(self.high_scores)} scores.")

        except FileNotFoundError:
            print(f"Score file '{self.SCORE_FILE}' not found during load. Will try to create.")
            self._ensure_score_file_exists()
            if os.path.exists(self.SCORE_FILE):
                 self._load_scores() 
            else: 
                 print("Failed to create/load score file. Using defaults.")
                 self.high_scores = [ScoreEntry(self.DEFAULT_NAME, 0) for _ in range(self.MAX_SCORES)]
                 self.high_scores.sort() 
        except IOError as e:
            print(f"Error reading score file '{self.SCORE_FILE}': {e}")
            self.high_scores = [ScoreEntry(self.DEFAULT_NAME, 0) for _ in range(self.MAX_SCORES)]
            self.high_scores.sort()
        except Exception as e:
             print(f"Unexpected error loading scores: {e}")
             self.high_scores = [ScoreEntry(self.DEFAULT_NAME, 0) for _ in range(self.MAX_SCORES)]
             self.high_scores.sort()
    def _save_scores(self):
        self.high_scores.sort()
        self.high_scores = self.high_scores[:self.MAX_SCORES]
        try:
            os.makedirs(os.path.dirname(self.SCORE_FILE), exist_ok=True)
            with open(self.SCORE_FILE, 'w', encoding='utf-8') as f:
                for entry in self.high_scores:
                    f.write(f"{entry.name.strip()} {entry.score}\n")
            print(f"Scores saved to '{self.SCORE_FILE}'.")
        except IOError as e:
            print(f"Error writing score file '{self.SCORE_FILE}': {e}")
        except Exception as e:
             print(f"Unexpected error saving scores: {e}")
    def handle_enter(self, parameters):
        print("Entering Score State")
        edit_mode_requested     = parameters.get('edit', False)
        player_total_score      = parameters.get('total_score', 0)
        self.is_editing         = False
        self.input_name         = ""
        self.player_score_entry = None 
        self._load_scores()
        if edit_mode_requested:
            print(f"Checking if score {player_total_score} qualifies...")
            qualifies = False
            if len(self.high_scores) < self.MAX_SCORES:
                qualifies = True
            elif self.high_scores: 
                 if player_total_score > self.high_scores[-1].score:
                      qualifies = True
            if qualifies:
                print("Score qualifies! Entering edit mode.")
                self.is_editing = True
                self.player_score_entry = ScoreEntry("", player_total_score) 
                temp_list = self.high_scores + [self.player_score_entry]
                temp_list.sort()
                self.high_scores = temp_list[:self.MAX_SCORES]
                found = False
                for entry in self.high_scores:
                    if entry is self.player_score_entry:
                        found = True
                        break
                if not found:
                    self.player_score_entry = next((entry for entry in self.high_scores if entry.score == player_total_score and entry.name == ""), None)
                if self.player_score_entry:
                    self.input_name   = "" 
                    self.cursor_timer = 0.0 
                    self.show_cursor  = True
                else:
                    print("Error: Could not find the inserted player score entry. Disabling edit.")
                    self.is_editing = False
                    self._load_scores() 
            else:
                print("Score did not qualify for the high score list.")
                self.is_editing = False 
    def handle_exit(self):
        print("Exiting Score State")
        if self.player_score_entry and not self.is_editing:
             print("Saving scores on exit after editing.")
             self._save_scores()
        self.player_score_entry = None
    def handle_event(self, event):
        if self.is_editing and self.player_score_entry:
            if event.type == pygame.KEYDOWN:
                if event.key == K_RETURN:
                    print("Finished editing name.")
                    final_name = self.input_name.strip()
                    if not final_name: final_name = self.DEFAULT_NAME
                    self.player_score_entry.name = final_name[:self.MAX_NAME_LENGTH]
                    self.is_editing = False
                    self.player_score_entry = None 
                    self._save_scores()
                elif event.key == K_BACKSPACE:
                    self.input_name = self.input_name[:-1]
                    self.player_score_entry.name = self.input_name
                    self.cursor_timer = 0.0 
                    self.show_cursor = True
                elif event.key == K_PAUSE_QUIT: 
                     print("Canceled score entry.")
                     self.is_editing         = False
                     self.player_score_entry = None
                     self._load_scores()    
                     if self.engine: self.engine.change_state('menu') 
                else:
                    if len(self.input_name) < self.MAX_NAME_LENGTH:
                        char = event.unicode
                        if char.isalnum() or char in [' ', '_', '-']: 
                             self.input_name             += char
                             self.player_score_entry.name = self.input_name 
                             self.cursor_timer            = 0.0
                             self.show_cursor             = True
        else:
            if event.type == pygame.KEYDOWN:
                if event.key in (K_PAUSE_QUIT, K_RETURN, K_BACKSPACE):
                    if self.engine: self.engine.change_state('menu')
    def handle_update(self, delta_time):
        if self.is_editing and self.player_score_entry:
            self.cursor_timer += delta_time
            blink_interval = 0.5 # seconds
            if self.cursor_timer >= blink_interval:
                self.cursor_timer %= blink_interval 
                self.show_cursor = not self.show_cursor
    def handle_erase(self, screen):
        screen.fill(BLACK)
    def handle_draw(self, screen):
        title_y = 50
        if self.font_title:
            try:
                title_surf = self.font_title.render("High Scores", True, RED)
                title_rect = title_surf.get_rect(center=(SCREEN_WIDTH / 2, title_y))
                screen.blit(title_surf, title_rect)
            except Exception as e: print(f"Error drawing score title: {e}")
        list_start_y = title_y + 70
        line_height  = 40
        rank_x       = SCREEN_WIDTH * 0.15 
        name_x       = rank_x + 60         
        score_x      = SCREEN_WIDTH * 0.85 
        if self.font_list:
            for i, entry in enumerate(self.high_scores):
                current_y = list_start_y + i * line_height
                is_player_entry = self.is_editing and entry is self.player_score_entry
                color = YELLOW if is_player_entry else WHITE
                try:
                    rank_text = f"{i+1}."
                    rank_surf = self.font_list.render(rank_text, True, color)
                    rank_rect = rank_surf.get_rect(topleft=(rank_x, current_y))
                    screen.blit(rank_surf, rank_rect)
                    display_name = self.input_name if is_player_entry else entry.name
                    name_surf = self.font_list.render(display_name, True, color)
                    name_rect = name_surf.get_rect(topleft=(name_x, current_y))
                    screen.blit(name_surf, name_rect)
                    score_surf = self.font_list.render(str(entry.score), True, color)
                    score_rect = score_surf.get_rect(topright=(score_x, current_y)) 
                    screen.blit(score_surf, score_rect)
                    if is_player_entry and self.show_cursor:
                        try:
                            name_width = self.font_list.size(display_name)[0]
                            cursor_x   = name_rect.left + name_width + 2 
                            cursor_y1  = name_rect.top
                            cursor_y2  = name_rect.bottom
                            pygame.draw.line(screen, color, (cursor_x, cursor_y1), (cursor_x, cursor_y2), 2)
                        except Exception as e: print(f"Error drawing cursor: {e}")
                except Exception as e:
                     print(f"Error drawing score line {i+1}: {e}")
        prompt_y = list_start_y + self.MAX_SCORES * line_height + 40 
        if self.is_editing and self.player_score_entry and self.font_input:
             prompt_text = "Enter your name, press Enter when done"
             prompt_color = YELLOW
        elif not self.is_editing: 
             prompt_text = "Press Enter or Escape to return to Menu"
             prompt_color = WHITE
        else:
             prompt_text = "" 
        if prompt_text and self.font_input:
            try:
                prompt_surf = self.font_input.render(prompt_text, True, prompt_color)
                prompt_rect = prompt_surf.get_rect(center=(SCREEN_WIDTH / 2, prompt_y))
                screen.blit(prompt_surf, prompt_rect)
            except Exception as e: print(f"Error drawing score prompt: {e}")