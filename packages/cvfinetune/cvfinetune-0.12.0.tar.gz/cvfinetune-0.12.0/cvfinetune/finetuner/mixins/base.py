import abc
import inspect


class BaseMixin(abc.ABC):

	def _after_init_check(self):
		pass

	@classmethod
	def extract_kwargs(cls, opts) -> dict:

		kwargs = {}

		for klass in cls.mro():
			sig = inspect.signature(klass.__init__)
			for attr, param in sig.parameters.items():
				if param.kind is not inspect.Parameter.KEYWORD_ONLY:
					continue

				if param.name in kwargs:
					continue

				if hasattr(opts, param.name):
					value = getattr(opts, param.name)
					kwargs[param.name] = value
		return kwargs


if __name__ == '__main__':

	from collections import namedtuple
	class Foo(BaseMixin):

		@classmethod
		def extract_kwargs(cls, opts) -> dict:
			return super().extract_kwargs(opts)

		def __init__(self, *args, foo, bar=0, **kwargs):
			super().__init__(*args, **kwargs)
			self.foo = foo
			self.bar = bar


	class Bar(BaseMixin):
		@classmethod
		def extract_kwargs(cls, opts) -> dict:
			return super().extract_kwargs(opts)

		def __init__(self, *args, bar2=-1, **kwargs):
			super().__init__(*args, **kwargs)
			self.bar2 = bar2


	class Final(Bar, Foo):


		def __init__(self, *args, beef=-1, **kwargs):
			super().__init__(*args, **kwargs)
			self.beef = beef

		def __repr__(self):
			return str(self.__dict__)


	_Opts = namedtuple("_Opts", "foo foo2 bar bar2 beef1")

	opts = _Opts(1,2,3, -4, "hat")
	kwargs = Final.extract_kwargs(opts)

	print(opts, Final(**kwargs))
