#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"


########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2020.11.04                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE: Consider moving to multiprocessing::Process instead.                                                       #
#                                                                                                                      #
########################################################################################################################


from typing import Optional


from . import BaseThread


class LoopingThread(BaseThread):
	def __init__(self, name: str, *, action: callable, time: callable):
		BaseThread.__init__(self, name, action=action, time=time)


	def __call__(self):
		try:  # make it safe!!!
			while(self._is_active):
				self.action();
				self.sleep(self.time());

		except Exception as error:
			print(error)
