% Run viral lifecycle model only (without immune response)
% This script simulates only the viral lifecycle portion of the model
% for validation against the BNGL version

clear; close all; clc;

%% Load parameters
% First generate param.mat if it doesn't exist
if ~exist('param.mat', 'file')
    fprintf('Generating param.mat from Param.xlsx...\n');
    Param_vector;
end
load('param.mat')

%% Initial Conditions for viral lifecycle components only
% From RunThis.m
V_E = 0;
V_0 = 100;  % MOI = 10 (line 106 in RunThis.m)
V_I = 0;
R_cyt = 0;
R_CM = 0;
P_S = 0;
P_NS = 0;
RC_CM = 0;
R_ds = 0;

% All immune system components set to zero/baseline
RIGI = 0;
aRIGI = 0;
MAVS = 0;
aMAVS = 0;
IKKe = 0;
pIKKe = 0;
TBK1 = 0;
pTBK1 = 0;
IRF3 = 0;
pIRF3 = 0;
IKK = 0;
aIKK = 0;
NFkB_IkBac = 0;
pNFkBn = 0;
NFkBn = 0;
NFkBc = 0;
IkBac = 0;
IRF7 = 0;
pIRF7 = 0;
IFNb_mRNA = 0;
IFNa_mRNA = 0;
IFNl_mRNA = 0;
IFN_c = 0;
IFNl_c = 0;
JAK = 0;
RJC = 0;
STAT1c = 0;
CP = 0;
ISGn = 0;
IFNex = 0;
STAT2c = 0;
TYK = 0;
RTC = 0;
ARC = 0;
IFNAR1 = 0;
IFNAR2 = 0;
IFNAR_d = 0;
IRF9c = 0;
ARC_STAT2c = 0;
ARC_STAT12c = 0;
STAT2c_IRF9 = 0;
ISGF3c = 0;
PSC_c = 0;
ISGF3_CP = 0;
PSC_CP = 0;
NP = 0;
STAT1n = 0;
STAT2n = 0;
PIAS = 0;
PSC_n = 0;
IRF9n = 0;
ISGF3n = 0;
PSC_NP = 0;
B_u = 0;
B_o_NP = 0;
B_o = 0;
ISGF3_PIAS = 0;
STAT2n_IRF9 = 0;
ISGF3_NP = 0;
ISGav_mRNA = 0;
ISGav = 0;
ISGn_mRNA_n = 0;
IRF9_mRNA_n = 0;
IRF7_mRNA = 0;
ISGn_mRNA_c = 0;
IRF9_mRNA_c = 0;

Init_Cond = [V_E V_0 V_I R_cyt R_CM P_S P_NS RC_CM R_ds RIGI aRIGI MAVS aMAVS IKKe pIKKe TBK1 ...
    pTBK1 IRF3 pIRF3 IKK aIKK NFkB_IkBac pNFkBn NFkBn NFkBc IkBac IRF7 pIRF7 IFNb_mRNA IFNa_mRNA IFNl_mRNA IFN_c IFNl_c JAK RJC STAT1c CP ISGn IFNex STAT2c TYK RTC ARC IFNAR1 IFNAR2 IFNAR_d IRF9c ARC_STAT2c ARC_STAT12c STAT2c_IRF9 ISGF3c PSC_c ISGF3_CP PSC_CP NP STAT1n STAT2n PIAS PSC_n IRF9n ISGF3n PSC_NP B_u B_o_NP B_o ISGF3_PIAS STAT2n_IRF9 ISGF3_NP ISGav_mRNA ISGav ISGn_mRNA_n IRF9_mRNA_n IRF7_mRNA ISGn_mRNA_c IRF9_mRNA_c];

%% Simulation parameters
% Set I_n = 0 and I_a = 0 to disable immune effects
% Set VC = 0 to disable viral antagonism
I_n = 0;
I_a = 0;
VC = 0;

% Simulate for 48 hours
tend = 48 * 60;  % 48 hours in minutes
tspan = linspace(0, tend, 200);

%% Solve ODE
[T, Y] = ode23s(@(t, y) ODEs(t, y, param, I_n, I_a, VC), tspan, Init_Cond);

%% Extract viral lifecycle species
% Column indices from ODEs.m (lines 137-145)
V_E_idx = 1;
V_0_idx = 2;
V_I_idx = 3;
R_cyt_idx = 4;
R_CM_idx = 5;
P_S_idx = 6;
P_NS_idx = 7;
RC_CM_idx = 8;
R_ds_idx = 9;

%% Save results for validation
% Convert time to hours
T_hours = T / 60;

% Create results structure
results = struct();
results.time = T;
results.time_hours = T_hours;
results.V_E = Y(:, V_E_idx);
results.V_0 = Y(:, V_0_idx);
results.V_I = Y(:, V_I_idx);
results.R_cyt = Y(:, R_cyt_idx);
results.R_CM = Y(:, R_CM_idx);
results.P_S = Y(:, P_S_idx);
results.P_NS = Y(:, P_NS_idx);
results.RC_CM = Y(:, RC_CM_idx);
results.R_ds = Y(:, R_ds_idx);

% Save to MAT file
save('viral_lifecycle_matlab_results.mat', 'results');

% Also save as CSV for Python comparison
data_table = table(T, T_hours, Y(:, V_E_idx), Y(:, V_0_idx), Y(:, V_I_idx), ...
    Y(:, R_cyt_idx), Y(:, R_CM_idx), Y(:, P_S_idx), Y(:, P_NS_idx), ...
    Y(:, RC_CM_idx), Y(:, R_ds_idx), ...
    'VariableNames', {'time_min', 'time_hours', 'V_E', 'V_0', 'V_I', ...
    'R_cyt', 'R_CM', 'P_S', 'P_NS', 'RC_CM', 'R_ds'});
writetable(data_table, 'viral_lifecycle_matlab_results.csv');

fprintf('MATLAB simulation completed!\n');
fprintf('Results saved to:\n');
fprintf('  - viral_lifecycle_matlab_results.mat\n');
fprintf('  - viral_lifecycle_matlab_results.csv\n');

%% Plot results
figure('Position', [100, 100, 800, 1000]);

species_names = {'V_E', 'V_0', 'V_I', 'R_{cyt}', 'R_{CM}', 'P_S', 'P_{NS}', 'RC_{CM}', 'R_{ds}'};
species_data = [V_E_idx, V_0_idx, V_I_idx, R_cyt_idx, R_CM_idx, P_S_idx, P_NS_idx, RC_CM_idx, R_ds_idx];

for i = 1:length(species_names)
    subplot(3, 3, i);
    semilogy(T_hours, Y(:, species_data(i)) + 1e-10, 'LineWidth', 2);
    ylabel(species_names{i}, 'Interpreter', 'tex', 'FontSize', 12);
    xlabel('Time (hours)', 'FontSize', 12);
    grid on;
    xlim([0, 48]);
end

sgtitle('Viral Lifecycle Model - MATLAB Simulation', 'FontSize', 14, 'FontWeight', 'bold');
saveas(gcf, 'viral_lifecycle_matlab_timecourse.png');

fprintf('Plot saved as: viral_lifecycle_matlab_timecourse.png\n');
