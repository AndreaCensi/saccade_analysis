function markov_analysis(saccades, prefix)
	
	letters = [saccades.letter];

	[r.L_after_L, r.R_after_L] = compute_seq_probability(letters, 'L');
	[r.L_after_R, r.R_after_R] = compute_seq_probability(letters, 'R');
	
	r.L = count(letters, 'L') / numel(letters);
	r.R = count(letters, 'R') / numel(letters);

	[r.L_after_LL, r.R_after_LL] = compute_seq_probability(letters, 'LL');
	[r.L_after_RL, r.R_after_RL] = compute_seq_probability(letters, 'RL');
	[r.L_after_RR, r.R_after_RR] = compute_seq_probability(letters, 'RR');
	[r.L_after_LR, r.R_after_LR] = compute_seq_probability(letters, 'LR');

	r.LL =  count(letters, 'LL') / (numel(letters)-1);
	r.RL =  count(letters, 'RL') / (numel(letters)-1);
	r.RR =  count(letters, 'RR') / (numel(letters)-1);
	r.LR =  count(letters, 'LR') / (numel(letters)-1);

    if not(exist(prefix,'dir'))
        mkdir(prefix)
    end

	copyfile(ffpath('first_order.eps'), sprintf('%s/markov_first_fm.eps', prefix))
	copyfile(ffpath('second_order.eps'), sprintf('%s/markov_second_fm.eps', prefix))

	output = fopen(sprintf('%s/markov_first_fm', prefix),'w');
	fields = fieldnames(r);
	for a=1:numel(fields)
		name = fields{a};
		value = r.(name);
		short_value = round( value * 100);
		fprintf(' %s = %f \n', name, value);
		fprintf(output, '\\psfrag{p%slong}[mc]{%f}\n', name, value);
		fprintf(output, '\\psfrag{p%s}[mc]{%d\\%%}\n', name, short_value);
	end

	copyfile(sprintf('%s/markov_first_fm', prefix),sprintf('%s/markov_second_fm', prefix));
	
%	unix(sprintf('cd %s; %s;', prefix, ffpath('fragmaster.pl')))
	

function  c = count(sequence, sub)
	c = numel(strfind(sequence, sub));
	
function [pL, pR] = compute_seq_probability(sequence, prefix)
	% [pL, pR] = compute_seq_probability(sequence, prefix)
	% computes the probability of L and R after the prefix "prefix" in sequence
	eL =  numel(strfind(sequence, strcat(prefix, 'L')));
	eR =  numel(strfind(sequence, strcat(prefix, 'R')));
	pL = eL / (eL + eR);
	pR = 1-pL;
