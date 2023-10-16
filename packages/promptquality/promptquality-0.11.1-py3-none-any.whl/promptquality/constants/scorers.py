from enum import Enum


class Scorers(str, Enum):
    toxicity = "toxicity"
    factuality = "factuality"
    groundedness = "groundedness"
    pii = "pii"
    latency = "latency"
    context_relevance = "context_relevance"
    sexist = "sexist"
    tone = "tone"
