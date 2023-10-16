import abc
import logging
import typing as T

from cvdatasets.utils import new_iterator

from cvfinetune.finetuner.mixins.base import BaseMixin

class _IteratorMixin(BaseMixin):

    def __init__(self,
                 *args,
                 batch_size: int = 32,
                 n_jobs: int = 1,
                 use_threads: bool = False,
                 **kwargs):
        super().__init__(*args, **kwargs)

        self._batch_size = batch_size
        self._n_jobs = n_jobs
        self._use_threads = use_threads


    def new_iterator(self, ds, **kwargs):
        if hasattr(ds, "new_iterator"):
            return ds.new_iterator(**kwargs)
        else:
            return new_iterator(ds, **kwargs)

    def init_iterators(self):
        """Creates training and validation iterators from training and validation datasets"""

        self._check_attr("val_data")
        self._check_attr("train_data")

        kwargs = dict(
            n_jobs=self._n_jobs,
            batch_size=self._batch_size,
            use_threads=self._use_threads,
        )

        self.train_iter, _ = self.new_iterator(self.train_data,
                                               **kwargs)

        self.val_iter, _ = self.new_iterator(self.val_data,
                                             repeat=False, shuffle=False,
                                             **kwargs)
