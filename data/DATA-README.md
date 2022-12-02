## CSV Data Files
The columns in the *.csv data files are as follows:
annotator,hitid,system,segid,itemtype,src,tgt,score,docid,docscore,start,end

- **annotator**: anonymous ID corresponding to a specific annotator
- **hitid**: ID for the specific HIT
- **system**: MT system
- **segid**: 0-indexed segment ID (0 is the first segment in a document, in a document of n segments, segid n corresponds to the document-level score)
- **itemtype**: TGT (valid score) or BAD (used for QA); see discussion below on how this interacts with docscores
- **src**: source language
- **tgt**: target language
- **score**: score (0-100) for the segment
- **docid**: document ID
- **docscore**: False (indicates segment-level score) or True (indicates document-level score)
- **start**: start time
- **end**: end time


## TSV Segment ID Mapping File
The tab-separated columns in the segment_id_mapping.tsv file are:

- **domain**: news or hansard
- **original document ID**: as found in the original test set data release (sgm files)
- **original segment ID**: 1-indexed segment ID as found in the original test set data release (sgm files)
- **final document ID**: document ID used in the Appraise output (csv files in this directory); note that Hansard is split into pseudo-documents
- **final segment ID**: 0-indexed segment ID; matches segment IDs in Appraise output csv files
- **metrics segment ID**: 0-indexed segment ID used for the metrics task (segment ID according to segment order in original sgm files)


## Document-level scores and itemtype

All csv files contain both segment-level and document-level indications, with the latter indicated by a value of True in the docscore column. These are collected in the same interface, with the segment-level scores produced within document context, and the document-level scores entered after all of a document's segment-level scores are complete.

We use only segment-level scores (docscore: False) in our work, but we provide all the data here for completeness.

The Hansard data contains no quality assurance/quality control items, so all segment-level and document-level scores are labeled TGT.

The News data does contain QA/QC items. At the segment-level, these are labeled with itemtype BAD. There are no document-level scores that are labeled BAD. However, an examination of the document level scores suggest that this may be a mislabeling; some document-level scores may be scores for documents containing BAD references (corrupted MT output which, whose scores compared to those with the uncorrupted output were used to remove annotations through QA/QC processes), and thus should be labeled BAD. We do not have access to the raw BAD reference text data to confirm this. We strongly urge caution in using any of the document-level News scores.
