#!/bin/bash

#  Copyright (C) 2022 David Arroyo Menéndez

#  Author: David Arroyo Menéndez <davidam@gmail.com> 
#  Maintainer: David Arroyo Menéndez <davidam@gmail.com> 
#  This file is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3, or (at your option)
#  any later version.
# 
#  This file is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with Damegender; see the file GPL.txt.  If not, write to
#  the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, 
#  Boston, MA 02110-1301 USA,

mkdir -p orig
cd orig
wget -c https://www.insee.fr/fr/statistiques/fichier/3536630/noms2008nat_txt.zip
unzip noms2008nat_txt.zip
# wget -c https://www.insee.fr/fr/statistiques/fichier/3536630/noms2008dep_txt.zip
# unzip noms2008dep_txt.zip
wget -c https://www.insee.fr/fr/statistiques/fichier/2540004/dpt_2000_2021_csv.zip
unzip dpt_2000_2021_csv.zip
wget -c https://www.insee.fr/fr/statistiques/fichier/2540004/dpt2021_csv.zip
unzip dpt_2021_csv.zip
wget -c https://www.insee.fr/fr/statistiques/fichier/2540004/nat2021_csv.zip
unzip nat2021_csv.zip
sed '/PRENOMS_RARES/d' nat2021.csv> aux.csv
sed '/sexe;preusuel;annais;nombre/d' aux.csv > aux2.csv
sed '/XXXX/d' aux2.csv > aux3.csv
cp aux3.csv nat2021.csv
rm aux.csv aux2.csv aux3.csv
cd ..
