#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2022.04.14                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from datetime import datetime, timedelta
import requests
from typing import Optional
import warnings
from warnings import warn as Warn


class DownloadIterator:
	"""
	SUMMARY: Used to wrap the response's iter_content iterator.
	DETAILS: Has iter and next functions to initialize and support iteration, wrapping the iter_content method.
	NOTES:   Based on:
	           https://towardsdatascience.com/how-to-loop-through-your-own-objects-in-python-1609c81e11ff
	           https://gist.github.com/zmwangx/0dcbdbe6f67f3540dd73e777ef1b2a89
	"""

	def __init__(self, response, *, timeout: Optional[int]=None, callback: Optional[callable]=None,
		chunk_size: Optional[int]=1024, suppress_warning: bool=False
	):
		"""
		SUMMARY: Contructs the DownloadIterator object.
		PARAMS:  Takes the HTTP reponse object, the timeout amount, OPTIONALLY: a callback function to run each
		         iteration of the loop, the chunk_size to collect from the response.
		"""
		self._callback: callable = callback  # Function pointer called in case you want to add something
		self._downloaded: int = 0  # The amount of byte download
		self._end: Optional[datetime] = None  # The timestamp of the max allotted time to download data (from iteration start)
		self._chunk_size: int = chunk_size  # The disired chunk size to download at once
		self._response: requests.Response = response  # The response for which the content download iterator is called
		self._response_content_iterator: iter = None  # The iter_content object
		self._suppress_warning: bool = suppress_warning
		self._timeout: Optional[int] = timeout  # The stored timeout amount

		warnings.formatwarning = DownloadIterator.warning_message


	def __iter__(self):
		"""
		SUMMARY: Initializes the iteration process for the DownloadIterator.
		DETAILS: Sets the timeout timestamp from the moment iteration initialization is called. Initialize iteration of
		         response's content.
		RETURNS: It's as the object being iterated over.
		"""
		if(self._timeout):
			self._end = datetime.now() + timedelta(seconds=self._timeout)
		elif(not self._suppress_warning):
			Warn(f"No time out specified. This can cause the download to run indefinitely.")

		self._response_content_iterator = iter(self._response.iter_content(chunk_size=self._chunk_size))
		return self


	def __next__(self) -> bytes:
		"""
		SUMMARY: Gets the next value for the iteration & checks whether the download elapsed time has timed out.
		DETAILS: Checks whether the download elapsed time has timed out. Calls optional callback function to do any
		         additional processes. Increments the downloaded amount.
		RETURNS: The next data downloaded.
		THROWS:  Timeout Exception if too much time has elapsed.
		"""
		if(self._timeout and self._end <= datetime.now()):
			error_message = f"Download for response has exceeded time amount of {self._timeout}." \
			  + f" Downloaded {self._downloaded} bytes"
			raise TimeoutError(error_message)

		if(self._callback is not None):  # Allow other optional actions
			self._callback(self)

		self._downloaded += self._chunk_size
		return next(self._response_content_iterator)


	@staticmethod
	def warning_message(message, *_: list) -> str:
		"""
		SUMMARY: Used to override warning format & return only the warning message.
		"""
		return str(message)+"\n"
