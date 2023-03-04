 function user = getUserScriptSettings()

%GETUSERSCRIPTSETTINGS User settings for processing
%   Prasanna Sritharan, Februaru 2019



%% FOLDER PATHS


% folder paths: Lenovo laptop
user.CODEROOT = 'C:\Users\Owner\Documents\data\FORCe\'; 
user.OUTPATH = 'C:\Users\Owner\Documents\data\FORCe\pcaDatabase\';   % location of output database
user.FEATPATH = 'C:\Users\Owner\Documents\data\FORCe\pcaDatabase\feature\'; % feature selection pipeline output path
user.SRCPATH = 'C:\Users\Owner\Documents\data\FORCe\outputDatabase\csvfolder';   % location of source data



%% GENERAL
% ------------------------------

% general parameters
user.LIMBS = {'pivot', 'nonpivot'};
user.GROUPS = {'sym','ctrl'};
user.SUBJPREFIX = {'FAILT', 'FAILTCRT'};
user.FOOT = {'r','l'};
user.RESAMP = 101;
user.GRAVITY = 9.81;    % m/s2

user.STATICPREFIX = 'STATIC';  % trial code prefix for static trials (eg. for trial code WALK01, the trialprefix is 'WALK')
user.DYNAMICPREFIX = 'HOPP';  % trial code prefix for dynamic trials (eg. for trial code WALK01, the trialprefix is 'WALK')
user.SEPARATOR = '_';   % file name separator between subject code and trial code (eg. for file FAILT01_WALK01.c3d, the separator is '_')
user.TRIALTYPE = {'static','dynamic'};  % trial type: static calibration trial, or dynamic gait trial


%% FEATURE SELECTION PARAMETERS

% gait2392 model
user.feature.rajagopal.ik.label = 'angle';
user.feature.rajagopal.ik.headers = {'hip_adduction','hip_flexion','hip_rotation','knee_angle','ankle_angle','lumbar_bending','lumbar_extension','lumbar_rotation'};
user.feature.rajagopal.ik.idx = [8:10 11 13 16:18];

user.feature.rajagopal.id.label = 'moment';
user.feature.rajagopal.id.headers = {'hip_adduction_moment','hip_flexion_moment','hip_rotation_moment','knee_angle_moment','ankle_angle_moment','lumbar_bending_moment','lumbar_extension_moment','lumbar_rotation_moment'};
user.feature.rajagopal.id.idx = [8:10 14 19 11:13];

% user.feature.gait2392.so.pcacols = [];
% user.feature.gait2392.so.flipcols = [];  % column indices *before* trimming to only PCA cols
% user.feature.gait2392.so.mergecols = {{21:23,2:4,9:11,29,30:32,33:34,35},{64:66,45:47,51:54,72,73:75,76:77,78}};    % column indices *before* trimming to only PCA cols
% user.feature.gait2392.so.label = 'force';
% user.feature.gait2392.so.headers = {'gmax','gmed','hams','rf','vas','gas','sol'};
% 
% user.feature.gait2392.rra.pcacols = {[8:14 2:4 26:28],[17:23 2:4 26:28]};
% user.feature.gait2392.rra.flipcols = [3 4 7 27 28];  % column indices *before* trimming to only PCA cols
% user.feature.gait2392.rra.mergecols = [];       % column indices *before* trimming to only PCA cols
% user.feature.gait2392.rra.label = 'angle';
% user.feature.gait2392.rra.headers = {'hip_flex','hip_add','hip_rot','knee_angle','knee_rot','knee_add','ankle_angle','pelvis_tilt','pelvis_list','pelvis_rot','lumbar_ext','lumbar_bend','lumbar_rot'};
% 
% user.feature.gait2392.cmc.pcacols = [];
% user.feature.gait2392.cmc.flipcols = [];  % column indices *before* trimming to only PCA cols
% user.feature.gait2392.cmc.mergecols = {{21:23,2:4,9:11,29,30:32,33:34,35},{64:66,45:47,51:54,72,73:75,76:77,78}};    % column indices *before* trimming to only PCA cols
% user.feature.gait2392.cmc.label = 'force';
% user.feature.gait2392.cmc.headers = {'gmax','gmed','hams','rf','vas','gas','sol'};




end
