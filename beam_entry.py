class BeamEntry:
    "information about one single beam at specific time-step"

    def __init__(self):
        self.prTotal = 0  # blank and non-blank
        self.prNonBlank = 0  # non-blank
        self.prBlank = 0  # blank
        self.prText = 1  # LM score
        self.lmApplied = False  # flag if LM was already applied to this beam
        self.labeling = ()  # beam-labeling
