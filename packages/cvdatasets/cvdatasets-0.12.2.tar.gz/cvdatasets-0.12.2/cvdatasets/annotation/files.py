# import abc
import os
import logging
import simplejson as json
import warnings

from pathlib import Path
from typing import Any
from typing import Callable
from typing import Dict
from typing import List

class AnnotationFiles(object):

	@staticmethod
	def _parse_opts(fpath_and_opts):
		if isinstance(fpath_and_opts, (list, tuple)):
			fpath, *opts = fpath_and_opts
		else:
			fpath, opts = fpath_and_opts, []

		return fpath, opts

	def __init__(self, *files, root=".", load_strict=False, **named_files):
		super(AnnotationFiles, self).__init__()
		self.load_strict = load_strict
		self.root = Path(root)
		self._files = []

		self.load_files(*files, **named_files)

	def load_files(self, *files, **named_files):
		for fpath in files:
			fpath, opts = self._parse_opts(fpath)
			self.add_file_content(fpath, *opts)

		for attr, fpath in named_files.items():
			fpath, opts = self._parse_opts(fpath)
			self.add_file_content(fpath, *opts, attr=attr)

	def _path(self, fname) -> Path:
		return self.root / fname

	def _json_reader(self, f) -> Dict[str, Any]:
		return json.load(f)

	def _line_reader(self, f) -> List[str]:
		return [line.strip() for line in f if line.strip()]

	def get_reader(self, fpath) -> Callable:
		return {
			".json": self._json_reader,
			".txt": self._line_reader,
		}.get(Path(fpath).suffix.lower())

	def read_file(self, fpath):
		with open(fpath) as f:
			reader = self.get_reader(fpath)

			if reader is None:
				raise NotImplementedError(f"Don't know how to read \"{fpath.name}\"!")

			elif not callable(reader):
				raise ValueError(f"The reader for \"{fpath.name}\" was not callable!")

			return reader(f)

	def read_directory(self, folder_path):
		logging.info(f"Loading files from folder \"{folder_path}\" ...")

		_content = [
			Path(path) / file
				for path, folders, files in os.walk(folder_path)
					for file in files
		]

		logging.info(f"Found {len(_content):,d} files in \"{folder_path}\"")
		return _content
		# setattr(self, attr, _content)

	def add_file_content(self, fpath, optional=False, *args, attr=None, **kwargs):
		fpath = self._path(fpath)
		attr = attr or fpath.stem.replace(".", "_")
		content = None

		if fpath.is_file():
			content = self.read_file(fpath)

		elif fpath.is_dir():
			content = self.read_directory(fpath)

		elif not optional:
			msg = f"File \"{fpath}\" was not found!"
			if self.load_strict:
				raise AssertionError(msg)
			else:
				warnings.warn(msg)
		else:
			logging.debug(f"\"{fpath}\" was not found and was ignored, since it was marked as optional")

		self._files.append(attr)
		setattr(self, attr, content)

if __name__ == '__main__':
	files = AnnotationFiles(
		"foo.txt",
		tad="bar.txt",
		bar=("fobar.txt", True),
		root="/Bla",
		# load_strict=True,
	)
	print(files.foo, files.tad, files.bar)
