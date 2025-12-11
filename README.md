# Infinite Thread Drift Simulation (Attack C3)

This repository contains a simulation harness for **Attack C3: Infinite Thread Drift**. It demonstrates how subtle, repeated negative feedback accumulates in a persistent multi-agent system, gradually shifting planning behavior without explicit commands.

## Overview

The attack exploits the "infinite context" of a never-resetting conversation thread. An operator provides mild negative feedback (e.g., "Sector B was a waste of time") after missions. Over time, the ScribeAgent's sentiment tracking causes it to downgrade Sector B from "Normal" to "AVOID", which the PlannerAgent respects.

## Structure

- `src/`: Core logic.
    - `agents.py`: ScribeAgent tracks sentiment scores; PlannerAgent reacts to status.
    - `coordinator.py`: Multi-mission manager.
    - `buffer.py`: Persistent shared buffer.
- `scripts/`:
    - `run_drift_experiment.py`: Runs 10 consecutive missions with feedback injection.
- `generate_report.py`: Runs the suite and produces `REPORT.md`.

## Usage

1. **Run Simulation**:
   ```bash
   python3 generate_report.py
   ```

2. **View Results**:
   See `REPORT.md` for the drift timeline.

## Credits

Developed by Antigravity Team.
