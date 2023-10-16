from enum import Enum
import logging

import pard._raw_python_dictionaries
from pard._handling_3_letter_code_decorator import handling_3_letter_code


class MatrixType(Enum):
    ALL_RESIDUES = 1
    HELIX = 2
    SHEET = 3
    EXPOSED = 4
    BURIED = 5
    TURN = 6
    COIL = 7
    BURIED_HELIX = 8
    BURIED_SHEET = 9
    EXPOSED_HELIX = 10
    EXPOSED_SHEET = 11
    BURIED_TURN = 12
    BURIED_COIL = 13
    EXPOSED_TURN = 14
    EXPOSED_COIL = 15


@handling_3_letter_code
def koshi_goldstein(
    amino_acid_1: str,
    amino_acid_2: str,
    matrix_type: MatrixType,
    symmetric: bool,
    warning: bool = True,
) -> float:
    """
    :param amino_acid_1: 1 letter code of the first amino acid
    :param amino_acid_2: 1 letter code of the third amino acid
    :param matrix_type: which optimal Koshi-Goldstein substitution matrix is desired, choose from the 15 Koshi Goldstein
                        available matrices: MatrixType.ALL_RESIDUES, MatrixType.HELIX, MatrixType.SHEET,
                        MatrixType.EXPOSED, MatrixType.BURIED, MatrixType.TURN, MatrixType.COIL,
                        MatrixType.BURIED_HELIX, MatrixType.BURIED_SHEET, MatrixType.EXPOSED_HELIX,
                        MatrixType.EXPOSED_SHEET, MatrixType.BURIED_TURN, MatrixType.BURIED_COIL,
                        MatrixType.EXPOSED_TURN, MatrixType.EXPOSED_COIL
    :param symmetric: whether the symmetric version of the matrix is wanted or not (i.e. exchanges of known* or
                      unknown direction)
                      * amino_acid_1 -> amino_acid_2
    :param warning: Set warning to False to stop seeing the warning

    :return: An integer / float / None representing the experimental exchangeability distance between amino_acid_1 and
             amino_acid_2 (x1000)
    """
    if warning:
        logging.warning(
            " Friendly reminder that the koshi_goldstein score is not a distance. Rather, it is the probability "
            "(from 0 to 100) of a mutation from amino_acid_1 to amino_acid_2. Meaning, high koshi_goldstein "
            "score is likely to mean that the amino acids are similar, although this statement certainly "
            "is debatable.\n"
            "To remove this warning, call the function koshi_goldstein with the optional argument "
            "'warning=False'."
        )

    match matrix_type:
        case MatrixType.ALL_RESIDUES:
            if symmetric:
                return pard._raw_python_dictionaries.SYMMETRIC_KOSHI_GOLDSTEIN_ALL_RESIDUES_DICT[
                    (amino_acid_1, amino_acid_2)
                ]
            else:
                return pard._raw_python_dictionaries.ASYMMETRIC_KOSHI_GOLDSTEIN_ALL_RESIDUES_DICT[
                    (amino_acid_1, amino_acid_2)
                ]
        case MatrixType.EXPOSED:
            if symmetric:
                return pard._raw_python_dictionaries.SYMMETRIC_KOSHI_GOLDSTEIN_EXPOSED_RESIDUES_DICT[
                    (amino_acid_1, amino_acid_2)
                ]
            else:
                return pard._raw_python_dictionaries.ASYMMETRIC_KOSHI_GOLDSTEIN_EXPOSED_RESIDUES_DICT[
                    (amino_acid_1, amino_acid_2)
                ]
        case MatrixType.BURIED:
            if symmetric:
                return pard._raw_python_dictionaries.SYMMETRIC_KOSHI_GOLDSTEIN_BURIED_RESIDUES_DICT[
                    (amino_acid_1, amino_acid_2)
                ]
            else:
                return pard._raw_python_dictionaries.ASYMMETRIC_KOSHI_GOLDSTEIN_BURIED_RESIDUES_DICT[
                    (amino_acid_1, amino_acid_2)
                ]
        case MatrixType.COIL:
            if symmetric:
                return pard._raw_python_dictionaries.SYMMETRIC_KOSHI_GOLDSTEIN_COIL_RESIDUES_DICT[
                    (amino_acid_1, amino_acid_2)
                ]
            else:
                return pard._raw_python_dictionaries.ASYMMETRIC_KOSHI_GOLDSTEIN_COIL_RESIDUES_DICT[
                    (amino_acid_1, amino_acid_2)
                ]
        case MatrixType.TURN:
            if symmetric:
                return pard._raw_python_dictionaries.SYMMETRIC_KOSHI_GOLDSTEIN_TURN_RESIDUES_DICT[
                    (amino_acid_1, amino_acid_2)
                ]
            else:
                return pard._raw_python_dictionaries.ASYMMETRIC_KOSHI_GOLDSTEIN_TURN_RESIDUES_DICT[
                    (amino_acid_1, amino_acid_2)
                ]
        case MatrixType.HELIX:
            if symmetric:
                return pard._raw_python_dictionaries.SYMMETRIC_KOSHI_GOLDSTEIN_HELIX_RESIDUES_DICT[
                    (amino_acid_1, amino_acid_2)
                ]
            else:
                return pard._raw_python_dictionaries.ASYMMETRIC_KOSHI_GOLDSTEIN_HELIX_RESIDUES_DICT[
                    (amino_acid_1, amino_acid_2)
                ]
        case MatrixType.SHEET:
            if symmetric:
                return pard._raw_python_dictionaries.SYMMETRIC_KOSHI_GOLDSTEIN_SHEET_RESIDUES_DICT[
                    (amino_acid_1, amino_acid_2)
                ]
            else:
                return pard._raw_python_dictionaries.ASYMMETRIC_KOSHI_GOLDSTEIN_SHEET_RESIDUES_DICT[
                    (amino_acid_1, amino_acid_2)
                ]
        case _:
            raise NotImplementedError(
                "The matrix type is not yet implemented."
            )
