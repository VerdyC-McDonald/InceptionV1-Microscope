# InceptionV1 Microscope

Buildless research explorer implemented in HTML, CSS, and JavaScript. Site source is synced with its managed Git repository. The deployable application is `dist/`.

## Included

- All 12 observation layers, 5,804 neurons, 363 ordered 4×4 groups.
- Four exploration levels with local layer scrolling, group expansion, neighboring-layer relations, and continuous details.
- Layer:neuron locator, URL fragment restore, in-session research history, persistent image mode, zoom, and compact scroll navigation.
- Manually transcribed mixed4c:327 statistics and 16 signed relations from the supplied audit.
- Explicit missing-image and missing-data states. No generated model data or inference.

## Data provenance and next integration

`dist/data/structure.json` and `sample.json` are the supplied audit files. They are not an official model export. The sample's class summary is incomplete; x/60 meaning remains unverified. Upstream and downstream color scales are independent. Missing relationships are unknown, not zero.

Image ingestion and full-corpus detail ingestion are not yet connected. A future data adapter should replace `datum()` and image placeholders with verified records keyed by layer and neuron, preserving method, source display order, missingness, and asset provenance. Do not substitute a different model's channels without explicit alignment.

## Validation

JavaScript syntax checked with `node --check dist/app.js`. Structure and sample validation confirmed layer counts, every consecutive neuron ID, 16-cell grouping including empty slots, and the validity/signs of all sample relation targets.

Browser visual and interaction QA could not run: the managed preview supervisor's mailbox is unavailable in this environment. This limitation does not constitute browser verification.

## Layer-card refinement

Layers now have full-area clickable rounded frames. Compact groups are vertically centered, with row-major two-column layouts above 12 groups; square cell dimensions are retained even for the 1,024-neuron layer. Focus frames resize over 640ms before staged content reveal. Reduced-motion preferences bypass movement. Current-layer background clicks preserve focus; group padding opens its group; adjacent neuron clicks continue to open the actual neuron.

Validated JavaScript syntax, click routing, and compact-grid fit calculations for all 12 layers. Managed browser preview remains unavailable, so visual animation QA is still pending.

## Group spacing and research overview refinement

Every compact 4×4 grid now has its own rounded frame, 2px internal padding, and 6px separation (8px for adjacent research layers). Dense compact layers use up to three columns to preserve these boundaries. Research mode has a taller canvas and neighboring overview layers with up to four columns; every neighboring group fits without local scrolling. Signed known relations use stronger colors, with a double outline for the largest absolute known positive and negative value in each direction. The original record order is preserved.

Rendering reuses unchanged layers and detail content. Width, min-width and flex-basis animations were replaced with transform/opacity FLIP transitions; geometry reads are batched before animation writes. Content reveal is limited to a few containers, rather than animating every group or neuron.

All 12 layers were checked in normal and adjacent-overview geometry for positive square cells, border/padding/gaps, and full fit. JavaScript syntax and diff checks passed. Browser preview remains unavailable; actual FPS and visual animation performance have not been measured.

## Direct source ingestion 2026-10-23

The previously unavailable source is now reachable from the executor. Direct HTTP 200 downloads verified meta.json, the viewer, robots.txt, all 12 layer JSON files (10,138,128 bytes), 3 boundary/interior connection records, and representative FV, sheet, thumbnail and heat files. The 12 JSONs contain all 5,804 consecutive neuron IDs. Downloaded JSONs retain original precision and ordering.

The app now loads layer metadata on demand from its own same-origin `source/data/` files. All neuron statistics, provided class summaries, example image IDs, labels, scores and ranks are available. Three connection records are adapted to the existing directional Top-4 UI; the original sparse lists are kept. mixed4c:327 has 4 visible FV variants and its 48-cell sheet/Top-4 thumbnail. Its fifth FV is marked hidden in the source, so the available placeholder PNG is not exposed. Two boundary nodes have Positive FV and connection records. Other image and connection assets remain explicitly unimported. The downloaded heat file is verified but no heat overlay UI has been added in this pass.

Verification: `node scripts/verify-source.mjs` checks all records, adapter precision and direction boundaries, original ordering, 1,118 hidden FV slots, hidden-neuron suppression, all 48 sprite cells and sample asset paths. `dist/source/verification.json` contains download responses and layer hashes. Browser QA remains unverified because the managed preview supervisor is unavailable.

Important limits: robots allows these paths but is not a redistribution license. Missing CORS headers prevent ordinary cross-origin frontend fetch; hosting verified files under this Site avoids that problem. The source connection files contain sparse positive/negative lists (8 per sign in the interior sample), not a full pairwise matrix. The viewer itself takes the first 4 per sign; this app preserves that behavior. x/60 is documented in the source viewer as same-sign support among 60 examples. The corpus has 29,020 FV slots, 1,118 marked hidden; hidden slots are not treated as failed downloads. No full-corpus image mirror or full connection download is claimed.
