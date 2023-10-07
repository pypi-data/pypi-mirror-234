#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2023.07.31                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


import asyncio
from flask import request
from inspect import iscoroutinefunction
import re
from typing import Dict, Optional, TypeVar


ArgMapping = Dict[type, any]
HTTPMethod = str
HTTPCallback = callable
HTTPMethodMapping = Dict[HTTPMethod, HTTPCallback]
URL = str


Route = TypeVar("Route")
Server = TypeVar("Server")


class Route:
	def __init__(self, url: URL, server: Optional[Server]=None, *, additional_args: Optional[ArgMapping]=None,
		authorization: Optional[callable]=None, **method_mappings: HTTPMethodMapping
	):
		self._additional_args: Dict[type, any] = additional_args or {}
		self._authorization: Optional[callable] = authorization
		self._methods: HTTPMethodMapping = {method.upper(): callback for method, callback in method_mappings.items()}
		self._server: Optional[Server] = server
		self._url: URL = url

		self._validate_HTTP_methods()
		self._validate_method_callbacks()


	def __call__(self, **kwargs: dict) -> str:
		"""
		SUMMARY: 
		PARAMS:  
		DETAILS: 
		RETURNS: 
		"""
		if(self._authorization is not None):
			self._authorization(request)

		# Add additional args to method call.
		for type, value in self._additional_args.items():
			if(type in (params := self._methods[request.method].__annotations__).values()):
				kwargs[list(params.keys())[list(params.values()).index(type)]] = value

		callback = self._methods[request.method]
		if(iscoroutinefunction(callback)):
			return asyncio.run(callback(**kwargs))

		return callback(**kwargs)


	def __iter__(self) -> Dict[str, str]:
		url = self._url
		yield from {
			f"{method} {url}": (function.__doc__ or "").strip() for method, function in self._methods.items()
		}.items()


	# ————————————————————————————————————————— ROUTES::CALLBACK  VALIDATION ————————————————————————————————————————— #

	@staticmethod
	def compare_function_params(func1: Dict[str, type], func2: Dict[str, type]) -> Dict[str, type]:
		"""
		SUMMARY: Compares the args and types of two functions.
		PARAMS:  Takes the args and types of function 1 and the args and types of function 2.
		DETAILS: Iterates through the functions' parameters. Checks whether each of the parameters names and types matches.
		RETURNS: A dictionary of {<param_name>: [<function1_type>, <function2_type>]} for mismatched parameters.
		"""
		mismatched_function_params = {}
		for param in set(list(func1) + list(func2)):
			if(param != "return" and (param not in func1 or param not in func2 or func1[param] != func2[param])):
				mismatched_function_params[param] = [func[param] if(param in func) else None for func in [func1, func2]]

		return mismatched_function_params


	def params_for_url(self) -> Dict[str, type]:
		"""
		SUMMARY: Determines the parameters and types for a URL.
		PARAMS:  Takes the URL to determine the parameters for.
		DETAILS: Determines the parameters and their types with a RegEx. Orders the parameters and types into a
		         dictionary.
		RETURNS: A dictionary of {<parameter>: <type>}.
		"""
		params = re.findall(r"<(int|string):([_a-zA-Z][_a-zA-Z0-9]*)>", self._url)
		return {param: {"int": int, "string": str}[type] for type, param in params}


	def _format_exception_string_for_bad_params(self, http_method: str, unknown_params: Dict[str, list[type]]) -> str:
		"""
		SUMMARY: 
		PARAMS:  
		DETAILS: 
		RETURNS: 
		"""
		callback_name = self._methods[http_method].__name__
		callback_params = self._methods[http_method].__annotations__

		message_strings = [f"""'{http_method}' callback '{callback_name}' is in compatable with URL '{self._url}'."""]
		if(len(params_missing_from_callback := [param for param in unknown_params if(param not in callback_params)])):
			message_strings.append(f"""'{"', '".join(params_missing_from_callback)}' missing from '{callback_name}'.""")

		url_params: Dict[str, type] = self.params_for_url()
		if(len(params_missing_from_url := [param for param in unknown_params if(param not in url_params)])):
			message_strings.append(f"""Params '{"', '".join(params_missing_from_url)}' missing from '{self._url}'.""")

		mismatched_types = [param for param in unknown_params if(param in url_params and param in callback_params)]
		if(len(mismatched_types_str := "', '".join(mismatched_types))):
			string = f"""'{http_method}' callback is missing arg(s) '{mismatched_types_str}' for URL '{self._url}'."""
			message_strings.append(string)

		return " ".join(message_strings)


	def _validate_HTTP_methods(self) -> None:
		"""
		SUMMARY: 
		PARAMS:  
		DETAILS: 
		RETURNS: 
		"""
		http_methods = ["CONNECT", "DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT", "TRACE"]

		# Ensure all methods are correct HTTP methods.
		bad_methods: list[str] = [method for method in self._methods if(method.upper() not in http_methods)]
		if((bad_methods_string := "', '".join(bad_methods)) != ""):
			raise Exception(f"Method(s) '{bad_methods_string}' not an HTTP method for URL '{self._url}'")

		if(len(self._methods) == 0):  # Ensure at least 1 method supplied
			raise Exception(f"At least one HTTP method must be supplied for URL '{self._url}")


	def _validate_method_callbacks(self) -> None:
		"""
		SUMMARY: 
		PARAMS:  
		DETAILS: 
		RETURNS: 
		"""
		# Ensure all set methods have a callback (as opposed to a different type being passed)
		for http_method, callback in self._methods.items():
			if(not hasattr(callback, '__call__')):
				url = self._url
				message = f"""'{http_method}' arg must be of type 'callable', not '{type(callback)}' for URL '{url}'"""
				raise Exception(message)

		callbacks = list(self._methods.values())
		if(any(iscoroutinefunction(callback) != iscoroutinefunction(callbacks[0]) for callback in callbacks)):
			raise Exception("Callbacks must be either all synchronous or all asynchronous.")

		# Ensure all set methods have a callback (as opposed to a different type being passed)
		for http_method, callback in self._methods.items():
			if(not callable(callback)):
				url = self._url
				message = f"""'{http_method}' arg must be of type 'callable', not '{type(callback)}' for URL '{url}'"""
				raise Exception(message)

		url_params = self.params_for_url()
		for http_method, callback in self._methods.items():
			additional_arg_types: list[list[type]] = list(self._additional_args.keys())

			callback_params = callback.__annotations__
			unknown_params: Dict[str, list[Optional[type]]] = Route.compare_function_params(callback_params, url_params)

			# If any url param type is not None or callback param is not in additional arg types
			if(any(types[1] is not None for types in unknown_params.values())
			or any(types[0] not in additional_arg_types for types in unknown_params.values())):
				message = self._format_exception_string_for_bad_params(http_method, unknown_params)
				raise Exception(message)
