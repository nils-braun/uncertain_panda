import pandas

from dask import array as da


class Function:
    @property
    def key(self):
        raise NotImplementedError

    def __call__(self, df, *args, **kwargs):
        raise NotImplementedError

    def call_on_dask_array(self, random_draws, *args, **kwargs):
        return da.apply_along_axis(arr=random_draws, func1d=lambda x: self(x, *args, **kwargs), axis=1)


class LambdaFunction(Function):
    def __init__(self, key, lambda_function):
        self._key = key
        self._lambda_function = lambda_function

    @property
    def key(self):
        return self._key

    def __call__(self, df, *args, **kwargs):
        return self._lambda_function(df, *args, **kwargs)


class PandasFunction(Function):
    def __init__(self, key):
        self._key = key

    def __call__(self, df, *args, **kwargs):
        return getattr(df, self._key)(*args, **kwargs)

    def call_on_dask_array(self, random_draws, *args, **kwargs):
        try:
            return getattr(da, self._key)(random_draws, *args, axis=1, **kwargs)
        except AttributeError:
            raise AttributeError(f"Using {self._key} is not supported in dask mode. Please switch to pandas instead!")


class NumpyFunction(Function):
    def __init__(self, numpy_name):
        self._numpy_name = numpy_name

    @property
    def key(self):
        return self._numpy_name

    def __call__(self, df, *args, **kwargs):
        return df.agg(self._numpy_name, *args, **kwargs)

    def call_on_dask_array(self, random_draws, *args, **kwargs):
        # For numpy functions we can cheat a bit here, as using the internal dask function is much faster
        return getattr(da, self._numpy_name)(random_draws, *args, axis=1, **kwargs)


class NonNanNumpyFunction(NumpyFunction):
    def call_on_dask_array(self, random_draws, *args, **kwargs):
        # for numpy functions we can cheat a bit here, as using the internal dask function is much faster
        return getattr(da, "nan" + self._numpy_name)(random_draws, *args, axis=1, **kwargs)
