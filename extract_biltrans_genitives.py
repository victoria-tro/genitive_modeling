#!/usr/bin/env python3.10


# Input should be from biltrans with forms. Use newest lttoolbox, and
# the `nob-nno-surf-biltrans` pipeline.

# $ head Genitive_models/Predict_how_to_rewrite/dataset/sorted.csv | cut -f1 | apertium -d .. nob-nno-surf-biltrans | python3 extract_biltrans_genitives.py

# lagmannsrettens flertall        lagmannsrett<n> fleirtal<n>
# § 3-5s forstand § 3-5<n> forstand<n>
# domfeltes adferd        domfelt<n> åtferd<n>
# lovens vilkår   lov<n> vilkår<n>
# elevenes rettigheter    elev<n> rett¹<n>
# barnets motstand        barn<n> motstand<n>
# barnets beste   barn<n> beste<n>
# sykehusenes eget ansvar sjukehus<n> eigen<det> ansvar<n>
# lagmannsrettens dom     lagmannsrett<n> dom<n>
# fremtidens oppgaver     framtid<n> oppgåve<n>

# Not done yet: matching this with the nno side of the corpus (which
# needs to run through nno-nob-tagger)

from __future__ import annotations  # for compatibility with python 3.7–3.9
from typing import List, Text
import sys

from streamparser import parse_file, LexicalUnit, SReading


def main_readings(readings: List[List[SReading]]) -> List[SReading]:
    """
    A reading is a list of subreadings; since there may be several
    lemma-translations, we have a list of lists.
    """
    return [r[0] for r in readings if len(r) >= 1]


def main_pos(sub: SReading) -> Text:
    return sub.tags[0] if len(sub.tags)>=1 else ""


current_genitive: None | List[LexicalUnit] = None
for lu in parse_file(sys.stdin):
    # Drop the first reading, which is the Source Language (Bokmål)
    # input, end up with just Target Language (Nynorsk) readings:
    tl_main_readings: List[SReading] = main_readings(lu.readings[1:])
    # Skip unknowns:
    if len(tl_main_readings) == 0:
        # print("unk", lu)
        continue
    is_gen = any('gen' in r.tags for r in tl_main_readings)
    is_noun = any(main_pos(r) == 'n' for r in tl_main_readings)
    is_sent = any(main_pos(r) == 'sent' for r in tl_main_readings)
    # print(lu, is_gen, is_noun)
    if is_gen:
        current_genitive = [lu]
    elif current_genitive is not None:
        current_genitive.append(lu)
        if is_noun:
            # TODO: This just prints the forms and nno-readings – we
            # want to also look up this line in the tagged nno corpus
            # and find the way it was expressed in nno:
            print(" ".join(gen_lu.wordform
                           for gen_lu in current_genitive),
                  end="\t")
            print(" ".join("/".join(set(r.baseform +"<"+ main_pos(r) + ">"
                                        for r in main_readings(gen_lu.readings[1:])))
                           for gen_lu in current_genitive))
            # Reached genitive phrase end, start fresh
            current_genitive = None
        elif is_sent:
            # Reached sentence end, start fresh
            current_genitive = None
        elif len(current_genitive) > 9:
            # If it's this long, it's likely noise:
            current_genitive = None
