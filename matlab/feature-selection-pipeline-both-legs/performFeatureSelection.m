function [final, weissind, training] = performFeatureSelection(paselected, pcainfo)



%PERFORMFEATURESELECTION Perform Feature Selection for FORCe SDP
%   Prasanna Sritharan, February 2022
%
% Based on PCA scripts by Prasanna Sritharan for ACLR hopping 
% (published AnnBiomedEng 2022)
%
% 1. Build training dataset
% 2. Get upper and lower quantiles for later interpretation of PCs
% 2. Reduce using Weiss-Indurkhya independent feature selection
% 3. Further reduce using Sequential Feature Selection using Naive Bayes
%       Classifier


% user settings
addpath('..');
user = getUserScriptSettings();
outpath = user.OUTPATH2;
groups = user.GROUPS;


fprintf('Perform feature selection on data.\n');
fprintf('------------------------------------------------\n'); 

% Data tables
training = struct;
weissind = struct;
final = struct;


% ********************
% Training data matrix

% prepare training data matrix from selected PCs
fprintf('Preparing training data matrix from PCs selected using Parallel Analysis...\n');
training.data = [];
training.labels = {};
for d={'ik','id'} 
    label = pcainfo.(d{1}).label;
    for v=1:length(pcainfo.(d{1}).varnames)        
        varname = pcainfo.(d{1}).varnames{v};        
        nsel = size(paselected.(d{1}).(varname).score,2);
        training.data = [training.data, paselected.(d{1}).(varname).score];
        training.labels = [training.labels, cellfun(@(x) [label '_' varname '_PC' num2str(x)], num2cell(1:nsel), 'UniformOutput', false)];    
    end    
end


% ********************
% Weiss-Indurkhya independent feature selection method

% Get signficance values from Weiss-Indurkhya method
fprintf('Reducing the number of PCs using the Weiss-Indurkhya independent feature selection method...\n');
indfeatout = IndFeat(training.data, pcainfo.(['is' groups{1}]));

% Retain only significant PCs
issigpc = indfeatout>=2.0;  % z-scores
weissind.data = training.data(:, issigpc);
weissind.labels = training.labels(issigpc);
weissind.trainidx = find(issigpc);


% ********************
% Sequential Feature Selection using Naive Bayes Classifier

fprintf('Determining final set of PCs using Sequential Feature Selection...\n');

% Function: number of misclassifications by Naive Bayes Classifier model
fun = @(XT,yT,Xt,yt)(sum(~eq(yt, predict(fitcnb(XT, yT), Xt))));

% Perform Sequential Feature Selection
niter = 1000;
ncSFS = zeros(1, size(weissind.data,2));
opts = statset('display', 'iter', 'UseParallel', false);    % set parallel processing off for local machine as parfor is slower than for loops
fprintf('\n*** Number of iterations: %d ***\n',niter);
for n=1:niter
    fprintf('\nITERATION: %d\n',n);
    cvpart = cvpartition(pcainfo.(['is' groups{1}]), 'k', 10);    % create k new partitions on every iteration
    fs = sequentialfs(fun, weissind.data, pcainfo.(['is' groups{1}]), 'cv', cvpart, 'NFeatures', 10, 'Direction', 'forward', 'options', opts);
    ncSFS(fs) = ncSFS(fs) + 1;    % increment counter
end

% Retain only selected PCs
fprintf('\nRetaining selected PCs only...')
[~, pcidx] = sort(ncSFS, 'descend');
pcidx = sort(pcidx(10:-1:1));
final.data = weissind.data(:, pcidx);
final.labels = weissind.labels(pcidx);
final.trainidx = weissind.trainidx(pcidx);


% Save results
fprintf('\nSaving Feature Selection inputs and outputs...\n');
if ~exist(outpath,'dir'), mkdir(outpath); end
save(fullfile(outpath,'featureselection.mat'),'training','weissind','final');

fprintf('------------------------------------------------\n');

end

