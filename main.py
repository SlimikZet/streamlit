import streamlit as st
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Настройка базы данных
engine = create_engine('sqlite:///test1.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Модель статьи
class Article(Base):
    tablename = 'article'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    intro = Column(String(300), nullable=False)
    text = Column(Text, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)

# Навигация по страницам
page = st.sidebar.radio("Меню", ["Главная", "О сайте", "Все статьи", "Создать статью"])

if page == "Главная":
    st.title("Главная страница")
    st.write("Добро пожаловать на сайт статей!")

elif page == "О сайте":
    st.title("О сайте")
    st.write("Это учебный проект на Streamlit для управления статьями.")

elif page == "Все статьи":
    st.title("Список всех статей")
    articles = session.query(Article).order_by(Article.date.desc()).all()
    for art in articles:
        with st.expander(f"{art.title} ({art.date.strftime('%Y-%m-%d %H:%M')})"):
            st.subheader(art.intro)
            st.write(art.text)
            if st.button("Удалить", key=f"delete_{art.id}"):
                session.delete(art)
                session.commit()
                st.experimental_rerun()

elif page == "Создать статью":
    st.title("Создать новую статью")
    title = st.text_input("Заголовок")
    intro = st.text_input("Интро")
    text = st.text_area("Контент")

    if st.button("Сохранить статью"):
        if title and intro and text:
            new_art = Article(title=title, intro=intro, text=text)
            session.add(new_art)
            session.commit()
            st.success("Статья успешно добавлена!")
        else:
            st.error("Пожалуйста, заполните все поля!")
