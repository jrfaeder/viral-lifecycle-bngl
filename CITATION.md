# Citation and Attribution

## Original Model

This BioNetGen implementation is based on the integrated virus-immune model developed by:

**Boddepalli R, Chhajer H, Roy R.** Integrative Modelling of Innate Immune Response Dynamics during Virus Infection. bioRxiv; 2025. p. 2025.06.17.660089. doi:10.1101/2025.06.17.660089

Available at: https://www.biorxiv.org/content/10.1101/2025.06.17.660089v3

The original MATLAB implementation includes:
- `ODEs.m` - Complete ODE system for virus-immune interactions
- `Param.xlsx` - Model parameters
- `Param_vector.m` - Parameter loading script

These files are included in this repository for validation and reference purposes.

## This Implementation

If you use this BioNetGen implementation in your research, please cite:

**Faeder, J.R. (2025).** BioNetGen Implementation of Viral Lifecycle Model.
GitHub repository: https://github.com/jrfaeder/viral-lifecycle-bngl

## BioNetGen

This implementation uses BioNetGen for rule-based modeling:

**Harris, L.A., et al. (2016).** BioNetGen 2.2: advances in rule-based modeling.
*Bioinformatics*, 32(21), 3366-3368.

## libroadrunner

Simulations use the libroadrunner library:

**Somogyi, E.T., et al. (2015).** libRoadRunner: a high performance SBML simulation and analysis library.
*Bioinformatics*, 31(20), 3315-3321.

## Acknowledgments

This work builds upon the original integrated virus-immune model developed by the Boddepalli laboratory. The BioNetGen implementation was created to provide:
- Rule-based representation of viral lifecycle dynamics
- Python/libroadrunner integration for flexible analysis
- Foundation for extending to immune response pathways
- Validation against the original MATLAB implementation

## License

This BioNetGen implementation is released under the MIT License (see LICENSE file).

The original MATLAB model files (ODEs.m, Param.xlsx, Param_vector.m) are included for validation and reference purposes, with attribution to the original authors.
