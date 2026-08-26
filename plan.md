## Refresh Button Audit Plan
- [x] Audit every existing refresh, reload, retry, and refresh-data control across the app and identify the exact data/state each one should refresh.
- [x] Fix refresh controls that are no-op or incomplete so they re-fetch/recompute the correct backend or uploaded-dataset state with loading/error handling and duplicate-request protection.
- [x] Verify the fixed controls with targeted event tests and desktop/mobile screenshots, then report every found component with PASS/FAIL status.