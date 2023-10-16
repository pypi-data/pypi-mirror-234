import pard._raw_python_dictionaries
from pard._handling_3_letter_code_decorator import handling_3_letter_code

@handling_3_letter_code
def epstein(amino_acid_1: str, amino_acid_2: str, symmetric: bool) -> float:
    """
    :param amino_acid_1: 1 letter code of the first amino acid
    :param amino_acid_2: 1 letter code of the third amino acid
    :param symmetric: whether the symmetric version of the matrix is wanted or not (i.e. exchanges of known or
                      unknown direction)

    :return: An integer representing the Miyata distance between amino_acid_1 and amino_acid_2
    """
    if symmetric:
        return pard._raw_python_dictionaries.SYMMETRIC_EPSTEIN_DICT[(amino_acid_1, amino_acid_2)]
    else:
        return pard._raw_python_dictionaries.ASYMMETRIC_EPSTEIN_DICT[(amino_acid_1, amino_acid_2)]
