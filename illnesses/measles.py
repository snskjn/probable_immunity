from typing import Dict

from flask import Markup
"""
CDC Presumptive evidence of immunity: https://www.cdc.gov/vaccines/pubs/surv-manual/chpt07-measles.html


"Birth before 1957 provides only presumptive evidence for measles, mumps, and
rubella. Before vaccines were available, nearly everyone was infected with
measles, mumps, and rubella viruses during childhood. The majority of people
born before 1957 are likely to have been infected naturally and therefore are
presumed to be protected against measles, mumps, and rubella. Healthcare
personnel born before 1957 without laboratory evidence of immunity or disease
should consider getting two doses of MMR vaccine." - https://www.cdc.gov/vaccines/vpd/mmr/public/index.html


"Measles is a highly contagious virus that lives in the nose and throat mucus 
of an infected person. It can spread to others through coughing and sneezing. 
Also, measles virus can live for up to two hours in an airspace where the 
infected person coughed or sneezed.

If other people breathe the contaminated air or touch the infected surface, 
then touch their eyes, noses, or mouths, they can become infected. Measles is 
so contagious that if one person has it, up to 90% of the people close to 
that person who are not immune will also become infected.

Infected people can spread measles to others from four days before through 
four days after the rash appears."
https://www.cdc.gov/measles/transmission.html
"""

rec_shots_under_6 = 2

conferred_immunity = 1

messages = {'pre_1957_message': ("According to the CDC, you are likely immune to measles due to "
                                 "childhood exposure.<br>"
                                 "NB: \"Birth before 1957 provides only "
                                 "presumptive evidence for measles, mumps, and rubella. Before "
                                 "vaccines were available, nearly everyone was infected with "
                                 "measles, mumps, and rubella viruses during childhood. The "
                                 "majority of people born before 1957 are likely to have been "
                                 "infected naturally and therefore are presumed to be protected "
                                 "against measles, mumps, and rubella. Healthcare personnel born "
                                 "before 1957 without laboratory evidence of immunity or disease "
                                 "should consider getting two doses of MMR vaccine.\" "
                                 "- <a href='https://www.cdc.gov/vaccines/vpd/mmr/public/index.html'>"
                                 "CDC - Measles, Mumps, and Rubella (MMR) Vaccination: What Everyone Should Know</a>"),
            'has_immunisations': ("This means you have a statistical probability of being immune "
                                  "to measles if you are exposed. The closer to 1.0, the more "
                                  "likely you are immune."),  # TODO make better message
            'greater_than_two_shots_before_age_six_message': ("Data not available for more than 2 "
                                                              "shots before age 6."),
            'no_immunisations': ("You are unlikely to have any immunity to measles, if you are "
                                 "exposed, you are very likely to be infected.")
            }

# shots before 6 years
shots_under_6_immunity = {
    1: 0.93,
    2: 0.97,
}


def immunity(birth_year=None, on_time_measles_vaccinations: int = None) -> Dict:
    """
    Takes year of birth, number of shots before age 6, and provides an
    estimated probability of being immune to measles if exposed.

    :param birth_year: int or None
    :param on_time_measles_vaccinations: int or None
    :return: Dict {'probability_of_measles_immunity': float, 'measles_message': str}
    """
    # Set defaults:
    probability, message = 0.0, messages['no_immunisations']
    if birth_year < 1957:
        probability, message = 1.0, messages['pre_1957_message']
    elif on_time_measles_vaccinations:
        if on_time_measles_vaccinations <= 2:
            probability, message = shots_under_6_immunity[on_time_measles_vaccinations], messages['has_immunisations']
        if on_time_measles_vaccinations > 2:
            probability, message = shots_under_6_immunity[2], messages['greater_than_two_shots_before_age_six_message']
    return {'probability_of_measles_immunity': probability, 'measles_message': Markup(message)}

# need case where shots after age 6
