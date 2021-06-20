from indic_transliteration import detect, sanscript
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate
import indicsyllabifier

# A Function to get a scheme_map used in conversion of a script of any of the mentioned languages or schemes into SLP1 and Devanagari
def get_scheme_map(scheme):
    
    supported_formats = ["HK", "Devanagari", "IAST", "ITRANS", "Kolkata", "SLP1", "Kannada", "Malayalam", "Telugu"]
    
    if scheme not in supported_formats:
        print("The input text is not in supported format.")
        print(f"List of supported formats : {supported_formats}")
        return "", ""
    
    if scheme == "HK":
        script = sanscript.HK
    
    if scheme == "Devanagari":
        script = sanscript.DEVANAGARI
        
    if scheme == "IAST":
        script = sanscript.IAST
        
    if scheme == "ITRANS":
        script = sanscript.ITRANS

    if scheme == "Kolkata":
        script = sanscript.KOLKATA
    
    if scheme == "SLP1":
        script = sanscript.SLP1
        
    if scheme == "Kannada":
        script = sanscript.KANNADA
        
    if scheme == 'Malayalam':
        script = sanscript.MALAYALAM
    
    if scheme == 'Telugu':
        script = sanscript.TELUGU
        
    
    s1 = SchemeMap(SCHEMES[script], SCHEMES[sanscript.SLP1])
    s2 = SchemeMap(SCHEMES[script], SCHEMES[sanscript.DEVANAGARI])
    
    return s1, s2

# A function for actual transliteration
def get_transliteration(data, scheme_map):

    return transliterate(data, scheme_map=scheme_map)

# A function for breaking down a word into syllables
def get_syllable(word):

    syllablizer_handle = indicsyllabifier.getInstance()   # Get the Syllabifier class
    syllables = syllablizer_handle.syllabify_hi(word)     # Initiate the Syllabifier for Hindi 
    
    # A loop for converting each syllable from devanagari into SLP1 encoding
    scheme_map = SchemeMap(SCHEMES[sanscript.DEVANAGARI], SCHEMES[sanscript.SLP1])
    for syallable in syllables:
        syallable_slp1 = transliterate(syallable, scheme_map=scheme_map)
    
    return syllables

def katapayadi(data, reverse=False):
    NonConsonants = ['a', 'A', 'i', 'I', 'u', 'U', 'e', 'E', 'o', 'O', 'f', 'F', 'x', 'X']
    Sorants = ['aM', 'aH']

    # List of "first letters" of the SLP1 enoding of all the consonants
    Consonants = ['k', 'K', 'g', 'G', 'N', 'c', 'C', 'j', 'J', 'Y', 'w', 'W', 'q', 'Q', 'R', 't', 'T', 'd', 'D', 'n', 'p', 'P', 'b', 'B', 'm', 'y', 'r', 'l', 'v', 'S', 'z', 's', 'h', 'L']
    
    # Each numeric value is matched to the consonant above (We can replace these both list by a dictionary)
    NumereicalValue = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    number = ""
    for syllable in data:

        # This is used to ignore some exceptions that arises in Malayalam 
        if syllable[0] not in Consonants + NonConsonants:
            continue

        if len(syllable) == 1 and syllable not in NonConsonants:
            continue
        
        elif syllable in NonConsonants or syllable in Sorants:
            new_digit = "0"

        elif len(syllable) == 2 and syllable[0] in NonConsonants and syllable[1] not in Consonants: # For likes of "AM (आं)"
            new_digit = "0"
        
        elif len(syllable) == 3 and syllable[1] in NonConsonants:
            new_digit = str(NumereicalValue[Consonants.index(syllable[0])]) #"kAe"
        
        elif len(syllable) == 3:
            new_digit = str(NumereicalValue[Consonants.index(syllable[1])])

        elif len(syllable) == 4 and syllable[-2:] in Sorants:
              new_digit = str(NumereicalValue[Consonants.index(syllable[-3])])
        
        else:
            new_digit = str(NumereicalValue[Consonants.index(syllable[0])])
        
        if reverse == False:
            number = new_digit + number
        
        else:
            number += new_digit
    
    return int(number)

def main():
    data = input("Enter data : ")
    reverse = input("Reverse the Katapayadi Number (T / F) : ")
    
    if reverse.lower() == "t":
        reverse = True
    else:
        reverse = False
    
    scheme = detect.detect(data)
    scheme_map = get_scheme_map(scheme)
    
    if scheme_map[0] != "":
        data_slp1 = get_transliteration(data, scheme_map[0])
        data_dev = get_transliteration(data, scheme_map[1])
        #print(f"\nData : {data}")
        print(f"\nThe scheme is : {scheme}")
        print(f"\nConverted in SLP1 : {data_slp1}")
        print(f"\nConverted in Devnagri : {data_dev}")

        syllables = []
        for word in data_dev.split():
            syllables += get_syllable(word)
        #print(syllables)

        scheme_map = SchemeMap(SCHEMES[sanscript.DEVANAGARI], SCHEMES[sanscript.SLP1])
        data = []
        for syllable in syllables:
            data.append(transliterate(syllable, scheme_map=scheme_map))
        #print(data)
        print(f"\nKatapayadi Number : {katapayadi(data, reverse)}")

main() # Example - bhadrāmbudhisiddhajanmagaṇitaśraddhā sma yad bhūpagīḥ

main() # Example - āyurārogyasaukhyam

main() # Example - gopIBAgyamaDuvrAta-SfNgiSodaDisanDiga..  KalajIvitaKAtAva galahAlArasaMDara..

main() # Example - jYAnam paramam Dyeyam

main() # Example - ಆಚಾರ್ಯವಾಗಭೇದ್ಯಾ

main() # Example - ಗೋಪೀಭಾಗ್ಯಮಧುವ್ರಾತ-ಶೃಂಗಿಶೋದಧಿಸಂಧಿಗ || ಖಲಜೀವಿತಖಾತಾವ ಗಲಹಾಲಾರಸಂಧರ ||

main() # Example - ചണ്ഡാംശുചന്ദ്രാധമകുംഭിപാല

main() # Example - గోపీభాగ్యమధువ్రాత-శృంగిశోదధిసంధిగ |  ఖలజీవితఖాతావ గలహాలారసంధర ||


