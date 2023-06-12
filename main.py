import kivy 
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (ListProperty,NumericProperty)
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label 
 
kivy.require('1.7.0')


class PainelJogoDaVelha(BoxLayout):
        pass

class BotaoEntrada(Button):
    coordenada = ListProperty([0, 0])

class GradeJogoDaVelha(GridLayout):
    status = ListProperty([0, 0, 0,0, 0, 0,0, 0, 0])
    jogadorAtual = NumericProperty(1)
    pontosO = NumericProperty(0)
    pontosX = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        super(GradeJogoDaVelha, self).__init__(*args, **kwargs)
        
        for linha in range(3):
            for coluna in range(3):
                botaoE = BotaoEntrada(coordenada=(linha,coluna))
                botaoE.bind(on_release=self.botao_pressionado)
                self.add_widget(botaoE)

    def botao_pressionado(self, botao):
        jogador = {1: 'O', -1: 'X'}
        cores = {1: (1, 0, 0, 1), -1: (0, 1, 0, 1)}

        linha, coluna = botao.coordenada  

        indiceStatus = 3*linha + coluna
        
        posicaoJaOcupada = self.status[indiceStatus]

        if not posicaoJaOcupada:
            self.status[indiceStatus] = self.jogadorAtual
            botao.text = {1: 'O', -1: 'X'}[self.jogadorAtual]
            botao.background_color = cores[self.jogadorAtual]
            self.jogadorAtual *= -1
            
    def reset(self, *args):
        self.status = [0 for _ in range(9)]
        for child in self.children:
            child.text = ''
            child.background_color = (1, 1, 1, 1)
            self.jogadorAtual = 1

    def reset2(self, *args):
        self.pontosX = 0
        self.pontosO = 0

        self.status = [0 for _ in range(9)]
        for child in self.children:
            child.text = ''
            child.background_color = (1, 1, 1, 1)
            self.jogadorAtual = 1
        

    def on_status(self, instance, new_value):
        status = new_value
        sums = [sum(status[0:3]),  # linhas
                sum(status[3:6]),
                sum(status[6:9]),
                sum(status[0::3]),  # colunas
                sum(status[1::3]),
                sum(status[2::3]),
                sum(status[::4]),  # diagonais
                sum(status[2:-2:2])]

        resultado = None
        if -3 in sums:
                self.pontosX = self.pontosX + 1
                if self.pontosX == 4:
                        resultado = 'X vai ganhar!'
                else:
                        if self.pontosX == 5:
                                resultado = 'X é o vencedor, Parabéns!!!'
                                App.get_running_app().stop()
                        else:
                                resultado = 'O X ganhou!'
                        
                            
        elif 3 in sums:
                self.pontosO = self.pontosO+ 1
                if self.pontosO == 4:
                        resultado = '0 vai ganhar!'
                else:
                        if self.pontosO == 5:
                                resultado = 'O é o vencedor, Parabéns!!!'
                                App.get_running_app().stop()
                        else:
                                resultado = 'O 0 ganhou!'
                

        elif 0 not in self.status:
            resultado = 'Empatado, velha ...!'

        if resultado:
            popup = ModalView(size_hint=(0.75, 0.5))
            labelResultado = Label(text=resultado,font_size=50)
            popup.add_widget(labelResultado)
            popup.bind(on_dismiss=self.reset)
            popup.open()


class JogoDaVelhaApp(App):
    def build(self):
        return  PainelJogoDaVelha()


if __name__ == '__main__':
    JogoDaVelhaApp().run()

