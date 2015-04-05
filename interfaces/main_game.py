import pygame, sys
from threading import Thread
from entities.individuals import *
from quadtree import Quadtree
from gui import *
from loader import *
from textprint import TextPrint
import interfaces
from interfaces.interface import Interface

class Main_Game(Interface):
    def __init__(self, gui):
        self.projs = []
        self.enemies = []
        self.drops = []
        super().__init__(gui)

    def reset(self):
        self.players = self.gui.players
        for player in self.players:
            player.health = 100
            player.width = 30
            player.height = 30
            player.hitbox = 8
            if player.ID == 0:
                player.x = 400
                player.y = 600
            if player.ID == 1:
                player.x = 800
                player.y = 600

        self.thread = Thread(target=self.loader_init)
        global loaded
        self.loaded = False
        self.loader = Loader()
        self.proj_tree = Quadtree(*self.gui.get_play_area())

    def loader_init(self):
        self.loader.gui = self.gui
        self.loader.players = self.players
        self.loader.enemies = self.enemies
        self.level = "levels/1.lvl"
        self.loader.load(self.level)

    def update(self, screen, dt):
        """
        Runs all the logic for the current frame
        """

        if not self.thread.is_alive() and not self.loaded:
            self.thread.start()
            self.loaded = True

        self.proj_tree.clear()

        for player in enumerate(self.players):
            player[1].update(self.projs, screen, dt)

        for enemy in self.enemies:
            enemy.update(self.projs, self.drops, screen, dt)

        for proj in self.projs:
            proj.update(screen, dt)
            self.proj_tree.insert(proj)

        for enemy in self.enemies:
            for proj in self.proj_tree.get_objects(enemy):
                proj.collide(enemy)

        for player in self.players:
            for proj in self.proj_tree.get_objects(player):
                proj.collide(player)
            for drop in self.drops:
                drop.collide(player)

        if not self.enemies:
            self.loader.set_clear(True)

        if self.players[0].health < 0:
            # self.kill_thread()
            # from interfaces.main_menu import Main_Menu
            # self.gui.remove_interface(self)
            # self.gui.add_interface(Main_Menu(self.gui))
            return (False, "main_menu")

        return True

    def kill_thread(self):
        if self.thread.is_alive():
            self.loader.game_is_running = False

    def draw(self, screen):
        self.gui.draw_game_background()
        self.gui.draw_player_status(self.players)

        for player in enumerate(self.players):
            self.gui.draw_rect(player[1])
            self.gui.draw_hit_box(player[1])

        for enemy in self.enemies:
            self.gui.draw_rect(enemy)

        for proj in self.projs:
            self.gui.draw_rect(proj)

        for drop in self.drops:
            if not drop.used:
                self.gui.draw_rect(drop)
            else:
                drop.update()

        self.proj_tree.draw_tree(screen)

        self.gui.refresh()

interfaces.interface_types["main_game"] = Main_Game