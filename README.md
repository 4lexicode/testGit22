# testGit2

Two Python apps: a terminal tic-tac-toe game, and a Streamlit dashboard for the Titanic passenger data.

## Tic-Tac-Toe

![Tic-Tac-Toe — two players, one terminal](assets/tictactoe-banner.jpg)

<p>
  <img alt="Python 3" src="https://img.shields.io/badge/Python-3-0B1220?style=flat-square">
  <img alt="Two players" src="https://img.shields.io/badge/players-2-FF5A5F?style=flat-square">
  <img alt="X" src="https://img.shields.io/badge/X-coral-FF5A5F?style=flat-square">
  <img alt="O" src="https://img.shields.io/badge/O-teal-2EC4B6?style=flat-square">
  <img alt="Terminal" src="https://img.shields.io/badge/board-terminal-F4F1EA?style=flat-square&labelColor=0B1220">
</p>

Two-player tic-tac-toe in the terminal. No dependencies beyond Python 3.

### Run

```bash
python tictactoe.py
```

### How to play

![Board numbered 1 through 9](assets/tictactoe-board.jpg)

- X goes first. Each player picks a free square by its number.
- Three in a row — across, down, or diagonal — wins.
- After 9 moves with no winner, the game is a draw.
- At the end, `y` plays again and `n` quits.

## Titanic dashboard

Interactive survival view of the 891-passenger Titanic dataset in `data/titanic.csv`. The sidebar filters by sex, class, embarkation port, and age. Metrics, bar charts, and the passenger table follow the filter.

Needs `streamlit`, `pandas`, and `altair` (`altair` is installed with Streamlit).

```bash
python -m streamlit run titanic_dashboard.py
```

Streamlit prints the local URL when it starts. The default port is 8501.
