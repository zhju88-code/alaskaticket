# Alaska Award Alerting (Public API Demo)

This repository provides a small, compliant alerting utility that consumes **public, authorized APIs**
for award availability. It also calculates the cents-per-point value so you can compare miles vs cash.

## Features

- Supports a sample data provider for local development.
- Supports a public API provider (bring your own endpoint + API key).
- Calculates cents per point (CPP) and applies alert thresholds.

## Usage

### Sample provider

```bash
python -m alaskaticket.app \
  --provider sample \
  --origin SEA \
  --destination JFK \
  --date 2025-03-15 \
  --min-cpp 1.5 \
  --max-points 60000
```

### Public API provider

Your API should return JSON in the following shape:

```json
{
  "awards": [
    {
      "carrier": "Alaska",
      "origin": "SEA",
      "destination": "JFK",
      "date": "2025-03-15",
      "points": 55000,
      "cash_usd": 892.40
    }
  ]
}
```

Then run:

```bash
python -m alaskaticket.app \
  --provider public \
  --endpoint "https://api.example.com/awards" \
  --api-key "your-token" \
  --origin SEA \
  --destination JFK \
  --date 2025-03-15
```

## Notes

- CPP is computed as `(cash_usd / points) * 100`.
- Alerts fire when `min-cpp` and `max-points` thresholds are met.
