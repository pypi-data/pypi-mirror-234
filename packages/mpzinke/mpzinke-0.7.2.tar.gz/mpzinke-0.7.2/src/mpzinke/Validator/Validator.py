
import mpzinke
import types
import typing
from typing import Any, Dict, Optional


class Validator:
	def __init__(self, argument_types: Dict[str, Any], descendent_class: Optional[type]=None):
		"""
		
		"""
		# Must be `type(self)` because an inheritted object returns true for `isinstance(self, Validator)`
		assert(type(self) is not Validator), "'Validator' must be inheritted"
		assert(issubclass(type(self), Validator)), f"'{type(self).__name__}' must be of type 'Validator'"

		descendent_class = descendent_class or Validator.class_with_Validator_parent(type(self))
		parameter_types = descendent_class.__init__.__annotations__
		Validator.check_for_missing_arguments(argument_types, parameter_types)
		Validator.check_argument_types(argument_types, parameter_types)


	@staticmethod
	def check_for_missing_arguments(argument_types: dict, parameter_types: dict) -> None:
		"""
		SUMMARY: Check if any parameter is not supplied in the arguments values.
		RAISES: KeyError
		"""
		missing_arguments_strings: list[str] = [] 
		for name, type in parameter_types.items():
			if(name not in argument_types):
				missing_arguments_strings.append(f"'{name}' of type '{type}'")

		if(len(missing_arguments_strings) != 0):
			raise KeyError(f"""Missing key(s) for {", ".join(missing_arguments_strings)}""")


	@staticmethod
	def check_argument_types(argument_types: dict, parameter_types: dict) -> None:
		"""
		Check if any parameter is not of proper type.
		RAISES: ValueError.
		"""
		failed_param_strings: list[str] = []
		for name, required_type in parameter_types.items():
			if(not Validator.check_argument_type(argument_types[name], required_type)):
				failed_argument_type = type(argument_types.get(name)).__name__
				failed_string = f"'{name}' must be of type '{required_type.__name__}' not '{failed_argument_type}'"
				failed_param_strings.append(failed_string)

		if(len(failed_param_strings) != 0):
			raise ValueError(", ".join(failed_param_strings))


	@staticmethod
	def check_argument_type(value: Any, needed_type: type) -> bool:
		"""
		https://stackoverflow.com/questions/49171189/whats-the-correct-way-to-check-if-an-object-is-a-typing-generic
		"""
		if((origin := typing.get_origin(needed_type)) is types.UnionType or origin is typing.Union):
			return Validator.union_types_match(value, needed_type)

		elif(isinstance(needed_type, (mpzinke.Generic, types.GenericAlias, typing._GenericAlias))):
			return Validator.generic_types_match(value, needed_type)

		# int
		return isinstance(value, needed_type)


	@staticmethod
	def generic_types_match(argument: Any, needed_type: type) -> bool:
		"""
		EG. `list[<__args__[0]>] or Dict[<__args__[0]>, <__args__[1]]`
		"""
		if(not isinstance(argument, typing.get_origin(needed_type))):  # if(not isinstance({1: ['1', '1'], ...}, dict))
			return False

		# If the number of types for the generic is one, iterate through those types
		if(len((generics_args := needed_type.__args__)) == 1):
			return all(Validator.check_argument_type(subargument, generics_args[0]) for subargument in argument)

		# {1: ['1', '1'], 2: ['2', '2'], 3: ['3', '3']}
		for argument_children in (argument.items() if(isinstance(argument, dict)) else argument):
			# (1, int), (['1', '1'], list[str])
			for grandchild, type in zip(argument_children, generics_args):
				if(not Validator.check_argument_type(grandchild, type)):
					return False

		return True


	@staticmethod
	def union_types_match(value: Any, needed_type: type) -> bool:
		"""
		EG. `int|str``
		"""
		return any(Validator.check_argument_type(value, unioned_type) for unioned_type in needed_type.__args__)


	@staticmethod
	def class_with_Validator_parent(class_type: type) -> type:
		for base in class_type.__bases__:
			if(base is not None):
				if(base == Validator):
					return class_type

				if((ancestor := Validator.class_with_Validator_parent(base)) is not None):
					return ancestor

		return None
