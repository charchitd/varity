"""Varity shared benchmark dataset.

15 hand-labelled test cases across 5 difficulty tiers:
  EASY    — obvious factual errors (dates, numbers)
  MEDIUM  — partial truths or contested claims
  HARD    — subtle misconceptions that read as plausible
  CLEAN_S — short clean responses (expect 0 flagged)
  CLEAN_L — long multi-claim clean responses (expect 0 flagged)
"""

from __future__ import annotations

from typing import Any

BENCHMARK_CASES: list[dict[str, Any]] = [
    # --- EASY: clear numerical/factual errors ---
    {
        "id": "b01",
        "tier": "EASY",
        "response": "Shakespeare wrote exactly 40 plays and 200 sonnets.",
        "expected_flagged": 1,
        "notes": "Wrong counts: 37 plays, 154 sonnets.",
    },
    {
        "id": "b02",
        "tier": "EASY",
        "response": "The speed of sound in air is approximately 340 km/h.",
        "expected_flagged": 1,
        "notes": "340 m/s is correct; 340 km/h is wrong by ~3.6×.",
    },
    {
        "id": "b03",
        "tier": "EASY",
        "response": (
            "Neil Armstrong landed on the Moon in July 1970 during the Apollo 11 mission."
        ),
        "expected_flagged": 1,
        "notes": "It was 1969, not 1970.",
    },
    # --- MEDIUM: partial truths, debated claims ---
    {
        "id": "b04",
        "tier": "MEDIUM",
        "response": (
            "The Great Wall of China is clearly visible from space with the naked eye. "
            "It was built entirely during the Ming Dynasty."
        ),
        "expected_flagged": 1,
        "notes": "Space visibility is a myth; Ming Dynasty is a partial truth (multiple dynasties built it).",
    },
    {
        "id": "b05",
        "tier": "MEDIUM",
        "response": (
            "The Amazon River is the longest river in the world. "
            "The Nile is the second longest."
        ),
        "expected_flagged": 1,
        "notes": "The Nile is generally considered the longest; the Amazon claim is contested.",
    },
    {
        "id": "b06",
        "tier": "MEDIUM",
        "response": (
            "Napoleon Bonaparte was very short for his time, standing around 5 feet 2 inches tall."
        ),
        "expected_flagged": 1,
        "notes": "The 'short Napoleon' is a myth; he was ~5'6\", average for his era.",
    },
    # --- HARD: subtle plausible-sounding errors ---
    {
        "id": "b07",
        "tier": "HARD",
        "response": (
            "Penicillin was discovered by Alexander Fleming in 1928 when he noticed "
            "mold killing bacteria on a petri dish. It became the first antibiotic "
            "used clinically in 1942."
        ),
        "expected_flagged": 0,
        "notes": "Broadly correct — Florey/Chain's clinical use is debated but 1942 is accepted.",
    },
    {
        "id": "b08",
        "tier": "HARD",
        "response": (
            "Humans and chimpanzees share approximately 99% of their DNA. "
            "This makes chimps our closest living relatives."
        ),
        "expected_flagged": 0,
        "notes": "~98.7% is commonly cited; 99% is within rounding — broadly correct.",
    },
    {
        "id": "b09",
        "tier": "HARD",
        "response": (
            "The Great Fire of London in 1666 destroyed most of the medieval city "
            "and killed thousands of people."
        ),
        "expected_flagged": 1,
        "notes": "Death toll was remarkably low (6 confirmed); 'thousands' is wrong.",
    },
    {
        "id": "b10",
        "tier": "HARD",
        "response": (
            "Albert Einstein failed mathematics as a child and was considered a poor student."
        ),
        "expected_flagged": 1,
        "notes": "Well-known myth — Einstein excelled at both math and physics from an early age.",
    },
    # --- CLEAN_S: short fully-correct responses (expect 0 flagged) ---
    {
        "id": "b11",
        "tier": "CLEAN_S",
        "response": "Python was created by Guido van Rossum and first released in 1991.",
        "expected_flagged": 0,
        "notes": "Fully correct — no claims should be flagged.",
    },
    {
        "id": "b12",
        "tier": "CLEAN_S",
        "response": "Water boils at 100°C at standard atmospheric pressure.",
        "expected_flagged": 0,
        "notes": "Correct physical fact.",
    },
    {
        "id": "b13",
        "tier": "CLEAN_S",
        "response": "Mount Everest is the tallest mountain on Earth at 8,849 metres.",
        "expected_flagged": 0,
        "notes": "Correct — 2020 survey figure.",
    },
    # --- CLEAN_L: multi-claim fully-correct responses (expect 0 flagged) ---
    {
        "id": "b14",
        "tier": "CLEAN_L",
        "response": (
            "The human body has 206 bones in adulthood. "
            "Babies are born with approximately 270 bones that fuse over time. "
            "The femur is the longest bone in the human body."
        ),
        "expected_flagged": 0,
        "notes": "All three anatomical facts are correct.",
    },
    {
        "id": "b15",
        "tier": "CLEAN_L",
        "response": (
            "Water covers about 71% of the Earth's surface. "
            "The Pacific Ocean is the largest ocean, covering more area than all "
            "land masses combined. "
            "The Mariana Trench is the deepest point in the ocean at about 11,000 metres."
        ),
        "expected_flagged": 0,
        "notes": "All three geographic facts are correct.",
    },
]
