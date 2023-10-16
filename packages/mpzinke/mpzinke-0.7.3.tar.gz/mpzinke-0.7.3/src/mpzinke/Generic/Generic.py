#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2023.04.08                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from typing import Any, Optional


class Generic:
	"""
	A class to set runtime generics for classes, methods, and functions.
	Uses:
		- Inheritance:
			```
			class A(Generic):
				...
			
			a_int = A[int]()
			a.int = 5			
			```
		- Static Method:
			```
			class A:
				@Generic
				def static(__args__, ...):  # __args__ is the type of the generic
					...

			A.static[int](...)
			```

		- Function:
			```
			@Generic
			def function(__args__):
				...

			function[int](...)
			```
	"""
	def __class_getitem__(cls, __args__):
		if(not isinstance(__args__, tuple)):
			__args__ = (__args__,)

		assert(all(isinstance(arg, type) for arg in __args__)), "All Generic arguments must be a type"

		name = f"""{cls.__name__}[{", ".join(arg.__name__ for arg in __args__)}]"""
		return type(name, (cls,), {"__args__": __args__})


	def get_or_set__args__(self, new__args__: Optional[Any]=None) -> Optional[Any]:
		__args___name = self.__args__[0].__name__
		if(new__args__ is None):
			return getattr(self, f"_{__args___name}")

		if(not isinstance(new__args__, self.__args__[0])):
			value_type_str = type(new__args__).__name__
			message = f"'__args__Option::{__args___name}' must be of type '{__args___name}' not '{value_type_str}'"
			raise Exception(message);

		setattr(self, f"_{__args___name}", new__args__)


	# ———— WRAPPER ———— #

	def __init__(self, function: callable):
		self._function = function
		self.__annotations__ = {arg: type for arg, type in function.__annotations__.items() if(arg != "__args__")}
		self.__doc__ = function.__doc__
		self.__name__ = function.__name__



	def __call__(self, *args: list, **kwargs: dict):
		return self._function(self.__args__, *args, **kwargs)


	def __getitem__(self, __args__) -> callable:
		if(not isinstance(__args__, tuple)):
			__args__ = (__args__,)

		typed_function = Generic[__args__](self._function)
		if(self.__doc__ is not None):
			typed_function.__doc__ = self.__doc__.format(__args___names=[__arg__.__name__ for __arg__ in __args__])

		return typed_function
