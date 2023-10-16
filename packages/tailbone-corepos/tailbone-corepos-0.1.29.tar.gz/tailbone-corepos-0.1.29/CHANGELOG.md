
# Changelog
All notable changes to tailbone-corepos will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [0.1.29] - 2023-10-07
### Changed
- Add view supplement for tenders.
- Add integration views for CORE/employees.
- Expose views for "transaction archive".
- Add view supplement for taxes.

## [0.1.28] - 2023-09-18
### Changed
- Show tender code for equity import batch rows.

## [0.1.27] - 2023-09-16
### Changed
- Make CORE key fields readonly when viewing equity payment.
- Add grid totals support for CORE stock purchases.

## [0.1.26] - 2023-09-15
### Changed
- Add views for CORE lanes, tenders.
- Add highlight for "overpaid" equity import batch row status.

## [0.1.25] - 2023-09-15
### Changed
- Add xref button to view equity payment in CORE.
- Use handler to get CORE Office URLs.
- Tweak CORE datetime field display for member equity payments grid.

## [0.1.24] - 2023-09-13
### Changed
- Add row highlight if equity payment already exists in CORE.
- Add views for CORE `CustomerNotifications` table.
- Show CORE-specific datetime for member equity payments.

## [0.1.23] - 2023-09-13
### Changed
- Add views for CORE equity import batches.

## [0.1.22] - 2023-09-08
### Changed
- Fix link to CORE stock purchase.

## [0.1.21] - 2023-09-07
### Changed
- Add CORE supplement for Member Equity Payments view.

## [0.1.20] - 2023-09-02
### Changed
- Expose views for StockPurchase; show equity in CORE member view.
- Add merge, delete-checked support for CORE Customers (classic).

## [0.1.19] - 2023-06-12
### Changed
- Add/improve some CORE member xref links.
- Add upstream credits view when custom purchases view is included.
- Use new pattern for adding link to view customer in CORE Office.
- Add view supplement for CustomerShopper.
- Rename model for `custdata` to `CustomerClassic`.
- Add views for CORE new-style Customer, CustomerAccount.

## [0.1.18] - 2023-05-17
### Changed
- Replace `setup.py` contents with `setup.cfg`.

## [0.1.17] - 2023-05-08
### Changed
- Avoid deprecated import for `OrderedDict`.
- Add column link for CORE Member batches.
- Tweak import per upstream changes.

## [0.1.16] - 2023-02-12
### Changed
- Refactor `Query.get()` => `Session.get()` per SQLAlchemy 1.4.

## [0.1.15] - 2023-02-03
### Changed
- Add way to override CORE-POS data views.
- Remove deprecated `use_buefy` logic.

## [0.1.14] - 2023-01-18
### Changed
- Register integration menu via provider.

## [0.1.13] - 2023-01-02
### Changed
- Add basic view support for CORE trans archive.
- Fix DB engine config references.
- Move the 'quantity' field for CORE Product form.
- Convert master view overrides into view supplements.

## [0.1.12] - 2022-03-15
### Changed
- Add logic for missing card number, in CORE member import batch.

## [0.1.11] - 2022-03-10
### Changed
- Add some CORE-specific things to vendor catalog batch view.

## [0.1.10] - 2022-03-07
### Changed
- Add tailbone provider to declare native and corepos view options.
- Allow download results by default for all CORE views.

## [0.1.9] - 2022-03-02
### Changed
- Show input filename column in CORE member batches grid.
- Include views for PendingProduct model.
- Tweak exposure for some fields.
- Add basic views for CORE user groups.
- Update config defaults for all corepos views.

## [0.1.8] - 2021-11-05
### Changed
- Show member type names for CORE member batch.

## [0.1.7] - 2021-11-04
### Changed
- Add views for CORE "Users" and "Suspensions".
- Only show "in use" products by default, in grid.
- Remove unwanted autocomplete view config.
- Add config for PendingCustomerView.
- Show "view in CORE" buttons for profile view.
- Add more views for product origins.
- Expose new CORE member batch feature.

## [0.1.6] - 2021-08-31
### Changed
- Add "view in CORE" button when viewing MemberInfo.

## [0.1.5] - 2021-08-02
### Changed
- Tweak form to make editing CORE product possible.
- Highlight products not in use.
- Expose views for `TableSyncRules`.
- Add web templates to manifest.
- Expose card number filter by default, for `meminfo` grid.

## [0.1.4] - 2021-06-11
### Changed
- Several more updates...mostly a "save point" release.

## [0.1.3] - 2020-09-25
### Changed
- Don't require CORE ID when creating/editing Person.
- Add generic menu link for CORE Office.

## [0.1.2] - 2020-09-16
### Changed
- A ton of updates, mostly a "save point" release.

## [0.1.1] - 2020-02-27
### Changed
- Add support for multiple DB engines, and HouseCoupon views.
- Show proper flags breakdown for products.
- Highlight inactive product flags as 'warning' in grid.
- Add master view for Parameter model.
- Allow CRUD actions by default, for CORE master views.
- Hide some problematic fields for create/edit CORE customer.
- Cleanup various attribute names, per changes in pyCOREPOS.

## [0.1.0] - 2019-07-09
### Changed
- Initial release.
