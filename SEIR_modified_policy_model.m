%--------------------------------------------------------------------------
%   Init
%--------------------------------------------------------------------------
clear;clc;

%--------------------------------------------------------------------------
%   para
%--------------------------------------------------------------------------
N = 10000;                                                                  %total population
E = 0;                                                                      %Exposed
I = 1;                                                                      %Infected
S = N - I;                                                                  %Susceptible
R = 0;                                                                      %Recovered

r = 20;                                                                     %contact rate
B = 0.03;                                                                   %infection rate
a = 0.1;                                                                    %E->I rate
r2 = 20;                                                                    %contact number(E)
B2 = 0.03;                                                                  %infection rate for E
y = 0.1;                                                                    %recovery rate
policy_flag = 21;

T = 1:140;
for idx = 1:length(T)-1
    if idx>=policy_flag
        r=5;
        r2=5;
    end
    S(idx+1) = S(idx) - r*B*S(idx)*I(idx)/N(1) - r2*B2*S(idx)*E(idx)/N;
    E(idx+1) = E(idx) + r*B*S(idx)*I(idx)/N(1)-a*E(idx) + r2*B2*S(idx)*E(idx)/N;
    I(idx+1) = I(idx) + a*E(idx) - y*I(idx);
    R(idx+1) = R(idx) + y*I(idx);
    
end

plot(T,S,T,E,T,I,T,R);grid on;
hold on
plot([policy_flag policy_flag],[0 10000])
xlabel('Day');ylabel('number')
legend('Susceptible','Exposed','Infected','Recovered','Policy')
title('The effect of policy on SEIR model')