%--------------------------------------------------------------------------
%   init
%--------------------------------------------------------------------------
clear;clc;

%--------------------------------------------------------------------------
%   para
%--------------------------------------------------------------------------
N = 10000;                                                                  %Total population
E = 0;                                                                      %Exposed
I = 1;                                                                      %Infectious
S = N - I;                                                                  %Susceptible
R = 0;                                                                      %Recovered
D = 0;                                                                      %Dead
SS = 0;                                                                     %Super-spreaders

r = 20;                                                                     % # contacts :I <-> S
r2 = 20;                                                                    % # contacts :E <-> S
r3 = 50;                                                                    % # contacts :SuSp <-> S
B = 0.03;                                                                   %Probability of infection
B2 = 0.03;                                                                  %Probability of infection: E -> S
B3 = 0.5;                                                                   %Probability of infection: SuSp -> S
a = 0.1;                                                                    %Probability of transmission: E -> I
a2 = 0.1;                                                                   %Probability of transmission: SuSp -> I
y1 = 0.1;                                                                   %Probability of recovery
y2 = 0.05;                                                                  %Probability of death
c = 0.005;                                                                  %Probability of E -> SuSp
policy_flag = 15;


T = 1:150;
for idx = 1:length(T)-1
    if idx >= policy_flag
        r = 5;
        r2 = 5;
        r3 = 5;
    end
    S(idx+1) = S(idx) - r*B*S(idx)*I(idx)/N - r2*B2*S(idx)*E(idx)/N - r3*B3*S(idx)*SS(idx)/N;
    E(idx+1) = E(idx) + r*B*S(idx)*I(idx)/N + r2*B2*S(idx)*E(idx)/N + r3*B3*S(idx)*SS(idx)/N - a*E(idx) - c*E(idx);
    SS(idx+1) = SS(idx) + c*E(idx) - a2*SS(idx);
    I(idx+1) = I(idx) + a*E(idx) + a2*SS(idx) - y1*I(idx) - y2*I(idx);
    R(idx+1) = R(idx) + y1*I(idx);
    D(idx+1) = D(idx) + y2*I(idx);
    
end

plot(T,S,T,E,T,I,T,R,T,SS,T,D);grid on;
hold on
plot([policy_flag policy_flag],[0 10000])
xlabel('Time (days)');%ylabel('counts')
legend('Susceptible','Exposed','Infectious','Recovered','Super-Spreaders','Dead','Policies implemented')
title('Modified SEIR model')