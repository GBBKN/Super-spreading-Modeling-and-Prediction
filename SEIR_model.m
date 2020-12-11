%--------------------------------------------------------------------------
%   init
%--------------------------------------------------------------------------
clear;clc;

%--------------------------------------------------------------------------
%   para
%--------------------------------------------------------------------------
N = 10000;                                                                  %Total population
E = 0;                                                                      %Exposed
I = 1;                                                                      %Infeccted
S = N - I;                                                                  %Susceptible
R = 0;                                                                      %Recovered

r = 20;                                                                     %contact rate
B = 0.03;                                                                   %infection rate
a = 0.1;                                                                    %E->I rate
y = 0.1;                                                                    %Recover rate

T = 1:140;
for idx = 1:length(T)-1
    S(idx+1) = S(idx) - r*B*S(idx)*I(idx)/N;
    E(idx+1) = E(idx) + r*B*S(idx)*I(idx)/N-a*E(idx);
    I(idx+1) = I(idx) + a*E(idx) - y*I(idx);
    R(idx+1) = R(idx) + y*I(idx);
end

plot(T,S,T,E,T,I,T,R);grid on;
xlabel('Time(days)');%ylabel('counts')
legend('Susceptible','Exposed','Infected','Recovered');title('SEIR Model')