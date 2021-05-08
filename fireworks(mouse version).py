import tkinter as tk
import math
import random

class Line:
    def __init__(self, x1, y1, end_x, end_y, full_length, rate, color):
        self.x1 = x1
        self.x2 = x1
        self.y1 = y1
        self.y2 = y1
        self.end_x = end_x
        self.end_y = end_y
        self.full_length = full_length
        self.color = color
        self.angle = math.atan2(end_x-x1, end_y-y1)
        self.rate = rate
    def line_length(self):
        return math.dist([self.x1, self.y1], [self.x2, self.y2])
    def dist_from_end(self):
        return math.dist([self.x2, self.y2], [self.end_x, self.end_y])
    def start_from_end(self):
        return math.dist([self.x1, self.y1], [self.end_x, self.end_y])
    def update_start(self):
        self.x1+=self.rate * math.sin(self.angle)
        self.y1+=self.rate * math.cos(self.angle)
    def update_end(self):
        self.x2+=self.rate * math.sin(self.angle)
        self.y2+=self.rate * math.cos(self.angle)

class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.title("Fireworks")
        self.canvas = tk.Canvas(self.root, height = 800, width = 800)
        self.iteration = 0
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.mouse_click)
    def mouse_click(self,event):
        self.fireworks(event.x, event.y, random.randint(5,15))
    def fireworks(self, x, y, branches):
        self.iteration+=1
        angle = (0.5 * random.random() + 0.5) * math.pi/2
        lines = []
        rate = random.randint(5, 10)
        length = random.randrange(50//rate * rate, 100//rate * rate + rate, rate)
        full_length = random.randrange(40//rate * rate, (length - rate)//rate * rate + rate, rate)
        for i in range(branches):
            lines.append(Line(x, y, x + length * math.cos(angle), y + length * math.sin(angle), full_length, rate, self.random_color()))
            angle += 2 * math.pi/branches
        self.update_lines(lines, self.iteration)
    def update_lines(self, lines, group):
        self.canvas.delete(f"group{group}")
        count = 0
        for line in lines:
            if line.dist_from_end() >= line.rate:
                line.update_end()
                if line.line_length() >= line.full_length:
                    line.update_start()
            elif line.start_from_end() >= line.rate:
                line.update_start()
            else:
                count+=1
                continue
            f = self.canvas.create_line(line.x1, line.y1, line.x2, line.y2, tags = f"group{group}", fill = line.color, width = 5)
        if count == len(lines):
            self.canvas.delete(f"group{group}")
            return
        self.root.after(100, self.update_lines, lines, group)
    def random_color(self):
        possible = [f"{i}" for i in range(10)] + [chr(65 + i) for i in range(6)]
        return "#"+"".join(random.choices(possible, k = 6))
        

application = Application()
tk.mainloop()
