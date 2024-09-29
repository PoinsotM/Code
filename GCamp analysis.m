clear all;
clc;
close all;

mat= load('2f.txt');   %Chargement du fichier
[l,c]=size(mat);

%mat(:,1:10)=[];
%mat(:,76:140)=[];

%vector=mat(2,:)';
%smat = sgolayfilt(vector,3,15);
%ssmat=smat';

%Standard deviation
s=std(mat,0,2);                 %Definition de la standard deviation globale
s2=std(mat(:,1:20),0,2);      %Definition de la standard deviation du bruit
q=quantile(mat,0.75,2);

 
for i=1:l
matmin(i,:)=mat(i,:)<=(max(i)/4);
%matmin(i,:)=mat(i,:)<=q(i);
end
matstd=matmin.*mat;

s3=std(matstd,0,2);

%Variables
x=0:1:150;                      %Nombre de frame dans l'acquisition
y=x*0.2;                        %Temps (en s)

%figure
%subplot(2,1,1);
%plot(x,mat(6,:))

%subplot(2,1,2);
%plot(x,ssmat(6,:))
%plot(x,ssmat)

%figure
%xlabel('Time(s)')
%ylabel('Deltaf/f')
%plot(x*0.2,mat(40,:))
%axis([0 30 -0.5 1.5])


%Detection des pics
for i=1:l
[pks,locs,w,p,wx1,wx2]=findpeaks2(mat(i,:),'MinPeakProminence',s(i)/2.5);

%figure
%findpeaks(mat(i,:),'MinPeakProminence',s(i)/2.5,'Annotate','extents','WidthReference','halfheight')

   for j=1:length(pks)
   peak(i,j)=pks(j);
   location(i,j)=locs(j);
   width(i,j)=w(j)*0.2;
   prominence(i,j)=p(j);
   widthX1(i,j)=wx1(j);
   widthX2(i,j)=wx2(j);
   
   %temps de montee (en s)
   tm(i,j)=(location(i,j)-widthX1(i,j))*2*0.2;
   
   if (location(i,j)==19)    
       tm1(i,1)=tm(i,j);
       width1(i,1)=width(i,j);
       prominence1(i,1)=prominence(i,j);
   end
   
   end
end


%Nombre de pics
for i=1:l
n(i)=sum(location(i,:)~=0);
end
n=n';

%Amplitude des pics
%width(width == 0) = NaN;
prominence(prominence == 0) = NaN;
%mw=nanmean(width,2);
mp=nanmean(prominence,2);

%figure, hold on
%for i=1:l
 %  scatter(i,mp(i),'filled','k')
%end


% Trace deltaf sur f
figure, hold on
axis([0 30 -1 7])
%axis([0 90 -1 2])
title('Deltaf/f')
xlabel('Time(s)')
ylabel('Deltaf/f')
for i=1:l
    %plot(x*0.1,mat(i,:))
    plot(x*0.2,mat(i,:))
end

%Rasterplot
figure, hold on
title('Rasterplot')
xlabel('Time(s)')
ylabel('Cell number')
for i=1:l
   A=[y location(i,:)*0.2;zeros(size(y)) i*ones(size(location(i,:)))];
   %plot (x, location(i,:))
   %A=[x location(i,:);zeros(size(x)) i*ones(size(location(i,:)))];
   
   B=sortrows(A',1)';
   scatter(B(1,:),B(2,:),10,'filled','k')
end

%Synchrony
    %On prend toutes les cellules a
    d=length(n);
    o=1;
    g=0;

    for a=1:d    %Sert a initialiser la matrice sy à la taille nécessaire pour que toutes les données rentrent
        [lloc,cloc]=size(location);
        m=nnz(location(a,:));
        if m>g
            g=m;
        end
    end  

  sy=zeros(g,d);
    for a=1:d  %construction matrice de synchronie
        [lloc,cloc]=size(location);
        for j=1:cloc        %Cherche les cellules synchronisées à la cellule a avec +/-200ms
            if location(a,j)~=0
                [row,col]=find(location>=(location(a,j)-1) & location<=(location(a,j)+1));
                sy(j,o)=length(row)/l*100-(1/l*100);
            end
        end
        o=o+1;
    end

%Suppression des 0 dans la matrice sy
T =location.';
sy0 = nan(size(sy));
for r = 1:size(sy,2)
    for s=1:size(sy,1)
        if T(s,r)~=0
        sy0(s,r)=sy(s,r);
        end
    end
end


%Trie des pics en fonction de leur synchronie
    treshS=45; %  seuil au dela duquel on considere qu'un evenement est un burst "si plus de 45% des ROI dont differentes de 0"
    n1=zeros(length(n),1);
    l1=zeros(50,1);
    e3=1;
    for r1=1:d
        for e1=1:cloc
           if sy(e1,r1)>=treshS  %selection par seuil de synchronie
               k=location(r1,e1); %detection de la frame où le burst à lieu
               if ismember(k,l1)==0 && ismember(k+1,l1)==0 && ismember(k-1,l1)==0 && ismember(k-2,l1)==0 && ismember(k+2,l1)==0    %mémoire des pics
                   l1(e3)=l1(e3)+k;
                   e3=e3+1; 
               end
            end
        end 
    end      



    %Matrice d'amplitude pics significatifs
    i1=0;
    for y=1:length(l1) %extraction nombre de pics significatifs
        if l1(y)~=0
            i1=i1+1;
        end
    end
    
    amp=zeros(d,i1); %Amplitude des neurones à chaque burst (toutes amplitudes)
    for v=1:i1
        for w=1:d
            k1=findv1(location(w,:),l1(v));          %On cherche içi l'indice à +/- 1 frame des pics
            k2=findv1(location(w,:),l1(v)+1);
            k3=findv1(location(w,:),l1(v)-1);
            if k1~=0                                 %La location du pic se trouve sur un des trois k. On trouve le bon et on cherche l'amplitude
                amp(v,w)=peak(w,k1);
            elseif k2~=0
                amp(v,w)=peak(w,k2);
            elseif k3~=0
                amp(v,w)=peak(w,k3);  
            end
        end
    end

    ampm=zeros(i1,1); %Matrice de l'amplitude moyenne des bursts
    for o1=1:i1
        o3=0;   %Somme des valeurs
        o5=0;   %Compte du nombre de ROI participant au pic
        for o2=1:d-8
            if amp(o1,o2)~=0
                o5=o5+1;
                o3=o3+amp(o1,o2);
            end
        end
        o4=o3/o5;
        ampm(o1,1)=o4;
    end

    %Trie des pics en fonction de leur amplitude & Comptage neurones
    %participants aux pics choisis respectifs

    n2=zeros(d,1);
    ampm2=zeros(i1,1);
    p4=1;
    treshA =0.3; %seuil amplitude
    for p1=1:length(ampm)
        if ampm(p1)>treshA %Selection amplitude
            for p2=1:d  
                for p3=1:cloc
                    if location(p2,p3)<=l1(p1)+1 && location(p2,p3)>=l1(p1)-1 % Fourchette de frame 
                        n2(p2)=n2(p2)+1;
                        if findv1(ampm2,ampm(p1))==0; %test de mémoire 
                            ampm2(p4)=ampm(p1);
                            p4=p4+1;
                        end
                    end
                end
            end
        end
    end    

    %Suppression des 0 dans la matrice ampm2
    c2=0;
    for c1=1:length(ampm2)
        if ampm2(c1)~=0
            c2=c2+1;
        end
    end
    ampm3=zeros(c2,1);
    for c3=1:c2
        ampm3(c3)=ampm2(c3);
    end
    
      
%Matrice de correlation
figure
 c=corrcoef(mat');
 imagesc(c)
 colormap(jet(300))
 colorbar
 caxis([0 1])               %Fixe l'echelle de la heatmap de 0 à 1
 
 



