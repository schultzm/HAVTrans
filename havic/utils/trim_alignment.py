#!/usr/bin/env python3

"""A class for trimming a BioPython MultipleSeqAlignment object.

Inherits from BioPython MultipleSeqAlignment

Input:
    MultipleSeqAlignment
"""

from Bio.Align import MultipleSeqAlignment
from Bio.Seq import MutableSeq
import sys


class Trimmed_alignment(MultipleSeqAlignment):
    """Trim a BioPython MSA object.

    Given an alignment, trim the 5' and 3' regions.
    """

    def __init__(self, alignment, trimguide, gap_char, trim_seqs):

        self.alignment = alignment
        self.trimguide = trimguide # trim to this reference guide sequence
        self.gap_char = gap_char
        self.boundary = None
        self.trim_seqs = trim_seqs

    def get_refseq_boundary(self):
        """
        Get the coords of the target region
        """
        start_pos = None
        end_pos = None
        for seq in self.alignment:
            if seq.id == self.trimguide:
                from re import finditer
                for match in finditer(f"{self.gap_char}[A-Z]",
                                      str(seq.seq).upper()):
                    start_pos = (match.span())
                for match in finditer(f"{self.gap_char}[A-Z]",
                                      str(seq.seq).upper()[::-1]):
                    end_pos = (len(str(seq.seq).upper()) - match.end(),
                               -match.start())
                    # end_pos = (match.span(), match.group())
                self.boundary = [start_pos[0] + 1, end_pos[0] + 1]
                break

    def trim_seqs_to_ref(self):
        """
        Trim the requested sequences to the reference length in the alignment.
        """
        temp_aln = MultipleSeqAlignment([])
        for seq in self.alignment:
            if seq.id in self.trim_seqs:
                sequence = MutableSeq(str(seq.seq))
                # print(help(sequence))
                sequence[0:self.boundary[0]] = self.gap_char * (self.boundary[0] - 0)
                # print(len(sequence))
                # print(self.boundary)
                sequence[self.boundary[1]:] = self.gap_char * (len(sequence) - self.boundary[1])
                seq.seq = sequence
            if set(seq.seq) == set({self.gap_char}):
                print(f"{seq.id} contains only gaps after trimming. "
                      f"Removing {seq.id} from alignment.",
                      file=sys.stderr)
            else:
                temp_aln.append(seq)
        self.alignment = temp_aln

    def depad_alignment(self):
        """
        Trim the entire alignment to remove 5' and 3' gap-padding.
        """
        site_set = {self.gap_char}
        start_pos = 0
        # Get the start_pos for trim
        while len(site_set) == 1:
            site_set = set(self.alignment[:, start_pos])
            if len(site_set) > 1:
                break
            else:
                start_pos += 1
        site_set = {self.gap_char}
        # subtract one to put slice position inside alignment
        end_pos = self.alignment.get_alignment_length() - 1

        # Get the end position for trim
        while len(site_set) == 1:
            site_set = set(self.alignment[:, end_pos])
            if len(site_set) > 1:
                break
            else:
                end_pos -= 1
        self.alignment = self.alignment[:, start_pos:end_pos + 1]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
