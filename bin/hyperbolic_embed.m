function [Z,r]=hyperbolic_embed(D,varargin)
% [Z,r]=hyperbolic_embed(D) computes the embedding of points into a hyperbolic space
% such that the distances are given by D
% Z is the inner-product (kernel) matrix of the points, r the radius of
% curvature of the space
% The embedded point positions can be found from Z=VEV^T
% (eigendecomposition) and X=r*U*sqrt(abs(E))
% 
% [Z,r]=hyperbolic_embed(D,'opt') 
% will attempt to optimize the resulting embedding to improve the result. 
% This may take some time on large datasets.
% 'opt' is an efficient optimisation method based on gradient descent
% on the tanget plane
% 
%
% [Z,r]=hyperbolic_embed(D,'',x) will attempt to find an embedding into 
% x-dimensional hyperbolic space. The embedding space will be (x+1)-dimensional


global M TZ

sz=size(D,1);
if( size(varargin,2)>1 ) edim=varargin{2};
else edim=sz-2;
end
M=eye(sz);
M(1,1)=-1;

%% mean distance scaling here
rescale=mean(mean(D));
D=D/rescale;

%% find r
r=estimate_r(D,edim);
Z=-cosh(D/r);
Z=0.5*(Z+Z');

%% Correction to eigenvalues
[U,E]=eig(Z);
if( ~issorted(diag(E)) )
    error('Eigenvalues not in sorted order');
end

if r>1.1            % then apply eigenvalue clipping
    v=E(1,1);
    E=max(E,0.0);  % with this threshold
    E(1,1)=v;
end

v=diag(E)+1;
mv=v(sz-edim);
if mv<0.75   % eigenvalue clipping
%    display('No solution'); 
    mv=E(1,1);
    d=max(0,diag(E));
    d(1)=mv;
else
    d=-1+v/mv;
end
d(2:sz-edim)=0;
Z=U*diag(d)*U';

%% Look for disallowed lengths in Z (Z(i,i)>0) and correct
idx=find(diag(Z)>-0.1);
if numel(idx)>0
    for i=idx'
        U(i,1)=sign(U(i,1))*sqrt(U(i,1)^2-(Z(i,i)+0.1)/d(1,1));
    end
    Z=U*diag(d)*U';
end

    

%% vector lengths should be -1 at this point, but need renormalising if we
% are using reduced dimensions
% then ensure symmetry of Z
S=diag(1./sqrt(diag(-Z)));
Z=S*Z*S';

%% size correction for distances
Dn=acosh(max(1,-Z));
a=sum(sum(D.*Dn))/sum(sum(Dn.^2));

%% Optimisation - this is very time consuming, could be improved?
if( size(varargin,2)>0 )
       disp('      Iteration      Error         Radius');

       if( strcmp(varargin{1},'opt') )
           tic;
            % size correction for distances
            Z=0.5*(Z+Z');
            Dn=acosh(max(1,-Z));
            r=sum(sum(D.*Dn))/sum(sum(Dn.^2));
            [U,E]=eig(Z);
            E(2:sz-edim,2:sz-edim)=0;
            X=r*U*sqrt(abs(E));
            Z=X;
            nX={X,X,X};
            err=[0 0 0];
            for iter=1:30
                nr=[r*0.95 r r*1.05];
                for ir=1:3
                     for i=1:sz
                        x=nr(ir)*X(i,:)/r;
                        for j=1:sz
                            y=nr(ir)*X(j,:)/r;
                            Z(j,:)=LogMapH(y,x,M);
                        end

                        idx=1:sz;
                        idx(i)=[];

                        [dx,resnorm]=doptimise(zeros(edim+1,1),i,Z(idx,:),D(idx,i),r*edim*0.0001,x);

                        y=ExpMapH(dx,x,M);
                        nX{ir}(i,:)=y;
                    end
                    Dc=nr(ir)*acosh(max(1,-nX{ir}*M*nX{ir}'/nr(ir)^2));
                    err(ir)=norm(D-Dc,'fro');
                end
                ir=find(err==min(err),1);
                X=nX{ir};
                r=nr(ir);
                disp([iter err(ir) r]);
            end
            Z=X*M*X'/r^2;
    end
end

%% Clip Z to max value -1
Z=min(-1,0.5*(Z+Z'));

%% size correction for distances
%  under some circumstances a can give a better result, not included
%  by default in the output.
Dn=acosh(max(1,-Z));
a=sum(sum(D.*Dn))/sum(sum(Dn.^2));

%% put back scaling
r=r*rescale;
a=a*rescale;
D=D*rescale;

%% some data about the quality of the embedding
disp(' Residual NEF      Corr size      r      D RMSErr  Z RMSErr   NN Err');
Dn=r*acosh(-Z);
Dnc=a*acosh(-Z);

Zo=r^2*cos(D/r);
disp([(-sum(min(diag(E),0))+min(diag(E)))/sum(abs(diag(E))) norm(d-diag(E)) r NormRMSError(Dn,D) norm(Zo-r^2*Z,'fro')/sz NNErr(Dn,D)]);

%% find the optimal radius by minimizing the second smallest eigenvalue
function r=estimate_r(D,edim)
sz=size(D,1);
evs=sz-edim;
rmin=0.08;
rminl=0.08;
%rmax=15*max(max(D));
rmax=2*max(max(D));
opts.issym=1;
opts.disp=0;

% small r search
fmins=1e32;
for n=0:20
        r1=rmin+0.01*n;
        Z=-r1^2*cosh(D/r1);
        E=eigv(Z,evs);
        E=sort(E);
        f1=sum(abs(E(2:evs)));
        if( f1<1e-20 ) 
            r=r1;
            return;
        end
        if(f1<fmins)
            rs=r1;
            fmins=f1;
        end
end
    

% section search - could be improved?
for j=1:6
    step=(rmax-rmin)/11;
    fmin=1e32;
    for r1=rmin+step/2:step:rmax
        Z=-r1^2*cosh(D/r1);
        E=eigv(Z,evs);
        f1=sum(abs(E(2:evs)));
        if( f1<1e-20 ) 
            r=r1;
            return;
        end
        if(f1<fmin)
            r=r1;
            fmin=f1;
        end
    end
    rmin=max(rminl,r-step);
    rmax=r+step;
end
if( fmin>fmins )
    r=rs;
end

if r>10*max(max(D))
    disp('r max');
end

%% Optimization functions

function [nx,resnorm]=doptimise(x,k,Y,d,TolX,m)
global M
[samples,dim]=size(Y);
nx=zeros(1,dim);
dsq=zeros(samples,1);
step=1.0;
resnorm=0;
for iter=1:1
    for p=1:samples
        xd=nx-Y(p,:);
        dsq(p)=xd*xd'-2*xd(1).^2;
    end

%    dx=4*(dsq-d.^2)'*(repmat(nx,samples,1)-Y)*M;
    dx=4*(dsq-d.^2)'*(repmat(nx,samples,1)-Y);
    c=zeros(1,4);
    
   dE2=dx*dx'-2*dx(1).^2;
   c(1)=4*samples*dE2.^2;

   for p=1:samples
        
        % formulae involving xMx' are too slow
        % speed up using xx'-2x(1)^2
        % assumes 1 is the negative dimension
        xd=nx-Y(p,:);
        
        fp=xd*xd'-2*xd(1).^2-d(p).^2;
%        fp=(nx-Y(p,:))*M*(nx-Y(p,:))'-d(p)^2;
        
        gp=dx*xd'-2*dx(1)*xd(1);
 %       gp=dx*M*(nx-Y(p,:))';
                
        c(2)=c(2)+12*gp*dE2;
        c(3)=c(3)+8*gp^2+4*fp*dE2;
        c(4)=c(4)+4*fp*gp;
        
   end

     
    rts=roots(c);
    step=max(rts(imag(rts)==0 & rts<0));
    if numel(step)<1
        keyboard();
    end
    nx=nx+step(1)*dx;
 
    if norm(step*dx)<TolX
        return;
    end
end


function x=LogMapH(v,m,M)
rsq=m*m'-2*m(1).^2;
lsq=v*m'-2*v(1)*m(1);
theta=acosh(lsq/rsq);
if abs(theta)<1e-8
    x=zeros(size(v));
    return;
end
x=theta*(m*cosh(theta)-v)/sinh(theta);

function v=ExpMapH(x,m,M)
r=sqrt(-m*M*m');
theta=sqrt(x*M*x')/r;
if abs(theta)<1e-8 
    v=m;
    return;
end
v=m*cosh(theta)-x*sinh(theta)/theta;
        