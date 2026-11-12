"""Titanic survival dashboard. Run: streamlit run titanic_dashboard.py"""

from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

DATA = Path(__file__).with_name("data") / "titanic.csv"
SEX = {"male": "גבר", "female": "אישה"}
EMBARKED = {"C": "שרבורג", "Q": "קווינסטאון", "S": "סאות'המפטון", "Unknown": "לא ידוע"}


def apply_filters(df, sexes, classes, ports, ages, keep_missing_age):
    out = df[df["Sex"].isin(sexes) & df["Pclass"].isin(classes) & df["Embarked"].isin(ports)]
    known = out["Age"].between(ages[0], ages[1])
    return out[known | (out["Age"].isna() if keep_missing_age else False)]


def _selfcheck():
    sample = pd.DataFrame(
        {
            "Sex": ["male", "female", "female"],
            "Pclass": [1, 3, 3],
            "Embarked": ["S", "C", "C"],
            "Age": [22.0, None, 40.0],
        }
    )
    got = apply_filters(sample, ["female"], [3], ["C"], (0, 30), True)
    assert list(got["Age"].isna()) == [True]


_selfcheck()

st.set_page_config(page_title="טיטאניק", layout="wide")
st.title("טיטאניק — הישרדות")
st.caption("891 נוסעים. הנתונים המקוריים של Kaggle, דרך datasciencedojo.")

df = pd.read_csv(DATA)
df["Embarked"] = df["Embarked"].fillna("Unknown")

with st.sidebar:
    st.header("סינון")
    sexes = st.multiselect("מין", list(SEX), default=list(SEX), format_func=SEX.get)
    classes = st.multiselect("מחלקה", [1, 2, 3], default=[1, 2, 3], format_func=lambda c: f"מחלקה {c}")
    ports = st.multiselect("נמל עלייה", list(EMBARKED), default=list(EMBARKED), format_func=EMBARKED.get)
    ages = st.slider("גיל", 0, 80, (0, 80))
    keep_missing_age = st.checkbox("כלול נוסעים בלי גיל ידוע", value=True)

view = apply_filters(df, sexes, classes, ports, ages, keep_missing_age)

if view.empty:
    st.warning("אין נוסעים שעונים על הסינון.")
    st.stop()

survived = int(view["Survived"].sum())
rate = view["Survived"].mean()
a, b, c, d = st.columns(4)
a.metric("נוסעים", f"{len(view):,}")
b.metric("שרדו", f"{survived:,}")
c.metric("אחוז הישרדות", f"{rate:.0%}")
d.metric("גיל חציוני", "—" if view["Age"].dropna().empty else f"{view['Age'].median():.0f}")

left, right = st.columns(2)
by_class = view.groupby("Pclass")["Survived"].mean().mul(100).round(1)
by_class.index = [f"מחלקה {i}" for i in by_class.index]
by_sex = view.groupby("Sex")["Survived"].mean().mul(100).round(1)
by_sex.index = [SEX.get(i, i) for i in by_sex.index]
left.subheader("הישרדות לפי מחלקה")
left.bar_chart(by_class, height=280)
right.subheader("הישרדות לפי מין")
right.bar_chart(by_sex, height=280)

st.subheader("התפלגות גיל")
labels = ["0–10", "11–20", "21–30", "31–40", "41–50", "51–60", "61–80"]
counts = (
    pd.cut(view["Age"].dropna(), bins=[0, 10, 20, 30, 40, 50, 60, 80], labels=labels)
    .value_counts()
    .reindex(labels, fill_value=0)
)
age = counts.rename("נוסעים").rename_axis("גיל").reset_index()
st.altair_chart(
    alt.Chart(age)
    .mark_bar()
    .encode(
        x=alt.X("גיל:N", sort=labels, title=None),
        y=alt.Y("נוסעים:Q", title=None, scale=alt.Scale(zero=True)),
    )
    .properties(height=240),
    use_container_width=True,
)

st.subheader("נוסעים")
show = view.assign(
    מין=view["Sex"].map(SEX),
    מחלקה=view["Pclass"],
    שרד=view["Survived"].map({1: "כן", 0: "לא"}),
)[["Name", "מין", "מחלקה", "Age", "Fare", "שרד"]]
show.columns = ["שם", "מין", "מחלקה", "גיל", "מחיר כרטיס", "שרד"]
st.dataframe(show, use_container_width=True, height=360)
