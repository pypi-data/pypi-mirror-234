from __future__ import annotations

import typing as T

class BoundingBox(T.NamedTuple):

	x: int = 0
	y: int = 0
	w: int = 0
	h: int = 0

	@property
	def x0(self) -> int:
		return self.x

	@property
	def x1(self) -> int:
		return self.x + self.w

	@property
	def y0(self) -> int:
		return self.y

	@property
	def y1(self) -> int:
		return self.y + self.h

	@property
	def center(self) -> T.Tuple[int, int]:
		return self.x + self.w // 2, self.y + self.h // 2

	def squared(self, *, smaller_size: bool = False) -> BoundingBox:
		cx, cy = self.center
		func = min if smaller_size else max

		size = func(self.w, self.h)
		x0 = max(cx - size // 2, 0)
		y0 = max(cy - size // 2, 0)

		return BoundingBox(x0, y0, size, size)

	@classmethod
	def new(cls, *, resize=None, **kwargs) -> BoundingBox:
		# parameters that should be passed once
		once = [
			("x", "x0"),
			("y", "y0"),
			("w", "x1"),
			("h", "y1"),
		]

		for p1, p2 in once:
			assert (p1 in kwargs and p2 not in kwargs) \
				or (p2 in kwargs and p1 not in kwargs), \
				f"please pass only one of these arguments: {p1}, {p2}"

		x = kwargs.get("x", kwargs["x0"])
		y = kwargs.get("y", kwargs["y0"])

		if "x1" in kwargs:
			w = kwargs["x1"] - x

		if "y1" in kwargs:
			h = kwargs["y1"] - y
		coords = x, y, w, h

		coords = cls.resize(*coords, resize=resize)
		coords = map(int, coords)
		return cls(*coords)

	@classmethod
	def resize(cls, *coords, resize=None):
		if resize is None or not isinstance(resize, (tuple, int, float)):
			return coords

		# check if the coordinates are relative
		_check = lambda value: 0 <= value < 1
		if not all(map(_check, coords)):
			return coords


		if isinstance(resize, tuple):
			W, H = resize
		else: # int
			W = H = resize

		x, y, w, h = coords

		return x*W, y*H, w*W, h*H


	def get(self, *attrs) -> T.Tuple:
		return tuple(getattr(self, attr) for attr in attrs)


	def __repr__(self) -> str:
		return f"<BoundingBox [0x{id(self):x}]: (({self.x0}, {self.y0}), ({self.x1}, {self.y1})) [{self.w}x{self.h} px]>"



if __name__ == '__main__':

	print(BoundingBox.new(x0=0., x1=0.999, y0=0., y1=0.999))
	print(BoundingBox.new(x0=1, x1=200, y0=10, y1=90))
	print(BoundingBox.new(x0=.1, x1=.5, y0=0, y1=.3, resize=1000))
	print(BoundingBox.new(x0=.25, x1=.5, y0=0, y1=.1, resize=(160, 90)))
	print(BoundingBox.new(x0=.25, x1=.5, y0=0, y1=.1, resize=(1600, 900)))
