class Function:
    @property
    def key(self):
        raise NotImplementedError

    def __call__(self, df, *args, **kwargs):
        raise NotImplementedError

    def call_on_dask_array(self, random_draws, *args, **kwargs):
        from dask import array as da
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

    @property
    def key(self):
        return self._key

    def __call__(self, df, *args, **kwargs):
        return getattr(df, self._key)(*args, **kwargs)

    def call_on_dask_array(self, random_draws, *args, **kwargs):
        try:
            from dask import array as da
            return getattr(da, self._key)(random_draws, *args, axis=1, **kwargs)
        except AttributeError:
            raise AttributeError(f"Using {self._key} is not supported in dask mode. Please switch to pandas instead!")


class NonNanNumpyFunction(PandasFunction):
    def call_on_dask_array(self, random_draws, *args, **kwargs):
        try:
            # for numpy functions we can cheat a bit here, as using the internal dask function is much faster
            from dask import array as da
            return getattr(da, "nan" + self._key)(random_draws, *args, axis=1, **kwargs)
        except AttributeError:
            raise AttributeError(f"Using {self._key} is not supported in dask mode. Please switch to pandas instead!")
