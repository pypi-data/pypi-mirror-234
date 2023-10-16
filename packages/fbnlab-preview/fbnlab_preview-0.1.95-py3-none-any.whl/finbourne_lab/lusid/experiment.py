from finbourne_lab.common.sdk_experiment import SdkExperiment


class LusidExperiment(SdkExperiment):

    def __init__(self, name, build_fn, *ranges, **kwargs):
        kwargs['application'] = 'lusid'
        super().__init__(name, build_fn, *ranges, **kwargs)
