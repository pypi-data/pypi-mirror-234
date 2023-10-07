"""Functional tests for FRAG.py"""

import os
import unittest.mock
import pytest
from pathlib import Path
from io import StringIO
from .context import rpg
from rpg import RapidPeptidesGenerator
from rpg import enzyme
from rpg import rule

@pytest.fixture
def truth():
    """ Solution """
    return [">A0A2C9KB11/1065-1162_0_Trypsin_2_2_289.29138_5.98\n",
            "DR\n",
            ">A0A2C9KB11/1065-1162_1_Trypsin_10_8_935.00128_4.29\n",
            "EALDSSWK\n",
            ">A0A2C9KB11/1065-1162_2_Trypsin_11_1_146.18938_8.06\n",
            "K\n",
            ">A0A2C9KB11/1065-1162_3_Trypsin_13_2_287.36218_9.71\n",
            "LR\n",
            ">A0A2C9KB11/1065-1162_4_Trypsin_19_6_503.51548_9.71\n",
            "SGAGGR\n",
            ">A0A2C9KB11/1065-1162_5_Trypsin_20_1_146.18938_8.06\n",
            "K\n",
            ">A0A2C9KB11/1065-1162_6_Trypsin_25_5_529.59668_9.71\n",
            "NAGIR\n",
            ">A0A2C9KB11/1065-1162_7_Trypsin_38_13_1623.99478_7.2\n",
            "LVLWMLDHVPNMR\n",
            ">A0A2C9KB11/1065-1162_8_Trypsin_42_4_535.60048_8.06\n",
            "NQFK\n",
            ">A0A2C9KB11/1065-1162_9_Trypsin_43_1_146.18938_8.06\n",
            "K\n",
            ">A0A2C9KB11/1065-1162_10_Trypsin_54_11_1297.43618_7.2\n",
            "FAHQPDSVLQR\n",
            ">A0A2C9KB11/1065-1162_11_Trypsin_64_10_1189.29028_3.89\n",
            "DPEFLAQVDR\n",
            ">A0A2C9KB11/1065-1162_12_Trypsin_88_24_2545.84688_3.63\n",
            "ILGGVESMINNVDDPVALEAAFDR\n",
            ">A0A2C9KB11/1065-1162_13_Trypsin_97_9_958.09728_5.22\n",
            "LADAHLSMT\n",
            ">A0A2C9KB11/1221-1332_0_Trypsin_2_2_303.31828_6.23\n",
            "ER\n",
            ">A0A2C9KB11/1221-1332_1_Trypsin_3_1_146.18938_8.06\n",
            "K\n",
            ">A0A2C9KB11/1221-1332_2_Trypsin_6_3_330.42758_8.06\n",
            "ALK\n",
            ">A0A2C9KB11/1221-1332_3_Trypsin_13_7_821.88518_5.87\n",
            "SSWDSLK\n",
            ">A0A2C9KB11/1221-1332_4_Trypsin_38_25_2643.03068_6.23\n",
            "SAAGGSQEAGVNLVLWMLQNVPNMR\n",
            ">A0A2C9KB11/1221-1332_5_Trypsin_40_2_289.29138_5.98\n",
            "DR\n",
            ">A0A2C9KB11/1221-1332_6_Trypsin_53_13_1463.56938_5.37\n",
            "FTFNAHQGDDALK\n",
            ">A0A2C9KB11/1221-1332_7_Trypsin_60_7_792.88708_4.29\n",
            "ADAEFIK\n",
            ">A0A2C9KB11/1221-1332_8_Trypsin_64_4_529.59678_9.71\n",
            "QVQR\n",
            ">A0A2C9KB11/1221-1332_9_Trypsin_81_17_1804.98958_3.89\n",
            "ITGGLESMIDNLDNQGK\n",
            ">A0A2C9KB11/1221-1332_10_Trypsin_88_7_785.89848_5.98\n",
            "LQAAIDR\n",
            ">A0A2C9KB11/1221-1332_11_Trypsin_110_22_2524.91728_5.5\n",
            "LVDAHLHMTPSVGLEYFEPLQK\n",
            ">A0A2C9KB11/1221-1332_12_Trypsin_111_1_132.11908_5.46\n",
            "N\n",
            ">A0A2C9KB11/1378-1486_0_Trypsin_2_2_289.29138_5.98\n",
            "DR\n",
            ">A0A2C9KB11/1378-1486_1_Trypsin_3_1_146.18938_8.06\n",
            "K\n",
            ">A0A2C9KB11/1378-1486_2_Trypsin_10_7_912.00988_6.12\n",
            "YIESSWK\n",
            ">A0A2C9KB11/1378-1486_3_Trypsin_11_1_146.18938_8.06\n",
            "K\n",
            ">A0A2C9KB11/1378-1486_4_Trypsin_21_10_947.99758_4.29\n",
            "LTDAAGGSEK\n",
            ">A0A2C9KB11/1378-1486_5_Trypsin_38_17_1994.29828_5.98\n",
            "AGTNFVFWLLDNVPNMR\n",
            ">A0A2C9KB11/1378-1486_6_Trypsin_40_2_289.29138_5.98\n",
            "DR\n",
            ">A0A2C9KB11/1378-1486_7_Trypsin_59_19_2255.34168_4.12\n",
            "FTFNAHQSDAALQEDEEFR\n",
            ">A0A2C9KB11/1378-1486_8_Trypsin_63_4_487.55648_8.06\n",
            "NQVK\n",
            ">A0A2C9KB11/1378-1486_9_Trypsin_108_45_4677.21938_4.05\n",
            "AITGGIESFVNNVNNPAALQSSIETLVDAHLNMQPSIGLSYFGSV\n",
            ">A0A2C9KB11/1535-1643_0_Trypsin_2_2_289.29138_5.98\n",
            "DR\n",
            ">A0A2C9KB11/1535-1643_1_Trypsin_3_1_174.20278_9.71\n",
            "R\n",
            ">A0A2C9KB11/1535-1643_2_Trypsin_10_7_775.90298_8.06\n",
            "AVVSSWK\n",
            ">A0A2C9KB11/1535-1643_3_Trypsin_11_1_146.18938_8.06\n",
            "K\n",
            ">A0A2C9KB11/1535-1643_4_Trypsin_17_6_603.67618_9.71\n",
            "LTASGR\n",
            ">A0A2C9KB11/1535-1643_5_Trypsin_36_19_2281.67528_5.98\n",
            "QSFGIDLVLWMFNNVPNMR\n",
            ">A0A2C9KB11/1535-1643_6_Trypsin_44_8_985.06128_4.29\n",
            "EQFTFDAK\n",
            ">A0A2C9KB11/1535-1643_7_Trypsin_51_7_803.82708_4.04\n",
            "QSDADLR\n",
            ">A0A2C9KB11/1535-1643_8_Trypsin_52_1_174.20278_9.71\n",
            "R\n",
            ">A0A2C9KB11/1535-1643_9_Trypsin_58_6_732.83448_5.87\n",
            "DPNFLK\n",
            ">A0A2C9KB11/1535-1643_10_Trypsin_79_21_2158.36788_3.75\n",
            "QVNSIVNGLGDMVDSVNDPGK\n",
            ">A0A2C9KB11/1535-1643_11_Trypsin_86_7_842.95038_6.23\n",
            "LQANLER\n",
            ">A0A2C9KB11/1535-1643_12_Trypsin_108_22_2521.94168_5.57\n",
            "LSEIHLHFVPSVGPEFFVPLEK\n",
            ">A0A2C9K1A5/128-239_0_Trypsin_3_3_374.43738_5.87\n",
            "DIK\n",
            ">A0A2C9K1A5/128-239_1_Trypsin_11_8_919.98958_5.87\n",
            "ALDSSWNK\n",
            ">A0A2C9K1A5/128-239_2_Trypsin_19_8_759.81728_5.98\n",
            "LTAGADGR\n",
            ">A0A2C9K1A5/128-239_3_Trypsin_37_18_2120.51518_9.71\n",
            "TTFGNNLVLWMLNVPNMR\n",
            ">A0A2C9K1A5/128-239_4_Trypsin_39_2_303.31828_6.23\n",
            "ER\n",
            ">A0A2C9K1A5/128-239_5_Trypsin_42_3_392.49858_8.06\n",
            "FVK\n",
            ">A0A2C9K1A5/128-239_6_Trypsin_53_11_1259.34088_5.53\n",
            "FNAHQSDEALK\n",
            ">A0A2C9K1A5/128-239_7_Trypsin_60_7_835.91208_4.29\n",
            "NDAEFIK\n",
            ">A0A2C9K1A5/128-239_8_Trypsin_63_3_373.45268_8.06\n",
            "QVK\n",
            ">A0A2C9K1A5/128-239_9_Trypsin_111_48_5318.17868_6.16\n",
            "LIVGGLQTLIINLNNPGQLQASIEHLADVHLHMKPSIGLEYFKPLQEN\n",
            ">A0A2C9K1A5/285-395_0_Trypsin_2_2_261.27798_5.87\n",
            "DK\n",
            ">A0A2C9K1A5/285-395_1_Trypsin_11_9_1034.13688_6.23\n",
            "VALESSWSR\n",
            ">A0A2C9K1A5/285-395_2_Trypsin_19_8_758.87288_8.06\n",
            "LTAGVNGK\n",
            ">A0A2C9K1A5/285-395_3_Trypsin_20_1_174.20278_9.71\n",
            "R\n",
            ">A0A2C9K1A5/285-395_4_Trypsin_25_5_515.56988_9.71\n",
            "NAGVR\n",
            ">A0A2C9K1A5/285-395_5_Trypsin_37_12_1520.87088_5.98\n",
            "LVLWMFNVPDMR\n",
            ">A0A2C9K1A5/285-395_6_Trypsin_39_2_303.31828_6.23\n",
            "ER\n",
            ">A0A2C9K1A5/285-395_7_Trypsin_42_3_422.48448_9.71\n",
            "FTR\n",
            ">A0A2C9K1A5/285-395_8_Trypsin_46_4_478.54858_8.06\n",
            "FNAK\n",
            ">A0A2C9K1A5/285-395_9_Trypsin_53_7_789.84058_4.29\n",
            "QSDEALK\n",
            ">A0A2C9K1A5/285-395_10_Trypsin_60_7_822.91338_4.29\n",
            "TDAEFLK\n",
            ">A0A2C9K1A5/285-395_11_Trypsin_85_25_2798.14518_3.68\n",
            "QVDVIIGGFETLINNLNDPTLLQDR\n",
            ">A0A2C9K1A5/285-395_12_Trypsin_96_11_1225.36408_4.66\n",
            "LESLADAHLEK\n",
            ">A0A2C9K1A5/285-395_13_Trypsin_110_14_1504.79238_8.32\n",
            "KPAIGVSYFGPLQK\n",
            ">A0A2C9K1A5/588-698_0_Trypsin_2_2_261.27798_5.87\n",
            "DK\n",
            ">A0A2C9K1A5/588-698_1_Trypsin_3_1_146.18938_8.06\n",
            "K\n",
            ">A0A2C9K1A5/588-698_2_Trypsin_25_22_2285.50118_8.06\n",
            "ALQSSWNTLVNQAGGQQNAGIK\n",
            ">A0A2C9K1A5/588-698_3_Trypsin_37_12_1519.88608_9.71\n",
            "LVLWMFNVPNMR\n",
            ">A0A2C9K1A5/588-698_4_Trypsin_39_2_289.29138_5.98\n",
            "DR\n",
            ">A0A2C9K1A5/588-698_5_Trypsin_42_3_380.44418_8.06\n",
            "FSK\n",
            ">A0A2C9K1A5/588-698_6_Trypsin_53_11_1204.26148_5.37\n",
            "FNAHSSDDALK\n",
            ">A0A2C9K1A5/588-698_7_Trypsin_60_7_792.88708_4.29\n",
            "ADAEFLK\n",
            ">A0A2C9K1A5/588-698_8_Trypsin_81_21_2198.41478_3.68\n",
            "QVNVIVGGLESLVNNVDDADK\n",
            ">A0A2C9K1A5/588-698_9_Trypsin_88_7_771.87168_6.23\n",
            "LQAGVER\n",
            ">A0A2C9K1A5/588-698_10_Trypsin_110_22_2438.78338_5.38\n",
            "LVDAHLHMSPSVGLEYFGPLQQ\n",
            ">A0A2C9K1A5/745-855_0_Trypsin_2_2_289.29138_5.98\n",
            "DR\n",
            ">A0A2C9K1A5/745-855_1_Trypsin_3_1_146.18938_8.06\n",
            "K\n",
            ">A0A2C9K1A5/745-855_2_Trypsin_7_4_515.61028_6.23\n",
            "VLER\n",
            ">A0A2C9K1A5/745-855_3_Trypsin_19_12_1257.41158_8.06\n",
            "TWNQLISGPGGK\n",
            ">A0A2C9K1A5/745-855_4_Trypsin_21_2_275.30488_6.13\n",
            "EK\n",
            ">A0A2C9K1A5/745-855_5_Trypsin_25_4_387.47948_8.06\n",
            "AGIK\n",
            ">A0A2C9K1A5/745-855_6_Trypsin_38_13_1649.00158_6.23\n",
            "LVLWMFENVPNMR\n",
            ">A0A2C9K1A5/745-855_7_Trypsin_43_5_623.66348_5.87\n",
            "DQFSK\n",
            ">A0A2C9K1A5/745-855_8_Trypsin_48_5_616.67448_7.08\n",
            "FDAHK\n",
            ">A0A2C9K1A5/745-855_9_Trypsin_60_12_1349.50358_4.67\n",
            "SDEALSKPEFVK\n",
            ">A0A2C9K1A5/745-855_10_Trypsin_96_36_3961.35988_4.38\n",
            "QVNNIFGGLESILNNLNKPGQLQSALENLADDHLDR\n",
            ">A0A2C9K1A5/745-855_11_Trypsin_99_3_399.49358_9.93\n",
            "KPR\n",
            ">A0A2C9K1A5/745-855_12_Trypsin_110_11_1248.48748_6.13\n",
            "IGLEFFGPLQK\n",
            ">A0A2C9K1A5/935-1004_0_Trypsin_10_10_1288.50498_7.2\n",
            "QMFEHVPNMR\n",
            ">A0A2C9K1A5/935-1004_1_Trypsin_15_5_651.71728_6.13\n",
            "EQFTK\n",
            ">A0A2C9K1A5/935-1004_2_Trypsin_26_11_1211.34268_7.08\n",
            "FDAHQPNAALK\n",
            ">A0A2C9K1A5/935-1004_3_Trypsin_37_11_1258.39948_6.23\n",
            "QNPEFLAQVGR\n",
            ">A0A2C9K1A5/935-1004_4_Trypsin_55_18_1881.15618_3.89\n",
            "ILGGIESLLNNDDPVALK\n",
            ">A0A2C9K1A5/935-1004_5_Trypsin_60_5_544.60838_5.98\n",
            "AAIDR\n",
            ">A0A2C9K1A5/935-1004_6_Trypsin_69_9_944.07038_5.22\n",
            "LADAHLSMS\n"]

@pytest.fixture
def truth_ipc():
    """ Solution """
    return [">A0A2C9KB11/1065-1162_0_Trypsin_2_2_289.29138_6.73\n",
            "DR\n",
            ">A0A2C9KB11/1065-1162_1_Trypsin_10_8_935.00128_4.12\n",
            "EALDSSWK\n",
            ">A0A2C9KB11/1065-1162_2_Trypsin_11_1_146.18938_10.04\n",
            "K\n",
            ">A0A2C9KB11/1065-1162_3_Trypsin_13_2_287.36218_11.04\n",
            "LR\n",
            ">A0A2C9KB11/1065-1162_4_Trypsin_19_6_503.51548_11.04\n",
            "SGAGGR\n",
            ">A0A2C9KB11/1065-1162_5_Trypsin_20_1_146.18938_10.04\n",
            "K\n",
            ">A0A2C9KB11/1065-1162_6_Trypsin_25_5_529.59668_11.04\n",
            "NAGIR\n",
            ">A0A2C9KB11/1065-1162_7_Trypsin_38_13_1623.99478_7.79\n",
            "LVLWMLDHVPNMR\n",
            ">A0A2C9KB11/1065-1162_8_Trypsin_42_4_535.60048_10.04\n",
            "NQFK\n",
            ">A0A2C9KB11/1065-1162_9_Trypsin_43_1_146.18938_10.04\n",
            "K\n",
            ">A0A2C9KB11/1065-1162_10_Trypsin_54_11_1297.43618_7.79\n",
            "FAHQPDSVLQR\n",
            ">A0A2C9KB11/1065-1162_11_Trypsin_64_10_1189.29028_3.74\n",
            "DPEFLAQVDR\n",
            ">A0A2C9KB11/1065-1162_12_Trypsin_88_24_2545.84688_3.47\n",
            "ILGGVESMINNVDDPVALEAAFDR\n",
            ">A0A2C9KB11/1065-1162_13_Trypsin_97_9_958.09728_4.96\n",
            "LADAHLSMT\n",
            ">A0A2C9KB11/1221-1332_0_Trypsin_2_2_303.31828_6.94\n",
            "ER\n",
            ">A0A2C9KB11/1221-1332_1_Trypsin_3_1_146.18938_10.04\n",
            "K\n",
            ">A0A2C9KB11/1221-1332_2_Trypsin_6_3_330.42758_10.04\n",
            "ALK\n",
            ">A0A2C9KB11/1221-1332_3_Trypsin_13_7_821.88518_6.71\n",
            "SSWDSLK\n",
            ">A0A2C9KB11/1221-1332_4_Trypsin_38_25_2643.03068_6.94\n",
            "SAAGGSQEAGVNLVLWMLQNVPNMR\n",
            ">A0A2C9KB11/1221-1332_5_Trypsin_40_2_289.29138_6.73\n",
            "DR\n",
            ">A0A2C9KB11/1221-1332_6_Trypsin_53_13_1463.56938_5.12\n",
            "FTFNAHQGDDALK\n",
            ">A0A2C9KB11/1221-1332_7_Trypsin_60_7_792.88708_4.12\n",
            "ADAEFIK\n",
            ">A0A2C9KB11/1221-1332_8_Trypsin_64_4_529.59678_11.04\n",
            "QVQR\n",
            ">A0A2C9KB11/1221-1332_9_Trypsin_81_17_1804.98958_3.74\n",
            "ITGGLESMIDNLDNQGK\n",
            ">A0A2C9KB11/1221-1332_10_Trypsin_88_7_785.89848_6.73\n",
            "LQAAIDR\n",
            ">A0A2C9KB11/1221-1332_11_Trypsin_110_22_2524.91728_5.22\n",
            "LVDAHLHMTPSVGLEYFEPLQK\n",
            ">A0A2C9KB11/1221-1332_12_Trypsin_111_1_132.11908_5.97\n",
            "N\n",
            ">A0A2C9KB11/1378-1486_0_Trypsin_2_2_289.29138_6.73\n",
            "DR\n",
            ">A0A2C9KB11/1378-1486_1_Trypsin_3_1_146.18938_10.04\n",
            "K\n",
            ">A0A2C9KB11/1378-1486_2_Trypsin_10_7_912.00988_6.87\n",
            "YIESSWK\n",
            ">A0A2C9KB11/1378-1486_3_Trypsin_11_1_146.18938_10.04\n",
            "K\n",
            ">A0A2C9KB11/1378-1486_4_Trypsin_21_10_947.99758_4.12\n",
            "LTDAAGGSEK\n",
            ">A0A2C9KB11/1378-1486_5_Trypsin_38_17_1994.29828_6.73\n",
            "AGTNFVFWLLDNVPNMR\n",
            ">A0A2C9KB11/1378-1486_6_Trypsin_40_2_289.29138_6.73\n",
            "DR\n",
            ">A0A2C9KB11/1378-1486_7_Trypsin_59_19_2255.34168_3.97\n",
            "FTFNAHQSDAALQEDEEFR\n",
            ">A0A2C9KB11/1378-1486_8_Trypsin_63_4_487.55648_10.04\n",
            "NQVK\n",
            ">A0A2C9KB11/1378-1486_9_Trypsin_108_45_4677.21938_3.88\n",
            "AITGGIESFVNNVNNPAALQSSIETLVDAHLNMQPSIGLSYFGSV\n",
            ">A0A2C9KB11/1535-1643_0_Trypsin_2_2_289.29138_6.73\n",
            "DR\n",
            ">A0A2C9KB11/1535-1643_1_Trypsin_3_1_174.20278_11.04\n",
            "R\n",
            ">A0A2C9KB11/1535-1643_2_Trypsin_10_7_775.90298_10.04\n",
            "AVVSSWK\n",
            ">A0A2C9KB11/1535-1643_3_Trypsin_11_1_146.18938_10.04\n",
            "K\n",
            ">A0A2C9KB11/1535-1643_4_Trypsin_17_6_603.67618_11.04\n",
            "LTASGR\n",
            ">A0A2C9KB11/1535-1643_5_Trypsin_36_19_2281.67528_6.73\n",
            "QSFGIDLVLWMFNNVPNMR\n",
            ">A0A2C9KB11/1535-1643_6_Trypsin_44_8_985.06128_4.12\n",
            "EQFTFDAK\n",
            ">A0A2C9KB11/1535-1643_7_Trypsin_51_7_803.82708_3.92\n",
            "QSDADLR\n",
            ">A0A2C9KB11/1535-1643_8_Trypsin_52_1_174.20278_11.04\n",
            "R\n",
            ">A0A2C9KB11/1535-1643_9_Trypsin_58_6_732.83448_6.71\n",
            "DPNFLK\n",
            ">A0A2C9KB11/1535-1643_10_Trypsin_79_21_2158.36788_3.62\n",
            "QVNSIVNGLGDMVDSVNDPGK\n",
            ">A0A2C9KB11/1535-1643_11_Trypsin_86_7_842.95038_6.94\n",
            "LQANLER\n",
            ">A0A2C9KB11/1535-1643_12_Trypsin_108_22_2521.94168_5.27\n",
            "LSEIHLHFVPSVGPEFFVPLEK\n",
            ">A0A2C9K1A5/128-239_0_Trypsin_3_3_374.43738_6.71\n",
            "DIK\n",
            ">A0A2C9K1A5/128-239_1_Trypsin_11_8_919.98958_6.71\n",
            "ALDSSWNK\n",
            ">A0A2C9K1A5/128-239_2_Trypsin_19_8_759.81728_6.73\n",
            "LTAGADGR\n",
            ">A0A2C9K1A5/128-239_3_Trypsin_37_18_2120.51518_11.04\n",
            "TTFGNNLVLWMLNVPNMR\n",
            ">A0A2C9K1A5/128-239_4_Trypsin_39_2_303.31828_6.94\n",
            "ER\n",
            ">A0A2C9K1A5/128-239_5_Trypsin_42_3_392.49858_10.04\n",
            "FVK\n",
            ">A0A2C9K1A5/128-239_6_Trypsin_53_11_1259.34088_5.26\n",
            "FNAHQSDEALK\n",
            ">A0A2C9K1A5/128-239_7_Trypsin_60_7_835.91208_4.12\n",
            "NDAEFIK\n",
            ">A0A2C9K1A5/128-239_8_Trypsin_63_3_373.45268_10.04\n",
            "QVK\n",
            ">A0A2C9K1A5/128-239_9_Trypsin_111_48_5318.17868_5.79\n",
            "LIVGGLQTLIINLNNPGQLQASIEHLADVHLHMKPSIGLEYFKPLQEN\n",
            ">A0A2C9K1A5/285-395_0_Trypsin_2_2_261.27798_6.71\n",
            "DK\n",
            ">A0A2C9K1A5/285-395_1_Trypsin_11_9_1034.13688_6.94\n",
            "VALESSWSR\n",
            ">A0A2C9K1A5/285-395_2_Trypsin_19_8_758.87288_10.04\n",
            "LTAGVNGK\n",
            ">A0A2C9K1A5/285-395_3_Trypsin_20_1_174.20278_11.04\n",
            "R\n",
            ">A0A2C9K1A5/285-395_4_Trypsin_25_5_515.56988_11.04\n",
            "NAGVR\n",
            ">A0A2C9K1A5/285-395_5_Trypsin_37_12_1520.87088_6.73\n",
            "LVLWMFNVPDMR\n",
            ">A0A2C9K1A5/285-395_6_Trypsin_39_2_303.31828_6.94\n",
            "ER\n",
            ">A0A2C9K1A5/285-395_7_Trypsin_42_3_422.48448_11.04\n",
            "FTR\n",
            ">A0A2C9K1A5/285-395_8_Trypsin_46_4_478.54858_10.04\n",
            "FNAK\n",
            ">A0A2C9K1A5/285-395_9_Trypsin_53_7_789.84058_4.12\n",
            "QSDEALK\n",
            ">A0A2C9K1A5/285-395_10_Trypsin_60_7_822.91338_4.12\n",
            "TDAEFLK\n",
            ">A0A2C9K1A5/285-395_11_Trypsin_85_25_2798.14518_3.53\n",
            "QVDVIIGGFETLINNLNDPTLLQDR\n",
            ">A0A2C9K1A5/285-395_12_Trypsin_96_11_1225.36408_4.48\n",
            "LESLADAHLEK\n",
            ">A0A2C9K1A5/285-395_13_Trypsin_110_14_1504.79238_10.18\n",
            "KPAIGVSYFGPLQK\n",
            ">A0A2C9K1A5/588-698_0_Trypsin_2_2_261.27798_6.71\n",
            "DK\n",
            ">A0A2C9K1A5/588-698_1_Trypsin_3_1_146.18938_10.04\n",
            "K\n",
            ">A0A2C9K1A5/588-698_2_Trypsin_25_22_2285.50118_10.04\n",
            "ALQSSWNTLVNQAGGQQNAGIK\n",
            ">A0A2C9K1A5/588-698_3_Trypsin_37_12_1519.88608_11.04\n",
            "LVLWMFNVPNMR\n",
            ">A0A2C9K1A5/588-698_4_Trypsin_39_2_289.29138_6.73\n",
            "DR\n",
            ">A0A2C9K1A5/588-698_5_Trypsin_42_3_380.44418_10.04\n",
            "FSK\n",
            ">A0A2C9K1A5/588-698_6_Trypsin_53_11_1204.26148_5.12\n",
            "FNAHSSDDALK\n",
            ">A0A2C9K1A5/588-698_7_Trypsin_60_7_792.88708_4.12\n",
            "ADAEFLK\n",
            ">A0A2C9K1A5/588-698_8_Trypsin_81_21_2198.41478_3.53\n",
            "QVNVIVGGLESLVNNVDDADK\n",
            ">A0A2C9K1A5/588-698_9_Trypsin_88_7_771.87168_6.94\n",
            "LQAGVER\n",
            ">A0A2C9K1A5/588-698_10_Trypsin_110_22_2438.78338_5.08\n",
            "LVDAHLHMSPSVGLEYFGPLQQ\n",
            ">A0A2C9K1A5/745-855_0_Trypsin_2_2_289.29138_6.73\n",
            "DR\n",
            ">A0A2C9K1A5/745-855_1_Trypsin_3_1_146.18938_10.04\n",
            "K\n",
            ">A0A2C9K1A5/745-855_2_Trypsin_7_4_515.61028_6.94\n",
            "VLER\n",
            ">A0A2C9K1A5/745-855_3_Trypsin_19_12_1257.41158_10.04\n",
            "TWNQLISGPGGK\n",
            ">A0A2C9K1A5/745-855_4_Trypsin_21_2_275.30488_6.92\n",
            "EK\n",
            ">A0A2C9K1A5/745-855_5_Trypsin_25_4_387.47948_10.04\n",
            "AGIK\n",
            ">A0A2C9K1A5/745-855_6_Trypsin_38_13_1649.00158_6.94\n",
            "LVLWMFENVPNMR\n",
            ">A0A2C9K1A5/745-855_7_Trypsin_43_5_623.66348_6.71\n",
            "DQFSK\n",
            ">A0A2C9K1A5/745-855_8_Trypsin_48_5_616.67448_7.77\n",
            "FDAHK\n",
            ">A0A2C9K1A5/745-855_9_Trypsin_60_12_1349.50358_4.49\n",
            "SDEALSKPEFVK\n",
            ">A0A2C9K1A5/745-855_10_Trypsin_96_36_3961.35988_4.25\n",
            "QVNNIFGGLESILNNLNKPGQLQSALENLADDHLDR\n",
            ">A0A2C9K1A5/745-855_11_Trypsin_99_3_399.49358_11.53\n",
            "KPR\n",
            ">A0A2C9K1A5/745-855_12_Trypsin_110_11_1248.48748_6.92\n",
            "IGLEFFGPLQK\n",
            ">A0A2C9K1A5/935-1004_0_Trypsin_10_10_1288.50498_7.8\n",
            "QMFEHVPNMR\n",
            ">A0A2C9K1A5/935-1004_1_Trypsin_15_5_651.71728_6.92\n",
            "EQFTK\n",
            ">A0A2C9K1A5/935-1004_2_Trypsin_26_11_1211.34268_7.77\n",
            "FDAHQPNAALK\n",
            ">A0A2C9K1A5/935-1004_3_Trypsin_37_11_1258.39948_6.94\n",
            "QNPEFLAQVGR\n",
            ">A0A2C9K1A5/935-1004_4_Trypsin_55_18_1881.15618_3.74\n",
            "ILGGIESLLNNDDPVALK\n",
            ">A0A2C9K1A5/935-1004_5_Trypsin_60_5_544.60838_6.73\n",
            "AAIDR\n",
            ">A0A2C9K1A5/935-1004_6_Trypsin_69_9_944.07038_4.96\n",
            "LADAHLSMS\n"]

@pytest.fixture
def file_a(tmp_path):
    """ Good fasta file """
    file_name = tmp_path.joinpath("A.fasta")
    with open(file_name, "w", encoding="utf-8") as f_file:
        f_file.write(">A0A2C9KB11/1065-1162\n"\
                     "DREALDSSWKKLRSgagGRKNAGIRLVLWMLDHVPNMRNQFKKFAHQPDSVLQRDPE\n"\
                     "FLAQVDRILGGVESMINNVDDPVALEAAFDRLADAHLSMT\n"\
                     ">A0A2C9KB11/1221-1332\n"\
                     "ERKALKSSWDSLKSaagGSQEAGVNLVLWMLQNVPNMRDRFTFNAHQGDDALKADAE\n"\
                     "FIKQVQRITGGLESMIDNLDNQGKLQAAIDRLVDAHLHMTpSVGLEYFEPLQKN\n"\
                     ">A0A2C9KB11/1378-1486\n"\
                     "DRKYIESSWKKLTDaagGSEKAGTNFVFWLLDNVPNMRDRFTFNAHQSDAALQEDEE\n"\
                     "FRNQVKAITGGIESFVNNVNNPAALQSSIETLVDAHLNMQpSIGLSYFGSV\n"\
                     ">A0A2C9KB11/1535-1643\n"\
                     "DRRAVVSSWKKLTAsGRQSFGIDLVLWMFNNVPNMREQFTFDAKQSDADLRRDPNFL\n"\
                     "KQVNSIVNGLGDMVDSVNDPGKLQANLERLSEIHLHFVpSVGPEFFVPLEK\n"\
                     ">A0A2C9K1A5/128-239\n"\
                     "DIKALDSSWNKLTAgadGRTTFGNNLVLWMLNVPNMRERFVKFNAHQSDEALKNDAE\n"\
                     "FIKQVKLIVGGLQTLIINLNNPGQLQASIEHLADVHLHMKpSIGLEYFKPLQEN\n"\
                     ">A0A2C9K1A5/285-395\n"\
                     "DKVALESSWSRLTAgvnGKRNAGVRLVLWMFNVPDMRERFTRFNAKQSDEALKTDAE\n"\
                     "FLKQVDVIIGGFETLINNLNDPTLLQDRLESLADAHLEKKpAIGVSYFGPLQK\n"\
                     ">A0A2C9K1A5/588-698\n"\
                     "DKKALQSSWNTLVNqagGQQNAGIKLVLWMFNVPNMRDRFSKFNAHSSDDALKADAE\n"\
                     "FLKQVNVIVGGLESLVNNVDDADKLQAGVERLVDAHLHMSpSVGLEYFGPLQQ\n"\
                     ">A0A2C9K1A5/745-855\n"\
                     "DRKVLERTWNQLISgpgGKEKAGIKLVLWMFENVPNMRDQFSKFDAHKSDEALSKPE\n"\
                     "FVKQVNNIFGGLESILNNLNKPGQLQSALENLADDHLDRKpRIGLEFFGPLQK\n"\
                     ">A0A2C9K1A5/935-1004\n"\
                     "QMFEHVPNMREQFTKFDAHQPNAALKQNPEFLAQVGRILGGIESLLNNDDPVALKAA\n"\
                     "IDRLADAHLSMS\n")
    return file_name

@pytest.fixture
def list_enz():
    """ Result for listing enzymes """
    return "1: Arg-C\n"\
           "2: Asp-N\n"\
           "3: BNPS-Skatole\n"\
           "4: Bromelain\n"\
           "5: Caspase-1\n"\
           "6: Caspase-2\n"\
           "7: Caspase-3\n"\
           "8: Caspase-4\n"\
           "9: Caspase-5\n"\
           "10: Caspase-6\n"\
           "11: Caspase-7\n"\
           "12: Caspase-8\n"\
           "13: Caspase-9\n"\
           "14: Caspase-10\n"\
           "15: Chymotrypsin-high\n"\
           "16: Chymotrypsin-low\n"\
           "17: Clostripain\n"\
           "18: CNBr\n"\
           "19: Enterokinase\n"\
           "20: Factor-Xa\n"\
           "21: Ficin\n"\
           "22: Formic-acid\n"\
           "23: Glu-C\n"\
           "24: Glutamyl-endopeptidase\n"\
           "25: Granzyme-B\n"\
           "26: Hydroxylamine\n"\
           "27: Iodosobenzoic-acid\n"\
           "28: Lys-C\n"\
           "29: Lys-N\n"\
           "30: Neutrophil-elastase\n"\
           "31: NTCB\n"\
           "32: Papain\n"\
           "33: Pepsin-pH1.3\n"\
           "34: Pepsin-pH>=2\n"\
           "35: Proline-endopeptidase\n"\
           "36: Proteinase-K\n"\
           "37: Staphylococcal-peptidase-I\n"\
           "38: Thermolysin\n"\
           "39: Thrombin\n"\
           "40: Thrombin-SG\n"\
           "41: Tobacco-Etch-Virus\n"\
           "42: Trypsin\n"\
           "43: Asp-N Endopeptidase"

@pytest.fixture
def res_dig_1_42():
    """ Result for digestion with 1 and 42 and IPC2 """
    return ">Input_0_Arg-C_2_2_289.29138_5.98\n"\
           "DR\n"\
           ">Input_1_Arg-C_13_11_1332.52228_7.79\n"\
           "EALDSSWKKLR\n"\
           ">Input_2_Arg-C_19_6_503.51548_9.71\n"\
           "SGAGGR\n"\
           ">Input_3_Arg-C_25_6_657.77078_9.93\n"\
           "KNAGIR\n"\
           ">Input_4_Arg-C_44_19_2283.62998_4.3\n"\
           "LVLWMLDFDAHQPDSVLQR\n"\
           ">Input_5_Arg-C_47_3_407.46678_3.74\n"\
           "EFL\n"\
           ">Input_0_Trypsin_2_2_289.29138_5.98\n"\
           "DR\n"\
           ">Input_1_Trypsin_10_8_935.00128_4.29\n"\
           "EALDSSWK\n"\
           ">Input_2_Trypsin_11_1_146.18938_8.06\n"\
           "K\n"\
           ">Input_3_Trypsin_13_2_287.36218_9.71\n"\
           "LR\n"\
           ">Input_4_Trypsin_19_6_503.51548_9.71\n"\
           "SGAGGR\n"\
           ">Input_5_Trypsin_20_1_146.18938_8.06\n"\
           "K\n"\
           ">Input_6_Trypsin_25_5_529.59668_9.71\n"\
           "NAGIR\n"\
           ">Input_7_Trypsin_44_19_2283.62998_4.3\n"\
           "LVLWMLDFDAHQPDSVLQR\n"\
           ">Input_8_Trypsin_47_3_407.46678_3.74\n"\
           "EFL\n"

@pytest.fixture
def res_dig_1_42_2():
    """ Result for digestion with 1 and 42 and IPC2 """
    return ">Input_0_Trypsin_2_2_289.29138_5.98\n"\
           "DR\n"\
           ">Input_1_Trypsin_10_8_935.00128_4.29\n"\
           "EALDSSWK\n"\
           ">Input_2_Trypsin_11_1_146.18938_8.06\n"\
           "K\n"\
           ">Input_3_Trypsin_13_2_287.36218_9.71\n"\
           "LR\n"\
           ">Input_4_Trypsin_19_6_503.51548_9.71\n"\
           "SGAGGR\n"\
           ">Input_5_Trypsin_20_1_146.18938_8.06\n"\
           "K\n"\
           ">Input_6_Trypsin_25_5_529.59668_9.71\n"\
           "NAGIR\n"\
           ">Input_7_Trypsin_44_19_2283.62998_4.3\n"\
           "LVLWMLDFDAHQPDSVLQR\n"\
           ">Input_8_Trypsin_47_3_407.46678_3.74\n"\
           "EFL\n"\
           ">Input_9_Trypsin_10_10_1206.27738_4.49\n"\
           "DREALDSSWK\n"\
           ">Input_10_Trypsin_11_9_1063.17538_6.12\n"\
           "EALDSSWKK\n"\
           ">Input_11_Trypsin_13_3_415.53628_9.93\n"\
           "KLR\n"\
           ">Input_12_Trypsin_19_8_772.86238_11.49\n"\
           "LRSGAGGR\n"\
           ">Input_13_Trypsin_20_7_631.68958_9.93\n"\
           "SGAGGRK\n"\
           ">Input_14_Trypsin_25_6_657.77078_9.93\n"\
           "KNAGIR\n"\
           ">Input_15_Trypsin_44_24_2795.21138_5.46\n"\
           "NAGIRLVLWMLDFDAHQPDSVLQR\n"\
           ">Input_16_Trypsin_47_22_2673.08148_4.12\n"\
           "LVLWMLDFDAHQPDSVLQREFL\n"\
           ">Input_17_Trypsin_11_11_1334.45148_6.16\n"\
           "DREALDSSWKK\n"\
           ">Input_18_Trypsin_13_11_1332.52228_7.79\n"\
           "EALDSSWKKLR\n"\
           ">Input_19_Trypsin_19_9_901.03648_11.49\n"\
           "KLRSGAGGR\n"\
           ">Input_20_Trypsin_20_9_901.03648_11.49\n"\
           "LRSGAGGRK\n"\
           ">Input_21_Trypsin_25_12_1143.27098_11.49\n"\
           "SGAGGRKNAGIR\n"\
           ">Input_22_Trypsin_44_25_2923.38548_7.08\n"\
           "KNAGIRLVLWMLDFDAHQPDSVLQR\n"\
           ">Input_23_Trypsin_47_27_3184.66288_4.61\n"\
           "NAGIRLVLWMLDFDAHQPDSVLQREFL\n"

@pytest.fixture
def res_dig_1_42_ipc():
    """ Result for digestion with 1 and 42 """
    return ">Input_0_Arg-C_2_2_289.29138_6.73\n"\
           "DR\n"\
           ">Input_1_Arg-C_13_11_1332.52228_9.84\n"\
           "EALDSSWKKLR\n"\
           ">Input_2_Arg-C_19_6_503.51548_11.04\n"\
           "SGAGGR\n"\
           ">Input_3_Arg-C_25_6_657.77078_11.53\n"\
           "KNAGIR\n"\
           ">Input_4_Arg-C_44_19_2283.62998_4.19\n"\
           "LVLWMLDFDAHQPDSVLQR\n"\
           ">Input_5_Arg-C_47_3_407.46678_3.36\n"\
           "EFL\n"\
           ">Input_0_Trypsin_2_2_289.29138_6.73\n"\
           "DR\n"\
           ">Input_1_Trypsin_10_8_935.00128_4.12\n"\
           "EALDSSWK\n"\
           ">Input_2_Trypsin_11_1_146.18938_10.04\n"\
           "K\n"\
           ">Input_3_Trypsin_13_2_287.36218_11.04\n"\
           "LR\n"\
           ">Input_4_Trypsin_19_6_503.51548_11.04\n"\
           "SGAGGR\n"\
           ">Input_5_Trypsin_20_1_146.18938_10.04\n"\
           "K\n"\
           ">Input_6_Trypsin_25_5_529.59668_11.04\n"\
           "NAGIR\n"\
           ">Input_7_Trypsin_44_19_2283.62998_4.19\n"\
           "LVLWMLDFDAHQPDSVLQR\n"\
           ">Input_8_Trypsin_47_3_407.46678_3.36\n"\
           "EFL\n"

def test_wrong_file(tmp_path, capsys):
    """ Try the full software with wrong fasta file """
    # False file A
    false_file_a = tmp_path.joinpath("FalseA.fasta")
    with open(false_file_a, "w", encoding="utf-8") as f_file:
        f_file.write("?A0A2C9KB11/1065-1162\n"\
                     "DREALDSSWKKLRSgagGRKNAGIRLVLWMLDHVPNMRAHQPDSVLQREFL\n"\
                     "AQVDRILGGVESMINNVDDPVALEAAFDRLADAHLSMT\n"\
                     ">A0A2C9KB11/1221-1332\n"\
                     "ERKALKSSWDSLKSaagGSQEAGVNLVLWMLQNVTKFNAHQGDDALKAEFI\n"\
                     "KQVQRITGGLESMIDNLDNQGKLQAAIDRLVDAHLHMTpSVGLEYEPLQKN\n")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        with unittest.mock.patch("sys.argv", ["func_test",
                                              "-i", str(false_file_a),
                                              "-e", str(42)]):
            RapidPeptidesGenerator.main()
    assert pytest_wrapped_e.value.code == 1
    # Error output
    captured = capsys.readouterr()
    assert "Input Error: input file format not recognized (?)." in captured.err

def test_wrong_file_in_middle(tmp_path, capsys):
    """ Try the full software with wrong fasta file (error in the middle) """
    # False file A
    false_file_a_mid = tmp_path.joinpath("FalseAmid.fasta")
    with open(false_file_a_mid, "w", encoding="utf-8") as f_file:
        f_file.write(">A0A2C9KB11/1065-1162\n"\
                     "DREALDSSWKKLRSgagGRKNAGIRLVLWMLDFDAHQPDSVLQREFL\n"\
                     "AQVDRILGGVESMINNVDDPVALEAAFDRLADAHLSMT\n"\
                     ">A0A2C9KB11/1221-1332\n"\
                     "ERKALKSSWDSLKSaagGSQEAGVNLVLWMLQNVPNQGDDALKAEFI\n"\
                     "KQVQRITGGLESMIDNLDNQGKLQAAIDRLVDAHLHMTpSVGLLQKN\n"\
                     ">A0A2C9KB11/1378-1486\n"\
                     "DRKYIESSWKKLTDaagGSEKAGTNFVFWLLDNVPHQSDAALQEDFR\n"\
                     "NQVKAITGGIESFVNNVNNPAALQSSIETLVDAHLNMQpSIGLSYSV\n"\
                     "?A0A2C9KB11/1535-1643\n"\
                     "DRRAVVSSWKKLTAsGRQSFGIDLVLWMFNNVPNMSDADLRRDFLKQ\n"\
                     "VNSIVNGLGDMVDSVNDPGKLQANLERLSEIHLHFVpSVGPEFFVEK\n"\
                     ">A0A2C9K1A5/128-239\n"\
                     "DIKALDSSWNKLTAgadGRTTFGNNLVLWMLDNVPNMSDEALKNEFI\n"\
                     "KQVKLIVGGLQTLIINLNNPGQLQASIEHLADVHLHMKpSIGLLQEN\n"\
                     ">A0A2C9K1A5/285-395\n"\
                     "DKVALESSWSRLTAgvnGKRNAGVRLVLWMFNAKQSDEALKTDAEFL\n"\
                     "KQVDVIIGGFETLINNLNDPTLLQDRLESLADAHLEKKpAIGVPLQK\n"\
                     ">A0A2C9K1A5/588-698\n"\
                     "DKKALQSSQNAGIKLVLWMFDNVPNMRFSKFNAHSSDDALKADAEFL\n"\
                     "KQVNVIVGGLESLVNNDKLQAGVERLVDAHLHMSpSVGLEYFGPLQQ\n"\
                     ">A0A2C9K1A5/745-855\n"\
                     "DRKVLERTWNQLISgpgGKEENVPNMRDSKFDAHKSDEALSKDPEFV\n"\
                     "KQVNNIFGGLESILNNLNKPGQLQSALENLADDHLDRKpRIGGPLQK\n"\
                     ">A0A2C9K1A5/935-1004\n"\
                     "QMFEHVPNMREQFTKFDAHQPNAALKQNPEFLLNNLDDPVALKAAID\n"\
                     "RLADAHLSMS\n")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        with unittest.mock.patch("sys.argv", ["func_test",
                                              "-i", str(false_file_a_mid),
                                              "-e", str(42)]):
            RapidPeptidesGenerator.main()
    assert pytest_wrapped_e.value.code == 1
    # Error output
    captured = capsys.readouterr()
    assert "Input Error: amino acid \"?\" in DRKYIESSWKKLTDAAGGSEKAGTNFVFWLLD"\
           "NVPHQSDAALQEDFRNQVKAITGGIESFVNNVNNPAALQSSIETLVDAHLNMQPSIGLSYSV?A0"\
           "A2C9KB11/1535-1643DRRAVVSSWKKLTASGRQSFGIDLVLWMFNNVPNMSDADLRRDFLKQ"\
           "VNSIVNGLGDMVDSVNDPGKLQANLERLSEIHLHFVPSVGPEFFVEK not recognized"\
           "." in captured.err

def test_l_option(capsys, list_enz):
    """ Test -l behavior """
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        with unittest.mock.patch("sys.argv", ["func_test",
                                              "-l"]):
            RapidPeptidesGenerator.main()
    # Check normal exit
    assert pytest_wrapped_e.value.code == 0
    # Output
    captured = capsys.readouterr()
    assert list_enz in captured.out

def test_s_option(capsys, res_dig_1_42):
    """ Test -s behavior """
    with unittest.mock.patch("sys.argv", ["func_test",
                                          "-s", "DREALDSSWKKLRSgagGRKNAGI"\
                                                "RLVLWMLDFDAHQPDSVLQREFL",
                                          "-e", "1", "42"]):
        RapidPeptidesGenerator.main()
    # Output
    captured = capsys.readouterr()
    assert res_dig_1_42 in captured.out

def test_s_option_ipc(capsys, res_dig_1_42_ipc):
    """ Test -s behavior """
    with unittest.mock.patch("sys.argv", ["func_test",
                                          "-s", "DREALDSSWKKLRSgagGRKNAGI"\
                                                "RLVLWMLDFDAHQPDSVLQREFL",
                                          "-e", "1", "42", "-p", "ipc"]):
        RapidPeptidesGenerator.main()
    # Output
    captured = capsys.readouterr()
    assert res_dig_1_42_ipc in captured.out

def test_d_option(capsys):
    """ Test -d behavior """
    # sequential
    with unittest.mock.patch("sys.argv", ["func_test",
                                          "-s", "PKPKPKPK",
                                          "-e", "28", "29", "-d", "s"]):
        RapidPeptidesGenerator.main()
    # Output
    captured = capsys.readouterr()
    assert ">Input_0_Lys-C_2_2_243.30608_8.06\nPK\n"\
           ">Input_1_Lys-C_4_2_243.30608_8.06\nPK\n"\
           ">Input_2_Lys-C_6_2_243.30608_8.06\nPK\n"\
           ">Input_3_Lys-C_8_2_243.30608_8.06\nPK\n"\
           ">Input_0_Lys-N_1_1_115.13198_5.46\nP\n"\
           ">Input_1_Lys-N_3_2_243.30608_8.06\nKP\n"\
           ">Input_2_Lys-N_5_2_243.30608_8.06\nKP\n"\
           ">Input_3_Lys-N_7_2_243.30608_8.06\nKP\n"\
           ">Input_4_Lys-N_8_1_146.18938_8.06\nK\n" in captured.out
    # concurrent
    with unittest.mock.patch("sys.argv", ["func_test",
                                          "-s", "PKPKPKPK",
                                          "-e", "28", "29", "-d", "c"]):
        RapidPeptidesGenerator.main()
    # Output
    captured = capsys.readouterr()
    assert ">Input_0_Lys-C-Lys-N_1_1_115.13198_5.46\nP\n"\
           ">Input_1_Lys-C-Lys-N_2_1_146.18938_8.06\nK\n"\
           ">Input_2_Lys-C-Lys-N_3_1_115.13198_5.46\nP\n"\
           ">Input_3_Lys-C-Lys-N_4_1_146.18938_8.06\nK\n"\
           ">Input_4_Lys-C-Lys-N_5_1_115.13198_5.46\nP\n"\
           ">Input_5_Lys-C-Lys-N_6_1_146.18938_8.06\nK\n"\
           ">Input_6_Lys-C-Lys-N_7_1_115.13198_5.46\nP\n"\
           ">Input_7_Lys-C-Lys-N_8_1_146.18938_8.06\nK\n" in captured.out

def test_d_option_ipc(capsys):
    """ Test -d behavior """
    # sequential
    with unittest.mock.patch("sys.argv", ["func_test",
                                          "-s", "PKPKPKPK", "-p", "ipc",
                                          "-e", "28", "29", "-d", "s"]):
        RapidPeptidesGenerator.main()
    # Output
    captured = capsys.readouterr()
    assert "Input_0_Lys-C_2_2_243.30608_10.04\nPK\n"\
           ">Input_1_Lys-C_4_2_243.30608_10.04\nPK\n"\
           ">Input_2_Lys-C_6_2_243.30608_10.04\nPK\n"\
           ">Input_3_Lys-C_8_2_243.30608_10.04\nPK\n"\
           ">Input_0_Lys-N_1_1_115.13198_5.97\nP\n"\
           ">Input_1_Lys-N_3_2_243.30608_10.04\nKP\n"\
           ">Input_2_Lys-N_5_2_243.30608_10.04\nKP\n"\
           ">Input_3_Lys-N_7_2_243.30608_10.04\nKP\n"\
           ">Input_4_Lys-N_8_1_146.18938_10.04\nK\n" in captured.out
    # concurrent
    with unittest.mock.patch("sys.argv", ["func_test",
                                          "-s", "PKPKPKPK", "-p", "ipc",
                                          "-e", "28", "29", "-d", "c"]):
        RapidPeptidesGenerator.main()
    # Output
    captured = capsys.readouterr()
    assert ">Input_0_Lys-C-Lys-N_1_1_115.13198_5.97\nP\n"\
           ">Input_1_Lys-C-Lys-N_2_1_146.18938_10.04\nK\n"\
           ">Input_2_Lys-C-Lys-N_3_1_115.13198_5.97\nP\n"\
           ">Input_3_Lys-C-Lys-N_4_1_146.18938_10.04\nK\n"\
           ">Input_4_Lys-C-Lys-N_5_1_115.13198_5.97\nP\n"\
           ">Input_5_Lys-C-Lys-N_6_1_146.18938_10.04\nK\n"\
           ">Input_6_Lys-C-Lys-N_7_1_115.13198_5.97\nP\n"\
           ">Input_7_Lys-C-Lys-N_8_1_146.18938_10.04\nK\n" in captured.out

def test_p_option(capsys):
    """ Test -p behavior """
    # default
    with unittest.mock.patch("sys.argv", ["func_test",
                                          "-s", "PKPKPKPK",
                                          "-e", "28", "29", "-p", "ipc2"]):
        RapidPeptidesGenerator.main()
    # Output
    captured = capsys.readouterr()
    assert ">Input_0_Lys-C_2_2_243.30608_8.06\nPK\n"\
           ">Input_1_Lys-C_4_2_243.30608_8.06\nPK\n"\
           ">Input_2_Lys-C_6_2_243.30608_8.06\nPK\n"\
           ">Input_3_Lys-C_8_2_243.30608_8.06\nPK\n"\
           ">Input_0_Lys-N_1_1_115.13198_5.46\nP\n"\
           ">Input_1_Lys-N_3_2_243.30608_8.06\nKP\n"\
           ">Input_2_Lys-N_5_2_243.30608_8.06\nKP\n"\
           ">Input_3_Lys-N_7_2_243.30608_8.06\nKP\n"\
           ">Input_4_Lys-N_8_1_146.18938_8.06\nK\n" in captured.out

    # stryer
    with unittest.mock.patch("sys.argv", ["func_test",
                                          "-s", "PKPKPKPK",
                                          "-e", "28", "29", "-p", "stryer"]):
        RapidPeptidesGenerator.main()
    # Output
    captured = capsys.readouterr()
    assert ">Input_0_Lys-C_2_2_243.30608_9.4\nPK\n"\
           ">Input_1_Lys-C_4_2_243.30608_9.4\nPK\n"\
           ">Input_2_Lys-C_6_2_243.30608_9.4\nPK\n"\
           ">Input_3_Lys-C_8_2_243.30608_9.4\nPK\n"\
           ">Input_0_Lys-N_1_1_115.13198_5.54\nP\n"\
           ">Input_1_Lys-N_3_2_243.30608_9.4\nKP\n"\
           ">Input_2_Lys-N_5_2_243.30608_9.4\nKP\n"\
           ">Input_3_Lys-N_7_2_243.30608_9.4\nKP\n"\
           ">Input_4_Lys-N_8_1_146.18938_9.4\nK\n" in captured.out

    # ipc
    with unittest.mock.patch("sys.argv", ["func_test",
                                          "-s", "PKPKPKPK",
                                          "-e", "28", "29", "-p", "ipc"]):
        RapidPeptidesGenerator.main()
    # Output
    captured = capsys.readouterr()
    assert ">Input_0_Lys-C_2_2_243.30608_10.04\nPK\n"\
           ">Input_1_Lys-C_4_2_243.30608_10.04\nPK\n"\
           ">Input_2_Lys-C_6_2_243.30608_10.04\nPK\n"\
           ">Input_3_Lys-C_8_2_243.30608_10.04\nPK\n"\
           ">Input_0_Lys-N_1_1_115.13198_5.97\nP\n"\
           ">Input_1_Lys-N_3_2_243.30608_10.04\nKP\n"\
           ">Input_2_Lys-N_5_2_243.30608_10.04\nKP\n"\
           ">Input_3_Lys-N_7_2_243.30608_10.04\nKP\n"\
           ">Input_4_Lys-N_8_1_146.18938_10.04\nK\n" in captured.out

def test_f_option(capsys):
    """ Test -f behavior """
    # default
    with unittest.mock.patch("sys.argv", ["func_test",
                                          "-s", "PKPKPKPK",
                                          "-e", "28", "29", "-f", "fasta"]):
        RapidPeptidesGenerator.main()
    # Output
    captured = capsys.readouterr()
    assert ">Input_0_Lys-C_2_2_243.30608_8.06\nPK\n"\
           ">Input_1_Lys-C_4_2_243.30608_8.06\nPK\n"\
           ">Input_2_Lys-C_6_2_243.30608_8.06\nPK\n"\
           ">Input_3_Lys-C_8_2_243.30608_8.06\nPK\n"\
           ">Input_0_Lys-N_1_1_115.13198_5.46\nP\n"\
           ">Input_1_Lys-N_3_2_243.30608_8.06\nKP\n"\
           ">Input_2_Lys-N_5_2_243.30608_8.06\nKP\n"\
           ">Input_3_Lys-N_7_2_243.30608_8.06\nKP\n"\
           ">Input_4_Lys-N_8_1_146.18938_8.06\nK\n" in captured.out

    # csv
    with unittest.mock.patch("sys.argv", ["func_test",
                                          "-s", "PKPKPKPK",
                                          "-e", "28", "29", "-f", "csv"]):
        RapidPeptidesGenerator.main()
    # Output
    captured = capsys.readouterr()
    assert "Original_header,No_peptide,Enzyme,Cleaving_pos,Peptide_size,"\
           "Peptide_mass,pI,Sequence\n"\
           "Input,0,Lys-C,2,2,243.30608,8.06,PK\n"\
           "Input,1,Lys-C,4,2,243.30608,8.06,PK\n"\
           "Input,2,Lys-C,6,2,243.30608,8.06,PK\n"\
           "Input,3,Lys-C,8,2,243.30608,8.06,PK\n"\
           "Input,0,Lys-N,1,1,115.13198,5.46,P\n"\
           "Input,1,Lys-N,3,2,243.30608,8.06,KP\n"\
           "Input,2,Lys-N,5,2,243.30608,8.06,KP\n"\
           "Input,3,Lys-N,7,2,243.30608,8.06,KP\n"\
           "Input,4,Lys-N,8,1,146.18938,8.06,K\n" in captured.out

    # tsv
    with unittest.mock.patch("sys.argv", ["func_test",
                                          "-s", "PKPKPKPK",
                                          "-e", "28", "29", "-f", "tsv"]):
        RapidPeptidesGenerator.main()
    # Output
    captured = capsys.readouterr()
    assert "Original_header\tNo_peptide\tEnzyme\tCleaving_pos\tPeptide_size\t"\
           "Peptide_mass\tpI\tSequence\n"\
           "Input\t0\tLys-C\t2\t2\t243.30608\t8.06\tPK\n"\
           "Input\t1\tLys-C\t4\t2\t243.30608\t8.06\tPK\n"\
           "Input\t2\tLys-C\t6\t2\t243.30608\t8.06\tPK\n"\
           "Input\t3\tLys-C\t8\t2\t243.30608\t8.06\tPK\n"\
           "Input\t0\tLys-N\t1\t1\t115.13198\t5.46\tP\n"\
           "Input\t1\tLys-N\t3\t2\t243.30608\t8.06\tKP\n"\
           "Input\t2\tLys-N\t5\t2\t243.30608\t8.06\tKP\n"\
           "Input\t3\tLys-N\t7\t2\t243.30608\t8.06\tKP\n"\
           "Input\t4\tLys-N\t8\t1\t146.18938\t8.06\tK\n" in captured.out

def test_f_option_ipc(capsys):
    """ Test -f behavior """
    # default
    with unittest.mock.patch("sys.argv", ["func_test",
                                          "-s", "PKPKPKPK", "-p", "ipc",
                                          "-e", "28", "29", "-f", "fasta"]):
        RapidPeptidesGenerator.main()
    # Output
    captured = capsys.readouterr()
    assert "Input_0_Lys-C_2_2_243.30608_10.04\nPK\n"\
           ">Input_1_Lys-C_4_2_243.30608_10.04\nPK\n"\
           ">Input_2_Lys-C_6_2_243.30608_10.04\nPK\n"\
           ">Input_3_Lys-C_8_2_243.30608_10.04\nPK\n"\
           ">Input_0_Lys-N_1_1_115.13198_5.97\nP\n"\
           ">Input_1_Lys-N_3_2_243.30608_10.04\nKP\n"\
           ">Input_2_Lys-N_5_2_243.30608_10.04\nKP\n"\
           ">Input_3_Lys-N_7_2_243.30608_10.04\nKP\n"\
           ">Input_4_Lys-N_8_1_146.18938_10.04\nK\n" in captured.out

    # csv
    with unittest.mock.patch("sys.argv", ["func_test",
                                          "-s", "PKPKPKPK", "-p", "ipc",
                                          "-e", "28", "29", "-f", "csv"]):
        RapidPeptidesGenerator.main()
    # Output
    captured = capsys.readouterr()
    assert "Original_header,No_peptide,Enzyme,Cleaving_pos,Peptide_size,"\
           "Peptide_mass,pI,Sequence\n"\
           "Input,0,Lys-C,2,2,243.30608,10.04,PK\n"\
           "Input,1,Lys-C,4,2,243.30608,10.04,PK\n"\
           "Input,2,Lys-C,6,2,243.30608,10.04,PK\n"\
           "Input,3,Lys-C,8,2,243.30608,10.04,PK\n"\
           "Input,0,Lys-N,1,1,115.13198,5.97,P\n"\
           "Input,1,Lys-N,3,2,243.30608,10.04,KP\n"\
           "Input,2,Lys-N,5,2,243.30608,10.04,KP\n"\
           "Input,3,Lys-N,7,2,243.30608,10.04,KP\n"\
           "Input,4,Lys-N,8,1,146.18938,10.04,K\n" in captured.out

    # tsv
    with unittest.mock.patch("sys.argv", ["func_test",
                                          "-s", "PKPKPKPK", "-p", "ipc",
                                          "-e", "28", "29", "-f", "tsv"]):
        RapidPeptidesGenerator.main()
    # Output
    captured = capsys.readouterr()
    assert "Original_header\tNo_peptide\tEnzyme\tCleaving_pos\tPeptide_size\t"\
           "Peptide_mass\tpI\tSequence\n"\
           "Input\t0\tLys-C\t2\t2\t243.30608\t10.04\tPK\n"\
           "Input\t1\tLys-C\t4\t2\t243.30608\t10.04\tPK\n"\
           "Input\t2\tLys-C\t6\t2\t243.30608\t10.04\tPK\n"\
           "Input\t3\tLys-C\t8\t2\t243.30608\t10.04\tPK\n"\
           "Input\t0\tLys-N\t1\t1\t115.13198\t5.97\tP\n"\
           "Input\t1\tLys-N\t3\t2\t243.30608\t10.04\tKP\n"\
           "Input\t2\tLys-N\t5\t2\t243.30608\t10.04\tKP\n"\
           "Input\t3\tLys-N\t7\t2\t243.30608\t10.04\tKP\n"\
           "Input\t4\tLys-N\t8\t1\t146.18938\t10.04\tK\n" in captured.out

def test_i_option(capsys, truth, file_a):
    """ Test the functional behavior of FRAG of i option """
    # Test -i behavior with fasta file
    with unittest.mock.patch("sys.argv", ["func_test",
                                          "-i", str(file_a),
                                          "-e", "42"]):
        RapidPeptidesGenerator.main()
    # Output
    captured = capsys.readouterr()
    # Check result
    for i in truth:
        assert i in captured.out

def test_i_option_ipc(capsys, truth_ipc, file_a):
    """ Test the functional behavior of FRAG of i option """
    # Test -i behavior with fasta file
    with unittest.mock.patch("sys.argv", ["func_test",
                                          "-i", str(file_a),
                                          "-e", "42", "-p", "ipc"]):
        RapidPeptidesGenerator.main()
    # Output
    captured = capsys.readouterr()
    # Check result
    for i in truth_ipc:
        assert i in captured.out

def test_i_option_parallel(capsys, truth, file_a):
    """ Test the functional behavior of FRAG of i option """
    # Test -i behavior with fasta file
    with unittest.mock.patch("sys.argv", ["func_test",
                                          "-i", str(file_a),
                                          "-e", "42",
                                          "-c", "8"]):
        RapidPeptidesGenerator.main()
    # Output
    captured = capsys.readouterr()
    # Check result
    for i in truth:
        assert i in captured.out

def test_i_option_parallel_ipc(capsys, truth_ipc, file_a):
    """ Test the functional behavior of FRAG of i option """
    # Test -i behavior with fasta file
    with unittest.mock.patch("sys.argv", ["func_test",
                                          "-i", str(file_a),
                                          "-e", "42",
                                          "-c", "8", "-p", "ipc"]):
        RapidPeptidesGenerator.main()
    # Output
    captured = capsys.readouterr()
    # Check result
    for i in truth_ipc:
        assert i in captured.out

def test_o_option(tmp_path, truth, file_a):
    """ Test the functional behavior of FRAG of o (and q) option """
    # Output folder
    output_folder = tmp_path / "res_functional_tests"
    output_folder.mkdir()
    # Test -o behavior with fasta file
    with unittest.mock.patch("sys.argv", ["func_test",
                                          "-i", str(file_a),
                                          "-e", "42",
                                          "-q",
                                          "-o", str(output_folder/"res.fa")]):
        RapidPeptidesGenerator.main()
    # Check result
    nb_line = 0
    with open(os.path.join(output_folder, "res.fa")) as file_res:
        for line in file_res:
            nb_line += 1
            assert line in truth
    assert nb_line == len(truth)

def test_o_option_ipc(tmp_path, truth_ipc, file_a):
    """ Test the functional behavior of FRAG of o (and q) option """
    # Output folder
    output_folder = tmp_path / "res_functional_tests"
    output_folder.mkdir()
    # Test -o behavior with fasta file
    with unittest.mock.patch("sys.argv", ["func_test",
                                          "-i", str(file_a),
                                          "-e", "42",
                                          "-q", "-p", "ipc",
                                          "-o", str(output_folder/"res.fa")]):
        RapidPeptidesGenerator.main()
    # Check result
    nb_line = 0
    with open(os.path.join(output_folder, "res.fa")) as file_res:
        for line in file_res:
            nb_line += 1
            assert line in truth_ipc
    assert nb_line == len(truth_ipc)

def test_no_enz(capsys, monkeypatch, list_enz, res_dig_1_42):
    """ Test correct behavior """
    responses = iter(["arg-c 42", ""])
    with unittest.mock.patch("sys.argv", ["func_test",
                                          "-s", "DREALDSSWKKLRSgagGRKNAGI"\
                                                "RLVLWMLDFDAHQPDSVLQREFL"]):
        monkeypatch.setattr('builtins.input', lambda msg: next(responses))
        RapidPeptidesGenerator.main()
    # Output
    captured = capsys.readouterr()
    assert list_enz in captured.out
    assert res_dig_1_42 in captured.out

def test_no_enz_ipc(capsys, monkeypatch, list_enz, res_dig_1_42_ipc):
    """ Test correct behavior plus ipc """
    responses = iter(["1 42", ""])
    with unittest.mock.patch("sys.argv", ["func_test", "-p", "ipc",
                                          "-s", "DREALDSSWKKLRSgagGRKNAGI"\
                                                "RLVLWMLDFDAHQPDSVLQREFL"]):
        monkeypatch.setattr('builtins.input', lambda msg: next(responses))
        RapidPeptidesGenerator.main()
    # Output
    captured = capsys.readouterr()
    assert list_enz in captured.out
    assert res_dig_1_42_ipc in captured.out

def test_no_enz_quit(capsys, monkeypatch, list_enz):
    """ Test -l behavior """
    responses = iter(["q"])
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        with unittest.mock.patch("sys.argv", ["func_test",
                                              "-s", "DREALDSSWKKLRSgagGRKNAGI"\
                                                    "RLVLWMLDFDAHQPDSVLQREF"\
                                                    "L"]):
            monkeypatch.setattr('builtins.input', lambda msg: next(responses))
            RapidPeptidesGenerator.main()
    assert pytest_wrapped_e.value.code == 0
    captured = capsys.readouterr()
    assert list_enz in captured.out

def test_no_enz_err(capsys, monkeypatch, list_enz, res_dig_1_42):
    """ Test -l behavior """
    responses = iter(["1 42 b", ""])
    with unittest.mock.patch("sys.argv", ["func_test",
                                          "-s", "DREALDSSWKKLRSgagGRKNAGI"\
                                                "RLVLWMLDFDAHQPDSVLQREFL"]):
        monkeypatch.setattr('builtins.input', lambda msg: next(responses))
        RapidPeptidesGenerator.main()
    # Output
    captured = capsys.readouterr()
    assert list_enz in captured.out
    assert res_dig_1_42 in captured.out

def test_no_enz_err_ipc(capsys, monkeypatch, list_enz, res_dig_1_42_ipc):
    """ Test -l behavior """
    responses = iter(["1 42 b", ""])
    with unittest.mock.patch("sys.argv", ["func_test", "-p", "ipc",
                                          "-s", "DREALDSSWKKLRSgagGRKNAGI"\
                                                "RLVLWMLDFDAHQPDSVLQREFL"]):
        monkeypatch.setattr('builtins.input', lambda msg: next(responses))
        RapidPeptidesGenerator.main()
    # Output
    captured = capsys.readouterr()
    assert list_enz in captured.out
    assert res_dig_1_42_ipc in captured.out

def test_na_option(capsys):
    """ Test the functional behavior of FRAG of b, n and a option """
    # Test -na behavior
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        with unittest.mock.patch("sys.argv", ["func_test",
                                              "-a",
                                              "-n",
                                              "-x", "(C,)",
                                              "-y", "Pwet",
                                              "-z", "(C,)(E)"]):
            RapidPeptidesGenerator.main()
    assert pytest_wrapped_e.value.code == 0
    # Output
    captured = capsys.readouterr()
    # Check result
    user_file = str(Path.home()) + "/rpg_user.py"

    # Number of line of user file after inserting enzyme in previous test
    nb_line = 1
    with open(user_file) as usr_file:
        for line in usr_file:
            nb_line += 1
    assert nb_line == 24

    # Virtually add enzyme Pwet
    tmp = []
    ENZ = []

    R_1 = rule.Rule(0, "R", True, 1) # Always cleaves after R, except...
    ENZ.append(R_1)

    ENZYME = enzyme.Enzyme(44, "Pwet", ENZ, 0)
    # Add it to available enzymes
    tmp.append(ENZYME)
    # Delete the enzyme
    enzyme.delete_enzyme(tmp, "Pwet")
    # We should be back at 11 lines
    nb_line = 1
    with open(user_file) as usr_file:
        for line in usr_file:
            nb_line += 1
    assert nb_line == 9

def test_theoretical(capsys, monkeypatch, list_enz, res_dig_1_42_2):
    """ Test correct behavior """
    with unittest.mock.patch("sys.argv", ["func_test",
                                          "-s", "DREALDSSWKKLRSgagGRKNAGI"\
                                                "RLVLWMLDFDAHQPDSVLQREFL",
                                          "-e", "42",
                                          "-t", "1", "2", "3"]):
        RapidPeptidesGenerator.main()
    captured = capsys.readouterr()
    assert "Too much miscleavage values. Last values will be ignored.\n" in captured.err


    with unittest.mock.patch("sys.argv", ["func_test",
                                          "-s", "DREALDSSWKKLRSgagGRKNAGI"\
                                                "RLVLWMLDFDAHQPDSVLQREFL",
                                          "-e", "42",
                                          "-t", "2"]):
        RapidPeptidesGenerator.main()
    captured = capsys.readouterr()
    assert res_dig_1_42_2 in captured.out

    with unittest.mock.patch("sys.argv", ["func_test",
                                          "-s", "DREALDSSWKKLRSgagGRKNAGI"\
                                                "RLVLWMLDFDAHQPDSVLQREFL",
                                          "-e", "42", "2",
                                          "-t", "2"]):
        RapidPeptidesGenerator.main()
    captured = capsys.readouterr()
    assert res_dig_1_42_2 in captured.out
