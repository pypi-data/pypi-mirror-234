import abc
import networkx as nx
import numpy as np
import typing as T

from collections import defaultdict
from cvdatasets.annotation.files import AnnotationFiles

### Code is inspired by https://github.com/cabrust/chia

class Hierarchy:
	_force_prediction_targets = False
	_raw_output = False

	def __init__(self, tuples: T.Tuple[int],
		label_transform: T.Optional[T.Callable] = None):

		self._label_transform = label_transform
		self.graph = nx.DiGraph()

		for child, parent in tuples:
			self.graph.add_edge(parent, child)


		self.topo_sorted_orig_labels = list(nx.topological_sort(self.graph))

		self.orig_lab_to_dimension = {
			lab: dimension
				for dimension, lab in enumerate(self.topo_sorted_orig_labels)
		}

		self._create_lookups()

	def _create_lookups(self):
		self.root = next(nx.topological_sort(self.graph))
		self.successors = {}
		self.predecessors = {}
		self.ancestors = {}

		for label in self.topo_sorted_orig_labels:
			self.successors[label] = list(self.graph.successors(label))
			self.predecessors[label] = list(self.graph.predecessors(label))
			self.ancestors[label] = list(nx.ancestors(self.graph, label))

	def label_transform(self, label):
		func = self._label_transform
		if func is None or not callable(func):
			return label
		return func(label)

	@property
	def n_concepts(self):
		""" Returns number of concepts. In this context, a concept is
			an element from a set of hierarchical labels.
		"""
		return len(self.orig_lab_to_dimension)

	def embed_labels(self, labels: np.ndarray, *, xp=np, dtype=np.int32) -> np.ndarray:
		embedding = xp.zeros((len(labels), self.n_concepts), dtype=dtype)

		for i, label in enumerate(labels):
			if isinstance(label, str) and label == "chia::UNCERTAIN":
				# "enable" all labels of this sample
				embedding[i] = 1.0
				continue
			label = self.label_transform(label)

			embedding[i, self.orig_lab_to_dimension[label]] = 1.0
			for ancestor in self.ancestors[label]:
				embedding[i, self.orig_lab_to_dimension[ancestor]] = 1.0

		return embedding

	def loss_mask(self, labels: np.ndarray, *, xp=np, dtype=bool) -> np.ndarray:

		mask = xp.zeros((len(labels), self.n_concepts), dtype=bool)
		for i, label in enumerate(labels):
			label = self.label_transform(label)

			mask[i, self.orig_lab_to_dimension[label]] = True

			for ancestor in self.ancestors[label]:
				mask[i, self.orig_lab_to_dimension[ancestor]] = True
				for successor in self.successors[ancestor]:
					mask[i, self.orig_lab_to_dimension[successor]] = True
					# This should also cover the node itself, but we do it anyway

			if not self._force_prediction_targets:
				# Learn direct successors in order to "stop"
				# prediction at these nodes.
				# If MLNP is active, then this can be ignored.
				# Because we never want to predict
				# inner nodes, we interpret labels at
				# inner nodes as imprecise labels.
				for successor in self.successors[label]:
					mask[i, self.orig_lab_to_dimension[successor]] = True
		return mask


	def deembed_dist(self, embedded_labels, *, single: bool = False):
		if single:
			return [
				self._deembed_single(embedded_label) for embedded_label in embedded_labels
			]

		if self._raw_output:
			# Directly output conditional probabilities
			return [(label, embedded_label[dim]) for label, dim in self.orig_lab_to_dimension.items()]


		# Stage 1 calculates the unconditional probabilities
		uncond_probs = self._uncond_probs(embedded_labels)

		# Stage 2 calculates the joint probability of the synset and "no children"
		joint_probs = self._joint_probs(uncond_probs)

		sorted_dims = (-joint_probs).argsort(axis=1)

		_dim2lab = {dim:lab for lab, dim in self.orig_lab_to_dimension.items()}

		result = []

		for i, dims in enumerate(sorted_dims):
			result.append([(_dim2lab[dim], joint_probs[i, dim]) for dim in dims])

		return result


	def _uncond_probs(self, cond_probs):
		uncond_probs = np.zeros_like(cond_probs, dtype=np.float16)
		_dim = self.orig_lab_to_dimension.get

		for lab in self.topo_sorted_orig_labels:

			unconditional_probability = cond_probs[:, _dim(lab)].copy()

			no_parent_probability = 1.0
			has_parents = False
			for parent in self.predecessors[lab]:
				has_parents = True
				no_parent_probability *= 1.0 - uncond_probs[:, _dim(parent)].copy()

			if has_parents:
				unconditional_probability *= 1.0 - no_parent_probability

			uncond_probs[:, _dim(lab)] = unconditional_probability

		return uncond_probs

	def _joint_probs(self, uncond_probs):
		joint_probs = np.zeros_like(uncond_probs, dtype=np.float16)
		_dim = self.orig_lab_to_dimension.get

		for lab in reversed(self.topo_sorted_orig_labels):
			joint_probability = uncond_probs[:, _dim(lab)]
			no_child_probability = 1.0
			for child in self.successors[lab]:
				no_child_probability *= 1.0 - uncond_probs[:, _dim(child)]

			joint_probs[:, _dim(lab)] = joint_probability * no_child_probability

		return joint_probs

	def _deembed_single(self, embedded_label):
		"""
			code from https://github.com/cabrust/chia/blob/main/chia/components/classifiers/keras_idk_hc.py#L68
		"""
		cond_probs = {
			label: embedded_label[dim] for label, dim in self.orig_lab_to_dimension.items()
		}

		if self._raw_output:
			# Directly output conditional probabilities
			return list(cond_probs.items())


		# Stage 1 calculates the unconditional probabilities
		uncond_probs = self._uncond_probs_single(cond_probs)

		# Stage 2 calculates the joint probability of the synset and "no children"
		joint_probs = self._joint_probs_single(uncond_probs)

		tuples = joint_probs.items()
		sorted_tuples = list(sorted(tuples, key=lambda tup: tup[1], reverse=True))

		# If requested, only output scores for the forced prediction targets
		if self._force_prediction_targets:
			for i, (lab, p) in enumerate(sorted_tuples):
				if lab not in self.prediction_target_uids:
					sorted_tuples[i] = (lab, 0.0)

			total_scores = sum([p for lab, p in sorted_tuples])
			if total_scores > 0:
				sorted_tuples = [
					(lab, p / total_scores) for lab, p in sorted_tuples
				]

		return sorted_tuples

	def _uncond_probs_single(self, cond_probs):
		uncond_probs = {}

		for lab in self.topo_sorted_orig_labels:
			unconditional_probability = cond_probs[lab]

			no_parent_probability = 1.0
			has_parents = False
			for parent in self.predecessors[lab]:
				has_parents = True
				no_parent_probability *= 1.0 - uncond_probs[parent]

			if has_parents:
				unconditional_probability *= 1.0 - no_parent_probability

			uncond_probs[lab] = unconditional_probability

		return uncond_probs

	def _joint_probs_single(self, uncond_probs):
		joint_probs = {}
		for lab in reversed(self.topo_sorted_orig_labels):
			joint_probability = uncond_probs[lab]
			no_child_probability = 1.0
			for child in self.successors[lab]:
				no_child_probability *= 1.0 - uncond_probs[child]

			joint_probs[lab] = joint_probability * no_child_probability

		return joint_probs

class HierarchyMixin(abc.ABC):

	def parse_annotations(self):
		super().parse_annotations()
		self._parse_hierarchy()

	def _parse_hierarchy(self):
		if self.files.hierarchy is None:
			return

		tuples = [entry.split(" ") for entry in self.files.hierarchy]
		tuples = [(int(child), int(parent)) for child, parent in tuples]

		self.hierarchy = Hierarchy(tuples, self.unq2orig)
