from novelai_api.BanList import BanList
from novelai_api.BiasGroup import BiasGroup
from novelai_api.GlobalSettings import GlobalSettings
from novelai_api.Preset import Model, Preset
from typing import List, Optional


class GenerationSettings:
    model: Model = None
    preset: Preset = None
    global_settings: GlobalSettings = None
    bad_words: Optional[BanList] = None
    bias_groups: List[BiasGroup] = []
    module: Optional[str] = None
    stop_sequences: Optional[List] = None
    repetition_penalty_whitelist: Optional[List] = None

    def __init__(
            self,
            model: Model = Model.Kayra,
            preset: Preset = None,
            global_settings: GlobalSettings = GlobalSettings(num_logprobs=GlobalSettings.NO_LOGPROBS,
                                                             bias_dinkus_asterism=True,
                                                             rep_pen_whitelist=True, generate_until_sentence=True),
            bad_words: Optional[BanList] = None,
            bias_groups: Optional[List[BiasGroup]] = None,
            module: Optional[str] = "vanilla",
            stop_sequences: Optional[List] = None,
            repetition_penalty_whitelist: Optional[List] = None,
    ):
        self.model = model
        self.preset = preset
        self.global_settings = global_settings
        self.bad_words = bad_words
        if bias_groups is None:
            self.bias_groups: List[BiasGroup] = []
        else:
            self.bias_groups = bias_groups
        self.module = module
        self.stop_sequences = stop_sequences
        self.repetition_penalty_whitelist = repetition_penalty_whitelist
