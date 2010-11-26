function res = find_saccades_test(snpall_pos, episode)


interval = snpall_pos.episode_id == episode;
data.timestamp = snpall_pos.time(interval);
data.position = snpall_pos.position(interval,:);
data.debug = 1;
data.decimate = 1;
data.min_velocity = 0.10;

res=find_saccades_xy(data);