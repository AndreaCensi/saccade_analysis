tmp_conf = struct;
tmp_conf.id = 'mamarama';
tmp_conf.saccade_detection_method = 'mamarama';
tmp_conf.debug = 0;
tmp_conf.min_significant_amplitude = 15; % deg
tmp_conf.robust_amplitude_delta = 0.05; % seconds
tmp_conf.robust_amplitude_var = 20;

% 1) Starting with
% min_significant_amplitude: 20
%     robust_amplitude_delta: 0.03
%       robust_amplitude_var: 15
% gibes
% false_negative: 0.0296
% false_positive: 0.3022
%  true_positive: 0.9407
% 2) juggling with delta, I get
%   I now choose
% min_significant_amplitude: 20
%     robust_amplitude_delta: 0.0650
%       robust_amplitude_var: 15
% I move 0.03 -> 0.05
%  now 15 -> 20
process_species('data/mamaramanopost', tmp_conf);
r=roc_analysis_species_conf('data/mamaramanopost', tmp_conf.id, false)

r=roc_analysis_species_conf('data/mamaramanopost', tmp_conf.id, true)
pause

%robust_amplitude_delta =  0.01:0.005:0.08;
robust_amplitude_var = 10:20;

clear configurations 
for i=1:numel(robust_amplitude_var)
	configurations(i) = tmp_conf;
	configurations(i).robust_amplitude_var = robust_amplitude_var(i);
	configurations(i).id = sprintf('prova%d', i);
end

for i=1:numel(configurations)
process_species('data/mamaramanopost', configurations(i))
end

rall = roc_analysis_species('data/mamaramanopost')
print_roc_curves(rall)
% figure;hold on
% plot([rall.true_positive],[rall.false_positive],'.')
% for i=1:numel(rall)
% 	x = rall(i).true_positive;
% 	y = rall(i).false_positive;
% 	x2 = x + 0.1; 
% 	y2 = y + 0.1 * mod(i,3);
% 	plot([x x2],[y,y2],'r-')
% 	text(x2,y2, rall(i).conf_id)
% end
% xlabel('true positive')
% ylabel('false_positive')
% 
% 
% 
