# Word conversion template contract

Reference: D:\Work_files\Vessel intervention Robot\力波动方法\write\论文撰写\14371982995898.docx
Reference SHA256: df597ceac1d22789ecfa9e9e7e1f7a1e2597ebe7d9ee0d515be65aaf3c5bb3c5
Source SHA256: f8d006762f6f4436c4a190d2d1b5a48c624502b0efa954edbbbbc10443958cbb

- Reference has 5 pages and 4 sections; title and bilingual front matter are single column, body is double column, template-only appendices are removed.
- A4 11907 × 16840 twips. Front margins top 1247, bottom 1021, left/right 1134 twips. Body margins 720 twips, gap 1133 twips, two columns of 4667 twips each.
- The manuscript table keeps its original full-width role using continuous single-column section breaks before and after the table. Body resumes two columns.
- Use the template title, author, affiliation, and bilingual abstract styles. Body: Songti/Times New Roman 10.5 pt, two-character/21pt first-line indent, at-least 12pt line spacing, zero paragraph before/after.
- User overrides: H1 12pt SimHei before/after 6pt; H2 10.5pt SimHei before6pt after0pt; H3 10.5pt SimHei keeps template second-level spacing2pt/2pt. Captions 9pt Songti/Times New Roman, adjacent Chinese and English centered paragraphs, no terminal period.
- All styles explicitly specify ascii/hAnsi/eastAsia fonts. Manual literal numbering throughout; remove numPr from all content and styles.
- MathType native Equation.DSMT4 embedded objects for all math, WMF vector previews. MathType Times/Symbol preferences Full=10.5pt, table/figure math9pt. Preserve original mathematical meaning and numbering1–27. Center/right tab stops reserve26pt for equation labels.
- Figures1 and5 use the two images actually included by the current TeX. Figures2–4 and6–8 retain their actual source placeholder text and captions. Do not substitute older unused figures.
- Read bibliography from the current compiled BBL, preserve26 references and key-to-number citation mapping. Author metadata, biographies, and placeholders come from current TeX. Footer uses supplied correspondence and manuscript dates; template guidance and sample funding are removed.
- Preserve all template header/footer layout, page rules, existing opaque package parts and original reference. User-requested style fonts, numbering and manuscript content are editable. Current body/XML, relationship graph, bibliography, figures and equations are intentionally replaced.
- Final gate: inspect every page rendered by Microsoft Word, verify no isolated equation label, broken delimiter, symbol spacing, orphaned captions, lost glyphs, or unintended columns. Verify all formula embeddings and every style font structurally, and source/template hashes.

Final verification completed:
- Native Microsoft Word 16.0 (Microsoft Office Office16 path) exported render_v3.pdf, 8 pages. All eight page PNGs visually inspected after the final rebuild.
- Every one of the 172 Equation.DSMT4 objects reopened through the installed MathType native server and round-tripped to the expected expression; no OMML or automatic numbering in the document/styles.
- Equation16 wraps at the equality and keeps the whole row vector within paired brackets. Equation19 fits as a complete set expression. Equation25 wraps at its external subtraction and retains the entire quantified set on one line. The loss22 wraps at the external addition.
- Chinese affiliation postcodes preserved. All58 source occurrences of 待补 plus the English to-be-added placeholder preserved. Source/template SHA256 remain unchanged.
- Title uses a manual break at the subject/predicate boundary to avoid an isolated two-character final line. Figure placeholder paragraphs, bilingual caption pairs, and individual references stay together. Source table separator before the repeatability row retained.
- All73 styles explicitly declare ascii/hAnsi/eastAsia; font sizes and heading spaces passed the structural audit in final_audit.json.
