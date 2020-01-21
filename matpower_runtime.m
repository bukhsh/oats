%%%
% Authors: Calum Edmunds, Waqquas Bukhsh
% University of Strathclyde
% This code is used for determining run times for cplex and ipopt for
% Matpower7.0. Note that 'clear all' is required to clear the cache at the
% start of each run. A user should change 'test_number' at two locations in
% the script to point it to the case that is being run. The output will
% produce a 'runtimes_matpower.csv' file.
%%%

clear all
test_number = 12; %values between 1 and 12. more cases could be added if required.
cases={'case6ww','case9Q','case14','case24_ieee_rts','case30','case39','case118','case300','case2383wp','case2869pegase','case3012wp','case3120sp'};
fid = fopen( 'runtimes_matpower.csv', 'a' );
fprintf( fid, 'CaseFile: %s,', char(cases(test_number)));
fclose(fid);
for no_of_runs = 1:20
    clear all
    test_number = 12;
    cases={'case6ww','case9Q','case14','case24_ieee_rts','case30','case39','case118','case300','case2383wp','case2869pegase','case3012wp','case3120sp'};
    mpopt=mpoption;
    %mpopt = mpoption(mpopt,'opf.ac.solver','IPOPT');
    mpopt = mpoption(mpopt,'opf.dc.solver','CPLEX');
    mpc = loadcase(char(cases(test_number)));
    % flat start
    mpc.bus(:, 8) = 1;
    mpc.bus(:, 9) = 0;
    mpc.gen(:, 6) = 1;
    %pg values:
    mpc.gen(:,2) = 0.5*(mpc.gen(:,9)+mpc.gen(:,10));
    %qg values:
    mpc.gen(:,3) = 0.5*(mpc.gen(:,4)+mpc.gen(:,5));
    results=rundcopf(mpc,mpopt);
    fid = fopen( 'runtimes_matpower.csv', 'a' );
    fprintf( fid, '%4.4f,',results.et);
    fclose(fid);
end
fid = fopen( 'runtimes_matpower.csv', 'a' );
fprintf( fid, '\n');
fclose(fid);