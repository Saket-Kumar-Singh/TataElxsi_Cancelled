addpath("C:\Users\HP\Downloads\casadi-3.6.4-windows64-matlab2018b")

import casadi.*
T = 0.2; %Sampling time%
N = 3; %Perception horizon%
rob_diam = 0.3; %Robot Diameter%
v_max = 0.6;
v_min = -v_max;
omega_max= pi/4; omega_min = -omega_max;
x = SX.sym('x');
y = SX.sym('y');
theta = SX.sym('theta');

states = [x;y;theta];
n_states = length(states);

v = SX.sym('v'); omega = SX.sym('omega');
controls = [v;omega]; n_controls = length(controls);

%r.h.s for robot%
rhs = [v*cos(theta); v*sin(theta); omega];

U = SX.sym('U', n_controls, N);
X = SX.sym('X', n_states, N+1);
P = SX.sym('P', n_states+ n_states);

f = Function('f', {states, controls}, {rhs});

X(:, 1) = P(1:3);
%Initial 3 values of p are initial states of robot%

for k = 1:N
    st = X(:,k); cont = U(:, k);
    f_val = f(st, cont);
    st_next = st + T*f_val;
    X(:,k+1) = st_next;
end

ff = Function('ff', {U,P}, {X});
disp("ok")


Q = zeros(N,N); Q(1:1) = 0.3; Q(2,2) = 0.3; Q(3, 3) = 3;
R = zeros(2, 2); R(1, 1) = 0.3; R(2,2) = 3;

for k = 1:N
    st = X(:, k); cont = U(:, k);
    obj = obj + (str - P(4:6))*Q*(str - P(4:6)) + (cont)*R*cont;
end

g = [];

for k=  1:N
    g = [g; X(1, k)];
    g = [g; X(2, k)];
end

OBJ_func = 