import streamlit as st
import matplotlib.pyplot as plt
import math
import random
import streamlit.components.v1 as components
import Menezes_vanstone_Ascii as Mv
import Kurven as curves
import numpy as np



#def plot_diagram(percentages):
#    plt.figure(figsize=(8, 6))
#    plt.bar(percentages.keys(), percentages.values())
#    plt.xlabel('Pateien')
#    plt.ylabel('% der Stimmen')
#    plt.title('Stimmverhältnisse')
#    plt.xticks(rotation=45)
#    for party, percentage in percentages.items():
#        plt.text(party, percentage,
#                 f'{percentage:.2f}%', ha='center', va='bottom')
#    st.pyplot(plt)





#def plot_sitze(sitze):
#    plt.figure(figsize=(8, 6))
#    plt.bar(sitze.keys(), sitze.values())
#    plt.xlabel('Pateien')
#    plt.ylabel('Sitze')
#    plt.title('Sitzzuteilung')
#    plt.xticks(rotation=45)#
#
#    for party, sitze in sitze.items():
#        plt.text(party, sitze,
#                 f'{sitze}', ha='center', va='bottom')
#
#    st.pyplot(plt)


def main():
    # title
    st.set_page_config(page_title="Menezes Vanstone Kryptosystem am Körpoer F(p^n)")

    # Side title in the main field
    st.title('Praktisches Beispiel des Menezes Vanstone Verfahren')
    st.latex( '''y^2 = x^3 + ax + b ''',help=None )
    st.write('''**p = 131**, irreduzibles Polynom = [1,85,12,128,128,83,3,116,95]
                          Zudem: a = [17, 67, 125, 20, 5, 96, 122, 78], b = [66, 3, 98, 88, 85, 68, 57, 38] ''')
    #st.write(
    st.sidebar.title('Praktische Kurve')

    Kurve = curves.Ascii()
    startpunkt = Kurve.startpoint()

    privatekeya = random.randrange(int(Kurve.bound()[0]))
    publickey_ga = startpunkt * privatekeya
    
    text = st.sidebar.text_input("Text zu verschlüsseln: ")
   
    

    # if button then perform calculations
    if st.button('Berechnungen starten'):
        

        totalmessage = (Mv.text_to_ascii(text))
        st.write("Text: ", text)
        st.write("Text geordnet in Paketen", np.array(totalmessage[1]))
        st.write("Text geordnet in Paken und in ASCII ungewandelt", np.array(totalmessage[0]))
        message = totalmessage [0]
        print("")
        encrypted = Mv.Menezes_Vanstone_encrybtion(message,Kurve,publickey_ga)

        print(encrypted)
        st.write("Verschlüsselt: ", encrypted)
        print("")
        decrypted = Mv.Menezes_Vanstone_decrybtion(encrypted, Kurve, privatekeya)
        st.write("Entschlüsselt: ", decrypted)
        #print(decrypted)
        print("")
        textdecripted= Mv.ascii_to_text(decrypted)
        print(textdecripted)
        st.write("Zusammengefügter Text: ", textdecripted)


if __name__ == '__main__':
    main()