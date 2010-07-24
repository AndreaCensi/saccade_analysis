function sample2episodes = group_samples(snpall)
% groups all episode

% returns sample2episodes{i} == [index of episodes]

num_episodes = 1 + max(snpall.episode_id);

cur_index = 1;
name2id = struct;


for i=1:num_episodes
	f =  snpall.episode_data{i}.fh5_filename;
	id = f(1:(numel(f)-4));
	if ~isfield(name2id, id)
		name2id.(id).index = cur_index;
		cur_index = cur_index + 1;
	end
	sample_index(i) = name2id.(id).index;
end

samples = fieldnames(name2id);
for k=1:numel(samples)
	sample2episodes{k} = find(sample_index == name2id.(samples{k}).index);
end




