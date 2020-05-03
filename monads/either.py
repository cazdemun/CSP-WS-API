from pymonad import Right, Left, Either

Right.fold = lambda self, f, g: g(self.value)

Left.fold = lambda self, f, g: f(self.value)

Right = Right
Left = Left
Either = Either