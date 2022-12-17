"""Provides an interface for loding entities from and LDTK entity layer 
"""
from typing import Any, Dict
from layer import Layer


class EntityLayer(Layer):
	"""_summary_

	Args:
		Layer (_type_): _description_
	"""
	def __init__(self, data: Dict[str, Any]):
		super(EntityLayer, self).__init__(data)
		self.entity_instances = data["entityInstances"]
		