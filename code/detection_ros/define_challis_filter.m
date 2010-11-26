function [filt_rate] = define_challis_filt_rate(sample)

% Defines challis butterworth filt_rate
% RWS NOTE: Calculated optimal cut-off freq for butterworth filt_rate via
% Challis method separately in Linux machine using Andrew Straw's PYTHON code 'est1.py'
% & auto_filt_rate_cutoff.py, it was faster to run it on linux :/

% RWS 09/24/09

switch sample
        
    case 'Dmelanogaster-20080410-174953'; filt_rate =  0.64375; % high
    case 'Dmelanogaster-20080626-151946'; filt_rate =  0.18671875;
    case 'Dmelanogaster-20080626-174721'; filt_rate =  0.3984375; % high
    case 'Dmelanogaster-20080627-154223'; filt_rate =  0.33203125; % ?
    case 'Dmelanogaster-20080627-162448'; filt_rate =  0.3125; % ?
    case 'Dmelanogaster-20080627-172709'; filt_rate =  0.6453125; % high
    case 'Dmelanogaster-20080702-151655'; filt_rate =  0.1640625;
    case 'Dmelanogaster-20080702-175038'; filt_rate =  0.23828125;
    case 'Dmelanogaster-20080703-165245'; filt_rate =  0.31796875;
    case 'Dmelanogaster-20080703-175708'; filt_rate =  0.25390625;
    case 'Dmelanogaster-20080704-154647'; filt_rate =  0.28984375;
    case 'Dmelanogaster-20080704-165040'; filt_rate =  0.29296875;
    case 'Dmelanogaster-20080708-154007'; filt_rate =  0.35859375; % ?
    case 'Dmelanogaster-20080708-163736'; filt_rate =  0.2625;
    case 'Dmelanogaster-20080708-171906'; filt_rate =  0.38359375; % high

    case 'Dananassae-20080520-163311'; filt_rate = 0; % error
    case 'Dananassae-20080714-160112'; filt_rate = 0; % error
    case 'Dananassae-20080714-173605'; filt_rate = 0.2384375; % error 1.263449
    case 'Dananassae-20080715-151141'; filt_rate = 0; % error
    case 'Dananassae-20080715-160405'; filt_rate = 0.302421875; % error 1.147337
    case 'Dananassae-20080716-173643'; filt_rate = 0; % error
    case 'Dananassae-20080717-162351'; filt_rate = 0; % error
    case 'Dananassae-20080718-154844'; filt_rate = 0.203984375; % error 1.529037
    case 'Dananassae-20080718-173934'; filt_rate = 0.3259375; % error 1.145587
    case 'Dananassae-20080721-155946'; filt_rate = 0.267421875; % error 1.146585
    case 'Dananassae-20080722-151948'; filt_rate = 0; % error
    case 'Dananassae-20080723-165849'; filt_rate = 0.35875; % error 1.457656
    case 'Dananassae-20080723-180506'; filt_rate = 0.21328125; % error 1.242945
    case 'Dananassae-20080724-175131'; filt_rate = 0; % error
    case 'Dananassae-20080725-155649'; filt_rate = 0.349453125; % error 1.214257

    case 'Darizonae-20080409-173446'; filt_rate = 0.56328125; % error 1.483998
    case 'Darizonae-20080414-171002'; filt_rate =  0.67109375; % error 2.146096
    case 'Darizonae-20080414-192946'; filt_rate = 0; % error
    case 'Darizonae-20080729-155542'; filt_rate = 0.44375; % error 1.172421
    case 'Darizonae-20080730-153824'; filt_rate = 0.34375; % error 1.299676
    case 'Darizonae-20080801-172913'; filt_rate = 0.26640625; % error 0.850465
    case 'Darizonae-20080804-163617'; filt_rate = 0.52578125; % error 1.578478
    case 'Darizonae-20080806-153237'; filt_rate = 0.58671875; % error 1.592077
    case 'Darizonae-20080806-171120'; filt_rate = 0; % error
    case 'Darizonae-20080807-170941'; filt_rate = 0.54375; % error 1.293416

    case 'Dhydei-20080411-183739'; filt_rate = 0.22421875; % error 0.807984
    case 'Dhydei-20080411-193641'; filt_rate = 0.74140625; % error 2.646600
    case 'Dhydei-20080923-154552'; filt_rate = 0.19609375; % error 1.022851
    case 'Dhydei-20080924-151012'; filt_rate = 0.303125; % error 0.871600
    case 'Dhydei-20080925-153954'; filt_rate = 0; % error
    case 'Dhydei-20080925-183525'; filt_rate = 0.53984375; % error 1.403108
    case 'Dhydei-20081001-175905'; filt_rate = 0.31640625; % error 1.090943
    case 'Dhydei-20081001-190635'; filt_rate = 0.3671875; % error 0.956714
    case 'Dhydei-20081020-154620'; filt_rate = 0.3953125; % error 1.196599
    case 'Dhydei-20081020-165222'; filt_rate = 0.346875; % error 1.202831
    case 'Dhydei-20081020-173151'; filt_rate = 0.33515625; % error 1.099832
    case 'Dhydei-20081020-182244'; filt_rate = 0.534375; % error 1.256067
    case 'Dhydei-20081021-151348'; filt_rate = 0.56328125; % error 1.383730
    case 'Dhydei-20081021-161732'; filt_rate = 0; % error

    case 'Dmojavensis-20080616-162754'; filt_rate = 0; % error
    case 'Dmojavensis-20080617-162725'; filt_rate = 0.24140625; % error 0.911415
    case 'Dmojavensis-20080619-153037'; filt_rate = 0.18203125; % error 0.820719
    case 'Dmojavensis-20080619-175759'; filt_rate = 0; % error
    case 'Dmojavensis-20080620-150615'; filt_rate = 0; % error
    case 'Dmojavensis-20080620-153821'; filt_rate = 0.63046875; % error 1.819229
    case 'Dmojavensis-20080623-145945'; filt_rate = 0; % error
    case 'Dmojavensis-20080728-171617'; filt_rate = 0; % error
    case 'Dmojavensis-20080731-163626'; filt_rate = 0.6140625; % error 1.379616
    case 'Dmojavensis-20081002-153832'; filt_rate = 0; % error

    case 'Dpseudoobscura-20080413-190700'; filt_rate = 0.35234375; % error 1.264429
    case 'Dpseudoobscura-20080429-164759'; filt_rate = 0.363671875; % error 0.927467
    case 'Dpseudoobscura-20080710-160949'; filt_rate = 0.28203125; % error 0.892441
    case 'Dpseudoobscura-20080711-151244'; filt_rate = 0.10609375; % error 1.119884
    case 'Dpseudoobscura-20080812-173146'; filt_rate = 0.40625; % error 1.085548
    case 'Dpseudoobscura-20080929-163210'; filt_rate = 0.38984375; % error 0.953083
    case 'Dpseudoobscura-20080929-172136'; filt_rate = 0.353125; % error 0.906787
    case 'Dpseudoobscura-20080930-153336'; filt_rate = 0.32046875; % error 1.088685
    case 'Dpseudoobscura-20080930-162613'; filt_rate = 0.4265625; % error 0.957170
    case 'Dpseudoobscura-20080930-165131'; filt_rate = 0.28359375; % error 0.857780
        
end
