function y = conv_pad(x, f)
% convolves with a filter, preserving distance
pad = numel(f)*2;
x1 = [x(1)*ones(pad,1); x;  x(end)*ones(pad,1)];
y1 = conv(x1, f, 'same');
y = y1((pad+1):(end-pad));
assert(numel(x) == numel(y))