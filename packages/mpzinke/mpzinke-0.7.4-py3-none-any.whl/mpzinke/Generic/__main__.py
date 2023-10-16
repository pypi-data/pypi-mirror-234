

from . import Generic


def test():
	class Test(Generic):
		def __init__(self, a, b):
			print(f"Test[{self.__args__[0].__name__}]{a, b}")


		def my_method(self, a, b):
			print(f"""called `Test[{self.__args__[0].__name__}]::my_method({a}, {b})`""")


		@Generic
		def my_staticmethod(__args__, a, b):
			print(f"""called `Test::my_staticmethod[{__args__[0].__name__}]({a}, {b})`""")


	test = Test[int](1, 2)
	test.my_method(1, 2)
	Test.my_staticmethod[int](1, 2)


	@Generic
	def my_function(__args__, *args, **kwargs):
		args_string = ", ".join([str(arg) for arg in args])
		kwargs_string = ",".join([f"{key}={value}" for key, value in kwargs.items()])
		print(f"""called `my_function[{__args__[0].__name__}]({args_string}, {kwargs_string})`""")

	my_function_str = my_function[str]
	my_function_int = my_function[int]

	my_function_str("a", "b", key="word")
	my_function_int("a", "b", key="word")


if(__name__ == "__main__"):
	test()
