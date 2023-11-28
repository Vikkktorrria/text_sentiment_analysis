from .ria_news import fipsParser
from .npParser import npParser
from .iidfParser import iidfParser
from .mineconomyOrbParser import mineconomyOrbParser
from .msrOrbParser import msrOrbParser
from .orenburgCciParser import orenburgCciParser
from .orenburgGovParser import orenburGovParser
from .orenburgMediaParser import orenburgMediaParser
from .orenminParser import orenminParser
from .orensauParser import orensauParser

parserDict = {
    'https://fips.ru': fipsParser,
    'https://56np.ru': npParser,
    'https://www.iidf.ru': iidfParser,
    'https://mineconomy.orb.ru': mineconomyOrbParser,
    'https://msr.orb.ru': msrOrbParser,
    'https://orenburg-cci.ru': orenburgCciParser,
    'https://orenburg-gov.ru':  orenburGovParser,
    'https://orenburg.media': orenburgMediaParser,
    'https://orenmin.ru': orenminParser,
    'https://orensau.ru': orensauParser,
}


def getParser(sourceLink):
    if sourceLink not in parserDict.keys():
        return None
    return parserDict[sourceLink]