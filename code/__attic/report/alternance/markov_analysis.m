function markov_analysis(saccades, out_dir)

	if report_should_I_skip(out_dir, 'markov_first_fm'), return, end

	letters = letters_from_saccades(saccades);
%	letters = [saccades.letter];

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

    if not(exist(out_dir,'dir'))
        mkdir(out_dir)
    end

	copyfile(ffpath('first_order.eps'), sprintf('%s/markov_first_fm.eps', out_dir))
	copyfile(ffpath('second_order.eps'), sprintf('%s/markov_second_fm.eps', out_dir))
	copyfile(ffpath('fragmaster.pl'), path_join(out_dir, 'fragmaster.pl'))

	output = fopen(sprintf('%s/markov_first_fm', out_dir),'w');
	fields = fieldnames(r);
	for a=1:numel(fields)
		name = fields{a};
		value = r.(name);
		short_value = round( value * 100);
		fprintf(' %s = %f \n', name, value);
		fprintf(output, '\\psfrag{p%slong}[mc]{%f}\n', name, value);
		fprintf(output, '\\psfrag{p%s}[mc]{%d\\%%}\n', name, short_value);
	end

	copyfile(sprintf('%s/markov_first_fm', out_dir),sprintf('%s/markov_second_fm', out_dir));
	
	output = fopen(sprintf('%s/markov_first.title', out_dir),'w');
	fprintf(output, 'First-order analysis of turning behavior');
	output = fopen(sprintf('%s/markov_second.title', out_dir),'w');
	fprintf(output, 'Second-order analysis of turning behavior');
	
	
%	unix(sprintf('cd %s; %s;', out_dir, ffpath('fragmaster.pl')))
	

function  c = count(sequence, sub)
	c = numel(strfind(sequence, sub));
	
function [pL, pR] = compute_seq_probability(sequence, out_dir)
	% [pL, pR] = compute_seq_probability(sequence, out_dir)
	% computes the probability of L and R after the out_dir "out_dir" in sequence
	eL =  numel(strfind(sequence, strcat(out_dir, 'L')));
	eR =  numel(strfind(sequence, strcat(out_dir, 'R')));
	pL = eL / (eL + eR);
	pR = 1-pL;
