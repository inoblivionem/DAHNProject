#Import des modules à utiliser
import re, sys

def non_indented_paragraph(text):  # <- AC: dans quels cas le paragraphe ne serait pas indenté ?
    """ Rajouter les balises de paragraphe dans le texte quand il n'est pas indenté
    
    :param text: Texte à modifier
    :type text: str
    :returns: Texte avec les balises <p>
    :rtype: str
    """
    punctuation = "!\"»?."  # <- AC: pourquoi pas les ";" et "," et "'", etc ?
    #Ont été inclus tous les signes de fin de ponctuation que pourraient contenir les lettres
    for sign in punctuation:
        text = text.replace(sign + "\n", sign + '</p>\n<p rend="indent">')  # <- AC: plus tard, si tu parses ce xml, il se pourrait que ces < et > ne soient pas interprétés comme des balises
        text = text.replace(sign + " \n", sign + '</p>\n<p rend="indent">')  # <- AC: n'as-tu pas, une fois que cette ligne est terminée, des </p> qui se baladent dans le texte et qu'il faudrait retirer ?
    #Rajout des balises paragraphes ouvrantes et fermantes
    return text

def indented_paragraph(text):
    """ Rajouter les balises de paragraphe dans le texte quand il est indenté
    
    :param text: Texte à modifier
    :type text: str
    :returns: Texte avec les balises <p>
    :rtype: str
    """

    if '\t' in text and "<" not in text:
       text = text.replace('\t', '<p rend="indent">')
       #Rajout des balises paragraphes ouvrantes quand le texte est indenté et qu'aucune autre balise ne se trouve dans la ligne
          # <- AC: es-tu sûre qu'il n'y a pas de "<" dans le texte original ?
          # <- AC: est-ce que le but n'est pas de vérifier s'il y a un \t ou un < au début de la ligne ? Tu pourrais vérifier ça en slicant text (ex: if "<" not in text[10:] (10 premiers caractères)
    else:
       text = text.replace('\t', '')
       #Suppression de la tabulation pour les textes indentés déjà balisés
    punctuation = "!\"»?."
    #Ont été inclus tous les signes de fin de ponctuation que pourraient contenir les lettres
    for sign in punctuation:
        text = text.replace(sign + "\n", sign + "</p>\n")
        text = text.replace(sign + " \n", sign + "</p>\n")
    #Rajout des balises paragraphes fermantes
    return text


## ------ DEBUT DU SCRIPT ------ ##

#Création d'un dictionnaire qui contient tous les termes récurrents que l'on a dans les lettres
#On y rajoute les balises qui conviennent
recurrent_terms = {
    "LETTRE": "<head>LETTRE",
    "SÉNAT": '<fw type="letterhead" place="align(left)" corresp="#entete-senat"><hi rend="underline">SÉNAT</hi></fw>',
    "PARIS,": '<dateline rend="align(right)"><placeName>PARIS</placeName>, <date when-iso="">',
    "LE MANS,": '<dateline rend="align(right)"><placeName>LE MANS</placeName>, <date when-iso="">',
    "Mon cher Butler,": '<salute rend="indent">Mon cher Butler,</salute></opener>',
    "à Monsieur le Président Nicholas Murray BUTLER.": '<note rend="align(left)"><address><addrLine>à Monsieur le Président Nicholas Murray BUTLER.</addrLine></address></note>',
    "à Monsieur le Président N. Murray BUTLER.": '<note rend="align(left)"><address><addrLine>à Monsieur le Président N. Murray BUTLER.</addrLine></address></note>',
    "à Monsieur le Président N.Murray BUTLER.": '<note rend="align(left)"><address><addrLine>à Monsieur le Président N.Murray BUTLER.</addrLine></address></note>',
    "à Monsieur le Président Nicholas Murray BUTLER,": '<address rend="align(left)"><addrLine>à Monsieur le Président Nicholas Murray BUTLER,</addrLine>',
    "à Monsieur le Président N. Murray BUTLER,": '<address rend="align(left)"><addrLine>à Monsieur le Président N. Murray BUTLER,</addrLine>',
    "à Monsieur le Président N.Murray BUTLER,": '<address rend="align(left)"><addrLine>à Monsieur le Président N.Murray BUTLER,</addrLine>',
    "NEW-YORK.": "<addrLine>NEW-YORK.</addrLine></address></closer>",
    "Votre affectueusement dévoué,": '<closer><signed rend="align(right)">Votre affectueusement dévoué,</signed>',
    "D'Estournelles de Constant": '<signed rend="align(right)" hand="#annotation">D’Estournelles de Constant</signed>'
}

#Création d'un dictionnaire qui contient les modifications faites à l'aide de regex
regex = {
    '-\n': '<lb break="no"/>',
    ' \n': '<lb/> ',
    "'\n": "'<lb/>"
}

#Ouverture des fichiers d'entrée et de sortie
file_in = open (sys.argv[1], mode='r', encoding='utf-8')   # <- AC: il vaut mieux utiliser "with open("fichier", "r|w|etc") as file: ..."
print("reading from "+sys.argv[1])
file_out = open (sys.argv[2], mode='w', encoding='utf-8')
print("writing to "+sys.argv[2])

#Le fichier lit le textes comme un ensemble de lignes
for text in file_in.readlines():
    #Homogénéisation des apostrophes
    text = text.replace("’", "'")
    #On définit des variables qui correspond aux clés et valeurs des dictionnaires définis
    #On remplace ensuite dans le texte la clé du dictionnaire par sa valeur
    for key, value in recurrent_terms.items():
        text = text.replace(key, value)  # <- AC: quand tu travailleras sur le résultat des transcriptions, il faudra sûrement utiliser des regex, notamment pour gérer les variations de casse (ex: PARiS)
    #Balisage des numéros de page en prenant en compte ses caractères particuliers
    if "- " and " -\n" in text:  # <-- AC: d'instinct, je ne suis pas sûre que chercher "-" et "-\n" soit infaillible car je pense que "peut-être est-il encore dans la mai-\n" n'est pas le genre de phrase que tu sembles chercher ici.
        text = text.replace("- ", '<pb n="" facs=".JPG"/><note type="foliation" place="top">- ')
        text = text.replace(" -\n", ' -</note> ')
    #On ferme la balise <head> en utilisant la récurrence des titres pour les lettres
    if "<head>" in text:
        text = text.replace(".\n", '.</head>\n<opener>')
    #On ferme la balise <dateline> en utilisant la récurrence des dates pour les lettres
    if '<dateline' in text:
        text = text.replace(".", '.</date></dateline>')
    #Application d'une des deux fonctions pour rajouter les balises de paragraphes
    #text = indented_paragraph(text)
    text = non_indented_paragraph(text)
    #On définit des variables qui correspond aux clés et valeurs des dictionnaires définis
    for key, value in regex.items():
        #Remplacement des clés du dictionnaire par leur valeurs dans le cas où la fin de ligne n'est pas balisé.
        if "> \n" not in text:
            text = text.replace(key, value)
    #Écriture de toutes les modifications effectuées dans le fichier de sortie
    file_out.write(text)

#Fermeture des fichiers
file_in.close()
file_out.close()
