import os
from enum import Enum
from functools import lru_cache
from typing import Type, List, cast

import blingfire
import tiktoken
from collections_extended import RangeMap
from pydantic import BaseModel, Field
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document, Sentence


class ChunkingUnit(str, Enum):
    character = "character"
    token = "token"


class TokenModel(str, Enum):
    wbd = "wbd"
    bert_base_tok = "bert_base_tok"
    bert_base_cased_tok = "bert_base_cased_tok"
    bert_chinese = "bert_chinese"
    bert_multi_cased = "bert_multi_cased"
    xlm_roberta_base = "xlm_roberta_base"
    gpt2 = "gpt2"
    gpt_4 = "gpt-4"
    gpt_3_5_turbo = "gpt-3.5-turbo"
    roberta = "roberta"
    laser100k = "laser100k"
    laser250k = "laser250k"
    laser500k = "laser500k"


class ChunkSentencesParameters(ProcessorParameters):
    unit: ChunkingUnit = Field(
        ChunkingUnit.character,
        description="""Which chunking unit to use to compute boundaries, can be one of:<br/>
                            <li>`character`: group consecutive sentences until their size is just below `chunk_char_max_length` characters.
                            <li>`token`: group consecutive sentences until their size is just below `chunk_token_max_length` tokens.""")

    model: TokenModel = Field(
        TokenModel.wbd,
        description="""Which [Blingfire tokenization](
                            https://github.com/microsoft/BlingFire) model to use, can be one of:<br/>
                            <li>`wbd`: Default Tokenization Model - Pattern based
                            <li>`bert_base_tok`: BERT Base/Large - WordPiece
                            <li>`bert_base_cased_tok`: BERT Base/Large Cased - WordPiece
                            <li>`bert_chinese`: BERT Chinese - WordPiece
                            <li>`bert_multi_cased`: BERT Multi Lingual Cased - WordPiece
                            <li>`xlm_roberta_base`: XLM Roberta Tokenization - Unigram LM
                            <li>`gpt2`: Byte-BPE tokenization model for GPT-2 - byte BPE
                            <li>`gpt-4`: Byte-BPE tokenization model for GPT-4 - byte BPE
                            <li>`gpt-3.5-turbo`: Byte-BPE tokenization model for GPT-3.5 - byte BPE
                            <li>`roberta`: Byte-BPE tokenization model for Roberta model - byte BPE
                            <li>`laser100k`: Trained on balanced by language WikiMatrix corpus of 80+ languages - Unigram LM
                            <li>`laser250k`: Trained on balanced by language WikiMatrix corpus of 80+ languages - Unigram LM
                            <li>`laser500k`: Trained on balanced by language WikiMatrix corpus of 80+ languages - Unigram LM""",
        extra="advanced")
    chunk_char_max_length: int = Field(
        1024, description="Maximum size of chunks (number of characters)"
    )
    chunk_token_max_length: int = Field(
        128, description="Maximum size of chunks (number of tokens)"
    )
    overlap: int = Field(
        0, description="Number of overlapping sentences between chunks"
    )


class MarkedSentence:
    def __init__(self, sentence: Sentence, is_marked=False):
        self.sentence = sentence
        self.is_marked = is_marked

    @property
    def start(self):
        return self.sentence.start

    @start.setter
    def start(self, value):
        self.sentence.start = value

    @property
    def end(self):
        return self.sentence.end

    @end.setter
    def end(self, value):
        self.sentence.end = value


class WrappedSentence:
    def __init__(self, sentence: MarkedSentence, start=None, end=None):
        self.wrapped = sentence
        self.start = start if start is not None else sentence.start
        self.end = end if end is not None else sentence.end


class ChunkSentencesProcessor(ProcessorBase):
    """Group sentences by chunks of given max length.
    To be used in a segmentation pipeline."""

    def process(
            self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:
        params: ChunkSentencesParameters = cast(ChunkSentencesParameters, parameters)
        for document in documents:
            sentences = []
            msentences = [MarkedSentence(s) for s in document.sentences]
            for cstart, cend in self.group_sentences(document.text, msentences,
                                                     params):
                sentences.append(Sentence(start=cstart, end=cend))
            if len(sentences) == 0:
                sentences.append(Sentence(start=0, end=len(document.text)))
            document.sentences = sentences
        return documents

    @classmethod
    def group_sentences(cls, text: str, sentences: List[MarkedSentence], params: ChunkSentencesParameters):
        uncase = 'bert' in params.model.value and 'cased' not in params.model.value
        h = get_model(params.model.value) if params.unit == ChunkingUnit.token else None
        chunk_size = params.chunk_token_max_length if params.unit == ChunkingUnit.token else params.chunk_char_max_length
        overlap = params.overlap
        chunks = RangeMap()
        start = 0
        text_length = 0 if params.unit == ChunkingUnit.token else len(text)
        for sent in sentences:
            if h is not None:
                stext = text[sent.start:sent.end].lower() if uncase else text[sent.start:sent.end]
                tokens = cls.tokenize_with_model(h, stext)
                text_length += len(tokens)
                end = start + len(tokens)
                if end > start:
                    chunks[start:end] = WrappedSentence(sent, start=start, end=end)
                start = end
            else:
                chunks[sent.start:sent.end] = WrappedSentence(sent)

        cstart = 0
        cend = 0
        while cend < text_length:
            ranges = chunks.get_range(cstart, cstart + chunk_size)
            if ranges.start is None or ranges.end is None:
                break
            candidate_sents = list(ranges.values())
            csstart = candidate_sents[0].wrapped.start
            if len(candidate_sents) == 1:
                cend = candidate_sents[-1].end
                cnext_start = cend
                csend = candidate_sents[-1].wrapped.end
            elif len(candidate_sents) > 1:
                last_index = len(candidate_sents) - 1
                if len(candidate_sents) > 2:
                    if ranges.end != candidate_sents[last_index].end:
                        last_index -= 1
                    marked = [index for index, cs in enumerate(candidate_sents) if index > 1 and cs.wrapped.is_marked]
                    if marked:  # Force to segment before all marked sentences
                        last_index = min(marked[0] - 1, last_index)
                cend = candidate_sents[last_index].end
                cnext_start = candidate_sents[last_index - overlap].end if (last_index - overlap >= 0) else cend
                csend = candidate_sents[last_index].wrapped.end
            yield (csstart, csend)
            cstart = cnext_start

    @classmethod
    def tokenize_with_model(cls, model, stext):
        if isinstance(model, int):
            tokens = blingfire.text_to_ids(model, stext, len(stext), unk=0,
                                           no_padding=True) if model != -1 else blingfire.text_to_words(
                stext).split(' ')
        else:
            tokens = model.encode(stext)
        return tokens

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return ChunkSentencesParameters


@lru_cache(maxsize=None)
def get_model(model: str):
    # load a provided with the package model
    if model == TokenModel.wbd.value:
        return -1
    elif model.startswith("gpt-"):
        h = tiktoken.encoding_for_model(model)
    else:
        h = blingfire.load_model(os.path.join(os.path.dirname(blingfire.__file__), f"{model}.bin"))
    return h
