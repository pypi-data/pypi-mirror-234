from __future__ import annotations

from finbourne_lab import Shopper
from typing import Dict, Callable, List, Iterable

from finbourne_lab.common.experiment import Experiment


class BaseLab:
    """Base class for standard measurement sets. Standard measurement sets are the set of standard measurements that
    characterise the performance of a given Finbourne application.

    Standard measurement sets should have a set of methods ending with _measurement for each individual standard
    measurement which output a Convener instance or a tuple of Convener instances.

    Each measurement method must be documented with a docstring.
    """

    def get_measurements(self) -> Dict[str, Callable]:
        """Get a dictionary of all the measurement methods of this class.

        Returns:
            Dict[str, Callable]: the dictionary of measurement names and methods.

        """
        return {m: getattr(self, m) for m in dir(self) if m.endswith('_measurement')}

    def list_experiments(self, **kwargs) -> List[Experiment]:
        """List all the conveners to run in this standard measurement set.

        Returns:
            List[Convener]: the list of conveners.

        """

        def _flatten(it):
            for x in it:
                if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
                    yield from _flatten(x)
                else:
                    yield x

        return list(_flatten(map(lambda x: x(**kwargs), self.get_measurements().values())))

    def shopper(self, **kwargs) -> Shopper:
        """Create a shopper object for each experiment in this lab object.

        Args:
            **kwargs: kwargs to pass down to list_experiments which will be passed to each *_measurement method.

        Returns:
            Shopper: the encapsulating shopper instance.
        """
        return Shopper(*self.list_experiments(**kwargs))

    def teardown(self):
        """Teardown step. Is a no-op in the base class.

        """
        pass

    def setup(self):
        """Setup step. Is a no-op in the base class.

        """
        pass

    def __enter__(self):
        self.setup()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.teardown()
