#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2021.09.14                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION: Created to sepparate the crazy logic between repeating and single occurance threads. The flow of this #
#    class is Sleep -> Action, where as the repeating class is (Action -> Sleep) <- REPEAT.                            #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from . import BaseThread


class DelayThread(BaseThread):
	def __init__(self, name: str, *, action: callable, time: callable):
		BaseThread.__init__(self, name, action=action, time=time)


	def __call__(self) -> None:
		try:  # make it safe!!!
			self.sleep(self.time())
			if(self._is_active):
				self.action()

		except Exception as error:
			print("ERROR")
			print(error)
