# Railmind Evaluation

This directory contains evaluation metrics and documentation for the AI models used within the Railmind platform, specifically the acoustic detection model.

## Swin Transformer Acoustic Detector

The acoustic detector is responsible for identifying potential anomalies (e.g., micro-cracks, wheel flats, rail breaks) from telemetry audio data.

### Model Architecture
The model uses a custom Swin Transformer architecture adapted for audio processing. Raw telemetry audio is converted into log-mel spectrograms, which are then passed through the hierarchical vision transformer to capture both local transient sounds and global acoustic patterns.

### Dataset
- **Source**: Synthetic acoustic data generated using track interaction simulations.
- **Total Samples**: 5,000 samples.
- **Split**: 70% Train, 15% Validation, 15% Test.
- **Classes**: 
  - `normal_operation`
  - `micro_crack`
  - `wheel_flat`
  - `rail_break`

### Evaluation Methodology
The model was evaluated on the held-out test set (750 samples). Metrics calculated include overall Precision, Recall, and F1-Score, alongside per-class metrics to ensure balanced performance across different anomaly types.

### Key Results
- **Overall Precision**: 0.94
- **Overall Recall**: 0.91
- **Overall F1-Score**: 0.92

The model shows strong performance, particularly in identifying `normal_operation` and critical `rail_break` events. `micro_crack` detection shows slightly lower performance due to the subtle acoustic signatures involved.

*Full details and confusion matrix can be found in `acoustic_model_metrics.json`.*

## Reproducing Evaluations

To run the evaluation pipeline locally (requires model weights and dataset access):

```bash
# Navigate to the model directory (if applicable)
cd backend/models/acoustic
python evaluate.py --config configs/eval_swin.yaml --checkpoint weights/best_model.pth
```
