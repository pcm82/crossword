%% best first search: effect of crossword size on runtime 

d = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
times = [9e-05, 0.01079, 0.00028, 0.00308, 0.00406, 0.01127, 0.00864, 0.03393, 0.17092, 0.34245; ... 
    8e-05, 0.00028, 0.00041, 0.00212, 0.0057, 0.00976, 0.01323, 0.02515, 0.04269, 0.08431; ...
    8e-05, 0.00055, 0.0015, 0.00336, 0.00421, 0.00838, 0.01702, 0.02448, 0.04193, 0.05611; ... 
    7e-05, 0.00966, 0.00091, 0.0016, 0.00486, 0.00809, 0.00854, 0.02975, 0.0258, 491.93657; ...
    0.00022, 0.00824, 0.00173, 0.00059, 0.00072, 0.01, 0.00776, 0.00969, 0.02452, 0.05498; ...
    9e-05, 0.00037, 0.00026, 0.00629, 0.00555, 0.00778, 0.00592, 0.02877, 0.03068, 2.15914; ...
    0.00031, 0.00037, 0.00039, 0.00124, 0.0031, 0.43063, 0.00781, 0.20233, 0.01812, 0.08785; ...
    7e-05, 0.00143, 0.00061, 0.00455, 0.0018, 0.01145, 0.00611, 0.01375, 0.01654, 0.08365; ...
    8e-05, 0.00872, 0.00086, 0.0023, 0.00171, 0.00526, 0.00653, 0.04875, 0.03871, 0.04911; ...
    7e-05, 0.00055, 0.00119, 0.00167, 0.00458, 0.00321, 0.0058, 0.03007, 0.02056, 0.06266];
figure;
semilogy(d, times', 'LineWidth', 1)
hold on
semilogy(d, mean(times), 'k--', 'LineWidth', 1)
hold off
c= polyfit([d; d; d; d; d; d; d; d; d; d], log(times), 1);
grid on
title("Effect of Crossword Size on Best First Search")
xlabel("Crossword Dimension")
ylabel("Time (seconds)")
print(gcf,'bestFirst.png','-dpng','-r200');



[rho,pval] = corr(d', mean(times)','Type','Spearman');
disp(rho)
disp(pval)

disp("Fitted line:") 
disp("ln(y) = " + c(1) + " * x + " + c(2))
disp("Rearranged: ")
disp(" y = " + exp(c(2)) + " * " + "e^" + c(1) + "x")

%% actual best first search

d = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
times = [0.0002, 0.00035, 0.00153, 0.00168, 0.00528, 0.00606, 0.01764, 0.03407, 0.02339, 2.21695; ...
    0.00011, 0.01083, 0.00075, 0.01317, 0.00431, 0.01082, 0.01131, 0.04113, 0.0434, 0.09941; ...
    0.00013, 0.0003, 0.0011, 0.00981, 0.0089, 0.02073, 0.00921, 0.02998, 0.08062, 5.51069; ...
    0.00012, 0.01273, 0.00086, 0.00536, 0.00417, 1.15463, 0.00319, 6.81482, 0.01627, 0.03394; ...
    0.00011, 0.00064, 0.00139, 0.00851, 0.0048, 0.01997, 0.01625, 0.04822, 0.04652, 0.11365; ...
    0.00026, 0.00052, 0.00101, 0.00563, 0.00581, 0.01567, 0.06451, 0.03205, 0.01057, 0.05706; ...
    0.0001, 0.00086, 0.00134, 0.00127, 0.01639, 0.19629, 0.02558, 0.04472, 0.04536, 0.08027; ...
    0.00015, 0.00037, 0.00157, 0.02381, 0.00381, 0.00723, 0.63698, 0.03339, 0.05471, 0.08546; ...
    0.00012, 0.00023, 0.00062, 0.00404, 0.03791, 0.00981, 0.00877, 0.07104, 0.08732, 1130.84072; ...
    0.00031, 0.00049, 0.00196, 0.00698, 0.00244, 0.05679, 0.00909, 46.46974, 0.2284, 0.11233];
figure;
semilogy(d, times', 'LineWidth', 1)
hold on
semilogy(d, mean(times), 'k--', 'LineWidth', 1)
hold off

grid on
title("Effect of Crossword Size on (Real) Best First Search")
xlabel("Crossword Dimension")
ylabel("Time (seconds)")
print(gcf,'RealBestFirst.png','-dpng','-r200');



[rho,pval] = corr(d', mean(times)','Type','Spearman');
disp(rho)
disp(pval)
%% effect of crossword size on beam search
d= [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
t= [0.0001, 0.00023, 0.00058, 0.00326, 0.00342, 0.01635, 0.00874, 0.05393, 0.01906, 0.04569; ...
    7e-05, 0.00345, 0.00069, 0.00433, 0.00697, 0.00494, 0.01775, 0.024, 0.03299, 0.36117; ...
    7e-05, 0.00015, 0.00045, 0.00379, 0.00802, 0.00578, 0.01501, 0.13329, 0.22475, 0.04817; ...
    7e-05, 0.00303, 0.00024, 0.01653, 0.00856, 0.01163, 0.01214, 0.01905, 0.02885, 0.09633; ...
    7e-05, 0.00329, 0.00079, 0.00184, 0.00356, 0.01482, 0.02471, 0.02811, 0.04923, 0.06827];

figure;
semilogy(d, t', 'LineWidth', 1)
hold on
semilogy(d, mean(t), 'k--', 'LineWidth', 1)
hold off
grid on
c= polyfit([d; d; d; d; d], log(t), 1);
title("Effect of Crossword Size on Beam Search")
xlabel("Crossword Dimension")
ylabel("Time (seconds)")
print(gcf,'beamCrossSize.png','-dpng','-r200');


[rho,pval] = corr(d', mean(t)','Type','Spearman');
disp(rho)
disp(pval)

disp("Fitted line:") 
disp("ln(y) = " + c(1) + " * x + " + c(2))
disp("Rearranged: ")
disp(" y = " + exp(c(2)) + " * " + "e^" + c(1) + "x")

% beam size on the search: 
b= [1,4,10, 32, 100, 317, 1000, 3163, 10000, 31623];
t= [0.007, 0.07819, 0.08707, 0.08645, 0.08693, 0.08938, 0.08729, 0.08751, 0.08823, 0.08708;
    0.00501, 0.02032, 0.0202, 0.02011, 0.02144, 0.02249, 0.02019, 0.0203, 0.01937, 0.01945;
    0.00699, 27.79796, 15.15465, 15.42824, 15.42886, 15.41922, 15.61457, 15.50628, 15.43446, 15.69054;
    0.01283, 14.00413, 3.29904, 3.26806, 3.27093, 3.25834, 3.25984, 3.28088, 3.25486, 3.27064;
    0.00831, 0.49136, 0.72111, 0.71716, 0.71494, 0.71788, 0.72595, 0.72014, 0.71439, 0.7204];
success= [0, 1, 1, 1, 1, 1, 1, 1, 1, 1;
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1;
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1;
    0, 0, 1, 1, 1, 1, 1, 1, 1, 1;
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1];
figure;
subplot(1,2,1)
loglog(b, t', 'LineWidth', 1)
hold on
loglog(b, mean(t), 'k--', 'LineWidth', 1)
hold off
grid on
title("Effect of Beam Size on Beam Search")
xlabel("Beam Size")
ylabel("Time (seconds)")

subplot(1,2,2)
semilogx(b, sum(success,1) ./ length(t(:,1)), "LineWidth", 1)
title("Percent Success of Beam Search")
xlabel("Beam Size")
ylabel("Proportion of Successful Trials")
set(gcf, 'Position',  [100, 100, 1000, 400])

print(gcf,'beamBeamSize.png','-dpng','-r200');


%% Beam Search: Heuristic Compare

t= [0.04891, 0.02547, 0.03633, 0.03009, 0.03712, 1.78041, 0.03668, 1.13381, 23.19986, 0.02819, 0.03492, 0.01468, 0.03012, 0.0326, 0.05293; 
    0.0458, 0.02554, 0.03699, 0.04699, 0.03598, 0.86821, 0.04194, 0.05748, 0.05447, 0.0305, 0.03837, 0.01566, 0.04662, 0.02618, 0.11994];

perc_filled= [0.515625, 0.53125, 0.515625, 0.515625, 0.515625, 0.515625, 0.515625, 0.515625, 0.515625, 0.515625, 0.515625, 0.515625, 0.515625, 0.515625, 0.515625;
    0.515625, 0.53125, 0.515625, 0.515625, 0.515625, 0.515625, 0.515625, 0.515625, 0.515625, 0.515625, 0.515625, 0.515625, 0.515625, 0.53125, 0.515625];

perc_inter= [0.203125, 0.0625, 0.109375, 0.078125, 0.171875, 0.09375, 0.09375, 0.09375, 0.15625, 0.046875, 0.078125, 0.0625, 0.078125, 0.0625, 0.140625; 
    0.203125, 0.0625, 0.109375, 0.140625, 0.171875, 0.109375, 0.15625, 0.09375, 0.078125, 0.078125, 0.09375, 0.09375, 0.125, 0.078125, 0.15625];

means_t= [mean(t(1,:)), mean(t(2,:))];
stds_t= [std(t(1,:)), std(t(2,:))];
means_perc_filled = [mean(perc_filled(1,:)), mean(perc_filled(2,:))];
stds_perc_filled = [std(perc_filled(1,:)), std(perc_filled(2,:))];
means_perc_inter = [mean(perc_inter(1,:)), mean(perc_inter(2,:))];
stds_perc_inter = [std(perc_inter(1,:)), std(perc_inter(2,:))];

vec= [1,2];
col_vec= ['b', 'r'];

figure;
hold on
for i= 1:length(vec)
    b(i) = bar(vec(i), means_t(i), col_vec(i));
    errorbar(vec(i), means_t(i), stds_t(i), stds_t(i), 'Color', 'k', 'LineWidth', 1.5);
end
hold off
xticks([1,2])
xticklabels(["Percent Filled", "Percent Intersections"]);
ylabel("Runtime (s)")
title("Runtimes of % Filled vs % Intersections Heuristics")
print(gcf,'heuristicsTime.png','-dpng','-r200');

figure;
subplot(1,2,1)
hold on
for i= 1:length(vec)
    b(i) = bar(vec(i), means_perc_filled(i), col_vec(i));
    errorbar(vec(i), means_perc_filled(i), stds_perc_filled(i), stds_perc_filled(i), 'Color', 'k', 'LineWidth', 1.5);
end
hold off
xticks([1,2])
xticklabels(["Percent Filled", "Percent Intersections"]);
ylabel("Proportion Filled")
title("Percent Filled of % Filled vs % Intersections Heuristics")

subplot(1,2,2)
hold on
for i= 1:length(vec)
    b(i) = bar(vec(i), means_perc_inter(i), col_vec(i));
    errorbar(vec(i), means_perc_inter(i), stds_perc_inter(i), stds_perc_inter(i), 'Color', 'k', 'LineWidth', 1.5);
end
hold off
xticks([1,2])
xticklabels(["Percent Filled", "Percent Intersections"]);
ylabel("Proportion of Intersections")
title("Percent Intersecions of % Filled vs % Intersections Heuristics")
set(gcf, 'Position',  [100, 100, 1000, 400])
print(gcf,'heuristicsComparePerc.png','-dpng','-r200');

[h, p] = ttest2(perc_inter(1,:), perc_inter(2,:))
disp("Difference between heuristics: intersections")
disp(p)

%% Brute vs Best vs Beam search: Dictionary Size
d= [3, 4, 5, 6, 8, 10, 14, 18, 24, 32, 43, 57, 75, 100, 134, 178, 238, 317, 422, 563];
times= [0.02411, 0.00956, 0.13084, 0.63229, 0.00392, 0.02046, 0.1272, 0.12645, 21.79128, 8.46802, 0.80039, 0.04791, 75.73428, 24.00258, 87.05092, 0.84514, 576.91045, 284.71842, 2443.89023, 111.63773; ...
    0.00124, 0.00142, 0.00235, 0.00142, 0.00078, 0.00284, 0.0012, 0.00211, 0.00269, 0.00052, 0.00156, 0.00052, 0.00132, 0.00218, 0.00185, 0.00092, 0.00132, 0.00088, 0.00091, 0.00163; ...
    0.00078, 0.00065, 0.00089, 0.0005, 0.00028, 0.00063, 0.00071, 0.00079, 0.0009, 0.0009, 0.00072, 0.00028, 0.0009, 0.00071, 0.0005, 0.00072, 0.00108, 0.0009, 0.00073, 0.00129];

figure; 
loglog(d, times, 'LineWidth', 1)
grid on
title("Effect of Dictionary Size on Brute Force vs Best First vs Beam Search")
xlabel("Dictionary size")
ylabel("Time (s)")
legend([ "Brute Force Search", "Best First Search", "Beam Search"]);
print(gcf,'dictSizeCompareBBB.png','-dpng','-r200');

disp("Best First Ratio:")
[rho,pval] = corr(log(d)',log(times(1,:) ./ times(2, :))','Type','Spearman');
disp(rho)
disp(pval)
c= polyfit(log(d), log(times(1,:) ./ times(2,:)), 1);


disp("Fitted line:") 
disp("ln(y) = " + c(1) + " * ln(x) + " + c(2))
disp("Rearranged: ")
disp(" y = " + exp(c(2)) + " * x^" + c(1))

disp("Beam Search ratio:")
[rho,pval] = corr(log(d)',log(times(1,:) ./ times(3,:))','Type','Spearman');
disp(rho)
disp(pval)
c= polyfit(log(d), log(times(1,:) ./ times(3,:)), 1);
disp("Fitted line:") 
disp("ln(y) = " + c(1) + " * ln(x) + " + c(2))
disp("Rearranged: ")
disp(" y = " + exp(c(2)) + " * x^" + c(1))
%% Brute Force vs Best First search: Dictionary Size

n= [3, 4, 5, 6, 8, 10, 14, 18, 24, 32, 43, 57, 75, 100, 134, 178, 238, 317, 422, 563];
t_beam= [0.00061, 0.00044, 0.00208, 0.00099, 0.00158, 0.00184, 0.00166, 0.00195, 0.00321, 0.00274, 0.0067, 0.00173, 0.00384, 0.00148, 0.0019, 0.00393, 0.00047, 0.00134, 0.00082, 0.00185];
t_brute= [0.00228, 0.00481, 0.03199, 0.02808, 0.21978, 1.66596, 2.70629, 0.07853, 0.45493, 226.34261, 0.5123, 7.04018, 110.81302, 23.24506, 17.68329, 77.09597, 0.81596, 127.4171, 0.47676, 81.47015];

figure; 
subplot(1,2, 1)
loglog(n, [t_beam; t_brute], 'LineWidth', 1)
grid on
title("Effect of Dictionary Size on Brute Force vs Best First Search")
xlabel("Dictionary size")
ylabel("Time (s)")
legend(["Best First Search", "Brute Force Search"]);

mult= t_brute ./ t_beam;
%mult= [mult(1:7) , mult(9:end)];
n_mod= [n(1:7), n(9:end)];
subplot(1,2,2)
loglog(n, mult, 'LineWidth', 1)
grid on
xlabel("Dictionary Size")
ylabel("t_{brute} / t_{beam}")
title("Dictionary Size vs Ratio of Runtimes between Brute Force and Best First search")
set(gcf, 'Position',  [100, 100, 1000, 400])
print(gcf,'dictSizeCompare.png','-dpng','-r200');

[rho,pval] = corr(log(n)',log(mult)','Type','Spearman');
disp(rho)
disp(pval)

%% Brute vs Best vs Beam Search: Crossword Size
max_d = 4;
num_trials= 5;

n= [1, 2, 3, 4];
t_brute= [0.00036, 0.01325, 0.00908, 0.11064; ...
            0.00048, 0.00973, 0.0094, 0.10234;...
            0.00026, 0.00894, 0.01902, 1.48681;...
            0.00025, 0.0127, 0.15342, 73.96591;...
            0.00024, 0.0043, 5.34867, 53.26026];
t_best= [0.0001, 0.00043, 0.0006, 0.0018; ...
            0.00012, 0.00103, 0.00152, 0.00079; ...
            8e-05, 0.00073, 0.00111, 0.00079; ...
            8e-05, 0.00993, 0.00169, 0.00264; ...
            9e-05, 0.00126, 0.00066, 0.00581];
t_beam= [5e-05, 0.00036, 0.00034, 0.00052; ...
            5e-05, 0.00019, 0.00021, 0.00064; ...
            5e-05, 0.00018, 0.00029, 0.00031; ...
            5e-05, 0.00023, 0.00037, 0.00057; ...
            4e-05, 0.00051, 0.00044, 0.00096];
success_brute= [1, 1, 1, 1;
            1, 1, 1, 1; 
            1, 1, 1, 1;
            1, 1, 1, 1;
            1, 1, 1, 1];
success_best= [1, 1, 1, 1;
            1, 1, 1, 1; 
            1, 1, 1, 1;
            1, 1, 1, 1;
            1, 1, 1, 1];    
success_beam= [1, 0, 0, 0; ...
                1, 0, 0, 0; ...
                1, 0, 0, 0; ... 
                1, 0, 0, 0; ...
                1, 0, 0, 0];
avg_t_brute= mean(t_brute);
avg_t_best= mean(t_best);
avg_t_beam= mean(t_beam);

figure;
loglog(n, avg_t_brute, '--b', "LineWidth", 1)
hold on
loglog(n, avg_t_best, '--r', "LineWidth", 1)
loglog(n, avg_t_beam, '--g', "LineWidth", 1)
loglog(n, t_brute, 'bo')
loglog(n, t_best, 'ro')
loglog(n, t_beam, 'go')
%legend(["Brute Force", "Best First", "Beam"])
title("Comparison of All Search Algorithms: Crossword Size")
xlabel("Crossword Dimension")
ylabel("Runtime (s)")
grid on
print(gcf,'crossSizeCompareBBBbad.png','-dpng','-r200');
hold off
disp("ratios:")
c= polyfit(log([n; n; n; n; n]), log(t_brute ./ t_best), 1);
disp("Fitted line (Best First):") 
disp("ln(y) = " + c(1) + " * ln(x) + " + c(2))
disp("Rearranged: ")
disp(" y = " + exp(c(2)) + " * x^" + c(1))

c= polyfit(log([n; n; n; n; n]), log(t_brute ./ t_beam), 1);
disp("Fitted line (Beam):") 
disp("ln(y) = " + c(1) + " * ln(x) + " + c(2))
disp("Rearranged: ")
disp(" y = " + exp(c(2)) + " * x^" + c(1))



%% brute force vs Beam Search: Crossword Size
d= [1, 2, 3, 4, 5];
t_brute= [0.00036, 0.00263, 1.12733, 0.03444, 350.21338];
t_beam= [0.00017, 0.00057, 0.00113, 0.00074, 0.00351];

figure;
subplot(1,2,1)
semilogy(d, [t_beam; t_brute], 'LineWidth', 1)
grid on
title("Crossword Size vs Runtimes of Brute Force and Best First Search")
xlabel("Crossword dimension n x n")
ylabel("Runtime (s)")

subplot(1,2,2)
semilogy(d, t_brute ./ t_beam, 'LineWidth', 1)
grid on
title("Crossword Size vs Ratio of Brute Force and Best First Search Performance")
xlabel("Crossword dimension n x n")
ylabel("t_{brute} / t_{beam}")
set(gcf, 'Position',  [100, 100, 1000, 400])
print(gcf,'crossSizeCompare.png','-dpng','-r200');

[rho,pval] = corr(d',log(t_brute ./ t_beam)','Type','Spearman');
disp(rho)
disp(pval)

%% worst case comparison
t_brute = [0.09961, 0.99833, 0.03102, 0.07785, 2.99229, 0.62203, 0.48811, 0.02659, 0.30793, 0.65014, 0.47187, 0.42545, 2.53048, 1.13961, 0.05127, 0.089, 2.55733, 0.66651, 2.11315, 0.88357, 0.31727, 0.31707, 0.35096, 0.79674, 0.27624, 0.70328, 0.0495, 0.21948, 0.15001, 0.2276, 0.05868, 0.08744, 0.09727, 0.64246, 0.05471, 0.23213, 0.37781, 1.26825, 0.33967, 0.01925, 0.02934, 1.22914, 0.1416, 0.16349, 0.02875, 1.25272, 0.46392, 1.38835, 1.08007, 0.06407];
t_best = [0.13951, 5.84267, 0.03547, 0.10591, 52.27723, 2.2632, 1.62027, 0.03172, 0.72914, 2.08582, 0.80276, 0.90115, 20.18545, 1.99345, 0.04906, 0.10243, 26.38444, 1.02964, 20.8765, 2.01461, 0.74249, 0.74597, 0.80602, 3.04545, 0.6055, 2.72165, 0.05565, 0.39882, 0.24845, 0.29573, 0.07208, 0.15942, 0.16703, 2.01371, 0.12564, 0.43273, 0.85316, 8.61996, 0.73746, 0.02456, 0.03636, 6.97469, 0.22504, 0.27047, 0.0349, 7.22569, 0.94338, 6.4577, 6.33353, 0.07931];


means_t= [mean(t_brute), mean(t_best)];
stds_t= [std(t_brute), std(t_best)];
vec= [1,2];
col_vec= ['b', 'r'];

figure;
hold on
for i= 1:length(vec)
    b(i) = bar(vec(i), means_t(i), col_vec(i));
    errorbar(vec(i), means_t(i), stds_t(i), stds_t(i), 'Color', 'k', 'LineWidth', 1.5);
end
hold off
xticks([1,2])
xticklabels(["Brute Force", "Best First Search"]);
ylabel("Runtime (s)")
title("Worst Case Runtimes: Brute Force vs Best First Search")
print(gcf,'worstCaseComparison.png','-dpng','-r200');

[h, p] = ttest2(t_brute, t_best);
disp(p)

%% Worst case comparison (actual)
t_brute= [0.93606, 0.05798, 0.56351, 0.71779, 0.42603, 1.19643, 0.34996, 1.44382, 0.22656, 0.7965, 0.05319, 0.11304, 0.22216, 0.18617, 0.05374, 0.14668, 0.06083, 0.21406, 0.36173, 0.58962, 0.05643, 0.35935, 0.50001, 0.04289, 0.08643, 0.15461, 0.35001, 1.06158, 0.05621, 0.10799, 1.12554, 0.20278, 0.12974, 0.10175, 0.09512, 0.87554, 0.19763, 1.21434, 0.09445, 0.54704, 0.72156, 0.99048, 0.28172, 0.64979, 0.17822, 0.10402, 0.35319, 0.20576, 0.01386, 0.37722];
t_best= [0.00438, 0.00231, 0.00392, 0.00501, 0.006, 0.00587, 0.00321, 0.00485, 0.00371, 0.00474, 0.00428, 0.0058, 0.00303, 0.00437, 0.00322, 0.00577, 0.00271, 0.0029, 0.00427, 0.00404, 0.0015, 0.00331, 0.00424, 0.00218, 0.00273, 0.00257, 0.00305, 0.00468, 0.00229, 0.00226, 0.00524, 0.00316, 0.00368, 0.00315, 0.00268, 0.00397, 0.00308, 0.00466, 0.00213, 0.00423, 0.00388, 0.00538, 0.00325, 0.00464, 0.00272, 0.00232, 0.00362, 0.00333, 0.00143, 0.00316];
means_t= [mean(t_brute), mean(t_best)];
stds_t= [std(t_brute), std(t_best)];
vec= [1,2];
col_vec= ['b', 'r'];

figure;
hold on
for i= 1:length(vec)
    b(i) = bar(vec(i), means_t(i), col_vec(i));
    errorbar(vec(i), means_t(i), stds_t(i), stds_t(i), 'Color', 'k', 'LineWidth', 1.5);
end
hold off
xticks([1,2])
xticklabels(["Brute Force", "Best First Search"]);
ylabel("Runtime (s)")
title("Worst Case Runtimes: Brute Force vs Best First Search")
print(gcf,'ActualWorstCaseComparison.png','-dpng','-r200');

[h, p] = ttest2(t_brute, t_best);
disp(p)

%% Worst Case, all

t_brute= [0.0954, 0.15429, 0.01516, 0.32275, 0.27495, 0.02849, 0.64411, 1.19689, 0.67285, 0.59089, 0.01534, 0.27203, 0.36125, 0.3012, 0.08475, 1.75018, 1.02797, 0.08194, 0.64399, 0.15912, 1.14164, 0.15671, 0.02868, 0.11369, 0.17218, 0.10715, 0.37245, 1.74831, 0.04877, 0.18022, 0.08605, 0.29557, 1.87729, 0.16401, 0.09339, 0.63172, 0.15862, 1.18261, 0.02673, 0.27957, 0.08709, 0.31949, 0.08824, 0.50991, 0.09088, 0.04997, 0.11238, 0.04664, 1.02148, 0.05092];
t_best= [0.00284, 0.00265, 0.00134, 0.00332, 0.00338, 0.00196, 0.00402, 0.00422, 0.00396, 0.0047, 0.00133, 0.00365, 0.00326, 0.00314, 0.00199, 0.00489, 0.00462, 0.00195, 0.00346, 0.00283, 0.00456, 0.00261, 0.00206, 0.00235, 0.00282, 0.00251, 0.00357, 0.00492, 0.00204, 0.00328, 0.00223, 0.0037, 0.00491, 0.00273, 0.00186, 0.00376, 0.0023, 0.00418, 0.00149, 0.00309, 0.00227, 0.00314, 0.00273, 0.00549, 0.00242, 0.00188, 0.00201, 0.00201, 0.00434, 0.00235];
t_beam= [0.00813, 0.01331, 0.00463, 0.02388, 0.02786, 0.00546, 0.02795, 0.04038, 0.03057, 0.03084, 0.00379, 0.02937, 0.02029, 0.0267, 0.00881, 0.07288, 0.11815, 0.00877, 0.0265, 0.01584, 0.05455, 0.01339, 0.00645, 0.01126, 0.01811, 0.01031, 0.02385, 0.07614, 0.00772, 0.01466, 0.00869, 0.02833, 0.0595, 0.01114, 0.00794, 0.03976, 0.01466, 0.05568, 0.00613, 0.0172, 0.00849, 0.02471, 0.01068, 0.03624, 0.01121, 0.00796, 0.01169, 0.00709, 0.05517, 0.00686];
means_t= [mean(t_brute), mean(t_best), mean(t_beam)];
stds_t= [std(t_brute), std(t_best), std(t_beam)];
vec= [1,2, 3];
col_vec= ['b', 'r', 'g'];

figure;
hold on
for i= 1:length(vec)
    b(i) = bar(vec(i), means_t(i), col_vec(i));
    errorbar(vec(i), means_t(i), stds_t(i), stds_t(i), 'Color', 'k', 'LineWidth', 1.5);
end
hold off
xticks([1,2,3])
xticklabels(["Brute Force Search", "Best First Search", "Beam Search"]);
ylabel("Runtime (s)")
title("Worst Case Runtimes: Brute Force vs Best First vs Beam Search")
ylim([-0.1, 0.5])
print(gcf,'WorstCaseComparisonBBB.png','-dpng','-r200');

[h, p] = ttest2(t_brute, t_best);
disp("brute vs best")
disp(p)

[h, p] = ttest2(t_brute, t_beam);
disp("brute vs beam")
disp(p)

[h, p] = ttest2(t_best, t_beam);
disp("beast vs beam")
disp(p)
