import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Wykresy
plt.rcParams['font.size'] = 10
sns.set_theme(style="ticks", context="talk")
plt.style.use("default")

# Kolory
custom_palette = ['#FF862D', '#5858C6', '#00C8B4', '#271651', '#8A2BE2', '#AA5013']

# Layout 
st.set_page_config(layout="wide")
col_left, col_right = st.columns(2)

# Strona główna lewa kolumna
with col_left:
    st.title("Poznajmy się")
    
    st.markdown(
        "<p style='font-size:17px; line-height:1.5; color:#444; margin-bottom:-15px;'>"
        "Aplikacja prezentuje wyniki ankiety powitalnej uczestników kursu „Pracuj w AI: Zostań Data Scientist od Zera”. "
        "Dzięki niej możesz zobaczyć, kim jesteśmy, czym się zajmujemy oraz co nas inspiruje — zarówno zawodowo, jak i prywatnie. "
        "To szybki sposób, by lepiej poznać społeczność kursu."
        "</p>",
        unsafe_allow_html=True
    )
    
    st.divider()

    st.markdown("<h3 style='margin-top:-15px; margin-bottom:-10px;'>Statystyki</h3>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:14px; color:#555; margin-bottom:-15px;'>Sekcja zawiera 10 losowo wybranych odpowiedzi z ankiety oraz podstawowe dane statystyczne. "
        "Pozwala to na szybki przegląd ogólnego obrazu grupy.</p>",
        unsafe_allow_html=True
    )
    st.divider()

    st.markdown("<h3 style='margin-top:-15px; margin-bottom:-10px;'>Kim jesteśmy</h3>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:14px; color:#555; margin-bottom:-15px;'>Ta sekcja pokazuje kto tworzy społeczność kursu. Zobacz, jak rozkłada się płeć uczestników oraz jakie są przedziały wiekowe.</p>",
        unsafe_allow_html=True
    )
    st.divider()

    st.markdown("<h3 style='margin-top:-15px; margin-bottom:-10px;'>Zawodowo</h3>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:14px; color:#555; margin-bottom:-15px;'>Ta część pokazuje w jakich branżach pracują uczestnicy oraz jaka jest ich motywacja do nauki AI. "
        "To inspirujące spojrzenie na to, skąd pochodzimy zawodowo i dokąd zmierzamy.</p>",
        unsafe_allow_html=True
    )
    st.divider()

    st.markdown("<h3 style='margin-top:-15px; margin-bottom:-10px;'>Prywatnie</h3>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:14px; color:#555; margin-bottom:-15px;'>Tutaj poznasz uczestników od bardziej osobistej strony — ich ulubione zwierzęta i hobby. "
        "Bo za każdą linią kodu stoi człowiek z pasjami!</p>",
        unsafe_allow_html=True
    )

# Strona główna prawa kolumna
with col_right:
    st.image("ankieta.png", use_container_width=True)

# Dane
df = pd.read_csv("35__welcome_survey_cleaned.csv", sep=";")

# Zakładki
tab1, tab2, tab3, tab4 = st.tabs(["Statystyki", "Kim jesteśmy", "Zawodowo", "Prywatnie"])

# Zakładka 1 Statystyki 
with tab1:
    col_stat_left, col_stat_right = st.columns(2)

    with col_stat_left:
        st.image("statystyki.png", use_container_width=True)

    with col_stat_right:
        st.subheader("10 losowych wierszy")
        st.dataframe(df.sample(n=10), use_container_width=True, hide_index=True, height=420)
        
        st.subheader("Podstawowe dane statystyczne")
        st.dataframe(df.describe(include='all').transpose(), use_container_width=True, height=420)

# Zakładka 2 Kim jesteśmy 
with tab2:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.image("kim_jestesmy.png", use_container_width=True)

    with col2:
        gender_counts = df['gender'].value_counts()
        labels = ['Mężczyźni' if idx == 0.0 else 'Kobiety' for idx in gender_counts.index]
        fig1, ax1 = plt.subplots()
        fig1.patch.set_facecolor('white')
        ax1.set_facecolor('white')
        wedges, texts, autotexts = ax1.pie(
            gender_counts,
            labels=labels,
            autopct='%1.1f%%',
            startangle=90,
            colors=custom_palette[:len(labels)]
        )
        ax1.axis('equal')

        for text in texts:
            text.set_color('black')
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        st.columns([1, 2, 1])[1].subheader("Płeć")
        st.pyplot(fig1)
        
        age_df = df[df['age'] != 'unknown']
        age_counts = age_df['age'].value_counts()
        age_order = ['<18', '18-24', '25-34', '35-44', '45-54', '55-64', '>=65']
        age_counts = age_counts.reindex(age_order, fill_value=0)
        fig2, ax2 = plt.subplots()
        fig2.patch.set_facecolor('white')
        ax2.set_facecolor('white')
        bars = ax2.bar(range(len(age_counts)), age_counts.values, color=custom_palette[:len(age_counts)])
        ax2.set_xlabel('Przedział wiekowy', fontsize=14)
        ax2.set_ylabel('Liczba osób', fontsize=14)
        ax2.set_xticks(range(len(age_counts)))
        ax2.set_xticklabels(age_counts.index, rotation=45, fontsize=12)
        ax2.tick_params(axis='y', labelsize=12)
        st.columns([1, 2, 1])[1].subheader("Przedział wiekowy")
        st.pyplot(fig2)

# Zakładka 3 Zawodowo 
with tab3:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image("zawodowo.png", use_container_width=True)
        
    with col2:
        industry_counts = df['industry'].value_counts()
        fig1, ax1 = plt.subplots(figsize=(10, 8))
        fig1.patch.set_facecolor('white')
        ax1.set_facecolor('white')
        bars = ax1.barh(industry_counts.index, industry_counts.values, color=custom_palette[0])
        ax1.set_xlabel('Liczba osób', fontsize=16)
        ax1.set_ylabel('Branża', fontsize=16)
        ax1.tick_params(axis='x', labelsize=14)
        ax1.tick_params(axis='y', labelsize=10)
        st.columns([1, 2, 1])[1].subheader("Branża")
        st.pyplot(fig1)
        
        motivation_cols = [
            'motivation_career', 'motivation_challenges', 'motivation_creativity_and_innovation',
            'motivation_money_and_job', 'motivation_personal_growth', 'motivation_remote'
        ]
        motivation_sums = df[motivation_cols].sum()
        total = motivation_sums.sum()
        motivation_percent = (motivation_sums / total * 100).round(1)
        motivation_labels = [
            'Kariera', 'Wyzwania', 'Kreatywność i innowacje',
            'Pieniądze i praca', 'Rozwój osobisty', 'Praca zdalna'
        ]
        other_sum = 0
        main_labels = []
        main_values = []
        for i, pct in enumerate(motivation_percent):
            if pct < 1:
                other_sum += motivation_sums.iloc[i]
            else:
                main_labels.append(motivation_labels[i])
                main_values.append(motivation_sums.iloc[i])
        if other_sum > 0:
            main_labels.append('Inne')
            main_values.append(other_sum)
        fig2, ax2 = plt.subplots()
        fig2.patch.set_facecolor('white')
        ax2.set_facecolor('white')
        wedges, texts, autotexts = ax2.pie(
            main_values,
            labels=main_labels,
            autopct='%1.1f%%',
            startangle=90,
            colors=custom_palette[:len(main_labels)]
        )
        ax2.axis('equal')
        for text in texts:
            text.set_color('black')
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        st.columns([1, 2, 1])[1].subheader("Motywacja do nauki AI")
        st.pyplot(fig2)

# Zakładka 4 Prywatnie 
with tab4:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image("prywatnie.png", use_container_width=True)

    with col2:
        animals_counts = df['fav_animals'].value_counts()
        fig1, ax1 = plt.subplots()
        fig1.patch.set_facecolor('white')
        ax1.set_facecolor('white')
        wedges, texts, autotexts = ax1.pie(
            animals_counts,
            labels=animals_counts.index,
            autopct='%1.1f%%',
            startangle=90,
            colors=custom_palette[:len(animals_counts)]
        )
        ax1.axis('equal')
        for text in texts:
            text.set_color('black')
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        st.columns([1, 2, 1])[1].subheader("Ulubione zwierzę")
        st.pyplot(fig1)
        
        hobby_cols = [
            'hobby_art', 'hobby_books', 'hobby_movies',
            'hobby_other', 'hobby_sport', 'hobby_video_games'
        ]
        hobby_sums = df[hobby_cols].sum()
        hobby_labels = [
            'Sztuka', 'Książki', 'Filmy',
            'Inne', 'Sport', 'Gry wideo'
        ]
        fig2, ax2 = plt.subplots()
        fig2.patch.set_facecolor('white')
        ax2.set_facecolor('white')
        wedges, texts, autotexts = ax2.pie(
            hobby_sums,
            labels=hobby_labels,
            autopct='%1.1f%%',
            startangle=90,
            colors=custom_palette[:len(hobby_labels)]
        )
        ax2.axis('equal')
        for text in texts:
            text.set_color('black')
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        st.columns([1, 2, 1])[1].subheader("Hobby")
        st.pyplot(fig2)
