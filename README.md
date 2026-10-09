

Design plan, wireframe and high-fidelity mock-up for an interactive supply chain
dashboard, produced for the Week 5 internship task *Development of Data Dashboards
and Reporting*.


| Path | Description |
|------|-------------|
| `docs/Week5_Dashboard_Design_Report.docx` | Full report: KPIs, visualization rationale, layout, challenges, roadmap |
| `images/mockup_dashboard.png` | High-fidelity Executive Overview mock-up |
| `images/wireframe_dashboard.png` | Wireframe with zones A-F |
| `images/data_flow.png` | Data flow from sources to dashboard |
| `src/make_mockups.py` | Python (Matplotlib) script that generates the images |

- **Headline KPIs:** OTIF, order fill rate, average lead time, inventory turnover, stock-out rate, freight cost per unit
- **Visuals:** KPI cards, OTIF trend line, supplier lead-time ranking, days-of-supply columns, cost-vs-volume combo chart, order-status 100% stacked bar, exception table
- **Planned tools:** Power BI / Tableau / Looker Studio
- **Public data sources:** DataCo Smart Supply Chain dataset, NY Fed GSCPI, World Bank LPI, BTS / UN Comtrade


![Dashboard mock-up](images/mockup_dashboard.png)


```bash
pip install -r requirements.txt
python src/make_mockups.py
```

> All values in the mock-ups are illustrative sample data, not real company data.
