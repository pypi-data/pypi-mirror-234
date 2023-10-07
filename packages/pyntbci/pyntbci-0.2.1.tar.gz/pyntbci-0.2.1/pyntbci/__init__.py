"""
PyntBCI
=======

Python Noise-Tagging Brain-Computer interface (PyntBCI) is a Python library for the noise-tagging brain-computer
interface (BCI) project developed at the Donders Institute for Brain, Cognition and Behaviour, Radboud University,
Nijmegen, the Netherlands. PyntBCI contains various signal processing steps and machine learning algorithms for BCIs
that make use of evoked responses of the electroencephalogram (EEG), specifically code-modulated responses such as the
code-modulated visual evoked potential (c-VEP). For a constructive review, see :
Martínez-Cagigal, V., Thielen, J., Santamaría-Vázquez, E., Pérez-Velasco, S., Desain, P., & Hornero, R. (2021).
Brain–computer interfaces based on code-modulated visual evoked potentials (c-VEP): a literature review. Journal of
Neural Engineering. DOI: [10.1088/1741-2552/ac38cf](https://doi.org/10.1088/1741-2552/ac38cf)

Available modules
-----------------
classifiers
    Core classification models.
codes
    Basic functions to generate stimulation sequences a.k.a. noise-codes.
plotting
    Basic functions to visualize data.
stopping
    Core dynamic stopping models.
transformers
    Core transformer models.
utilities
    Basic functions used by the other modules.
"""


__author__ = "Jordy Thielen"
__contact__ = "jordy.thielen@donders.ru.nl"
__credits__ = "Radboud University; Donders Institute for Brain, Cognition and Behaviour"
__license__ = "BSD"
__version__ = "0.2.1"


from pyntbci import classifiers
from pyntbci import codes
from pyntbci import plotting
from pyntbci import stopping
from pyntbci import transformers
from pyntbci import utilities
