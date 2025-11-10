# Quick Start Guide: Viral Lifecycle BNGL Model

This guide will help you get started with the BioNetGen implementation of the viral lifecycle model.

## Step-by-Step Instructions

### 1. Install Required Packages

```bash
pip install bionetgen libroadrunner pandas matplotlib numpy openpyxl
```

### 2. Run the BNGL Simulation

```bash
python simulate_viral_lifecycle.py
```

**Expected output:**
- Console messages showing simulation progress
- `viral_lifecycle.xml` - SBML model file
- `viral_lifecycle_results.csv` - Simulation data
- `viral_lifecycle_timecourse.png` - Plots
- Interactive plot window

**Time:** ~30 seconds

### 3. (Optional) Validate Against MATLAB

If you want to validate the BNGL model against the original MATLAB implementation:

#### 3a. Run MATLAB Simulation

In MATLAB:
```matlab
run_viral_lifecycle_matlab
```

Or from command line:
```bash
matlab -batch "run_viral_lifecycle_matlab"
```

**Expected output:**
- `viral_lifecycle_matlab_results.csv`
- `viral_lifecycle_matlab_timecourse.png`

**Time:** ~1-2 minutes

#### 3b. Compare Results

```bash
python validate_viral_lifecycle.py
```

**Expected output:**
- Error metrics printed to console
- `validation_comparison.png` - Side-by-side plots
- `validation_error_heatmap.png` - Error visualization
- Interactive plot windows

**Time:** ~10 seconds

### 4. View Results

The key files to examine:

1. **`viral_lifecycle_timecourse.png`** - BNGL simulation plots
2. **`viral_lifecycle_results.csv`** - Numeric results (can open in Excel)
3. **`validation_comparison.png`** - MATLAB vs BNGL comparison (if validation run)

## What You Should See

### Key Dynamics

The viral lifecycle simulation shows:

1. **V_0** (initial virus) rapidly enters cells (exponential decay)
2. **V_I** (intracellular virus) transiently increases then decreases as RNA is released
3. **R_cyt** (cytoplasmic RNA) accumulates from virus uncoating and replication
4. **P_S** and **P_NS** (proteins) increase steadily via translation
5. **RC_CM** (replication complexes) form after a lag period (membrane maturation)
6. **R_ds** (dsRNA) accumulates from replication complex activity
7. **V_E** (extracellular virus) increases over time from virion assembly/release

### Typical Values (48 hours)

| Species | Final Value (approx) |
|---------|---------------------|
| V_E | ~10^2 - 10^4 |
| V_I | ~10^0 - 10^1 |
| R_cyt | ~10^1 - 10^3 |
| P_S | ~10^2 - 10^4 |
| R_ds | ~10^1 - 10^2 |

### Validation Results

If validation is successful, you should see:
- Max relative error < 1% for all species
- "✓ VALIDATION PASSED" message

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'bionetgen'"

**Solution:**
```bash
pip install bionetgen
```

### Issue: "ModuleNotFoundError: No module named 'roadrunner'"

**Solution:**
```bash
pip install libroadrunner
```

### Issue: "BNGL file not found"

**Solution:** Make sure you're running the script from the correct directory:
```bash
cd /path/to/Integrated_Virus-Immune_Model
python simulate_viral_lifecycle.py
```

### Issue: Validation script says "MATLAB results not found"

**Solution:** Run the MATLAB simulation first:
```matlab
run_viral_lifecycle_matlab
```

### Issue: Plots don't appear

**Solution:**
- On macOS/Linux with remote connection, set backend:
  ```bash
  export MPLBACKEND=Agg
  ```
- Or modify the Python scripts to use `plt.savefig()` only (comment out `plt.show()`)

## Next Steps

Once you've successfully run the viral lifecycle model:

1. **Explore parameters**: Edit `viral_lifecycle.bngl` to change parameter values
2. **Modify initial conditions**: Change `V_0_init` to simulate different MOIs
3. **Extend simulation time**: Modify `t_end` in the BNGL file or Python script
4. **Add analysis**: Modify Python scripts to calculate additional metrics (peak time, AUC, etc.)
5. **Implement full model**: Extend to include immune response and viral antagonism

## File Overview

```
Integrated_Virus-Immune_Model/
├── viral_lifecycle.bngl              # BNGL model file
├── simulate_viral_lifecycle.py       # Python simulation script
├── run_viral_lifecycle_matlab.m      # MATLAB simulation script
├── validate_viral_lifecycle.py       # Validation script
├── README_viral_lifecycle_bngl.md    # Detailed documentation
└── QUICKSTART.md                     # This file
```

## Support

For questions or issues:
1. Check the detailed README: `README_viral_lifecycle_bngl.md`
2. Consult BioNetGen documentation: https://bionetgen.org
3. Consult libroadrunner documentation: https://libroadrunner.org

## Summary

You now have:
- ✓ A BNGL model of the viral lifecycle
- ✓ Python scripts for simulation and validation
- ✓ MATLAB validation code
- ✓ Complete documentation

The model is ready for extension to include immune response pathways and viral antagonism mechanisms!
