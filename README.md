# Graffiti Registry AI Pipeline

An automated municipal tracking registry that matches street tagging signatures using AI, aggregates property damage costs, and integrates with mailing APIs to dispatch legal summons and cleanup bills.

## System Workflow
1. **Detection:** Images of vandalism are scanned using a custom YOLO object detection model to crop out localized signatures/monikers.
2. **Matching:** Scaled feature embeddings are extracted from the cropped tags and compared against a registry database using structural similarity metrics.
3. **Escalation:** Confirmed matches aggregate ongoing municipal cleanup costs against a known suspect profile.
4. **Dispatched Summons:** When a legal threshold is met, a webhook triggers a print-and-mail API to issue a physical court summons.

## Project Structure
```text
graffiti-registry/
├── config/
│   └── config.json          # System configuration and API endpoints
├── data/
│   ├── incoming/            # Ingestion folder for new street reports
│   └── database/            # Registry of verified suspect monikers
├── models/
│   └── graffiti_yolo.pt     # Weights file for the object detector
├── src/
│   ├── detector.py          # YOLO bounding-box extraction logic
│   ├── matcher.py           # Feature embedding and matching engine
│   └── legal_trigger.py     # Cost aggregation and Mail API dispatch
├── .gitignore               # Ensures secure environment variables
├── LICENSE                  # MIT open-source permissions
├── main.py                  # Core automation orchestration script
└── requirements.txt         # Package dependencies
