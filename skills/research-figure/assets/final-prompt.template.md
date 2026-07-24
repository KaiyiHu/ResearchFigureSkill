[COMPILED_FROM: RF-COMPILE-2.0 | FIGURESPEC: {{FIGURESPEC_VERSION}} | FIGURE: {{FIGURE_ID}} | SUMMARY_SHA256: {{SUMMARY_SHA256}}]

# 1. JOB, TARGET, AND CANVAS

Create a publication-quality scientific figure for **{{VENUE_OR_MEDIUM}}**.

- Figure role: {{FIGURE_ROLE}}
- Reader question: {{READER_QUESTION}}
- Five-second message: {{FIVE_SECOND_MESSAGE}}
- Audience and language: {{AUDIENCE}} / {{LANGUAGE}}
- Canvas: {{WIDTH_OR_COLUMN}}; {{ASPECT_RATIO}}; {{PIXELS_OR_PHYSICAL_SIZE}}
- Editable source required: {{YES_OR_NO}}

# 2. REFERENCE-FIGURE CONTRACT

Reference available: {{YES_OR_NO}}

Use only these abstract attributes:

{{REFERENCE_ATTRIBUTES_TO_USE}}

Do not copy:

{{REFERENCE_CONTENT_OR_EXPRESSION_NOT_TO_COPY}}

The scientific inventory below overrides the reference whenever they conflict.

# 3. SCIENTIFIC TOPIC AND PURPOSE

{{TOPIC_AND_PURPOSE}}

Claim boundary:

{{CLAIM_BOUNDARY}}

# 4. SCIENTIFIC NARRATIVE

The figure must communicate this sequence or comparison:

{{SCIENTIFIC_NARRATIVE}}

# 5. CONTENT AND EXACT-TEXT INVENTORY

Main title:

{{TITLE}}

Required components:

{{COMPONENTS_WITH_IDS_AND_LABELS}}

Required exact text:

{{EXACT_TEXT}}

# 6. RELATION AND ARROW CONTRACT

{{RELATIONS_WITH_SOURCE_TARGET_DIRECTION_TYPE_AND_PAYLOAD}}

Never add an unlabeled or scientifically ambiguous arrow.

# 7. GLOBAL LAYOUT AND REGION GEOMETRY

{{GLOBAL_LAYOUT_AND_READING_ORDER}}

Normalized regions:

{{REGION_GEOMETRY_X_Y_WIDTH_HEIGHT_PERCENT}}

# 8. PER-PANEL COMPOSITION

{{PANEL_OR_REGION_INSTRUCTIONS}}

# 9. VISUAL LANGUAGE

- Background: {{BACKGROUND}}
- Palette and semantics: {{PALETTE_AND_MEANING}}
- Typography: {{FONT_AND_HIERARCHY}}
- Border and line treatment: {{BORDERS_AND_LINES}}
- Icon language: {{ICON_RULES}}
- Density and whitespace: {{DENSITY_AND_WHITESPACE}}
- Accessibility: pair color with shape, text, or line style.

# 10. EDITABLE CONSTRUCTION CONTRACT

{{RENDERER_ADAPTER}}

- Keep final labels as live editable text.
- Give important groups and relations stable IDs.
- Do not flatten the complete figure into one bitmap.
- If AI image generation is used, generate only the approved illustration
  layer; add exact text, arrows, equations, and values deterministically.

# 11. NEGATIVE PROMPT

Do not include:

{{ROLE_SPECIFIC_NEGATIVE_CONSTRAINTS}}

Always exclude:

- invented components, values, equations, citations, or causal links;
- wrong, pseudo-, warped, duplicated, or misspelled text;
- font substitution, missing glyphs, or corrupted symbols;
- rasterized final labels or unreadable microtext;
- blurred, fuzzy, melted, ghosted, or partially erased shapes;
- soft edges caused by low-resolution upscaling;
- overlapping, clipped, truncated, or off-canvas labels;
- decorative AI brains, robots, chips, logos, watermarks, or venue badges
  unless explicitly required;
- gradients, gloss, 3D decoration, or shadows unless the validated style
  contract explicitly asks for them.

# 12. OUTPUT CONTRACT

Return:

{{EDITABLE_FORMATS_AND_PREVIEWS}}

Return an editable master, crisp preview, provenance record, and completed
audit.

Also report any instruction that could not be rendered faithfully. Never fill
missing evidence with plausible-looking content.

# 13. PREFLIGHT BEFORE DELIVERY

- [ ] One dominant reader question is answered.
- [ ] Every required component appears and every forbidden component is absent.
- [ ] Every arrow has the correct endpoints, direction, type, and payload.
- [ ] Every required label matches the exact-text register.
- [ ] No text is garbled, misspelled, warped, clipped, or rasterized.
- [ ] No local region is blurred, fuzzy, melted, or visibly upscaled.
- [ ] The figure is readable at final publication size and crisp at 100% and 200%.
- [ ] SVG/PPTX/draw.io objects remain editable and grouped.
- [ ] The claim boundary cannot be misread from scale, color, or arrows.
