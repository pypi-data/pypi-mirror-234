#!/usr/bin/env python
if __name__ != '__main__': raise Exception("Do not import me!")

import logging
import multiprocessing as mp
import os
import shutil

from cvargparse import Arg
from cvargparse import BaseParser
from functools import partial
from pathlib import Path
from tqdm.auto import tqdm

from cvdatasets.utils.image import read_image

def resize(name, *, source: Path, dest: Path, size: int, fit_short: bool = False):
	src = source / name
	dst = dest / name

	im  = read_image(src)
	if im.mode == "RGBA":
		im = im.convert("RGB")
	w, h = im.size

	if fit_short:
		if w > h:
			W, H = (int(size * w / h), size)
		else:
			W, H = (size, int(size * h / w))

	else:
		if w > h:
			W, H = (size, int(size * h / w))
		else:
			W, H = (int(size * w / h), size)

	dst.parent.mkdir(parents=True, exist_ok=True)
	im.resize((W, H)).save(dst)


def main(args):

	source = Path(args.source)
	destination = Path(args.destination).resolve()
	assert source.exists(), \
		f"\"{source.resolve()}\" does not exist!"

	if destination.exists():
		if args.remove_existing:
			shutil.rmtree(destination)
		else:
			raise ValueError(f"\"{destination}\" exists, but --remove_existsing was not set!")

	logging.info(f"resized images will be written to \"{destination}\"")
	destination.mkdir(parents=True, exist_ok=True)

	images = []
	for root, dirs, files in os.walk(source):
		for file in files:
			if Path(file).suffix.lower() not in args.extensions:
				continue

			images.append(Path(root, file).relative_to(source))


	logging.info(f"Found {len(images)} images in \"{source}\"")

	work = partial(resize,
		source=source,
		dest=destination,
		size=args.size,
		fit_short=args.fit_short,
		)

	if args.n_jobs >= 1:
		with mp.Pool(args.n_jobs) as pool:
			runner = pool.imap(work, images)
			for i in tqdm(runner, total=len(images)):
				pass
	else:
		for imname in tqdm(images):
			work(imname)



parser = BaseParser([
	Arg("source"),

	Arg("destination"),

	Arg.int("--n_jobs", "-j", default=-1,
		help="number of concurrent resize processes"),

	Arg("--extensions", "-ext", nargs="+", default=[".jpg", ".jpeg", ".png"],
		help="file extensions to processs"),

	Arg.int("--size", "-s", default=1000,
		help="size in pixels"),

	Arg.flag("--fit_short",
		help="resize to the given size the short size or the long size (default)."),

	Arg.flag("--remove_existing",
		help="remove existing images."),
])

main(parser.parse_args())
