# 🦠 Epidemiological Decision Dashboard

An interactive Streamlit application for simulating and analyzing infectious disease spread using compartmental models.

## 📊 Models Included

* **SIR** — Susceptible → Infected → Recovered
* **SIRD** — Adds mortality (Deaths)
* **SIRDV** — Adds vaccination dynamics

## 🚀 Features

* Interactive parameter controls (Beta, Gamma, Mu, Vaccination)
* Real-time simulation of disease spread
* Dynamic Plotly visualizations (zoom, hover, toggle)
* Summary metrics:

  * Peak infection
  * Day of peak
  * Final outcomes
* Scenario comparison tool
* Download:

  * CSV results
  * PNG plots
* Educational insights based on model behavior

## 🧠 Use Cases

* Public health education
* Epidemiology coursework
* Policy scenario testing
* Disease outbreak modeling

## 🛠️ Tech Stack

* Python
* Streamlit
* Plotly
* Pandas

## ▶️ How to Run

```bash
pip install streamlit plotly pandas
streamlit run streamlit_app.py
```

Then open:

```
http://localhost:8501
```

## 📁 Project Structure

```
streamlit_app.py
Assignment3_Functions_Solution.py
Assignment3_Main_Solution.py
```

## 📌 Notes

* Built for academic use and demonstration purposes
* Model assumptions are simplified and not intended for real-world forecasting

## 👨‍💻 Author

Omar Abdul-Rahman
MPH Candidate

---

**Built with Streamlit | Epidemiological Decision Dashboard**
