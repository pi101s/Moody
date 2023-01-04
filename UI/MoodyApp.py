from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

from UI.Screens.ImageAnalysisScreen.ImageAnalysisScreen import ImageAnalysisScreen
from UI.Screens.SongAnalysisScreen.SongAnalysisScreen import SongAnalysisScreen
from UI.Screens.RecommenderScreen.RecommenderScreen import RecommenderScreen

from ModelLibrary.classify import Classifier

Window.clearcolor = (1, 1, 1, 1)


class MainScreen(Screen):
    def analyse_songs(self):
        classifier = Classifier("trained_MER.h5")
        classifier.classify()


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("UI/Screens/MainScreen/main_screen.kv")


class MoodyApp(App):
    def build(self):
        return kv
