from collections import OrderedDict
from functools import reduce

import numpy as np
from ecl.eclfile import EclInitFile, EclKW
from ecl.grid import EclGrid
from ecl.summary import EclSum
from ecl2df import EclFiles

from preprocessing.deck.section import find_includes
from preprocessing.modular.data import WellSpecsProcessor

SMSPEC_WELL_KEYWORDS = {
    "WOPR",
    "WOPRH",
    "WWPR",
    "WWPRH",
    "WGPR",
    "WWIR",
    "WBHP",
    "WBHPH",
    "WTHP",
    "WGPRH",
    "WTHPH",
    "WWIRH",
}
SMSPEC_FIELD_KEYWORDS = ["FOPR", "FWPR", "FGPR", "FOPRH", "FWPRH", "FGPRH"]


def preprocess(
    data_file_loc,
    egrid_file_loc,
    smspec_file_loc,
    init_file_loc,
    download_func,
    allow_missing_files=tuple(),
):
    find_includes(data_file_loc, download_func, data_file_loc, allow_missing_files=allow_missing_files)

    preprocessor = WellSpecsProcessor(data_file_loc)
    data = preprocessor.process()

    if smspec_file_loc:
        smry = EclSum(str(smspec_file_loc))
        wnames = OrderedDict((wname, {"injector": None, "type": None}) for wname in smry.wells())
        for wname, wprops in wnames.items():
            if wname in [x.upper() for x in data["wells"].keys()]:
                well_kw = next(filter(lambda x: x.upper() == wname, data["wells"]))
                wprops["type"] = data["wells"][well_kw]["well_type"]
                wprops["injector"] = "INJECTOR" in wprops["type"].upper()

        available_keywords_by_well = reduce(
            lambda d, p: d.setdefault(p[0], set()).add(p[1]) or d,
            (
                (p[1], p[0])
                for p in (x.split(":") for x in list(smry))
                if len(p) == 2 and p[1] in wnames and p[0] in SMSPEC_WELL_KEYWORDS
            ),
            {},
        )

        extractor_keywords = sorted(
            reduce(
                lambda p, n: p.intersection(n),
                (k for w, k in available_keywords_by_well.items() if wnames[w]["injector"] is False),
                SMSPEC_WELL_KEYWORDS,
            )
        )

        injector_keywords = sorted(
            reduce(
                lambda p, n: p.intersection(n),
                (k for w, k in available_keywords_by_well.items() if wnames[w]["injector"] is True),
                SMSPEC_WELL_KEYWORDS,
            )
        )

        # Discover implicit liquid keywords (_L__..) as a combination of oil and water [(_W__..) and (_O__..)]
        for keyword_set in (extractor_keywords, injector_keywords):
            liquid_keyword_candidates = set(f"{x[0]}_{x[2:]}" for x in extractor_keywords if x[1] in ("W", "O"))
            for liquid_keyword_candidate in liquid_keyword_candidates:
                include_liquid_keyword = (
                    liquid_keyword_candidate.replace("_", "O") in keyword_set
                    and liquid_keyword_candidate.replace("_", "W") in keyword_set
                )
                if include_liquid_keyword:
                    keyword_set.append(liquid_keyword_candidate.replace("_", "L"))

        field_keywords = set(SMSPEC_FIELD_KEYWORDS).intersection(list(smry))

    else:
        wnames = {}
        extractor_keywords = []
        injector_keywords = []
        field_keywords = []
        smry = None

    def get_ecl(data):
        import opm.io
        from pathlib import Path

        section_list = [opm.io.parser.eclSectionType.SCHEDULE, opm.io.parser.eclSectionType.GRID]

        if Path(data._eclbase + ".DATA").is_file():
            deckfile = data._eclbase + ".DATA"
        else:
            deckfile = data._eclbase
        builtin = opm.io.Builtin()

        kw_list = ["START", "ENDSCALE", "MULTOUT", "DIMENS", "GAS", "OIL", "WATER"]

        OPMIOPARSER_RECOVERY = [
            ("PARSE_RANDOM_SLASH", opm.io.action.warn),
            ("*UNSUPPORTED*", opm.io.action.warn),
            ("*MISSING*", opm.io.action.warn),
            ("*UNKNOWN*", opm.io.action.warn),
            ("PARSE_EXTRA_RECORDS", opm.io.action.ignore),
            ("PARSE_UNKNOWN_KEYWORD", opm.io.action.ignore),
            ("PARSE_RANDOM_TEXT", opm.io.action.ignore),
            ("PARSE_RANDOM_SLASH", opm.io.action.ignore),
            ("PARSE_MISSING_DIMS_KEYWORD", opm.io.action.ignore),
            ("PARSE_EXTRA_DATA", opm.io.action.ignore),
            ("PARSE_MISSING_SECTIONS", opm.io.action.ignore),
            ("PARSE_MISSING_INCLUDE", opm.io.action.ignore),
            ("PARSE_LONG_KEYWORD", opm.io.action.ignore),
            ("PARSE_WGNAME_SPACE", opm.io.action.ignore),
            ("PARSE_INVALID_KEYWORD_COMBINATION", opm.io.action.ignore),
            ("UNIT_SYSTEM_MISMATCH", opm.io.action.ignore),
            ("RUNSPEC_NUMWELLS_TOO_LARGE", opm.io.action.ignore),
            ("RUNSPEC_CONNS_PER_WELL_TOO_LARGE", opm.io.action.ignore),
            ("RUNSPEC_NUMGROUPS_TOO_LARGE", opm.io.action.ignore),
            ("RUNSPEC_GROUPSIZE_TOO_LARGE", opm.io.action.ignore),
            ("UNSUPPORTED_INITIAL_THPRES", opm.io.action.ignore),
            ("UNSUPPORTED_TERMINATE_IF_BHP", opm.io.action.ignore),
            ("INTERNAL_ERROR_UNINITIALIZED_THPRES", opm.io.action.ignore),
            ("SUMMARY_UNKNOWN_WELL", opm.io.action.ignore),
            ("SUMMARY_UNKNOWN_GROUP", opm.io.action.ignore),
            ("SUMMARY_UNKNOWN_NODE", opm.io.action.ignore),
            ("SUMMARY_UNKNOWN_AQUIFER", opm.io.action.ignore),
            ("SUMMARY_UNHANDLED_KEYWORD", opm.io.action.ignore),
            ("SUMMARY_UNDEFINED_UDQ", opm.io.action.ignore),
            ("SUMMARY_UDQ_MISSING_UNIT", opm.io.action.ignore),
            ("SUMMARY_INVALID_FIPNUM", opm.io.action.ignore),
            ("SUMMARY_EMPTY_REGION", opm.io.action.ignore),
            ("SUMMARY_REGION_TOO_LARGE", opm.io.action.ignore),
            ("RPT_MIXED_STYLE", opm.io.action.ignore),
            ("RPT_UNKNOWN_MNEMONIC", opm.io.action.ignore),
            ("SCHEDULE_INVALID_NAME", opm.io.action.ignore),
            ("ACTIONX_ILLEGAL_KEYWORD", opm.io.action.ignore),
            ("SIMULATOR_KEYWORD_NOT_SUPPORTED", opm.io.action.ignore),
            ("SIMULATOR_KEYWORD_NOT_SUPPORTED_CRITICAL", opm.io.action.ignore),
            ("SIMULATOR_KEYWORD_ITEM_NOT_SUPPORTED", opm.io.action.ignore),
            ("SIMULATOR_KEYWORD_ITEM_NOT_SUPPORTED_CRITICAL", opm.io.action.ignore),
            ("UDQ_PARSE_ERROR", opm.io.action.ignore),
            ("UDQ_TYPE_ERROR", opm.io.action.ignore),
            ("SCHEDULE_GROUP_ERROR", opm.io.action.ignore),
            ("SCHEDULE_IGNORED_GUIDE_RATE", opm.io.action.ignore),
            ("SCHEDULE_COMPSEG_INVALID", opm.io.action.ignore),
            ("SCHEDULE_COMPSEGS_NOT_SUPPORTED", opm.io.action.ignore),
        ]

        parseContext = opm.io.ParseContext(OPMIOPARSER_RECOVERY)
        parser = opm.io.Parser()

        for kw in kw_list:
            parser.add_keyword(builtin[kw])

        deck = parser.parse(deckfile, parseContext, section_list)

        return deck

    if data_file_loc:
        data = EclFiles(data_file_loc)
        ecldeck = get_ecl(data)
        data_keywords = sorted(set(x.name for x in ecldeck))
    else:
        data_keywords = []

    if egrid_file_loc and init_file_loc:
        grid = EclGrid(str(egrid_file_loc))
        init = EclInitFile(grid, str(init_file_loc))
        init_keywords = sorted(set(x.name for x in init if isinstance(x, EclKW)))
    else:
        init_keywords = []

    return {
        "phases": preprocess_phases(ecldeck),
        "start": preprocess_start(ecldeck),
        "timestep": preprocess_timestep(smry),
        "endscale": find_keyword(ecldeck, "ENDSCALE"),
        "multout": find_keyword(ecldeck, "MULTOUT"),
        "dimens": preprocess_dimens(ecldeck),
        "wnames": wnames,
        "wkeywords": {"injector": injector_keywords, "extractor": extractor_keywords},
        "fkeywords": sorted(field_keywords),
        "data_keywords": data_keywords,
        "init_keywords": init_keywords,
    }


def preprocess_start(ecldeck):
    from datetime import datetime

    try:
        start = str(ecldeck["START"][0]).strip(" \n/")
        return datetime.strptime(start, "%d '%b' %Y")
    except Exception:
        return False


def preprocess_timestep(smry):
    from datetime import timedelta

    try:
        data = smry["TIMESTEP"]
        unit = data.unit.lower()
        return timedelta(**{unit: int(data[0].value)})
    except Exception:
        return None


def preprocess_phases(ecldeck):
    return {
        "gas": find_keyword(ecldeck, "GAS"),
        "oil": find_keyword(ecldeck, "OIL"),
        "water": find_keyword(ecldeck, "WATER"),
    }


def preprocess_dimens(ecldeck):
    dimens = ecldeck["DIMENS"][0]
    return np.array([dimens[0].value, dimens[1].value, dimens[2].value])


def find_keyword(ecldeck, keyword):
    return hasattr(ecldeck, "__contains__") and keyword in ecldeck
