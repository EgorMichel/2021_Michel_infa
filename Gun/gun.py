from random import randrange as rnd, choice
from random import randint
import tkinter as tk
import math
import time

# print (dir(math))

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)


class ball():
    def __init__(self, vx=0, vy=0, x=40, y=450):
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = vx
        self.vy = vy
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canv.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color
        )
        self.live = 30

    def set_coords(self, dx=0.0, dy=0.0):
        """Устанавливает координаты объекта"""
        canv.coords(
            self.id,
            self.x - self.r + dx,
            self.y - self.r + dy,
            self.x + self.r + dx,
            self.y + self.r + dy
        )

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if self.x + self.vx > 800:
            self.vx = -1 * self.vx
        if self.y + self.vy > 600:
            if self.vy < 5:
                self.vy = 0
                self.y = 600
            self.vy = - 0.5 * self.vy
            self.vx = 0.5 * self.vx
        self.x += self.vx
        self.y += self.vy
        self.vy += 2
        self.set_coords(self.vx, self.vy)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if obj.x - obj.r - self.r < self.x < obj.x + obj.r + self.r and\
                obj.y - obj.r - self.r < self.y < obj.y + obj.r + self.r:
            return True
        else:
            return False


class gun():
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.id = canv.create_line(20, 450, 50, 420, width=7)

    # self.id = canv.create_line(20,450,50,420,width=7) # FIXME: don't know how to set it...

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = ball()
        new_ball.r += 5
        self.an = math.atan((event.y - new_ball.y) / (event.x - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.y - 450) / (event.x - 20))
        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, 20, 450,
                    20 + max(self.f2_power, 20) * math.cos(self.an),
                    450 + max(self.f2_power, 20) * math.sin(self.an)
                    )

    def power_up(self):
        """Реализует увеличение энергии пушки"""
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')


class target():
    # FIXME: don't work!!! How to call this functions when object is created?
    def __init__(self):
        self.points = 0
        self.live = 1
        self.id = canv.create_oval(0, 0, 0, 0)
        # self.id_points = canv.create_text(30, 30, text=self.points, font='28')
        self.new_target()
        self.x = 0
        self.y = 0
        self.r = 0
        self.color = 0

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(2, 50)
        color = self.color = 'red'
        canv.coords(self.id, x - r, y - r, x + r, y + r)
        canv.itemconfig(self.id, fill=color)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        canv.coords(self.id, -10, -10, -10, -10)
        self.points += points
        # canv.itemconfig(self.id_points, text=self.points)

    def move(self):
        """Исполняет движение цели"""
        dx = randint(-10, 10)
        dy = randint(-20, 0)
        canv.coords(self.id,
                    self.x - self.r + dx,
                    self.y - self.r + dy,
                    self.x + self.r + dx,
                    self.y + self.r + dy)


t1 = target()
t2 = target()
screen1 = canv.create_text(400, 300, text='', font='28')
points = canv.create_text(30, 30, text=t1.points + t2.points, font='28')
g1 = gun()
bullet = 0
balls = []


def new_game(event=''):
    """Главная функция игры. Реализует все взаимодействия объектов, реагирует на действия пользователя"""
    global gun, t1, t2, screen1, balls, bullet
    t1.new_target()
    t2.new_target()
    bullet = 0
    balls = []
    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', g1.targetting)

    z = 0.03
    t1.live = 1
    t2.live = 1
    while t1.live or t2.live or balls:
        if t1.live:
            t1.move()
        if t2.live:
            t2.move()
        for b in balls:
            b.move()
            if b.hittest(t1) and t1.live:
                t1.live = 0
                t1.hit()
                canv.itemconfig(points, text=t1.points + t2.points)
            if b.hittest(t2) and t2.live:
                t2.live = 0
                t2.hit()
                canv.itemconfig(points, text=t1.points + t2.points)
            if not t2.live and not t1.live:
                canv.bind('<Button-1>', '')
                canv.bind('<ButtonRelease-1>', '')
                canv.itemconfig(screen1, text='Вы уничтожили цели за ' + str(bullet) + ' выстрел(а)(ов)')
        canv.update()
        time.sleep(0.03)
        g1.targetting()
        g1.power_up()

    canv.itemconfig(screen1, text='')
    canv.delete(gun)
    root.after(750, new_game)


new_game()

mainloop()
