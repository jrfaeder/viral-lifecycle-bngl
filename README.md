# Viral Lifecycle Model - BioNetGen Implementation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![BioNetGen](https://img.shields.io/badge/BioNetGen-2.8+-green.svg)](https://bionetgen.org)

A BioNetGen (BNGL) reimplementation of the viral lifecycle model from:

**Boddepalli R, Chhajer H, Roy R.** Integrative Modelling of Innate Immune Response Dynamics during Virus Infection. bioRxiv; 2025. doi:10.1101/2025.06.17.660089
https://www.biorxiv.org/content/10.1101/2025.06.17.660089v3

This repository provides a rule-based implementation of the viral lifecycle portion of the Boddepalli et al. model, with Python/libroadrunner simulation tools and MATLAB validation code.

## Overview

This repository contains a rule-based implementation of viral infection dynamics, including:
- Virus entry and internalization
- RNA replication and trafficking
- Protein translation
- Replication complex formation
- Virus assembly and release

The model is implemented in BioNetGen Language (BNGL) and can be simulated using Python with the `bionetgen` and `libroadrunner` packages.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/jrfaeder/viral-lifecycle-bngl.git
cd viral-lifecycle-bngl

# Install dependencies
pip install bionetgen libroadrunner pandas matplotlib numpy openpyxl

# Run simulation
python simulate_viral_lifecycle.py
```

See **[QUICKSTART.md](QUICKSTART.md)** for detailed instructions.

## Repository Contents

```
viral-lifecycle-bngl/
├── README.md                          # This file
├── QUICKSTART.md                      # Step-by-step guide
├── CITATION.md                        # Citation and attribution
├── LICENSE                            # MIT License
│
├── viral_lifecycle.bngl               # BioNetGen model (9 species, 13 reactions)
├── simulate_viral_lifecycle.py        # Python simulation script
├── validate_viral_lifecycle.py        # Validation script
│
├── ODEs.m                             # Original MATLAB ODE system
├── Param.xlsx                         # Model parameters
├── Param_vector.m                     # Parameter loading script
└── run_viral_lifecycle_matlab.m       # MATLAB validation script
```

## Model Description

### Species (9)

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

### Key Processes

1. **Virus Entry**: V_0 → V_I (entry) → R_cyt (fusion)
2. **Translation**: R_cyt → P_S, P_NS
3. **Replication Complex Formation**: R_cyt + P_NS → RC_CM
4. **RNA Replication**: RC_CM → R_CM + R_ds
5. **Virus Assembly**: P_S + R_cyt → V_E
6. **Degradation**: All species undergo degradation

### Parameters

All 15 parameters are extracted from `Param.xlsx`:

- `k_en = 2.00e-03` - Virus entry rate (1/min)
- `k_f = 5.17e-04` - Viral fusion rate (1/min)
- `k_a = 6.00e-07` - Virus assembly rate (1/mol·min)
- `k_t = 3.95e-01` - Translation rate (1/min)
- `tau = 3.48e+02` - Membrane formation time constant (min)
- And 10 more...

See [README_viral_lifecycle_bngl.md](README_viral_lifecycle_bngl.md) for complete parameter list.

## Installation

### Prerequisites

- **Python 3.7+**
- **MATLAB R2018a+** (optional, for validation only)

### Python Packages

```bash
pip install bionetgen libroadrunner pandas matplotlib numpy openpyxl
```

### Verify Installation

```bash
python -c "import bionetgen; print('bionetgen:', bionetgen.__version__)"
python -c "import roadrunner; print('libroadrunner:', roadrunner.__version__)"
```

## Usage

### 1. Simulate BNGL Model

```bash
python simulate_viral_lifecycle.py
```

**Output:**
- `viral_lifecycle.xml` - SBML model
- `viral_lifecycle_results.csv` - Simulation data
- `viral_lifecycle_timecourse.png` - Plots

### 2. Validate Against MATLAB (Optional)

```bash
# In MATLAB
matlab -batch "run_viral_lifecycle_matlab"

# Or in MATLAB interactive session
>> run_viral_lifecycle_matlab
```

**Output:**
- `viral_lifecycle_matlab_results.csv`
- `viral_lifecycle_matlab_timecourse.png`

### 3. Compare Results (Optional)

```bash
python validate_viral_lifecycle.py
```

**Output:**
- `validation_comparison.png` - Side-by-side comparison
- `validation_error_heatmap.png` - Error metrics
- Console output with error statistics

## Expected Results

Simulating with default parameters (MOI=10, 48 hours) produces:

- **V_0** rapidly decays (virus entry)
- **V_I** transiently increases then decreases
- **R_cyt** accumulates from virus uncoating
- **P_S** and **P_NS** increase via translation
- **RC_CM** forms after membrane maturation
- **R_ds** accumulates from replication
- **V_E** increases from virus assembly

Validation should show < 1% relative error between BNGL and MATLAB.

## Documentation

- **[README.md](README.md)** - Quick overview (this file)
- **[QUICKSTART.md](QUICKSTART.md)** - Step-by-step tutorial
- **[README_viral_lifecycle_bngl.md](README_viral_lifecycle_bngl.md)** - Complete technical documentation
- **[CITATION.md](CITATION.md)** - How to cite this work

## Development

### Project Structure

The BNGL model is designed to be modular and extensible:

```
viral_lifecycle.bngl
├── parameters      # 15 parameters from original model
├── molecule types  # 9 species definitions
├── seed species    # Initial conditions (MOI=10)
├── observables     # Output species concentrations
├── functions       # Time-dependent membrane formation
└── reaction rules  # 13 rules for viral lifecycle
```

### Extending the Model

This implementation serves as a foundation for:

1. **Adding immune response pathways**:
   - RIG-I/MAVS signaling
   - IRF3/NFκB activation
   - JAK-STAT signaling
   - ISG production

2. **Viral antagonism**:
   - P_NS inhibition of immune sensors
   - Viral control parameters

3. **Advanced analysis**:
   - Parameter sensitivity
   - Bifurcation analysis
   - Stochastic simulations (NFsim)

## Citation

If you use this code in your research, please cite:

```bibtex
@software{faeder2025viral,
  author = {Faeder, James R.},
  title = {BioNetGen Implementation of Viral Lifecycle Model},
  year = {2025},
  url = {https://github.com/jrfaeder/viral-lifecycle-bngl}
}
```

See [CITATION.md](CITATION.md) for complete citation information, including the original model reference.

## Original Model

This implementation is based on the integrated virus-immune model developed by Boddepalli et al. (2025), available at https://www.biorxiv.org/content/10.1101/2025.06.17.660089v3. The original MATLAB files (`ODEs.m`, `Param.xlsx`, `Param_vector.m`) are included for validation and reference.

## License

MIT License - see [LICENSE](LICENSE) file for details.

The original MATLAB model files are included with attribution to the original authors.

## Contributing

Contributions are welcome! Please feel free to:

- Report bugs or issues
- Suggest enhancements
- Submit pull requests
- Extend the model with additional features

## Support

- **BioNetGen Documentation**: https://bionetgen.org
- **libroadrunner Documentation**: https://libroadrunner.org
- **Issues**: Please open an issue on GitHub

## Roadmap

- [x] Viral lifecycle implementation
- [x] Python simulation tools
- [x] MATLAB validation
- [ ] Add immune response pathways
- [ ] Add viral antagonism
- [ ] Parameter sensitivity analysis
- [ ] Stochastic simulations
- [ ] Interactive Jupyter notebooks

## Acknowledgments

- Original model: Boddepalli et al. (2025) - https://www.biorxiv.org/content/10.1101/2025.06.17.660089v3
- BioNetGen development team
- libroadrunner development team

---

**Created:** November 2025
**Version:** 1.0.0
**Status:** Active Development
