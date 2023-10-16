from pangeamt_nlp.processor.base.normalizer_base import NormalizerBase
from pangeamt_nlp.seg import Seg
import re as _re


class LowercaseNorm(NormalizerBase):
    NAME = "lowercase_norm"

    DESCRIPTION_DECODING = """
    This normalizer is applied to fix specific translation errors related to a client.
    """

    def __init__(self, src_lang: str, tgt_lang: str) -> None:
        if tgt_lang != "es":
            raise ValueError("This normalizer requires a Spanish target.")

        super().__init__(src_lang, tgt_lang)

    def normalize_src(self, txt: str) -> str:
        

        if txt.isupper():

            txt_low = txt.lower()
            txt_list = txt_low.split('.')
            result = '' 

            for sent in txt_list:
                if len(sent) == 0:
                    pass
                elif sent[0] == ' ':
                    result += ' ' + sent[1:].capitalize() + '.'
                else:
                    result += sent.capitalize() + '.'
        
        else:
            result = txt      
        
        return result
    
    def normalize_tgt(self, txt: str) -> str:

        if txt.isupper():
            result = txt.lower()
        else:
            result
        
        return result

    def process_train(self, seg: Seg) -> None:
        pass

    def process_src_decoding(self, seg: Seg) -> None:
        seg.src = self.normalize_src(seg.src)

    def process_tgt_decoding(self, seg: Seg) -> None:
        seg.tgt = self.normalize_tgt(seg.tgt)