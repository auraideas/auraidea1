# Detector research notes

Sources:
- https://gowinston.ai/plagiarism-checker/
- https://gowinston.ai/ai-content-detector/
- https://docs.gowinston.ai/api-reference/introduction
- https://docs.gowinston.ai/api-reference/v2/ai-content-detection/post.md
- https://docs.gowinston.ai/api-reference/v2/plagiarism/post.md
- https://proofademic.ai/blog/how-does-turnitin-detect-ai/

Key findings used for product design:
- Winston presents sentence-level scores/highlights, sources and match sequences, shareable reports, AI detection, plagiarism, readability and writing feedback.
- Winston's official AI API requires text of at least 300 characters for detection; under 600 characters may be unreliable; maximum 150,000 characters. Response includes a human score, sentence scores, readability, attack indicators, credits and model version.
- Winston's official plagiarism API requires at least 100 characters and returns source details, match sequences, indexes, citations and credit usage.
- Winston's docs state API auth is Bearer token; AI detection costs 1 credit per word and plagiarism costs 2 credits per word.
- Winston's current official AI detector language list includes English, French, Spanish, Portuguese, Dutch, German, Polish, Italian, Romanian, Indonesian, Tagalog, Russian, Bulgarian and Simplified Chinese; Arabic is not listed in the fetched API documentation.
- Proofademic's Turnitin explainer emphasizes that detectors use statistical/linguistic pattern likelihood rather than semantic understanding; signals include word predictability/perplexity, sentence rhythm/burstiness and templated transitions. It also notes false positives, effects of polished or non-native writing, limits on short/list/table content, and that low scores are not proof of human authorship.

Implementation implication: the static Aura site can provide a transparent heuristic sentence-level indicator, but a Winston-class engine requires a server-side model/API and a source-search corpus. Never present the heuristic as a definitive verdict.
