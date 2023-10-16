from ....datalog.expression_processing import extract_logic_atoms
from ....expression_walker import IdentityWalker, PatternWalker, add_match
from ....expressions import Symbol
from ....logic import Implication

RESAMPLE = Symbol("RESAMPLE")


class TranslateResamplingMixin(PatternWalker):
    @add_match(
        Implication,
        lambda e: any(
            a.functor is RESAMPLE for a in extract_logic_atoms(e.antecedent)
        )
    )
    def translate_resampling(self, expression):
        resample_set = 
