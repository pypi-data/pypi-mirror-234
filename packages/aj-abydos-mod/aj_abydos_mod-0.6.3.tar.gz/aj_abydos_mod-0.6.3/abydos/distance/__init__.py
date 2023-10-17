# Copyright 2014-2020 by Christopher C. Little.
# This file is part of Abydos.
#
# Abydos is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Abydos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Abydos. If not, see <http://www.gnu.org/licenses/>.

r"""abydos.distance.

The distance package implements string distance measure and metric classes:

These include traditional Levenshtein edit distance and related algorithms:

    - Levenshtein distance (:py:class:`.Levenshtein`)
    - Optimal String Alignment distance (:py:class:`.Levenshtein` with
      ``mode='osa'``)
    - Damerau-Levenshtein distance (:py:class:`.DamerauLevenshtein`)
    - Yujian-Bo normalized edit distance (:py:class:`.YujianBo`)
    - Higuera-Micó contextual normalized edit distance
      (:py:class:`.HigueraMico`)
    - Indel distance (:py:class:`.Indel`)
    - Syllable Alignment Pattern Searching similarity
      (:py:class:`.distance.SAPS`)
    - Meta-Levenshtein distance (:py:class:`.MetaLevenshtein`)
    - Covington distance (:py:class:`.Covington`)
    - ALINE distance (:py:class:`.ALINE`)
    - FlexMetric distance (:py:class:`.FlexMetric`)
    - BI-SIM similarity (:py:class:`.BISIM`)
    - Discounted Levenshtein distance (:py:class:`.DiscountedLevenshtein`)
    - Phonetic edit distance (:py:class:`.PhoneticEditDistance`)

Hamming distance (:py:class:`.Hamming`), Relaxed Hamming distance
(:py:class:`.RelaxedHamming`), and the closely related Modified
Language-Independent Product Name Search distance (:py:class:`.MLIPNS`) are
provided.

Block edit distances:

    - Tichy edit distance (:py:class:`.Tichy`)
    - Levenshtein distance with block operations
      (:py:class:`.BlockLevenshtein`)
    - Rees-Levenshtein distance (:py:class:`.ReesLevenshtein`)
    - Cormode's LZ distance (:py:class:`.CormodeLZ`)
    - Shapira-Storer I edit distance with block moves, greedy algorithm
      (:py:class:`.ShapiraStorerI`)

Distance metrics developed for the US Census or derived from them are included:

    - Jaro distance (:py:class:`.JaroWinkler` with ``mode='Jaro'``)
    - Jaro-Winkler distance (:py:class:`.JaroWinkler`)
    - Strcmp95 distance (:py:class:`.Strcmp95`)
    - Iterative-SubString (I-Sub) correlation
      (:py:class:`.IterativeSubString`)

A large set of multi-set token-based distance metrics are provided, including:

    - AMPLE similarity (:py:class:`.AMPLE`)
    - AZZOO similarity (:py:class:`.AZZOO`)
    - Anderberg's D similarity (:py:class:`.Anderberg`)
    - Andres & Marzo's Delta correlation (:py:class:`.AndresMarzoDelta`)
    - Baroni-Urbani & Buser I similarity (:py:class:`.BaroniUrbaniBuserI`)
    - Baroni-Urbani & Buser II correlation (:py:class:`.BaroniUrbaniBuserII`)
    - Batagelj & Bren similarity (:py:class:`.BatageljBren`)
    - Baulieu I distance (:py:class:`.BaulieuI`)
    - Baulieu II distance (:py:class:`.BaulieuII`)
    - Baulieu III distance (:py:class:`.BaulieuIII`)
    - Baulieu IV distance (:py:class:`.BaulieuIV`)
    - Baulieu V distance (:py:class:`.BaulieuV`)
    - Baulieu VI distance (:py:class:`.BaulieuVI`)
    - Baulieu VII distance (:py:class:`.BaulieuVII`)
    - Baulieu VIII distance (:py:class:`.BaulieuVIII`)
    - Baulieu IX distance (:py:class:`.BaulieuIX`)
    - Baulieu X distance (:py:class:`.BaulieuX`)
    - Baulieu XI distance (:py:class:`.BaulieuXI`)
    - Baulieu XII distance (:py:class:`.BaulieuXII`)
    - Baulieu XIII distance (:py:class:`.BaulieuXIII`)
    - Baulieu XIV distance (:py:class:`.BaulieuXIV`)
    - Baulieu XV distance (:py:class:`.BaulieuXV`)
    - Benini I correlation (:py:class:`.BeniniI`)
    - Benini II correlation (:py:class:`.BeniniII`)
    - Bennet's S correlation (:py:class:`.Bennet`)
    - Braun-Blanquet similarity (:py:class:`.BraunBlanquet`)
    - Canberra distance (:py:class:`.Canberra`)
    - Cao similarity (:py:class:`.Cao`)
    - Chao's Dice similarity (:py:class:`.ChaoDice`)
    - Chao's Jaccard similarity (:py:class:`.ChaoJaccard`)
    - Chebyshev distance (:py:class:`.Chebyshev`)
    - Chord distance (:py:class:`.Chord`)
    - Clark distance (:py:class:`.Clark`)
    - Clement similarity (:py:class:`.Clement`)
    - Cohen's Kappa similarity (:py:class:`.CohenKappa`)
    - Cole correlation (:py:class:`.Cole`)
    - Consonni & Todeschini I similarity (:py:class:`.ConsonniTodeschiniI`)
    - Consonni & Todeschini II similarity (:py:class:`.ConsonniTodeschiniII`)
    - Consonni & Todeschini III similarity (:py:class:`.ConsonniTodeschiniIII`)
    - Consonni & Todeschini IV similarity (:py:class:`.ConsonniTodeschiniIV`)
    - Consonni & Todeschini V correlation (:py:class:`.ConsonniTodeschiniV`)
    - Cosine similarity (:py:class:`.Cosine`)
    - Dennis similarity (:py:class:`.Dennis`)
    - Dice's Asymmetric I similarity (:py:class:`.DiceAsymmetricI`)
    - Dice's Asymmetric II similarity (:py:class:`.DiceAsymmetricII`)
    - Digby correlation (:py:class:`.Digby`)
    - Dispersion correlation (:py:class:`.Dispersion`)
    - Doolittle similarity (:py:class:`.Doolittle`)
    - Dunning similarity (:py:class:`.Dunning`)
    - Euclidean distance (:py:class:`.Euclidean`)
    - Eyraud similarity (:py:class:`.Eyraud`)
    - Fager & McGowan similarity (:py:class:`.FagerMcGowan`)
    - Faith similarity (:py:class:`.Faith`)
    - Fidelity similarity (:py:class:`.Fidelity`)
    - Fleiss correlation (:py:class:`.Fleiss`)
    - Fleiss-Levin-Paik similarity (:py:class:`.FleissLevinPaik`)
    - Forbes I similarity (:py:class:`.ForbesI`)
    - Forbes II correlation (:py:class:`.ForbesII`)
    - Fossum similarity (:py:class:`.Fossum`)
    - Generalized Fleiss correlation (:py:class:`.GeneralizedFleiss`)
    - Gilbert correlation (:py:class:`.Gilbert`)
    - Gilbert & Wells similarity (:py:class:`.GilbertWells`)
    - Gini I correlation (:py:class:`.GiniI`)
    - Gini II correlation (:py:class:`.GiniII`)
    - Goodall similarity (:py:class:`.Goodall`)
    - Goodman & Kruskal's Lambda similarity (:py:class:`.GoodmanKruskalLambda`)
    - Goodman & Kruskal's Lambda-r correlation
      (:py:class:`.GoodmanKruskalLambdaR`)
    - Goodman & Kruskal's Tau A similarity (:py:class:`.GoodmanKruskalTauA`)
    - Goodman & Kruskal's Tau B similarity (:py:class:`.GoodmanKruskalTauB`)
    - Gower & Legendre similarity (:py:class:`.GowerLegendre`)
    - Guttman Lambda A similarity (:py:class:`.GuttmanLambdaA`)
    - Guttman Lambda B similarity (:py:class:`.GuttmanLambdaB`)
    - Gwet's AC correlation (:py:class:`.GwetAC`)
    - Hamann correlation (:py:class:`.Hamann`)
    - Harris & Lahey similarity (:py:class:`.HarrisLahey`)
    - Hassanat distance (:py:class:`.Hassanat`)
    - Hawkins & Dotson similarity (:py:class:`.HawkinsDotson`)
    - Hellinger distance (:py:class:`.Hellinger`)
    - Henderson-Heron similarity (:py:class:`.HendersonHeron`)
    - Horn-Morisita similarity (:py:class:`.HornMorisita`)
    - Hurlbert correlation (:py:class:`.Hurlbert`)
    - Jaccard similarity (:py:class:`.Jaccard`) &
      Tanimoto coefficient (:py:meth:`.Jaccard.tanimoto_coeff`)
    - Jaccard-NM similarity (:py:class:`.JaccardNM`)
    - Johnson similarity (:py:class:`.Johnson`)
    - Kendall's Tau correlation (:py:class:`.KendallTau`)
    - Kent & Foster I similarity (:py:class:`.KentFosterI`)
    - Kent & Foster II similarity (:py:class:`.KentFosterII`)
    - Köppen I correlation (:py:class:`.KoppenI`)
    - Köppen II similarity (:py:class:`.KoppenII`)
    - Kuder & Richardson correlation (:py:class:`.KuderRichardson`)
    - Kuhns I correlation (:py:class:`.KuhnsI`)
    - Kuhns II correlation (:py:class:`.KuhnsII`)
    - Kuhns III correlation (:py:class:`.KuhnsIII`)
    - Kuhns IV correlation (:py:class:`.KuhnsIV`)
    - Kuhns V correlation (:py:class:`.KuhnsV`)
    - Kuhns VI correlation (:py:class:`.KuhnsVI`)
    - Kuhns VII correlation (:py:class:`.KuhnsVII`)
    - Kuhns VIII correlation (:py:class:`.KuhnsVIII`)
    - Kuhns IX correlation (:py:class:`.KuhnsIX`)
    - Kuhns X correlation (:py:class:`.KuhnsX`)
    - Kuhns XI correlation (:py:class:`.KuhnsXI`)
    - Kuhns XII similarity (:py:class:`.KuhnsXII`)
    - Kulczynski I similarity (:py:class:`.KulczynskiI`)
    - Kulczynski II similarity (:py:class:`.KulczynskiII`)
    - Lorentzian distance (:py:class:`.Lorentzian`)
    - Maarel correlation (:py:class:`.Maarel`)
    - Manhattan distance (:py:class:`.Manhattan`)
    - Morisita similarity (:py:class:`.Morisita`)
    - marking distance (:py:class:`.Marking`)
    - marking metric (:py:class:`.MarkingMetric`)
    - MASI similarity (:py:class:`.MASI`)
    - Matusita distance (:py:class:`.Matusita`)
    - Maxwell & Pilliner correlation (:py:class:`.MaxwellPilliner`)
    - McConnaughey correlation (:py:class:`.McConnaughey`)
    - McEwen & Michael correlation (:py:class:`.McEwenMichael`)
    - mean squared contingency correlation (:py:class:`.MSContingency`)
    - Michael similarity (:py:class:`.Michael`)
    - Michelet similarity (:py:class:`.Michelet`)
    - Millar distance (:py:class:`.Millar`)
    - Minkowski distance (:py:class:`.Minkowski`)
    - Mountford similarity (:py:class:`.Mountford`)
    - Mutual Information similarity (:py:class:`.MutualInformation`)
    - Overlap distance (:py:class:`.Overlap`)
    - Pattern difference (:py:class:`.Pattern`)
    - Pearson & Heron II correlation (:py:class:`.PearsonHeronII`)
    - Pearson II similarity (:py:class:`.PearsonII`)
    - Pearson III correlation (:py:class:`.PearsonIII`)
    - Pearson's Chi-Squared similarity (:py:class:`.PearsonChiSquared`)
    - Pearson's Phi correlation (:py:class:`.PearsonPhi`)
    - Peirce correlation (:py:class:`.Peirce`)
    - q-gram distance (:py:class:`.QGram`)
    - Raup-Crick similarity (:py:class:`.RaupCrick`)
    - Rogers & Tanimoto similarity (:py:class:`.RogersTanimoto`)
    - Rogot & Goldberg similarity (:py:class:`.RogotGoldberg`)
    - Russell & Rao similarity (:py:class:`.RussellRao`)
    - Scott's Pi correlation (:py:class:`.ScottPi`)
    - Shape difference (:py:class:`.Shape`)
    - Size difference (:py:class:`.Size`)
    - Sokal & Michener similarity (:py:class:`.SokalMichener`)
    - Sokal & Sneath I similarity (:py:class:`.SokalSneathI`)
    - Sokal & Sneath II similarity (:py:class:`.SokalSneathII`)
    - Sokal & Sneath III similarity (:py:class:`.SokalSneathIII`)
    - Sokal & Sneath IV similarity (:py:class:`.SokalSneathIV`)
    - Sokal & Sneath V similarity (:py:class:`.SokalSneathV`)
    - Sørensen–Dice coefficient (:py:class:`.Dice`)
    - Sorgenfrei similarity (:py:class:`.Sorgenfrei`)
    - Steffensen similarity (:py:class:`.Steffensen`)
    - Stiles similarity (:py:class:`.Stiles`)
    - Stuart's Tau correlation (:py:class:`.StuartTau`)
    - Tarantula similarity (:py:class:`.Tarantula`)
    - Tarwid correlation (:py:class:`.Tarwid`)
    - Tetrachoric correlation coefficient (:py:class:`.Tetrachronic`)
    - Tulloss' R similarity (:py:class:`.TullossR`)
    - Tulloss' S similarity (:py:class:`.TullossS`)
    - Tulloss' T similarity (:py:class:`.TullossT`)
    - Tulloss' U similarity (:py:class:`.TullossU`)
    - Tversky distance (:py:class:`.Tversky`)
    - Weighted Jaccard similarity (:py:class:`.WeightedJaccard`)
    - Unigram subtuple similarity (:py:class:`.UnigramSubtuple`)
    - Unknown A correlation (:py:class:`.UnknownA`)
    - Unknown B similarity (:py:class:`.UnknownB`)
    - Unknown C similarity (:py:class:`.UnknownC`)
    - Unknown D similarity (:py:class:`.UnknownD`)
    - Unknown E correlation (:py:class:`.UnknownE`)
    - Unknown F similarity (:py:class:`.UnknownF`)
    - Unknown G similarity (:py:class:`.UnknownG`)
    - Unknown H similarity (:py:class:`.UnknownH`)
    - Unknown I similarity (:py:class:`.UnknownI`)
    - Unknown J similarity (:py:class:`.UnknownJ`)
    - Unknown K distance (:py:class:`.UnknownK`)
    - Unknown L similarity (:py:class:`.UnknownL`)
    - Unknown M similarity (:py:class:`.UnknownM`)
    - Upholt similarity (:py:class:`.Upholt`)
    - Warrens I correlation (:py:class:`.WarrensI`)
    - Warrens II similarity (:py:class:`.WarrensII`)
    - Warrens III correlation (:py:class:`.WarrensIII`)
    - Warrens IV similarity (:py:class:`.WarrensIV`)
    - Warrens V similarity (:py:class:`.WarrensV`)
    - Whittaker distance (:py:class:`.Whittaker`)
    - Yates' Chi-Squared similarity (:py:class:`.YatesChiSquared`)
    - Yule's Q correlation (:py:class:`.YuleQ`)
    - Yule's Q II distance (:py:class:`.YuleQII`)
    - Yule's Y correlation (:py:class:`.YuleY`)
    - YJHHR distance (:py:class:`.YJHHR`)

    - Bhattacharyya distance (:py:class:`.Bhattacharyya`)
    - Brainerd-Robinson similarity (:py:class:`.BrainerdRobinson`)
    - Quantitative Cosine similarity (:py:class:`.QuantitativeCosine`)
    - Quantitative Dice similarity (:py:class:`.QuantitativeDice`)
    - Quantitative Jaccard similarity (:py:class:`.QuantitativeJaccard`)
    - Roberts similarity (:py:class:`.Roberts`)
    - Average linkage distance (:py:class:`.AverageLinkage`)
    - Single linkage distance (:py:class:`.SingleLinkage`)
    - Complete linkage distance (:py:class:`.CompleteLinkage`)

    - Bag distance (:py:class:`.Bag`)
    - Soft cosine similarity (:py:class:`.SoftCosine`)
    - Monge-Elkan distance (:py:class:`.MongeElkan`)
    - TF-IDF similarity (:py:class:`.TFIDF`)
    - SoftTF-IDF similarity (:py:class:`.SoftTFIDF`)
    - Jensen-Shannon divergence (:py:class:`.JensenShannon`)
    - Simplified Fellegi-Sunter distance (:py:class:`.FellegiSunter`)
    - MinHash similarity (:py:class:`.MinHash`)

    - BLEU similarity (:py:class:`.BLEU`)
    - Rouge-L similarity (:py:class:`.RougeL`)
    - Rouge-W similarity (:py:class:`.RougeW`)
    - Rouge-S similarity (:py:class:`.RougeS`)
    - Rouge-SU similarity (:py:class:`.RougeSU`)

    - Positional Q-Gram Dice distance (:py:class:`.PositionalQGramDice`)
    - Positional Q-Gram Jaccard distance (:py:class:`.PositionalQGramJaccard`)
    - Positional Q-Gram Overlap distance (:py:class:`.PositionalQGramOverlap`)

Three popular sequence alignment algorithms are provided:

    - Needleman-Wunsch score (:py:class:`.NeedlemanWunsch`)
    - Smith-Waterman score (:py:class:`.SmithWaterman`)
    - Gotoh score (:py:class:`.Gotoh`)

Classes relating to substring and subsequence distances include:

    - Longest common subsequence (:py:class:`.LCSseq`)
    - Longest common substring (:py:class:`.LCSstr`)
    - Ratcliff-Obserhelp distance (:py:class:`.RatcliffObershelp`)

A number of simple distance classes provided in the package include:

    - Identity distance (:py:class:`.Ident`)
    - Length distance (:py:class:`.Length`)
    - Prefix distance (:py:class:`.Prefix`)
    - Suffix distance (:py:class:`.Suffix`)

Normalized compression distance classes for a variety of compression algorithms
are provided:

    - zlib (:py:class:`.NCDzlib`)
    - bzip2 (:py:class:`.NCDbz2`)
    - lzma (:py:class:`.NCDlzma`)
    - LZSS (:py:class:`.NCDlzss`)
    - arithmetic coding (:py:class:`.NCDarith`)
    - PAQ9A (:py:class:`.NCDpaq9a`)
    - BWT plus RLE (:py:class:`.NCDbwtrle`)
    - RLE (:py:class:`.NCDrle`)

Three similarity measures from SeatGeek's FuzzyWuzzy:

    - FuzzyWuzzy Partial String similarity
      (:py:class:`FuzzyWuzzyPartialString`)
    - FuzzyWuzzy Token Sort similarity (:py:class:`FuzzyWuzzyTokenSort`)
    - FuzzyWuzzy Token Set similarity (:py:class:`FuzzyWuzzyTokenSet`)

A convenience class, allowing one to pass a list of string transforms (phonetic
algorithms, string transforms, and/or stemmers) and, optionally, a string
distance measure to compute the similarity/distance of two strings that have
undergone each transform, is provided in:

    - Phonetic distance (:py:class:`.PhoneticDistance`)

The remaining distance measures & metrics include:

    - Western Airlines' Match Rating Algorithm comparison
      (:py:class:`.distance.MRA`)
    - Editex (:py:class:`.Editex`)
    - Bavarian Landesamt für Statistik distance (:py:class:`.Baystat`)
    - Eudex distance (:py:class:`.distance.Eudex`)
    - Sift4 distance (:py:class:`.Sift4`, :py:class:`.Sift4Simplest`,
      :py:class:`.Sift4Extended`)
    - Typo distance (:py:class:`.Typo`)
    - Synoname (:py:class:`.Synoname`)
    - Ozbay metric (:py:class:`.Ozbay`)
    - Indice de Similitude-Guth (:py:class:`.ISG`)
    - INClusion Programme (:py:class:`.Inclusion`)
    - Guth (:py:class:`.Guth`)
    - Victorian Panel Study (:py:class:`.VPS`)
    - LIG3 (:py:class:`.LIG3`)
    - String subsequence kernel (SSK) (:py:class:`.SSK`)

Most of the distance and similarity measures have ``sim`` and ``dist`` methods,
which return a measure that is normalized to the range :math:`[0, 1]`. The
normalized distance and similarity are always complements, so the normalized
distance will always equal 1 - the similarity for a particular measure supplied
with the same input. Some measures have an absolute distance method
``dist_abs`` and/or a similarity score ``sim_score``, which are not limited to
any range.

The first three methods can be demonstrated using the
:py:class:`.DamerauLevenshtein` class, while :py:class:`.SmithWaterman` offers
the fourth:

>>> dl = DamerauLevenshtein()
>>> dl.dist_abs('orange', 'strange')
2
>>> dl.dist('orange', 'strange')
0.2857142857142857
>>> dl.sim('orange', 'strange')
0.7142857142857143

>>> sw = SmithWaterman()
>>> sw.sim_score('TGTTACGG', 'GGTTGACTA')
4.0

----

"""

from abydos.distance._affinegap import AffineGapSimilarity, AffineGapDistance
from abydos.distance._aline import ALINE
from abydos.distance._ample import AMPLE
from abydos.distance._anderberg import Anderberg
from abydos.distance._andres_marzo_delta import AndresMarzoDelta
from abydos.distance._average_linkage import AverageLinkage
from abydos.distance._azzoo import AZZOO
from abydos.distance._bag import Bag
from abydos.distance._baroni_urbani_buser_i import BaroniUrbaniBuserI
from abydos.distance._baroni_urbani_buser_ii import BaroniUrbaniBuserII
from abydos.distance._batagelj_bren import BatageljBren
from abydos.distance._baulieu_i import BaulieuI
from abydos.distance._baulieu_ii import BaulieuII
from abydos.distance._baulieu_iii import BaulieuIII
from abydos.distance._baulieu_iv import BaulieuIV
from abydos.distance._baulieu_ix import BaulieuIX
from abydos.distance._baulieu_v import BaulieuV
from abydos.distance._baulieu_vi import BaulieuVI
from abydos.distance._baulieu_vii import BaulieuVII
from abydos.distance._baulieu_viii import BaulieuVIII
from abydos.distance._baulieu_x import BaulieuX
from abydos.distance._baulieu_xi import BaulieuXI
from abydos.distance._baulieu_xii import BaulieuXII
from abydos.distance._baulieu_xiii import BaulieuXIII
from abydos.distance._baulieu_xiv import BaulieuXIV
from abydos.distance._baulieu_xv import BaulieuXV
from abydos.distance._baystat import Baystat
from abydos.distance._benini_i import BeniniI
from abydos.distance._benini_ii import BeniniII
from abydos.distance._bennet import Bennet
from abydos.distance._bhattacharyya import Bhattacharyya
from abydos.distance._bisim import BISIM
from abydos.distance._bleu import BLEU
from abydos.distance._block_levenshtein import BlockLevenshtein
from abydos.distance._brainerd_robinson import BrainerdRobinson
from abydos.distance._braun_blanquet import BraunBlanquet
from abydos.distance._canberra import Canberra
from abydos.distance._cao import Cao
from abydos.distance._chao_dice import ChaoDice
from abydos.distance._chao_jaccard import ChaoJaccard
from abydos.distance._chebyshev import Chebyshev
from abydos.distance._chord import Chord
from abydos.distance._clark import Clark
from abydos.distance._clement import Clement
from abydos.distance._cohen_kappa import CohenKappa
from abydos.distance._cole import Cole
from abydos.distance._complete_linkage import CompleteLinkage
from abydos.distance._consonni_todeschini_i import ConsonniTodeschiniI
from abydos.distance._consonni_todeschini_ii import ConsonniTodeschiniII
from abydos.distance._consonni_todeschini_iii import ConsonniTodeschiniIII
from abydos.distance._consonni_todeschini_iv import ConsonniTodeschiniIV
from abydos.distance._consonni_todeschini_v import ConsonniTodeschiniV
from abydos.distance._cormode_lz import CormodeLZ
from abydos.distance._cosine import Cosine
from abydos.distance._covington import Covington
from abydos.distance._damerau_levenshtein import DamerauLevenshtein
from abydos.distance._dennis import Dennis
from abydos.distance._dice import Dice
from abydos.distance._dice_asymmetric_i import DiceAsymmetricI
from abydos.distance._dice_asymmetric_ii import DiceAsymmetricII
from abydos.distance._digby import Digby
from abydos.distance._discounted_levenshtein import DiscountedLevenshtein
from abydos.distance._dispersion import Dispersion
from abydos.distance._distance import _Distance
from abydos.distance._doolittle import Doolittle
from abydos.distance._dunning import Dunning
from abydos.distance._editex import Editex
from abydos.distance._euclidean import Euclidean
from abydos.distance._eudex import Eudex
from abydos.distance._eyraud import Eyraud
from abydos.distance._fager_mcgowan import FagerMcGowan
from abydos.distance._faith import Faith
from abydos.distance._fellegi_sunter import FellegiSunter
from abydos.distance._fidelity import Fidelity
from abydos.distance._fleiss import Fleiss
from abydos.distance._fleiss_levin_paik import FleissLevinPaik
from abydos.distance._flexmetric import FlexMetric
from abydos.distance._forbes_i import ForbesI
from abydos.distance._forbes_ii import ForbesII
from abydos.distance._fossum import Fossum
from abydos.distance._fuzzywuzzy_partial_string import FuzzyWuzzyPartialString
from abydos.distance._fuzzywuzzy_token_set import FuzzyWuzzyTokenSet
from abydos.distance._fuzzywuzzy_token_sort import FuzzyWuzzyTokenSort
from abydos.distance._generalized_fleiss import GeneralizedFleiss
from abydos.distance._gilbert import Gilbert
from abydos.distance._gilbert_wells import GilbertWells
from abydos.distance._gini_i import GiniI
from abydos.distance._gini_ii import GiniII
from abydos.distance._goodall import Goodall
from abydos.distance._goodman_kruskal_lambda import GoodmanKruskalLambda
from abydos.distance._goodman_kruskal_lambda_r import GoodmanKruskalLambdaR
from abydos.distance._goodman_kruskal_tau_a import GoodmanKruskalTauA
from abydos.distance._goodman_kruskal_tau_b import GoodmanKruskalTauB
from abydos.distance._gotoh import Gotoh
from abydos.distance._gower_legendre import GowerLegendre
from abydos.distance._guth import Guth
from abydos.distance._guttman_lambda_a import GuttmanLambdaA
from abydos.distance._guttman_lambda_b import GuttmanLambdaB
from abydos.distance._gwet_ac import GwetAC
from abydos.distance._hamann import Hamann
from abydos.distance._hamming import Hamming
from abydos.distance._harris_lahey import HarrisLahey
from abydos.distance._hassanat import Hassanat
from abydos.distance._hawkins_dotson import HawkinsDotson
from abydos.distance._hellinger import Hellinger
from abydos.distance._henderson_heron import HendersonHeron
from abydos.distance._higuera_mico import HigueraMico
from abydos.distance._horn_morisita import HornMorisita
from abydos.distance._hurlbert import Hurlbert
from abydos.distance._ident import Ident
from abydos.distance._inclusion import Inclusion
from abydos.distance._indel import Indel
from abydos.distance._isg import ISG
from abydos.distance._iterative_substring import IterativeSubString
from abydos.distance._jaccard import Jaccard
from abydos.distance._jaccard_nm import JaccardNM
from abydos.distance._jaro_winkler import JaroWinkler
from abydos.distance._jensen_shannon import JensenShannon
from abydos.distance._johnson import Johnson
from abydos.distance._kendall_tau import KendallTau
from abydos.distance._kent_foster_i import KentFosterI
from abydos.distance._kent_foster_ii import KentFosterII
from abydos.distance._koppen_i import KoppenI
from abydos.distance._koppen_ii import KoppenII
from abydos.distance._kuder_richardson import KuderRichardson
from abydos.distance._kuhns_i import KuhnsI
from abydos.distance._kuhns_ii import KuhnsII
from abydos.distance._kuhns_iii import KuhnsIII
from abydos.distance._kuhns_iv import KuhnsIV
from abydos.distance._kuhns_ix import KuhnsIX
from abydos.distance._kuhns_v import KuhnsV
from abydos.distance._kuhns_vi import KuhnsVI
from abydos.distance._kuhns_vii import KuhnsVII
from abydos.distance._kuhns_viii import KuhnsVIII
from abydos.distance._kuhns_x import KuhnsX
from abydos.distance._kuhns_xi import KuhnsXI
from abydos.distance._kuhns_xii import KuhnsXII
from abydos.distance._kulczynski_i import KulczynskiI
from abydos.distance._kulczynski_ii import KulczynskiII
from abydos.distance._lcprefix import LCPrefix
from abydos.distance._lcsseq import LCSseq
from abydos.distance._lcsstr import LCSstr
from abydos.distance._lcsuffix import LCSuffix
from abydos.distance._length import Length
from abydos.distance._levenshtein import Levenshtein
from abydos.distance._lig3 import LIG3
from abydos.distance._lorentzian import Lorentzian
from abydos.distance._maarel import Maarel
from abydos.distance._manhattan import Manhattan
from abydos.distance._marking import Marking
from abydos.distance._marking_metric import MarkingMetric
from abydos.distance._masi import MASI
from abydos.distance._matusita import Matusita
from abydos.distance._maxwell_pilliner import MaxwellPilliner
from abydos.distance._mcconnaughey import McConnaughey
from abydos.distance._mcewen_michael import McEwenMichael
from abydos.distance._meta_levenshtein import MetaLevenshtein
from abydos.distance._michelet import Michelet
from abydos.distance._millar import Millar
from abydos.distance._minhash import MinHash
from abydos.distance._minkowski import Minkowski
from abydos.distance._mlipns import MLIPNS
from abydos.distance._monge_elkan import MongeElkan
from abydos.distance._morisita import Morisita
from abydos.distance._mountford import Mountford
from abydos.distance._mra import MRA
from abydos.distance._ms_contingency import MSContingency
from abydos.distance._mutual_information import MutualInformation
from abydos.distance._ncd_arith import NCDarith
from abydos.distance._ncd_bwtrle import NCDbwtrle
from abydos.distance._ncd_bz2 import NCDbz2
from abydos.distance._ncd_lzma import NCDlzma
from abydos.distance._ncd_lzss import NCDlzss
from abydos.distance._ncd_paq9a import NCDpaq9a
from abydos.distance._ncd_rle import NCDrle
from abydos.distance._ncd_zlib import NCDzlib
from abydos.distance._needleman_wunsch import NeedlemanWunsch
from abydos.distance._overlap import Overlap
from abydos.distance._ozbay import Ozbay
from abydos.distance._pattern import Pattern
from abydos.distance._pearson_chi_squared import PearsonChiSquared
from abydos.distance._pearson_heron_ii import PearsonHeronII
from abydos.distance._pearson_ii import PearsonII
from abydos.distance._pearson_iii import PearsonIII
from abydos.distance._pearson_phi import PearsonPhi
from abydos.distance._peirce import Peirce
from abydos.distance._phonetic_distance import PhoneticDistance
from abydos.distance._phonetic_edit_distance import PhoneticEditDistance
from abydos.distance._positional_q_gram_dice import PositionalQGramDice
from abydos.distance._positional_q_gram_jaccard import PositionalQGramJaccard
from abydos.distance._positional_q_gram_overlap import PositionalQGramOverlap
from abydos.distance._prefix import Prefix
from abydos.distance._q_gram import QGram
from abydos.distance._quantitative_cosine import QuantitativeCosine
from abydos.distance._quantitative_dice import QuantitativeDice
from abydos.distance._quantitative_jaccard import QuantitativeJaccard
from abydos.distance._ratcliff_obershelp import RatcliffObershelp
from abydos.distance._raup_crick import RaupCrick
from abydos.distance._rees_levenshtein import ReesLevenshtein
from abydos.distance._relaxed_hamming import RelaxedHamming
from abydos.distance._roberts import Roberts
from abydos.distance._rogers_tanimoto import RogersTanimoto
from abydos.distance._rogot_goldberg import RogotGoldberg
from abydos.distance._rouge_l import RougeL
from abydos.distance._rouge_s import RougeS
from abydos.distance._rouge_su import RougeSU
from abydos.distance._rouge_w import RougeW
from abydos.distance._russell_rao import RussellRao
from abydos.distance._saps import SAPS
from abydos.distance._scott_pi import ScottPi
from abydos.distance._shape import Shape
from abydos.distance._shapira_storer_i import ShapiraStorerI
from abydos.distance._sift4 import Sift4
from abydos.distance._sift4_extended import Sift4Extended
from abydos.distance._sift4_simplest import Sift4Simplest
from abydos.distance._single_linkage import SingleLinkage
from abydos.distance._size import Size
from abydos.distance._smith_waterman import SmithWaterman
from abydos.distance._soft_cosine import SoftCosine
from abydos.distance._softtf_idf import SoftTFIDF
from abydos.distance._sokal_michener import SokalMichener
from abydos.distance._sokal_sneath_i import SokalSneathI
from abydos.distance._sokal_sneath_ii import SokalSneathII
from abydos.distance._sokal_sneath_iii import SokalSneathIII
from abydos.distance._sokal_sneath_iv import SokalSneathIV
from abydos.distance._sokal_sneath_v import SokalSneathV
from abydos.distance._sorgenfrei import Sorgenfrei
from abydos.distance._ssk import SSK
from abydos.distance._steffensen import Steffensen
from abydos.distance._stiles import Stiles
from abydos.distance._strcmp95 import Strcmp95
from abydos.distance._stuart_tau import StuartTau
from abydos.distance._suffix import Suffix
from abydos.distance._synoname import Synoname
from abydos.distance._tarantula import Tarantula
from abydos.distance._tarwid import Tarwid
from abydos.distance._tetrachoric import Tetrachoric
from abydos.distance._tf_idf import TFIDF
from abydos.distance._tichy import Tichy
from abydos.distance._token_distance import _TokenDistance
from abydos.distance._tulloss_r import TullossR
from abydos.distance._tulloss_s import TullossS
from abydos.distance._tulloss_t import TullossT
from abydos.distance._tulloss_u import TullossU
from abydos.distance._tversky import Tversky
from abydos.distance._typo import Typo
from abydos.distance._unigram_subtuple import UnigramSubtuple
from abydos.distance._unknown_a import UnknownA
from abydos.distance._unknown_b import UnknownB
from abydos.distance._unknown_c import UnknownC
from abydos.distance._unknown_d import UnknownD
from abydos.distance._unknown_e import UnknownE
from abydos.distance._unknown_f import UnknownF
from abydos.distance._unknown_g import UnknownG
from abydos.distance._unknown_h import UnknownH
from abydos.distance._unknown_i import UnknownI
from abydos.distance._unknown_j import UnknownJ
from abydos.distance._unknown_k import UnknownK
from abydos.distance._unknown_l import UnknownL
from abydos.distance._unknown_m import UnknownM
from abydos.distance._upholt import Upholt
from abydos.distance._vps import VPS
from abydos.distance._warrens_i import WarrensI
from abydos.distance._warrens_ii import WarrensII
from abydos.distance._warrens_iii import WarrensIII
from abydos.distance._warrens_iv import WarrensIV
from abydos.distance._warrens_v import WarrensV
from abydos.distance._weighted_jaccard import WeightedJaccard
from abydos.distance._whittaker import Whittaker
from abydos.distance._yates_chi_squared import YatesChiSquared
from abydos.distance._yjhhr import YJHHR
from abydos.distance._yujian_bo import YujianBo
from abydos.distance._yule_q import YuleQ
from abydos.distance._yule_q_ii import YuleQII
from abydos.distance._yule_y import YuleY

__all__ = [
    '_Distance',
    '_TokenDistance',
    'Levenshtein',
    'DamerauLevenshtein',
    'ShapiraStorerI',
    'Marking',
    'MarkingMetric',
    'YujianBo',
    'HigueraMico',
    'Indel',
    'SAPS',
    'MetaLevenshtein',
    'Covington',
    'ALINE',
    'FlexMetric',
    'BISIM',
    'DiscountedLevenshtein',
    'PhoneticEditDistance',
    'Hamming',
    'MLIPNS',
    'RelaxedHamming',
    'Tichy',
    'BlockLevenshtein',
    'CormodeLZ',
    'JaroWinkler',
    'Strcmp95',
    'IterativeSubString',
    'AMPLE',
    'AZZOO',
    'Anderberg',
    'AndresMarzoDelta',
    'BaroniUrbaniBuserI',
    'BaroniUrbaniBuserII',
    'BatageljBren',
    'BaulieuI',
    'BaulieuII',
    'BaulieuIII',
    'BaulieuIV',
    'BaulieuV',
    'BaulieuVI',
    'BaulieuVII',
    'BaulieuVIII',
    'BaulieuIX',
    'BaulieuX',
    'BaulieuXI',
    'BaulieuXII',
    'BaulieuXIII',
    'BaulieuXIV',
    'BaulieuXV',
    'BeniniI',
    'BeniniII',
    'Bennet',
    'BraunBlanquet',
    'Canberra',
    'Cao',
    'ChaoDice',
    'ChaoJaccard',
    'Chebyshev',
    'Chord',
    'Clark',
    'Clement',
    'CohenKappa',
    'Cole',
    'ConsonniTodeschiniI',
    'ConsonniTodeschiniII',
    'ConsonniTodeschiniIII',
    'ConsonniTodeschiniIV',
    'ConsonniTodeschiniV',
    'Cosine',
    'Dennis',
    'Dice',
    'DiceAsymmetricI',
    'DiceAsymmetricII',
    'Digby',
    'Dispersion',
    'Doolittle',
    'Dunning',
    'Euclidean',
    'Eyraud',
    'FagerMcGowan',
    'Faith',
    'Fidelity',
    'Fleiss',
    'FleissLevinPaik',
    'ForbesI',
    'ForbesII',
    'Fossum',
    'GeneralizedFleiss',
    'Gilbert',
    'GilbertWells',
    'GiniI',
    'GiniII',
    'Goodall',
    'GoodmanKruskalLambda',
    'GoodmanKruskalLambdaR',
    'GoodmanKruskalTauA',
    'GoodmanKruskalTauB',
    'GowerLegendre',
    'GuttmanLambdaA',
    'GuttmanLambdaB',
    'GwetAC',
    'Hamann',
    'HarrisLahey',
    'Hassanat',
    'HawkinsDotson',
    'Hellinger',
    'HendersonHeron',
    'HornMorisita',
    'Hurlbert',
    'Jaccard',
    'JaccardNM',
    'Johnson',
    'KendallTau',
    'KentFosterI',
    'KentFosterII',
    'KoppenI',
    'KoppenII',
    'KuderRichardson',
    'KuhnsI',
    'KuhnsII',
    'KuhnsIII',
    'KuhnsIV',
    'KuhnsV',
    'KuhnsVI',
    'KuhnsVII',
    'KuhnsVIII',
    'KuhnsIX',
    'KuhnsX',
    'KuhnsXI',
    'KuhnsXII',
    'KulczynskiI',
    'KulczynskiII',
    'Lorentzian',
    'Maarel',
    'Morisita',
    'Manhattan',
    'Michelet',
    'Millar',
    'Minkowski',
    'MASI',
    'Matusita',
    'MaxwellPilliner',
    'McConnaughey',
    'McEwenMichael',
    'Mountford',
    'MutualInformation',
    'MSContingency',
    'Overlap',
    'Pattern',
    'PearsonHeronII',
    'PearsonII',
    'PearsonIII',
    'PearsonChiSquared',
    'PearsonPhi',
    'Peirce',
    'QGram',
    'RaupCrick',
    'ReesLevenshtein',
    'RogersTanimoto',
    'RogotGoldberg',
    'RussellRao',
    'ScottPi',
    'Shape',
    'Size',
    'SokalMichener',
    'SokalSneathI',
    'SokalSneathII',
    'SokalSneathIII',
    'SokalSneathIV',
    'SokalSneathV',
    'Sorgenfrei',
    'Steffensen',
    'Stiles',
    'StuartTau',
    'Tarantula',
    'Tarwid',
    'Tetrachoric',
    'TullossR',
    'TullossS',
    'TullossT',
    'TullossU',
    'Tversky',
    'UnigramSubtuple',
    'UnknownA',
    'UnknownB',
    'UnknownC',
    'UnknownD',
    'UnknownE',
    'UnknownF',
    'UnknownG',
    'UnknownH',
    'UnknownI',
    'UnknownJ',
    'UnknownK',
    'UnknownL',
    'UnknownM',
    'Upholt',
    'WarrensI',
    'WarrensII',
    'WarrensIII',
    'WarrensIV',
    'WarrensV',
    'WeightedJaccard',
    'Whittaker',
    'YatesChiSquared',
    'YuleQ',
    'YuleQII',
    'YuleY',
    'YJHHR',
    'Bhattacharyya',
    'BrainerdRobinson',
    'QuantitativeCosine',
    'QuantitativeDice',
    'QuantitativeJaccard',
    'Roberts',
    'AverageLinkage',
    'SingleLinkage',
    'CompleteLinkage',
    'Bag',
    'SoftCosine',
    'MongeElkan',
    'TFIDF',
    'SoftTFIDF',
    'JensenShannon',
    'FellegiSunter',
    'MinHash',
    'BLEU',
    'RougeL',
    'RougeW',
    'RougeS',
    'RougeSU',
    'PositionalQGramDice',
    'PositionalQGramJaccard',
    'PositionalQGramOverlap',
    'NeedlemanWunsch',
    'SmithWaterman',
    'Gotoh',
    'LCSseq',
    'LCSstr',
    'LCPrefix',
    'LCSuffix',
    'RatcliffObershelp',
    'Ident',
    'Length',
    'Prefix',
    'Suffix',
    'NCDzlib',
    'NCDbz2',
    'NCDlzma',
    'NCDarith',
    'NCDbwtrle',
    'NCDrle',
    'NCDpaq9a',
    'NCDlzss',
    'FuzzyWuzzyPartialString',
    'FuzzyWuzzyTokenSort',
    'FuzzyWuzzyTokenSet',
    'PhoneticDistance',
    'MRA',
    'Editex',
    'Baystat',
    'Eudex',
    'Sift4',
    'Sift4Simplest',
    'Sift4Extended',
    'Typo',
    'Synoname',
    'Ozbay',
    'ISG',
    'Inclusion',
    'Guth',
    'VPS',
    'LIG3',
    'SSK',
]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
