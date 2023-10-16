"""Convenient plotting wrapper around matplotlib."""
from __future__ import annotations

__version__ = "1.1.3"

from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

Y = Any
X = Any
Z = Any
XY = Tuple[X, Y]
XYZ = Tuple[X, Y, Z]
NativeArgument = Any
CycledArguments = Optional[Union[NativeArgument, List[Optional[NativeArgument]], Tuple[Optional[NativeArgument]]]]
ClippedArguments = Optional[Union[NativeArgument, List[Optional[NativeArgument]], Tuple[Optional[NativeArgument]]]]


class ChartError(ValueError):
	pass


class Dataset(list):
	"""
	List of data, e.g. [x, y].
	"""

	def __init__(self, items, *, label: Optional[str] = None):
		if not len(items):
			raise ValueError('Empty dataset.')
		super().__init__(items)
		self.label = label

	@property
	def T(self) -> Dataset:
		return Dataset(np.array(self).T, label=self.label)

	def flatten(self) -> Dataset:
		return Dataset([np.array(x).flatten() for x in self], label=self.label)

	@property
	def min_x(self) -> Any:
		if len(self) > 1:
			return np.array(self[0]).min()
		else:
			return 0

	@property
	def max_x(self) -> Any:
		if len(self) > 1:
			return np.array(self[0]).max()
		else:
			return len(self[0]) - 1

	@property
	def min_y(self) -> Any:
		return np.array(self[-1]).min()

	@property
	def max_y(self) -> Any:
		return np.array(self[-1]).max()


class ContextPlotter(tuple):
	def __init__(self, results: Tuple[plt.Figure, plt.Axes, List[plt.Artist]], show: bool, block: Optional[bool]):
		self.block = block
		self.show = show

	def __new__(cls, results, *_, **__):
		return super(ContextPlotter, cls).__new__(cls, results)

	def __enter__(self) -> Tuple[plt.Figure, plt.Axes, List[plt.Artist]]:
		return self

	def __exit__(self, *_):
		if self.show:
			plt.show(block=self.block)


def _cycle(arguments: CycledArguments, index: int) -> Optional[NativeArgument]:
	if arguments is not None:
		if isinstance(arguments, (list, tuple)):
			return arguments[index % len(arguments)]
		else:
			return arguments


def _clip(arguments: CycledArguments, index: int) -> Optional[NativeArgument]:
	if arguments is not None:
		if isinstance(arguments, str) or not isinstance(arguments, (list, tuple)):
			return arguments
		try:
			return tuple(arguments)[index]
		except IndexError:
			pass
		except TypeError:
			return arguments


def _cycle_and_set(dictionary, key, arguments: CycledArguments, index: int) -> None:
	value = _cycle(arguments, index)
	if value is not None:
		dictionary[key] = value
	elif key in dictionary:
		del dictionary[key]


def _clip_and_set(dictionary, key, arguments: CycledArguments, index: int) -> None:
	value = _clip(arguments, index)
	if value is not None:
		dictionary[key] = value
	elif key in dictionary:
		del dictionary[key]


def _convert_to_list(dataset) -> Union[List[Any], Any]:
	if _is_iterable(dataset):
		return [_convert_to_list(x) for x in dataset]
	else:
		return dataset


def _is_iterable(x) -> bool:
	return isinstance(x, Iterable)  # ignore obsolete __getitem__ iteration


def _normalize_datasets(dataset, *, xcolumn: Optional[str] = None, transpose: Optional[bool] = None, flatten: bool = False) -> List[Dataset]:
	if isinstance(dataset, (pd.DataFrame, pd.Series)):  # process pandas
		if xcolumn is not None:  # pairwise columns with xcolumn as different datasets
			if isinstance(dataset, pd.DataFrame) and len(dataset.columns) > 1 and xcolumn in dataset.columns:
				return [ds for dsl in [_normalize_datasets(dataset[[xcolumn, column]], flatten=flatten, transpose=transpose) for column in dataset.columns if column != xcolumn] for ds in dsl]
			else:
				return _normalize_datasets(dataset, flatten=flatten, transpose=transpose)
		else:  # just use all columns as data
			if isinstance(dataset, pd.Series):
				return _normalize_datasets(Dataset(np.array(dataset), label=str(dataset.name) if dataset.name else None), transpose=transpose in [True, None], flatten=flatten)
			else:
				return _normalize_datasets(Dataset(np.array(dataset), label=str(dataset.columns[-1]) if dataset.columns[-1] else None), transpose=transpose in [True, None], flatten=flatten)
	elif not isinstance(dataset, Dataset):  # convert any other data to Dataset
		if not _is_iterable(dataset):  # just scalar
			return _normalize_datasets(Dataset([[dataset]]), transpose=bool(transpose), flatten=flatten)
		else:
			dataset = list(dataset)
			if not len(dataset) or not _is_iterable(dataset[0]):  # one dimension iterable
				return _normalize_datasets(Dataset([list(dataset)]), transpose=bool(transpose), flatten=flatten)
			else:  # multi-dimensions iterable
				return _normalize_datasets(Dataset([list(data) for data in dataset]), transpose=bool(transpose), flatten=flatten)
	else:  # process Dataset
		if transpose is True:
			dataset = dataset.T
		if flatten:
			dataset = dataset.flatten()
		return [dataset]


def plot(*datasets: Union[XY, Y, XYZ],
		 # common parameters
		 kind='plot',
		 flatten: bool = False,
		 transpose: Optional[bool] = None,
		 xcolumn: Optional[str] = 'x',
		 guess_label: bool = True,
		 show: bool = True,
		 block: Optional[bool] = None,
		 context: bool = False,
		 # plotter explict parameters
		 label: ClippedArguments = None,
		 color: CycledArguments = None,
		 marker: ClippedArguments = None,
		 linestyle: ClippedArguments = None,
		 linewidth: ClippedArguments = None,
		 markersize: ClippedArguments = None,
		 # figure and axes parameters
		 legend: Optional[bool] = None,
		 legend_kwargs: Optional[Dict[str, Any]] = None,
		 title: Optional[str] = None,
		 title_kwargs: Optional[Dict[str, Any]] = None,
		 xlabel: Optional[str] = None,
		 xlabel_kwargs: Optional[Dict[str, Any]] = None,
		 ylabel: Optional[str] = None,
		 ylabel_kwargs: Optional[Dict[str, Any]] = None,
		 limit: Union[Tuple[Any, Any, Any, Any], bool] = True,
		 figsize: Tuple[float, float] = (10, 8),
		 dpi: float = 100,
		 subplots_kwargs: Optional[Dict[str, Any]] = None,
		 grid: Optional[bool] = False,
		 grid_kwargs: Optional[Dict[str, Any]] = None,
		 theme='seaborn-v0_8-deep',
		 # plotter rest parameters
		 **plotter_kwargs
		 ) -> Tuple[plt.Figure, plt.Axes, List[plt.Artist]]:
	if not datasets:
		raise ChartError('No data to plot.')
	plt.style.use(theme)
	fig, ax = plt.subplots(figsize=figsize, dpi=dpi, **(subplots_kwargs or {}))
	try:
		plotter = getattr(ax, kind)
	except AttributeError:
		raise ChartError(f'Plot kind {kind} could not be found.')
	normalized_datasets = [ds for dataset in datasets for ds in _normalize_datasets(dataset, xcolumn=xcolumn, transpose=transpose, flatten=flatten)]
	diagrams = []
	labels_count = 0
	dimensions = len(normalized_datasets[0])
	x_minimum = normalized_datasets[0].min_x
	x_maximum = normalized_datasets[0].max_x
	y_minimum = normalized_datasets[0].min_y
	y_maximum = normalized_datasets[0].max_y
	for i, dataset in enumerate(normalized_datasets):
		params = plotter_kwargs.copy()
		for k, v in plotter_kwargs.items():
			_clip_and_set(params, k, v, i)
		_clip_and_set(params, 'label', label, i)
		_cycle_and_set(params, 'color', color, i)
		_clip_and_set(params, 'marker', marker, i)
		_clip_and_set(params, 'linestyle', linestyle, i)
		_clip_and_set(params, 'linewidth', linewidth, i)
		_clip_and_set(params, 'markersize', markersize, i)
		if guess_label and 'label' not in params and dataset.label:
			params['label'] = dataset.label
		if 'label' in params:
			labels_count += 1
		diagrams.append(plotter(*dataset, **params))
		if i:
			dimensions = max(dimensions, len(dataset))
			x_minimum = min(x_minimum, dataset.min_x)
			x_maximum = max(x_maximum, dataset.max_x)
			y_minimum = min(y_minimum, dataset.min_y)
			y_maximum = max(y_maximum, dataset.max_y)
	diagrams = [diagram for container in diagrams for diagram in container]
	if legend is True or legend is None and len(diagrams) > 1 and labels_count:
		ax.legend(**(legend_kwargs or {}))
	if xlabel is not None:
		ax.set_xlabel(xlabel, **(xlabel_kwargs or {}))
	if ylabel is not None:
		ax.set_ylabel(ylabel, **(ylabel_kwargs or {}))
	if title is not None:
		ax.set_title(title, **(title_kwargs or {}))
	if limit is True and dimensions == 2:
		ax.set_xlim(left=x_minimum, right=x_maximum)
		ax.set_ylim(bottom=y_minimum, top=y_maximum)
	elif not isinstance(limit, bool):
		ax.set_xlim(left=limit[0], right=limit[1])
		ax.set_ylim(bottom=limit[2], top=limit[3])
	if grid in [True, None]:
		plt.grid(visible=grid, **(grid_kwargs or {}))
	ctx = ContextPlotter(results=(fig, ax, diagrams), show=show, block=block)
	if context:
		return ctx
	with ctx as results:
		return results


def cplot(*args, **kwargs) -> Tuple[plt.Figure, plt.Axes, List[plt.Artist]]:
	return plot(*args, **{'context': True, **kwargs})
