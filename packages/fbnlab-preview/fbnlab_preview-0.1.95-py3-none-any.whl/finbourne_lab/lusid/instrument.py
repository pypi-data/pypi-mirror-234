from finbourne_lab.lusid.base import BaseLusidLab
from finbourne_lab.lusid import LusidExperiment
from lusid import models
import shortuuid


class LusidInstrumentLab(BaseLusidLab):
    """Lab class for lusid instrument endpoint methods.

    """

    def list_instruments_measurement(self, **kwargs) -> LusidExperiment:
        """Make an experiment object for lusid list instruments read performance.

        Keyword Args:
            x_rng (Union[int, List[int]]): the range to sample when getting x-many instruments. Given as a list containing
            two integers or a const int value. Defaults to [1, 5000].

        Returns:
            LusidExperiment: the list instruments experiment object.
        """
        method = self.lusid.instruments_api.list_instruments

        def build(x):
            return lambda: method(limit=x, _preload_content=False)

        rng = kwargs.get('x_rng', [1, 5000])
        return LusidExperiment('list_instruments', build, rng)

    def upsert_instruments_measurement(self, **kwargs) -> LusidExperiment:
        """Make an experiment object for lusid upsert instruments' performance.

        Keyword Args:
            x_rng (Union[int, List[int]]): the range to sample when upserting x-many instruments. Given as a list containing
                 two integers or a const int value. Defaults to [1, 2000].
            n_props: number of properties to create on each instrument
            scope: scope of the instruments, default to f"fbnlab-test-{str(shortuuid.uuid())}"
            id_prefix: prefix for naming the instruments, default to "fbnlab-test-{str(shortuuid.uuid())}"

        Returns:
            LusidExperiment: the upsert instruments experiment object.
        """

        x_rng = kwargs.get('x_rng', [1, 2000])
        n_props = kwargs.get('n_props', None)
        scope = kwargs.get('scope', f"fbnlab-test-{str(shortuuid.uuid())}")
        domain = "Instrument"

        if n_props is not None:
            self.lusid.ensure_property_definitions(n_props, scope, domain)
            properties = self.lusid.build_properties(n_props=n_props, scope=scope, domain=domain)
        else:
            properties = []

        method = self.lusid.instruments_api.upsert_instruments

        def build(x):
            # making sure we create a new instrument every time
            id_prefix = kwargs.get('id_prefix', f"fbnlab-test-{str(shortuuid.uuid())}")
            instruments = {
                f'inst_{i}': models.InstrumentDefinition(
                    name=f'Instrument{i}',
                    identifiers={"ClientInternal": models.InstrumentIdValue(f'{id_prefix}_{i}')},
                    properties=properties
                )
                for i in range(x)
            }

            return lambda: method(request_body=instruments, scope=scope, _preload_content=False)

        return LusidExperiment('upsert_instruments', build, x_rng)
