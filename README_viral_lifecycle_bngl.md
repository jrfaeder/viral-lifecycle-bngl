# Viral Lifecycle Model - BioNetGen Implementation

This directory contains a BioNetGen (BNGL) implementation of the viral lifecycle model, which can be simulated using Python and libroadrunner.

## Overview

The viral lifecycle model describes the infection dynamics of a virus, including:
- Virus entry and internalization
- RNA replication and trafficking
- Protein translation
- Virus assembly and release

This BNGL implementation replicates the viral lifecycle portion of the integrated virus-immune model described in the original MATLAB code.

## Files

### Model Files
- **`viral_lifecycle.bngl`**: BioNetGen model file defining the viral lifecycle reactions, species, and parameters

### Simulation Scripts
- **`simulate_viral_lifecycle.py`**: Python script to simulate the BNGL model using bionetgen and libroadrunner
- **`run_viral_lifecycle_matlab.m`**: MATLAB script to simulate only the viral lifecycle using the original ODE model

### Validation Scripts
- **`validate_viral_lifecycle.py`**: Python script to compare BNGL and MATLAB simulation results

### Data Files (Generated)
- `viral_lifecycle.xml`: SBML file generated from BNGL (automatically created)
- `viral_lifecycle_results.csv`: BNGL simulation results
- `viral_lifecycle_matlab_results.csv`: MATLAB simulation results
- `viral_lifecycle_timecourse.png`: Plots from BNGL simulation
- `viral_lifecycle_matlab_timecourse.png`: Plots from MATLAB simulation
- `validation_comparison.png`: Side-by-side comparison of MATLAB vs BNGL
- `validation_error_heatmap.png`: Error metrics visualization

## Model Species

The viral lifecycle model includes the following species:

| Species | Description |
|---------|-------------|
| `V_E` | Extracellular virus |
| `V_0` | Initial virus (before entry) |
| `V_I` | Intracellular virus |
| `R_cyt` | Cytoplasmic (+) RNA |
| `R_CM` | Cell membrane-associated (+) RNA |
| `P_S` | Structural proteins |
| `P_NS` | Non-structural proteins |
| `RC_CM` | Replication complex at cell membrane |
| `R_ds` | Double-stranded RNA |

## Model Parameters

Key parameters from the original model:

| Parameter | Value | Units | Description |
|-----------|-------|-------|-------------|
| `k_en` | 2.00e-03 | 1/min | Virus entry rate |
| `k_f` | 5.17e-04 | 1/min | Viral fusion rate |
| `k_a` | 6.00e-07 | 1/(mol·min) | Virus assembly rate |
| `k_e` | 1.10e-03 | 1/min | RNA export rate |
| `k_r` | 6.00e-02 | 1/min | RNA return rate |
| `k_c` | 4.33e-02 | 1/(mol·min) | RC formation rate |
| `k_t` | 3.95e-01 | 1/min | Translation rate |
| `tau` | 3.48e+02 | min | Membrane formation time |
| `a_RC` | 4.67e-04 | 1/min | RC maturation rate |
| `mu_r` | 4.17e-03 | 1/min | RNA degradation rate |
| `mu_p` | 1.83e-03 | 1/min | Protein degradation rate |
| `mu_V_I` | 6.67e-04 | 1/min | Intracellular virus decay |
| `mu_V_E` | 1.00e-04 | 1/min | Extracellular virus decay |

## Installation

### Prerequisites

1. **Python packages**:
```bash
pip install bionetgen libroadrunner pandas matplotlib numpy openpyxl
```

2. **MATLAB** (for validation only):
   - MATLAB R2018a or later
   - Required files: `ODEs.m`, `Param.xlsx`, `param.mat`

### Verification

Check that bionetgen is installed:
```bash
python -c "import bionetgen; print(bionetgen.__version__)"
```

Check that libroadrunner is installed:
```bash
python -c "import roadrunner; print(roadrunner.__version__)"
```

## Usage

### Step 1: Simulate the BNGL Model

Run the Python simulation script:

```bash
python simulate_viral_lifecycle.py
```

This will:
1. Load the BNGL model from `viral_lifecycle.bngl`
2. Generate SBML using bionetgen
3. Simulate using libroadrunner
4. Generate plots and save results to CSV

**Output files:**
- `viral_lifecycle.xml` - SBML model
- `viral_lifecycle_results.csv` - Simulation results
- `viral_lifecycle_timecourse.png` - Time course plots

### Step 2: Run MATLAB Validation (Optional)

If you want to validate against the original MATLAB model:

```bash
matlab -batch "run_viral_lifecycle_matlab"
```

Or in MATLAB:
```matlab
run_viral_lifecycle_matlab
```

**Output files:**
- `viral_lifecycle_matlab_results.csv` - MATLAB results
- `viral_lifecycle_matlab_timecourse.png` - MATLAB plots

### Step 3: Validate BNGL vs MATLAB (Optional)

Compare the BNGL and MATLAB results:

```bash
python validate_viral_lifecycle.py
```

This will:
1. Load both MATLAB and BNGL results
2. Interpolate to common time points
3. Calculate error metrics
4. Generate comparison plots

**Output files:**
- `validation_comparison.png` - Side-by-side comparison
- `validation_error_heatmap.png` - Error metrics heatmap

## Model Structure

### Reactions

The BNGL model includes the following reaction classes:

1. **Virus Entry & Internalization**
   - `V_0 -> V_I` (entry)
   - `V_I -> R_cyt` (fusion/uncoating)

2. **RNA Trafficking**
   - `R_CM -> R_cyt` (export to cytoplasm)
   - `RC_CM -> R_CM` (from replication complex)

3. **Protein Translation**
   - `R_cyt -> R_cyt + P_S` (structural protein synthesis)
   - `R_cyt -> R_cyt + P_NS` (non-structural protein synthesis)

4. **Replication Complex Formation**
   - `R_cyt + P_NS -> RC_CM` (complex assembly)
   - `RC_CM -> R_CM + R_ds` (maturation)

5. **Virus Assembly & Release**
   - `P_S + R_cyt -> P_S + V_E` (virion assembly)

6. **Degradation**
   - Species degradation: `V_I`, `V_E`, `R_cyt`, `R_ds`, `P_S`, `P_NS`

### Key Features

- **Time-dependent membrane formation**: The replication complex formation rate depends on a sigmoidal function of time (`f_CM`)
- **Saturation kinetics**: RC formation includes saturation at `rcsat` molecules
- **Catalytic reactions**: Structural proteins act catalytically in virus assembly

## Simulation Parameters

- **Initial condition**: V_0 = 100 (MOI = 10)
- **Simulation time**: 48 hours (2880 minutes)
- **Time points**: 200 points
- **Solver**: ODE solver with adaptive time stepping

## Expected Results

When running the viral lifecycle model with default parameters:

1. **V_0** (initial virus) decays rapidly (entry into cell)
2. **V_I** (intracellular virus) peaks early, then decays as RNA is released
3. **R_cyt** (cytoplasmic RNA) increases from virus uncoating and replication
4. **P_S** and **P_NS** (proteins) increase via translation
5. **RC_CM** (replication complexes) form after membrane maturation
6. **R_ds** (dsRNA) accumulates from replication
7. **V_E** (extracellular virus) increases from virion assembly and release

## Validation

The validation script compares BNGL and MATLAB simulations using:

- **Absolute error**: |MATLAB - BNGL|
- **Relative error**: |MATLAB - BNGL| / |MATLAB|

Expected validation results:
- Max relative error < 1% indicates excellent agreement
- Max relative error < 10% indicates acceptable agreement

## Next Steps

1. **Add immune response**: Extend the BNGL model to include the host immune response pathways (RIG-I, MAVS, IRF3, NFκB, JAK-STAT)

2. **Add viral antagonism**: Include viral antagonism of immune signaling (P_NS inhibition of MAVS, IRF3, etc.)

3. **Parameter sensitivity**: Use BioNetGen's parameter scanning capabilities to explore model behavior

4. **Stochastic simulations**: Compare deterministic ODE simulations with stochastic simulations using NFsim

5. **Model analysis**: Use BioNetGen's network analysis tools to study model structure and dynamics

## References

- BioNetGen documentation: https://bionetgen.org
- libroadrunner documentation: https://libroadrunner.org
- Original model: See `ODEs.m` and associated publication

## Troubleshooting

### Common Issues

1. **"bionetgen not found"**
   - Install: `pip install bionetgen`

2. **"libroadrunner not found"**
   - Install: `pip install libroadrunner`

3. **"SBML file not generated"**
   - Check that the BNGL file has no syntax errors
   - Ensure bionetgen can write to the output directory

4. **"MATLAB results not found"**
   - Run `run_viral_lifecycle_matlab.m` in MATLAB first
   - Ensure you have the required `ODEs.m` and `param.mat` files

### Getting Help

If you encounter issues:
1. Check that all prerequisites are installed
2. Verify file paths are correct
3. Check the console output for error messages
4. Consult BioNetGen and libroadrunner documentation

## License

This implementation is provided for research and educational purposes.
