# Housing/Real-Estate Datasets to Replace or Supplement California Housing (CSC-114 Artificial Intelligence I)

**Bottom line: North Carolina is fully covered — a ready-made NC census-block-group CSV (`NC_Housing_Prices_2018.csv`, derived from the 2018 American Community Survey) mirrors the California Housing dataset almost column-for-column and downloads with a single `pd.read_csv()` call, making it the best drop-in replacement — while a genuinely pre-cleaned Hawaii equivalent does not exist and must be built from the Census API or filtered from a national listings set.**

## TL;DR
- **North Carolina (Priority 1): STRONG.** D. Michael Senter's `NC_Housing_Prices_2018.csv` (ACS 2018 5-year, block-group rows, target = median_house_value) is a near-exact structural twin of California Housing and is a direct-download CSV — recommended, with a ~10-minute cleaning step for a few known bugs.
- **Hawaii (Priority 2): WEAK / effectively unavailable pre-cleaned.** The only Hawaii "housing" open-data CSV is a 3-row cost-of-living breakdown, and no Hawaii-specific Kaggle dataset resembling California Housing exists; the workable Hawaii routes are (a) filter the 2,226,382-row national "USA Real Estate Dataset" to Hawaii, or (b) pull Hawaii tracts from the Census ACS API.
- **Fallbacks: STRONG.** West Coast — **King County, WA (Seattle) house sales** (21,613 rows, 21 columns, continuous `price` target, CC0). Additional clean, one-line-loadable options: **Ames, Iowa** (2,930 rows) and **UCI Taipei real-estate valuation** (414 rows, CC BY 4.0).

## Key Findings

### Priority 1 — North Carolina: recommended primary replacement
The closest existing structural match to California Housing is **`NC_Housing_Prices_2018.csv`**, created by data scientist D. Michael Senter explicitly as a North Carolina analogue to the Kaggle California housing set.

- **Source/author:** D. Michael Senter (dmsenter89.github.io), built from **U.S. Census Bureau American Community Survey (ACS) 2018 5-year estimates** plus TIGER/Line block-group centroids for latitude/longitude.
- **Direct download:** `https://dmsenter89.github.io/files/NC_Housing_Prices_2018.csv` — a plain CSV that loads with `pandas.read_csv(url)`; no Kaggle account or API key needed.
- **Format:** CSV, analysis-ready.
- **Geographic unit:** census **block group** — the same unit California Housing uses.
- **Columns:** `population, households, median_income, median_house_value` (target), `total_bedrooms, total_rooms, latitude, longitude, housing_median_age`. This is an almost exact match to California Housing's eight features plus a continuous dollar target.
- **Time period:** 2018 (far more recent than California's 1990 census).
- **Approximate size:** roughly 6,000+ NC block-group rows (statewide).
- **License:** the underlying ACS data is U.S. Government public domain; the derived CSV is posted freely for public/educational use.
- **Caveats (must address in class):** In the file, `total_rooms` and `total_bedrooms` are **identical in every row** — a variable-mapping bug (the ACS "bedrooms" table B25041 was pulled for both), so "total_rooms" is not a true room count. There is at least one placeholder `9999` for `median_house_value`, some blank/NaN cells, and at least one row where `housing_median_age` computed to `2018` (a bad median-year-built value). Students should drop or repair these. This is imperfect but pedagogically useful as a light data-cleaning exercise.

**Cleaner NC alternative (no third-party quirks):** pull the data yourself in one call with the Census API via the Python `census` package (`pip install census`, free API key) or R `tidycensus`, using variables such as `B25077_001E` (median home value = target), `B19013_001E` (median income), `B01003_001E` (population), `B11001_001E` (households) for `state:37` at tract or block-group level. This returns a tidy pandas DataFrame, current to the 2020–2024 ACS 5-year release, and doubles as an API lesson. Note: the Census API returns `-666666666` sentinels for missing values that must be masked to NaN.

### Priority 2 — Hawaii: no genuinely pre-cleaned option exists
- The **"Honolulu County Avg Housing" CSV** on Hawaii Open Data (opendata.hawaii.gov) is **NOT** a home-value dataset. Its entire contents are three rows of a cost-of-living budget breakdown (Housing 33%, Transportation 19%, Remaining Income 48%, dated 01/01/2017). Unusable for regression.
- **No Hawaii-specific Kaggle dataset** resembling California Housing was found. Existing Hawaii housing data (Honolulu Board of Realtors/hicentral.com historical sales, DBEDT housing-market dashboard, Redfin Hawaii, FRED's `HISTHPI` Hawaii house-price index) is aggregate time-series, not row-per-geographic-unit with numeric predictors and a scalar target.
- **Two workable Hawaii routes, both requiring light effort:**
  1. **Filter the national "USA Real Estate Dataset"** (ahmedshahriarsakib, Kaggle) to Hawaii. Per its Kaggle page, "The dataset has 1 CSV file with 10 columns – realtor-data.csv (**2,226,382 entries**)," sourced from realtor.com (described there as "the second most visited real estate listing website in the United States as of 2024, with over 100 million monthly active users"). It is "broken by State and zip code," has a continuous `price` target, and columns `bed, bath, acre_lot, house_size, city, state, zip_code, prev_sold_date`. Filtering `df[df['state']=='Hawaii']` yields a Hawaii listing-level set. **Caveats:** exact HI row count is unverified — confirm with `df['state'].value_counts()` after download; rows are individual homes, not census tracts; and the dataset description says the data is "intended to use for educational purposes only… all rights reserved to the respective owners," so it is fine for classroom use but the license badge should be verified before any redistribution.
  2. **Census ACS API pull for `state:15` (Hawaii)** at tract level — identical recipe to the NC alternative above. This is the only way to obtain a Hawaii dataset **structurally identical** to California Housing (tract rows, median-home-value target). Hawaii has relatively few tracts (~350), so the set is small but usable.

### Fallbacks — East Coast & West Coast

**West Coast — King County, WA (Seattle) house sales — recommended fallback.**
- **Source:** Kaggle (`harlfoxem/housesalesprediction`); also mirrored in R's `moderndive` package as `house_prices`.
- **Size:** confirmed **21,613 observations, 21 columns**; homes sold **May 2014–May 2015**. Kaggle notes it is "a great dataset for evaluating simple regression models."
- **Target:** `price` (continuous, dollars) — a clean scalar-regression target.
- **Features:** bedrooms, bathrooms, sqft_living, sqft_lot, floors, waterfront, view, condition, grade, sqft_above, sqft_basement, yr_built, yr_renovated, zipcode, **lat, long**, sqft_living15, sqft_lot15.
- **License:** CC0 / public domain.
- **Why chosen:** famously clean, West Coast, large (comparable to California's 20,640-row "large" version), and includes lat/long like California Housing. Difference: rows are individual houses, not census aggregates, and there is no median-income feature.

**East Coast — the NC ACS CSV is itself the East Coast pick.** If a second Atlantic option is wanted, a `tidycensus`/Census-API pull for Virginia, New York, or Florida at tract level produces a California-Housing-style tidy frame. There is no equally famous "clean CSV" East Coast home-value teaching set analogous to King County.

**Other reputable, truly-clean regression alternatives (location-agnostic):**
- **Ames, Iowa Housing** (Dean De Cock): per the original documentation (jse.amstat.org/v19n3/decock), **2,930 observations, 82 variables** ("23 nominal, 23 ordinal, 14 discrete, and 20 continuous, plus 2 identifiers"; the commonly cited "79 features" excludes SalePrice and the two ID columns), covering "residential properties sold in Ames, IA from 2006 to 2010." Target = `SalePrice`. Loadable via `sklearn.datasets.fetch_openml(name="house_prices", as_frame=True)` or OpenML. The modern replacement for the deprecated Boston Housing set. Row = individual house.
- **UCI Real Estate Valuation (New Taipei City, Taiwan):** per UCI (archive.ics.uci.edu/dataset/477), **414 instances, 6 numeric inputs** (transaction date, house age, distance to nearest MRT station, number of convenience stores, latitude, longitude); target `Y = house price of unit area`. Donated by Prof. I-Cheng Yeh, Tamkang University, on 18 August 2018. Loadable via `from ucimlrepo import fetch_ucirepo; fetch_ucirepo(id=477)`. **License: CC BY 4.0.** Very clean, tiny (comparable to California's 600-row "small" version), includes lat/long. Not U.S., and the target is price-per-area rather than total value.

## Details

**Structural comparison to California Housing** (row = block group; features longitude, latitude, housing_median_age, total_rooms, total_bedrooms, population, households, median_income; target median_house_value in dollars):

| Dataset | Row unit | Numeric features | Continuous $ target | Rows | Recent? | Load method | Clean? |
|---|---|---|---|---|---|---|---|
| **NC ACS 2018 CSV** | Block group | ~8 (near-identical) | median_house_value | ~6,000+ | 2018 | `pd.read_csv(url)` | Mostly; minor bugs |
| **Census API (NC or HI)** | Tract / BG | user-selected | median home value (B25077) | NC ~2,600 tracts / HI ~350 | 2020–2024 | `census` / `tidycensus` + free key | Very clean |
| **USA Real Estate (filter HI)** | Listing | bed/bath/lot/size | price | 2,226,382 total (HI subset TBD) | recent | Kaggle CSV | Needs filtering/dedup |
| **King County, WA** | House | ~18 | price | 21,613 | 2014–15 | Kaggle CSV / moderndive | Very clean |
| **Ames, Iowa** | House | up to 79 | SalePrice | 2,930 | 2006–10 | `fetch_openml` | Clean |
| **UCI Taipei** | House | 6 | price / unit area | 414 | 2012–13 | `ucimlrepo` id=477 | Very clean |

**The California Housing reference itself (for parity checking):** the Keras loader `keras.datasets.california_housing.load_data(version="small"|"large")` offers a **600-row "small"** version (intended as a Boston-Housing replacement) and a **20,640-row "large"** version; 8 features each; target = median house value in dollars; derived from the 1990 U.S. census with one row per census block group. The scikit-learn twin `fetch_california_housing()` exposes the same 20,640×8 data with per-household ratio features (MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude).

## Recommendations

1. **Do this first — Primary NC replacement.** Use `NC_Housing_Prices_2018.csv` via its direct URL. It is the truest drop-in for the Chapter 4 scalar-regression exercise. Add a short cleaning cell: drop rows where `median_house_value == 9999` or is NaN; drop/repair the `housing_median_age == 2018` outlier; and either drop `total_rooms` (it duplicates `total_bedrooms`) or regenerate both from the correct ACS tables (B25041 bedrooms, B25017 rooms).
2. **If tidiness matters more than convenience — Census API pull.** Have students pull NC (and optionally Hawaii) directly from the ACS API with the `census` package and a free key. This guarantees correctly-mapped, current (2020–2024) data and teaches API access. Supply the variable list (`B25077_001E` target; `B19013_001E`, `B01003_001E`, `B11001_001E`, `B25035_001E`, etc.).
3. **Hawaii — treat as an optional extension, not a ready CSV.** Offer it as a "get real data yourself" task: either filter the USA Real Estate Kaggle set to Hawaii (`price` target, house-level) or pull `state:15` tracts from the ACS API (median-home-value target, tract-level — structurally identical to California Housing).
4. **West Coast fallback for a large, clean set.** Use King County, WA. It behaves very well for a first neural-net regression, is CC0, and is a proven teaching set.
5. **Smallest/cleanest option matching the 600-row "small" California set.** UCI Taipei (414 rows, CC BY 4.0, one-line load). Use if you want a tiny, guaranteed-clean set and don't need U.S. geography.

**Thresholds that would change these recommendations:**
- *If correctness/tidiness outweighs "just a CSV":* switch from the NC CSV to the Census-API pull.
- *If rows must be census geographic units (not individual homes):* only the NC CSV and the Census-API pulls qualify — King County, Ames, and Taipei are all house-level.
- *If you need licensing for redistribution (not just classroom use):* prefer the Census API (public domain) or UCI Taipei (CC BY 4.0) over the Kaggle listings sets.
- *If you want the closest possible parity with California's "small" 600-row version:* pull ~350 Hawaii tracts or a single NC county from the ACS API, or use UCI Taipei's 414 rows.

## Caveats
- The NC CSV's `total_rooms`/`total_bedrooms` duplication is a genuine bug; do not present those two as independent features without fixing them, and expect a `9999` sentinel and a stray `2018` age value.
- The "USA Real Estate Dataset" license text ("educational purposes only… all rights reserved to the respective owners") is ambiguous — acceptable for in-class use but not clearly open for redistribution; the exact Hawaii row count must be verified after download, and the `state` field stores full names ("Hawaii"), not the "HI" abbreviation.
- King County, Ames, and Taipei rows are individual properties, so they lack median_income / population features and frame the problem slightly differently from the census-aggregate California set.
- Census API pulls require a free API key and return `-666666666` sentinels for missing values that must be masked to NaN.
- Only the Census-API route gives 2020–2024 currency; the NC CSV is 2018, King County is 2014–15, Ames is 2006–10, and Taipei is 2012–13.
- Aggregator/broker pages (Bright Data, ZenRows, Crawlfeeds, Gigasheet, Dewey/RentHub) sell related listing data but are paid and/or scraped and are not recommended for a short educational course when free, vetted options above suffice.