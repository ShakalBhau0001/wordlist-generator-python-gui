# 🔐 Wordlist Generator (GUI) 📝

A modern **GUI-based Wordlist Generator** built using **Python + Streamlit**.
This tool takes personal-info inputs (name, nickname, team, date) and generates a **targeted, custom password wordlist** through a **clean, interactive web interface**.

---

## 🔄 Also Available as a CLI Tool

Prefer terminal-based workflows or scripting?

👉 **_wordlist-generator-python-cli_** is the command-line version of this project, designed for developers and power users.

> **🔗 CLI Repository: [wordlist-generator-python-cli](https://github.com/ShakalBhau0001/wordlist-generator-python-cli)**

---

## 🧱 Project Structure

```bash
wordlist-generator-python-gui/
│
├── assets/              # Screenshots
├── core/                # All generation logic
│   ├── __init__.py
│   └── engine.py
├── gui/                 # Streamlit Tabs
│   ├── __init__.py
│   ├── wordlist.py
│   ├── instructions.py
│   └── about.py
├── main.py              # Streamlit entry point
├── requirements.txt     # Project Dependencies
├── LICENSE              # MIT LICENSE
└── README.md            # Project documentation
```

---

## ✨ Features

### 🔑 Personal-Info Token Generator

- Takes **First name, Last name, Nickname, Team/Company, Date**
- Cleans and normalizes every input into safe tokens
- Auto-splits dates into day, month, year, and combined sub-tokens

### 🔒 Smart Word Builder

- Permutes tokens in every order (configurable combo length)
- Joins combinations with `-`, `_`, `.`, or no separator
- Case variants: lower, UPPER, Capitalized, CamelCase
- Leetspeak substitutions (`a→4`, `e→3`, `i→1`, `o→0`, `s→5`, `t→7`, `b→8`)
- Numeric tail suffixes (`00`–`99` + last 10 years)
- Length filtering (min/max characters)

### 🖥️ Modern GUI Interface

- Built with **Streamlit**
- Clean, responsive, form-based layout

### 📊 Live Results Dashboard

- Total words generated
- Tokens used
- Base permutation count

### 🔍 Preview Table

- Instantly preview the first 50 generated words

### ⬇️ One-Click Download

- Download the full wordlist as a `.txt` file

### 🛡️ Safety Guard

- Staged size checks prevent unsafe/huge configurations from freezing or crashing the app

### 📌 Horizontal Tabs

- **Wordlist** – generation form + results
- **Instructions** – step-by-step usage guide
- **About** – project info & disclaimer

---

## 🛠 Technologies Used

| Technology      | Role                          |
| --------------- | ----------------------------- |
| **Python 3**    | Core programming              |
| **itertools**   | Token permutation logic       |
| **re**          | Token cleaning & date parsing |
| **dataclasses** | Config & result containers    |
| **Streamlit**   | GUI framework                 |

---

## ▶️ How to Run

### 1️⃣ Clone Repository

```bash
git clone https://github.com/ShakalBhau0001/wordlist-generator-python-gui.git
```

### 2️⃣ Navigate to Project

```bash
cd wordlist-generator-python-gui
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

OR

```bash
pip install streamlit
```

### 4️⃣ Run Application

```bash
streamlit run main.py
```

> **Note: ⚠️ Fill in at least one field (name, nickname, team, or date) before generating**

---

## 🖥️ UI Preview

- 🔐 Header with app title
- 📝 Personal-info input form
- ⚙️ Generation options (length, combo, case, leet, separators, numbers)
- 🚀 Generate button
- 📊 Results dashboard with metrics
- 🔍 Preview table of generated words
- ⬇️ Download button for full `.txt` wordlist

---

## ⚙️ How It Works

### 1️⃣ Collect Tokens

- Cleans first name, last name, nickname, team, and date into tokens
- Splits date into day / month / year sub-tokens

### 2️⃣ Build & Expand Words

- Permutes tokens (up to selected combo length)
- Adds separators, case variants, leetspeak, and numeric tails
- Filters by min/max length

### 3️⃣ Display in GUI

- Data is shown in a results table with:
  - ✔ Word count
  - 🔢 Tokens used
  - 📊 Base permutation count

---

## ⚠️ Limitations

- Not a bulk/general-purpose dictionary generator
- Word count grows fast with more tokens and higher "max combo"
- Only ASCII alphanumerics plus `. _ -` are kept in tokens
- Single-session GUI (no accounts / saved history)

---

## 🌟 Future Enhancements

- Additional personal-info fields (pet name, city, etc.)
- Export directly in Hashcat/John-compatible formats
- Save/load generation presets
- Smarter multi-substitution leetspeak

---

## ⚠️ Disclaimer

> **Use responsibly**

- For **personal, educational, and authorized security-testing use only**
- Only use on systems and accounts you own or are explicitly permitted to test
- Developer is not responsible for misuse

---

## 📸 Preview

 ![GUI Preview](assets/WGG.png)

---

## 🪪 Author

> **Creator: Shakal Bhau**

> **GitHub: [ShakalBhau0001](https://github.com/ShakalBhau0001)**

---

## 💙 Support

If you like this project:

- ⭐ Star the repo
- 🍴 Fork it
- 🧠 Contribute ideas

---
