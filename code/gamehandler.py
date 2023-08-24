import pygame

from level import Level
from save import Save
from ingame_menu import IngameMenu, Ingame_settings, HowToPlay, Leaderboard
from menuenums import menuenums
from settings import Settings


class GameHandler():
    def __init__(self, user, what_to_load):

        self.user = user
        if self.user is not None:
            self.save = Save(what_to_load, self.user.characters)
            self.leaderboard = Leaderboard(self.open_leaderboard)
        else:
            self.save = Save(what_to_load, None)
        self.game_paused = False
        self.load_data = self.save.load_data()
        self.level = Level(self.load_data)
        self.ingame_menu = IngameMenu(
            self.pause_game, self.save_game, self.open_ingame_settings)

        self.is_settings_menu_open = False
        self.Ingame_settings = Ingame_settings(self.open_ingame_settings)

        self.how_to_play = HowToPlay(self.open_how_to_play)

        self.is_talent_menu_open = False
        self.talent_menu_open_time = None
        self.key_press_cooldown = 300

        self.is_how_to_play_open = False
        self.how_to_play_open_time = None
        self.is_how_to_play_openable = True

        self.is_leaderboard_open = False
        self.leaderboard_open_time = None
        self.is_leaderboard_openable = True

    def run(self):
        self.cooldown()
        if self.game_paused:
            if self.is_settings_menu_open:
                self.Ingame_settings.render()
                self.Ingame_settings.update()
            else:
                self.ingame_menu.display()
        else:
            self.input()
            self.level.run()
            if self.is_how_to_play_open:
                self.how_to_play.display()
            if self.is_leaderboard_open and self.user is not None:
                self.leaderboard.display()

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.pause_game()

        if keys[pygame.K_n]:
            if not self.is_talent_menu_open:
                self.level.toggle_menu(menuenums.TALENTS)
                self.talent_menu_open_time = pygame.time.get_ticks()
                self.is_talent_menu_open = True

        if keys[pygame.K_F1] and self.is_how_to_play_openable:
            self.open_how_to_play()

            self.level.player.progress_quest('open_control_panel')

        if keys[pygame.K_F2] and self.is_leaderboard_openable and self.user is not None:
            self.open_leaderboard()

    def open_leaderboard(self):
        self.is_leaderboard_openable = False
        self.is_leaderboard_open = not self.is_leaderboard_open
        self.leaderboard.update_top_players()
        self.leaderboard_open_time = pygame.time.get_ticks()

    def open_how_to_play(self):
        self.is_how_to_play_openable = False
        self.is_how_to_play_open = not self.is_how_to_play_open
        self.how_to_play_open_time = pygame.time.get_ticks()

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if self.is_talent_menu_open:
            if current_time - self.talent_menu_open_time > self.key_press_cooldown:
                self.is_talent_menu_open = False

        if not self.is_how_to_play_openable:
            if current_time - self.how_to_play_open_time > self.key_press_cooldown:
                self.is_how_to_play_openable = True

        if not self.is_leaderboard_openable and self.user is not None:
            if current_time - self.leaderboard_open_time > self.key_press_cooldown:
                self.is_leaderboard_openable = True

    def save_game(self):

        if self.level.player.current_quest != len(Settings.quest_data):

            print("game saved")

            self.level.player.progress_quest('save_game')

            if self.user is not None and self.load_data[0] == 'online':
                self.save.create_online_save(
                    self.level.player, self.save.load_data()[1]['id'], self.user.id, self.level.level)

            elif self.user is not None and self.load_data[0] == 'new':

                characters = self.user.load_characters()

                for character in characters:
                    print(character.player_name)

                    if character.player_name == self.level.player.name:
                        self.save.create_online_save(
                            self.level.player, character.id, self.user.id)

                        return

                self.save.create_new_online_save(
                    self.level.player, self.user.id, self.level.level)

            else:
                self.save.create_save(self.level.player)

    def pause_game(self):
        self.game_paused = not self.game_paused

    def open_ingame_settings(self):
        self.is_settings_menu_open = not self.is_settings_menu_open
