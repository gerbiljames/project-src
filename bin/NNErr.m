function err=NNErr(Dn,D)

sz=size(D,1);
err=0.0;
for i=1:sz
%    D(i,i)=inf;
%    Dn(i,i)=inf;
    err=err+corr(D(:,i),Dn(:,i),'type','Spearman');
%    [d,idx]=sort(D(i,:));
%    [dn,idxn]=sort(Dn(i,:));
%    for j=1:n
%        err=err+(idx(j)~=idxn(j));
%    end
end
err=1-err/(sz);

    

