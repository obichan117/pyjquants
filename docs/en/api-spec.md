# J-Quants API V2 Specification

!!! info "Unofficial OpenAPI Spec"
    This is an **unofficial** OpenAPI 3.0 specification for the J-Quants V2 API,
    created by the pyjquants project since J-Quants does not provide an official one.

## Interactive Documentation

<div style="text-align: center; margin: 20px 0;">
<a href="../openapi/" class="md-button md-button--primary" target="_blank">
    Open Swagger UI
</a>
<a href="../openapi/openapi.yaml" class="md-button" download>
    Download OpenAPI Spec (YAML)
</a>
</div>

## Rate Limits by Tier

| Tier | Requests/min | Monthly Price |
|------|-------------|---------------|
| Free | 5 | Free |
| Light | 60 | ~1,650 JPY |
| Standard | 120 | ~3,300 JPY |
| Premium | 500 | ~16,500 JPY |

## Endpoint Availability

### Free/Light Tier
- `/equities/bars/daily` - Daily stock prices
- `/equities/master` - Listed securities info
- `/equities/earnings-calendar` - Earnings calendar
- `/equities/investor-types` - Trading by investor type (market-wide)
- `/fins/summary` - Financial statements summary
- `/markets/calendar` - Trading calendar
- `/indices/bars/daily/topix` - TOPIX prices

### Standard Tier (adds)
- `/equities/bars/daily/am` - AM session prices
- `/fins/details` - Detailed financials
- `/fins/dividend` - Dividend data
- `/indices/bars/daily` - All index prices (incl. Nikkei 225)
- `/markets/sectors/topix17` - TOPIX-17 sectors
- `/markets/sectors/topix33` - TOPIX-33 sectors
- `/markets/breakdown` - Trading breakdown
- `/markets/short-ratio` - Short selling ratio
- `/markets/short-sale-report` - Short positions
- `/markets/margin-alert` - Margin alerts
- `/derivatives/bars/daily/futures` - Futures prices
- `/derivatives/bars/daily/options` - Options prices

## API Base URL

```
https://api.jquants.com/v2
```

## Authentication

All endpoints require an API key via the `x-api-key` header:

```bash
curl -H "x-api-key: YOUR_API_KEY" \
  "https://api.jquants.com/v2/equities/bars/daily?code=7203"
```

## Response Format

All V2 endpoints return data in this format:

```json
{
  "data": [
    { ... },
    { ... }
  ],
  "pagination_key": "..."  // optional, for paginated endpoints
}
```

## Field Name Convention

V2 uses abbreviated field names:

| Full Name | V2 Abbrev | Description |
|-----------|-----------|-------------|
| CompanyName | CoName | Company name (Japanese) |
| CompanyNameEnglish | CoNameEn | Company name (English) |
| Sector17Code | S17 | TOPIX-17 sector code |
| Sector33Code | S33 | TOPIX-33 sector code |
| MarketCode | Mkt | Market segment code |
| Open | O | Open price |
| High | H | High price |
| Low | L | Low price |
| Close | C | Close price |
| Volume | Vo | Trading volume |
| TurnoverValue | Va | Turnover value |
| HolidayDivision | HolDiv | Holiday flag (0=trading, 1=holiday) |

## Useful Links

- [J-Quants Official Site](https://jpx-jquants.com/)
- [J-Quants API Documentation](https://jpx-jquants.com/en/spec)
- [pyjquants GitHub](https://github.com/obichan117/pyjquants)
