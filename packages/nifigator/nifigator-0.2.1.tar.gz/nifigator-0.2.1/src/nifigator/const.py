# -*- coding: utf-8 -*-

"""
"""

from collections import namedtuple
from rdflib.namespace import Namespace
from rdflib.term import URIRef
import rdflib

OffsetBasedString = URIRef(
    "http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#OffsetBasedString"
)
RFC5147String = URIRef(
    "http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#RFC5147String"
)

EntityOccurrence = "EntityOccurrence"
TermOccurrence = "TermOccurrence"

NIF = Namespace("http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#")
NIF_ONTOLOGY = "http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core/2.1"
OLIA = Namespace("http://purl.org/olia/olia.owl#")
ITSRDF = Namespace("http://www.w3.org/2005/11/its/rdf#")
NIFVEC = Namespace("http://mangosaurus.eu/ontology/nifvec#")

RDF = rdflib.namespace.RDF
RDFS = rdflib.namespace.RDFS
DCAT = rdflib.namespace.DCAT
DC = rdflib.namespace.DC
DCT = rdflib.namespace.DCTERMS
SKOS = rdflib.namespace.SKOS
XSD = rdflib.namespace.XSD
TBX = Namespace("http://tbx2rdf.lider-project.eu/tbx#")
ONTOLEX = Namespace("http://www.w3.org/ns/lemon/ontolex#")
LEXINFO = Namespace("http://www.lexinfo.net/ontology/3.0/lexinfo#")
DECOMP = Namespace("http://www.w3.org/ns/lemon/decomp#")

DEFAULT_URI = "https://mangosaurus.eu/rdf-data/"
DEFAULT_PREFIX = "mangosaurus"

MIN_PHRASE_COUNT = "min_phrase_count"
MIN_CONTEXT_COUNT = "min_context_count"
MIN_PHRASECONTEXT_COUNT = "min_phrasecontext_count"
MAX_PHRASE_LENGTH = "max_phrase_length"
MAX_CONTEXT_LENGTH = "max_context_length"
CONTEXT_SEPARATOR = "context_separator"
PHRASE_SEPARATOR = "phrase_separator"
WORDS_FILTER = "words_filter"
TRIPLE_BATCH_SIZE = "triple_batch_size"
FORCED_SENTENCE_SPLIT_CHARACTERS = "force_sentence_split_characters"
REGEX_FILTER = "regex_filter"

STOPWORDS = [
    "a",
    "an",
    "the",
    "and",
    "but",
    "if",
    "or",
    "because",
    "as",
    "until",
    "while",
    "of",
    "at",
    "by",
    "for",
    "with",
    "about",
    "against",
    "between",
    "into",
    "through",
    "during",
    "before",
    "after",
    "above",
    "below",
    "to",
    "from",
    "up",
    "down",
    "in",
    "out",
    "on",
    "off",
    "over",
    "under",
    "further",
    "per",
]

# Tense
# VerbForm
# Case
# Degree
# NumType
# Voice
# Poss

upos2olia = {
    "SYM": URIRef("http://purl.org/olia/olia.owl#Symbol"),
    "ADJ": URIRef("http://purl.org/olia/olia.owl#Adjective"),
    "X": URIRef("http://purl.org/olia/olia-top.owl#Word"),
    "ADV": URIRef("http://purl.org/olia/olia.owl#Adverb"),
    "PUNCT": URIRef("http://purl.org/olia/olia.owl#Punctuation"),
    "AUX": URIRef("http://purl.org/olia/olia.owl#AuxiliaryVerb"),
    "ADP": URIRef("http://purl.org/olia/olia.owl#Adposition"),
    "NUM": URIRef("http://purl.org/olia/olia.owl#Quantifier"),
    "PROPN": URIRef("http://purl.org/olia/olia.owl#ProperNoun"),
    "INTJ": URIRef("http://purl.org/olia/olia.owl#Interjection"),
    "CONJ": URIRef("http://purl.org/olia/olia.owl#CoordinatingConjunction"),
    # possibly an error in Stanza with CCONJ (does not exist in Olia):
    "CCONJ": URIRef("http://purl.org/olia/olia.owl#CoordinatingConjunction"),
    "DET": URIRef("http://purl.org/olia/olia.owl#Determiner"),
    "PART": URIRef("http://purl.org/olia/olia.owl#Particle"),
    "SCONJ": URIRef("http://purl.org/olia/olia.owl#SubordinatingConjunction"),
    "PRON": URIRef("http://purl.org/olia/olia.owl#Pronoun"),
    "NOUN": URIRef("http://purl.org/olia/olia.owl#CommonNoun"),
    "VERB": URIRef("http://purl.org/olia/olia.owl#Verb"),
}

UD2OLIA_mappings = {
    "Definite": {
        "Com": None,
        "Cons": None,
        "Def": "olia:Definite",
        "Ind": "olia:Indefinite",
        "Spec": None,
    },
    "PronType": {
        "Art": "olia:Article",
        "Dem": "olia:DemonstrativePronoun",
        "Emp": "olia:EmphaticPronoun",
        "Exc": None,
        "Ind": "olia:IndefinitePronoun",
        "Int": "olia:InterrogativePronoun",
        "Neg": "NegativePronoun",
        "Prs": "olia:PersonalPronoun",
        "Rcp": "olia:ReciprocalPronoun",
        "Rel": "olia:RelativePronoun",
        "Tot": "olia:PronounOrDeterminer",
    },
    "Number": {
        "Coll": None,
        "Count": None,
        "Dual": None,
        "Grpa": None,
        "Grpl": None,
        "Inv": None,
        "Pauc": None,
        "Plur": "olia:Plural",
        "Ptan": None,
        "Sing": "olia:Singular",
        "Tri": None,
    },
    "Person": {
        "0": None,
        "1": "olia:First",
        "2": "olia:Second",
        "3": "olia:Third",
        "4": None,
    },
    "Mood": {
        "Adm": None,
        "Cnd": None,
        "Des": None,
        "Imp": "olia:ImperativeMood",
        "Ind": "olia:IndicativeMood",
        "Irr": None,
        "Jus": None,
        "Nec": None,
        "Opt": "olia:OptativeMood",
        "Pot": None,
        "Prp": None,
        "Qot": None,
        "Sub": "olia:SubjunctiveMood",
    },
    "Tense": {
        "Pres": "olia:Present",
        "Past": "olia:Past",
        "Fut": "olia:Future",
        "Pqp": "olia:PluperfectTense",
    },
    "VerbForm": {
        "Inf": "olia:Infinitive",
        "Fin": "olia:FiniteVerb",
        "Part": "olia:Participle",
        "Past": "olia:Past",
        "Ger": "olia:Gerund",
        "Gdv": "olia:NonFiniteVerb",  # (?)
    },
    "Case": {
        "Nom": "olia:Nominative",
        "Gen": "olia:Genitive",
        "Dat": "olia:DativeCase",
        "Acc": "olia:Accusative",
        "Voc": "olia:VocativeCase",
    },
    "Degree": {
        "Pos": "olia:Positive",
        "Sup": "olia:Superlative",
        "Cmp": "olia:Comparative",
    },
    "NumType": {
        "Card": "olia:CardinalNumber",
        "Ord": "olia:OrdinalNumber",
        "Mult": "olia:MultiplicativeNumeral",
        "Frac": "olia:Fraction",
    },
    "NumForm": {
        "Word": "olia:LetterNumeral",
        "Digit": "olia:DigitNumeral",
        "Roman": "olia:RomanNumeral",
    },
    "Voice": {
        "Pass": "olia:PassiveVoice",
        "Act": "olia:ActiveVoice",
        "Mid": "olia:MiddleVoice",
    },
    "Gender": {
        "Com": "olia:CommonGender",
        "Neut": "olia:Neuter",
        "Com,Neut": "olia:CommonGender",  # correct?
        "Masc,Neut": "olia:CommonGender",  # correct?
        "Fem,Masc": "olia:CommonGender",  # correct?
        "Fem": "olia:Feminine",
        "Masc": "olia:Masculine",
    },
    "pos": {
        "adj": "olia:Adjective",
        "adp": "olia:Adposition",
        "adv": "olia:Adverb",
        "aux": "olia:AuxiliaryVerb",
        "conj": "olia:CoordinatingConjunction",
        "cconj": "olia:CoordinatingConjunction",  # ??
        "det": "olia:Determiner",
        "intj": "olia:Interjection",
        "noun": "olia:CommonNoun",
        "num": "olia:Quantifier",
        "part": "olia:Particle",
        "pron": "olia:Pronoun",
        "propn": "olia:ProperNoun",
        "punct": "olia:Punctuation",
        "sconj": "olia:SubordinatingConjunction",
        "sym": "olia:Symbol",
        "verb": "olia:Verb",
        "x": "olia:X",  # &olia-top;Word"  # not correct
    },
    "Polarity": {
        "Neg": "olia:Negation",
    },
    "ExtPos": {
        "ADP": "olia:Adposition",
        "ADV": "olia:Adverb",
        "CCONJ": "olia:CoordinatingConjunction",  # ??
        "PRON": "olia:Pronoun",
        "SCONJ": "olia:SubordinatingConjunction",
    },
    "Typo": {
        "Yes": "olia:Typo",
    },
    "Style": {
        "Arch": None,
        "Coll": None,
        "Expr": None,
        "Form": "olia:FormalRegister",
        "Rare": None,
        "Slng": "olia:SlangRegister",
        "Vrnc": "olia:DialectRegister",  # possibly not correct
        "Vulg": "olia:VulgarRegister",
    },
    "Aspect": {"Perf": "olia:PerfectiveAspect", "Imp": "olia:ImperfectiveAspect"},
    "Reflex": {"Yes": "olia:ReflexivePronoun"},
    "Abbr": {"Yes": "olia:Abbreviation"},
    "Poss": {"Yes": "olia:PossessivePronoun"},
    "Foreign": {"Yes": "olia:Foreign"},
}


def mapobject(p: str = "", o: str = ""):
    if p not in UD2OLIA_mappings.keys():
        print("UD Not found: " + p)
    else:
        if o not in UD2OLIA_mappings[p].keys():
            print("UD Not found: " + p + " , " + o)
    return (
        UD2OLIA_mappings.get(p, {})
        .get(o, "olia:" + o)
        .replace("olia:", "http://purl.org/olia/olia.owl#")
    )


# nafdocument definition

ProcessorElement = namedtuple(
    "lp", "name version model timestamp beginTimestamp endTimestamp hostname"
)

WordformElement = namedtuple("WfElement", "id sent para page offset length xpath text")

TermElement = namedtuple(
    "TermElement",
    "id type lemma pos morphofeat netype case head component_of \
    compound_type span ext_refs comment",
)

Entity = namedtuple("Entity", "start end type")

EntityElement = namedtuple(
    "EntityElement", "id type status source span ext_refs comment"
)

DependencyRelation = namedtuple(
    "DependencyRelation", "from_term to_term rfunc case comment"
)

ChunkElement = namedtuple("ChunkElement", "id head phrase case span comment")

RawElement = namedtuple("RawElement", "text")

MultiwordElement = namedtuple(
    "MultiwordElement", "id lemma pos morphofeat case status type components"
)

ComponentElement = namedtuple(
    "ComponentElement", "id type lemma pos morphofeat netype case head span"
)
