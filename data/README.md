# Data Documentation

TaxHelper Rwanda currently uses a small, curated FAQ knowledge base embedded in the backend source code (`main.py`). It is not currently connected to a live Rwanda Revenue Authority (RRA) API, a live NISR database, or an external real-time tax dataset.

The FAQ content is intended to provide basic educational guidance on topics such as TIN, VAT, EBM, PAYE, business registration, income tax, and filing deadlines. Answers should be checked against current official guidance before users make tax decisions.

## Reference sources

- Rwanda Revenue Authority (RRA): https://www.rra.gov.rw/
- RRA contact / support information: https://www.rra.gov.rw/

## How the data is used

The backend matches a user's question to relevant curated FAQ entries and returns an explanatory response. The current prototype does not submit tax returns, make payments, or retrieve personal tax records.

## Future improvement

A future version could organize the FAQ into a separately maintained dataset, record source URLs and review dates for each answer, and connect to approved official data services if access is available.
