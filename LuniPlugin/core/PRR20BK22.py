# -*- coding: cp1252 -*-
# Separatore 86
# ====================================================================================
# Uso rapido Presenze e Ruoli
# ROUTINE DI INIZIALIZZAZIONE
# Legge megaLista da C:/Users/Paolo/PRR20DUMP/DumpPRR20     DA ADATTARE
# ====================================================================================
def PRRBA20 ():   
# ------------------------------------------------------------------------------------
    from pathlib import Path
    import sys, os, pickle
    import time
    global megaLista
    
    fileDumpNome=str(Path(__file__).parents[1])+'\\DumpPRR20'  
    fileDump=open(fileDumpNome,'rb')        # GESTIRE EXCEPTION
    megaLista=pickle.load(fileDump)         #[BeneInt,retcode,listaKMP,listaKMF]
    fileDump.close()
    return True

# ====================================================================================
# Uso rapido Presenze e Ruoli
# ROUTINE DI CALCOLO PRESENZA/RUOLO
# Trova megaLista come "global"
# Riceve Bene (stringa), Anno1 (num o None), Anno2 (num o None)
# ====================================================================================   
def PRRBB20 (Bene,Anno1,Anno2):   
# ------------------------------------------------------------------------------------
    PRRBA20 () 
    import sys, os, pickle
    import time
    annocorrente = time.localtime()[0]
#   Analisi della correttezza formale dell'ID del Bene
    if not VFstringaDiNumeri(Bene): return 0,0,0,[],5   # Id deb Bene non corretto
#   Analisi della correttezza della coppia Anno1-Anno2
    if Anno1==None: Anno1=''
    if Anno2==None: Anno2=''    
    Anno1R,Anno2R,Dummy=ternaConverti(str(Anno1),str(Anno2),'normale')   
    if Anno1R==-1 or Anno1R==9999: tipoquery='queryErrata'
    elif Anno1R < Anno2R: tipoquery='queryPeriodo'
    else:       tipoquery='queryAnno'
    if tipoquery=='queryErrata': return 0,0,0,[],6      # Anno1 e/o Anno2 non corretti
# ------------------------------------------------------------------------------------
# Verifica presenza del Bene in megaLista
    #print (len(megaLista), str(Bene))
    for i in range(len(megaLista)):
        if int(Bene)==megaLista[i][0]:      # trovato  Bene
            if megaLista[i][1]==0:          # e anche retcode == 0
                listaKMP=megaLista[i][2]
                listaKMF=megaLista[i][3]
                if tipoquery=='queryAnno':	# Analisi in un punto temporale
                    zfloat=matValPuntoDaFunz (listaKMP,Anno1R)	        
                    PP=int(round(zfloat))	# Probab.Presenza
                    PR,RP,RS=matValPuntoDaFunzConVal(listaKMF,Anno1R)
                    # data listakmF, calc.PRuolo, RuoloP, RuoloS al punto "Anno"
                    pRP = int(round(PR)); pRS=99-int(round(PR))
                    return PP,PP,PP,[[RP,pRP,pRP,pRP],[RS,pRS,pRS,pRS]],0
                else:                           # Analisi in un punto temporale
                    max,min,med=matValMaxMinDaFunz(listaKMP,Anno1R,Anno2R)	# qui calcola valore PP in un intervallo
                    Pmax=int(round(max)); Pmin=int(round(min)); Pmed=int(round(med))
                    lf=matValMaxMinMedRuoloDaFunz(listaKMF,Anno1R,Anno2R)   #  ATTENZIONE - Esce anche un float ������������������������
# esempio: [[['pieve'],90,10,30], [['ignoto'],42,2,24], [['convento', 'pieve'],88,14,46]]
             
                    return Pmax,Pmin,Pmed,lf,0
            else:
                return 0,0,0,[],700   # record trovato in megaLista, ma RC NON 0
        else: pass
    return 0,0,0,[],703
            
    
# ---------------------------------------------------------------------------------
def VFstringaDiNumeri(STR):
    if STR is None: return False
    STRS=STR.strip()
    if len(STRS)==0: return False
    if not STRS.isdigit(): return False
    return True



# ====================================================================================
# GESTIONE DATA3
# ====================================================================================
# ------------------------------------------------------------------------------------
def dataVera(DS):	# verifica che una stringa sia una data vera
# riceve in ingresso una stringa (1300, 13001231 ,XII, XI inizio, ...)
# la stringa pu� essere:
# a) un qualsiasi numero in formato stringa. Se ha 4 char o meno ('321') � un anno; se ha 5-8 char � a[aaa]mmgg  ATTENZIONE
# b) un numero romano: I,II,III,IV o IIII,V,VI,VII,VIII,IX,X,XI, XII, XIII, XIV, XV, XVI, XVII, XVIII, XIX, XX, XXI
# c) una stringa formata da (b) e seguita da inizio, fine, meta, prima meta, primameta, seCOnda meta, secondameta 
# In questa versione la risoluzione � l'anno e manca 'a.C.'
# Restituisce True se � una data valida, altrimenti False
# NULL � considerato un valore valido per il campo. Controlli successivi valuteranno se � un valore coerente
# "" � considerato un valore valido per il campo.   Controlli successivi valuteranno se � un valore coerente 
# "   " � considerato un valore NON valido per il campo.
# Elenco date che vengono definite vere (e false): 0,1,101,('1 01'),'',2000, 2019, (2020),(9999),11111,160229,(170229),170228, ...
# ... X, I, XX, (XXI), xinizio, 'x i n i zio',(inizio), xmeta, (xmeta)
    import datetime
    from datetime import date
    annomax = date.today().year			# ANNO CORRENTE cone anno max
    if DS is None: return True                  # Se � NULL va bene (data ignota)
    if len(DS)==0: return True			# Se � stringa lunga 0 va bene (data ignota)
    #sin = DS.replace(' ','')                    # Elimina tutti i blank NO !    '1300 1400' � un errore (??)
    sin=DS.strip()                              # VIA eventuali blank iniziali e finali
    if len(sin)==0: return False		# Era una stringa di blank !!!
    if sin.isdigit():				# se ci sono solo numeri ...
        if len(sin)<=4:         		# numero di <= 4 cifre: � solo anno
            if int(sin)>annomax: return False   # anno futuro = False
            else: return True                   
        elif len(sin)>8: return False           # 5,6,7,8 cifre - se pi� di 8 cifre False
        anno=sin[:-4]; mese=sin[-4:-2]; giorno=sin[-2:]	# ricorda - sono stringhe
        if int(anno)>annomax:  return False
        if int(anno)%4==0 and int(anno) not in (2000,1600,1200,800,400): bisesto=True
        else: bisesto=False
        if int(mese) in (1,3,5,7,8,10,12) and int(giorno)<=31: return True
        elif int(mese) in (4,6,9,11) and int(giorno)<=30: return True
        elif int(mese)==2 and bisesto and int(giorno)<=29: return True
        elif int(mese)==2 and not bisesto and int(giorno)<=28: return True
        else: return False
   				
    RomToArab1 = ['I',1,'II',2,'III',3,'IIII',4,'IV',4,'V',5,'VI',6,'VII',7,'VIII',8,'IX',9,'VIIII',9,'X',10]
    RomToArab2 = ['XI',11,'XII',12,'XIII',13,'XIIII',14,'XIV',14,'XV',15,'XVI',16,'XVII',17,'XVIII',18,'XVIIII',19,'XIX',19,'XX',20]
    RomToArab = RomToArab1 + RomToArab2
    RomDett = ['','inizio','fine','metà','primametà','secondametà']
    # la stringa NON � tutta numerica
    sin = sin.replace(' ','')                   # ORA considero la stringa tutta packed
    for secolo in RomToArab:
        if type(secolo) == str:
            for frazione in RomDett:
                ipotesi = (secolo+frazione).lower()
                if ipotesi == sin.lower():
                    return True
    return False
# ------------------------------------------------------------------------------------
def dataTipoVera(TS):        # verifica che una stringa sia un tipodata vera
# riceve una stringa che pu� essere None (NULL), '', 'normale','niente prima','primaniente',
# ... 'niente dopo','dopo niente', 'niente prima e dopo','prima e dopo niente'
# NULL � considerato un valore valido per il campo. Controlli successivi valuteranno se � un valore coerente
# ... anzi, si fa di tutto perch� None NON arrivi qui, ma sia gi� diventato ''
# I blank non contano: � corretto 'prima e dopo   ni ente' !!
# restituisce True se TS � null o appartiene all'insieme; else False
# Elenco stringhe che vengono definite vere (e false): (5),'',normale,(normal),(primanulla),primaniente, ...
# ... 'prima niente', Prima niente
    if TS is None: return True
    if len(TS)==0: return True
    Tipi=['normale','nienteprima','primaniente','nientedopo','doponiente','nienteprimaedopo','primaedoponiente']
    TSnob=TS.replace(' ','')                    # appiccica tutto
    if len(TSnob)==0: return False
    TSnobmin=TSnob.lower()
    if TSnobmin in Tipi: return True
    else: return False
# ------------------------------------------------------------------------------------
def dataConverti (DS):     			# Converti stringa in dataante-datapost standard
# riceve in ingresso una stringa (1300, XII, 8001225, XI inizio, ...)
# la stringa pu� essere:
# a) un qualsiasi numero in formato stringa ('1321' '29071946'  '25120')
# b) un numero romano: I,II,III,IV o IIII,V,VI,VII,VIII,IX,X,XI, XII, XIII, XIV, XV, XVI, XVII, XVIII, XIX, XX, XXI
# c) una stringa formata da (b) e seguita da inizio, fine, meta, primameta, seconda    meta 
# In questa versione la risoluzione � l'anno e manca 'a.C.'
# RESTITUISCE UNA LISTA       
# Restituisce [data1, data2] relativi alla data DS
# Se data ignota, restituisce [9999,9999]
# Prima controlla se DataValida e se non valida restituisce [-1,-1]
# Se le due date sono uguali era un singolo anno; se diverse era un periodo romano
# Restituisce due valori (annoA,annoP)  -  Se sono 9999,9999 l'anno � sconosciuto
# NULL e stringa lunga 0 � considerato un valore che indica Data sconosciuta.
# ... anzi, si fa di tutto perch� None NON arrivi qui, ma sia gi� diventato ''
    if not dataVera(DS): return (-1,-1)     
    if DS is None: return[9999,9999]            # 9999 indica Data Sconosciuta <<<<<<!=>>>>>>
    if len(DS)==0: return[9999,9999]		# MI SEMBRA CHE DOVREBBE ESSERE TRUE - Perch� ??????????????????
    sin = DS.replace(' ','')                    # Elimina tutti i blank                         	                      
    if sin.isdigit():				# se ci sono solo numeri ...
        if len(sin)<=4: return [int(sin),int(sin)]  # numero di <= 4 cifre: � solo anno
        else: return [int(sin[:-4]),int(sin[:-4])]  # cifre dalla quintultima in su
   				
    RomToArab1 = ['I',1,'II',2,'III',3,'IIII',4,'IV',4,'V',5,'VI',6,'VII',7,'VIII',8,'IX',9,'VIIII',9,'X',10]
    RomToArab2 = ['XI',11,'XII',12,'XIII',13,'XIIII',14,'XIV',14,'XV',15,'XVI',16,'XVII',17,'XVIII',18,'XVIIII',19,'XIX',19,'XX',20,'XXI',21]
    RomToArab = RomToArab1 + RomToArab2
    RomDett = ['inizio','fine','metà','primametà','secondametà']

    sispart=''                                  # inizializzazione
    sinsec=sin                                  # cerca il secolo. forse � solo ...
    for dett in RomDett:                        # ... a meno che ...
        i=sin.lower().find(dett)                # ... nella stringa ci sia inizio, fine o altro ...
        if i >=0:                               # Se c'� "inizio" o altro ...
            sinsec=sin[:i]                      # ... di 'Xinizio' qui resta 'X'
            sispart=sin[i:]                     # ... di 'Xinizio' qui resta 'inizio'
    sinsec=sinsec.upper()
    sispart=sispart.lower()
    for i in range(len(RomToArab)):
        if sinsec==RomToArab[i]: secolonum=RomToArab[i+1]   # secolo 'X' diventa 10
    anno1=(secolonum-1) * 100 + 1
    anno2 = anno1 + 99                                      # 1401-1500
    meta=int((anno2-anno1)/2)
    quarto=int(meta/2)
    if   sispart=='inizio'      : anno2=anno1+quarto        # 1401-1425
    elif sispart=='fine'        : anno1=anno2-quarto        # 1476-1500          
    elif sispart=='metà'        : anno1=anno1+meta-quarto; anno2=anno1+meta # 1426-1475
    elif sispart=='primametà'   : anno2=anno1+meta          # 1401-1450
    elif sispart=='secondametà' : anno1=anno2-meta          # 1451-1500
    return [anno1,anno2]
# ------------------------------------------------------------------------------------
def ternaVera(DataA, DataP, DataTipo):	# CONTROLLO dei tre valori di Data3
# riceve una Data3 formata da DataA, DataP, DataTipo.
# Prima controlla che i valori siano "validi" come valori isolati
# Restituisce True, se la terna ha coerenza tra i 3 valori; altrimenti False
# NULL � un valore valido che, nei calcoli, � trattato come '', ma nel DB resta NULL ...
# ... anzi, si fa di tutto perch� None NON arrivi qui, ma sia gi� diventato ''
# ATTENZIONE: datavera � TRUE se il campo DATA � vuoto, cio� 9999 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if not dataVera(DataA) or not dataVera(DataP) or not dataTipoVera(DataTipo): return False
    DataA2=dataConverti(DataA)          # DataA2 � una lista [Data1, Data2]
    DataP2=dataConverti(DataP)
    if DataTipo is None: DataTipo=''

    if DataA2[0]==9999:
        if DataP2[0]==9999 and DataTipo=='':
            return True                # Data sconosciuta
        else: return False             # Data errata (DataA sconosciuta e valori sul resto)
    if DataP2[1]<DataA2[0]: return False
    else: return True
# ------------------------------------------------------------------------------------
def ternaConverti(DataA, DataP, DataTipo):
# riceve una Data3 formata da DataA, DataP, DataTipo.
# Prima controlla la validit� totale con 'ternaVera'
# Restituisce anno1 e anno2 come estremi dell'intervallo (anche uguali)
# None � un valore valido che, nei calcoli, � trattato come '', ma nel DB resta None ...
# ... anzi, si fa di tutto perch� None NON arrivi qui, ma sia gi� diventato ''
# Restituisce 9999,9999 se il dato � ignoto o -1,-1 se trova un errore
# C'� RIDONDANZA nei controlli - BENE
    if not ternaVera(DataA, DataP, DataTipo): return -1,-1,DataTipo
    DataA2=dataConverti(DataA)
    DataP2=dataConverti(DataP)
    if DataTipo is None: DataTipo=''
    
    if DataA2[0]==9999:                     # Se primo valore sconosciuto ...
        return 9999,9999,DataTipo           # ...  Data mancante (9999,9999
    elif DataP2[0]==9999:                   # Se primo valore OK e secondo mancante ...
        return DataA2[0],DataA2[1], DataTipo    # ... vale solo il primo (1200-1200) oppure XI (1001-1100)
    return DataA2[0],DataP2[1],DataTipo     # Se tutti noti, vale l'intervallo (anche X-XII come 901-1200)   
# ------------------------------------------------------------------------------------

# ====================================================================================
# Calcolo Presenze e Ruoli
# ROUTINE DI INTERPOLAZIONE
# Legge megaLista da C:/Users/Paolo/PRR20DUMP/DumpPRR20     DA ADATTARE
# ====================================================================================
# ---------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ---------    matkm calcola i parametri di una funzione di grado 1   ----------
# ---  Riceve due punti (x1,y1 e x2,y2 e restituisce k,m tali che y = kx+m  ----
# --  x1,x2,k,m = matkm(x1,y1,x2,y2)   (restituisce anche x1 e x2 che sono ...--
# --  l'intervallo in cui la funzione � utilizzabile  --------------------------
# ------------------------------------------------------------------------------
def matkm(x1,v1,x2,v2):	
    X1=float(x1)			# deve lavorare in float
    if X1==x2: return x1,x2,0,max(v1,v2)	# se due punti con stessa x, ...
#   ... restituisce il valore y maggiore
    k=(v2-v1)/(x2-X1)
    m=v1-X1*k
    return x1,x2,k,m
# ------------------------------------------------------------------------------
# ----    matValPuntoDaFunz calcola il valore di una funzione al punto x  ------
# ---  Riceve una lista di tipo "listakm" e un valore x (intero o float) e ..---
# ---  .. restituisce il valore FLOAT della funzione in x                    ---
# ------------------------------------------------------------------------------
def matValPuntoDaFunz(listakm,x):
#   listaKM:  [x1,y1,x2,y2,k,m]    
    xf=float(x)
    for rec in listakm:
        if xf>=rec[0] and xf<=rec[2]:		 
            k=rec[4]; m=rec[5]
            return xf*k+m
    return -9999
# ------------------------------------------------------------------------------
# ----    matValPuntoDaFunzConVal calcola il valore di una funzione al punto x  ------
# ---  Riceve una lista di tipo "listakm" e un valore x (intero o float) e ..---
# ---  .. restituisce il valore FLOAT della funzione in x                    ---
# ------------------------------------------------------------------------------
def matValPuntoDaFunzConVal(listakmv,x):
#   listaKMV:  [x1,y1,x2,y2,k,m,'Ruolo1','Ruolo2']
    xf=float(x)
    for rec in listakmv:
        if xf>=rec[0] and xf<=rec[2]:		# �������������������������� 
            k=rec[4]; m=rec[5]
            z=xf*k+m
            RP=rec[6]; RS=rec[7]	# z si riferisce a RP. Prob. di RS � 99-RP
            return z,RP,RS
    return -9999
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------ 
# ----  matValMaxMinMedDaFunz calcola il valore max(min) di una funzione ... ---
# ----    ... in un intervallo x1-x2                                      ------
# ---  Riceve una lista di tipo "listakm" e gli estremi dell'intervallo ... ----
# ---  x1/x2  (interi o float) e restituisce ...                             ---
# ---  ..  i valori max/min/medio FLOAT della funzione nell'intervallo       ---
# ------------------------------------------------------------------------------
def matValMaxMinDaFunz(listakm,x1,x2):
#   listaKM:  [x1,y1,x2,y2,k,m]    
    if x1>x2:					# deve essere x1<=x2
        xf=x1; x1=x2; x2=xf			# inverti i valori
    x1f=float(x1); x2f=float(x2)

    punti=[]
    y=matValPuntoDaFunz(listakm,x1f); punti.append([int(round(x1f)),int(round(y))])	# primo punto - questo va calcolato
    for punto in listakm:
        if punto[0]>x1 and punto[0]<x2:	    #  con > e < l'insieme � aperto
            punti.append([punto[0],punto[1]])
    y=matValPuntoDaFunz(listakm,x2f); punti.append([int(round(x2f)),int(round(y))])	# ultimo punto
# punti[] � l'elenco di tutti i punti [x,y] dove la funzione (fatta da segmenti) cambia direzione
    max=-9999; min=9999
    for punto in punti:
        if punto[1]>max: max=punto[1] 
        if punto[1]<min: min=punto[1] 
    inte=0
    if len(punti)>1:				# NO evita divis x zero
        for p in range(len(punti)-1):
            inte=inte+(punti[p+1][0]-punti[p][0])*((punti[p+1][1]+punti[p][1])/2)
    med=inte/(punti[-1][0]-punti[0][0])
    return max, min, med
# ------------------------------------------------------------------------------
def matValMaxMinMedRuoloDaFunz(listaKMF,x1,x2):
#   listaKMV:  [x1,y1,x2,y2,k,m,'Ruolo1','Ruolo2']
    if x1>x2:					# deve essere x1<=x2
        xf=x1; x1=x2; x2=xf
    x1f=float(x1); x2f=float(x2)

    punti=[]
    PR1,R1,R2 = matValPuntoDaFunzConVal(listaKMF,x1f)
    punti.append([int(round(x1f)),int(round(PR1)),R1,R2])	# calcola primo punto
    for punto in listaKMF:
        if punto[0]>x1 and punto[0]<x2:		# se s�, l'estremo inferiore sta nell'intervallo
            punti.append([punto[0],punto[1],punto[6],punto[7]])
    PR1,R1,R2 = matValPuntoDaFunzConVal(listaKMF,x2f)
    punti.append([int(round(x2f)),int(round(PR1)),R1,R2])	# calcola ultimo punto
# punti[x,y,RuoloP,RuoloS] � l'elenco di tutti i punti dove la funzione (fatta da segmenti) ...
# ... cambia direzione sia per RuoloP che per RuoloS
# -----------------------------------------------
    RuoliL = []; RuoliV=[]; RuoliP=[]  # Lista dei [ruoli], dei [Valori], di [ProbMax,ProbMin]
    for id  in range(len(punti)-1):  # scorre punti da 0 al penultimo
        # prima guarda se i ruoli ci sono
        if punti[id][2] not in RuoliL:
            RuoliL.append(punti[id][2]); RuoliV.append(0); RuoliP.append([-9999,+9999])
        if punti[id][3] not in RuoliL:
            RuoliL.append(punti[id][3]); RuoliV.append(0); RuoliP.append([-9999,+9999])
 
        areaP=(punti[id+1][0]-punti[id][0])*(punti[id+1][1]+punti[id][1])/2
        maxP=max(punti[id][1],punti[id+1][1])
        minP=min(punti[id][1],punti[id+1][1])

        areaS=(punti[id+1][0]-punti[id][0])*100-areaP
        maxS=100-minP; minS=100-maxP
        
        ip=RuoliL.index(punti[id][2]); RuoliV[ip]=RuoliV[ip]+areaP
        RuoliP[ip][0]=max(RuoliP[ip][0],maxP); RuoliP[ip][1]=min(RuoliP[ip][1],minP)
       
        ip=RuoliL.index(punti[id][3]); RuoliV[ip]=RuoliV[ip]+areaS
        RuoliP[ip][0]=max(RuoliP[ip][0],maxS); RuoliP[ip][1]=min(RuoliP[ip][1],minS)
        
        #print (" Stampa creazione dell'integrale 1")
        #for i in range(len(RuoliL)): print (RuoliV[i], RuoliL[i], RuoliP[i])
    
    areaTot = sum(RuoliV)
    for i in range(len(RuoliV)):
        RuoliV[i]=round(100*RuoliV[i]/areaTot)
        
    delta = sum(RuoliV)-100    # se positivo bisogna togliere
    if delta !=0:
        pos=RuoliV.index(max(RuoliV)) # qui ci sta un massimo
        RuoliV[pos]=RuoliV[pos]-delta

    funz=[]
    for i in range(len(RuoliV)):
        funz.append([RuoliL[i],RuoliP[i][0],RuoliP[i][1],RuoliV[i]])
    
    funzO=[]
    while len(funz)>0:
        RVmax=-1; ind=-1            # scorri funz e cerca max
        for i in range(len(funz)):
            if funz[i][3]>RVmax:
                ind=i; RVmax=funz[i][3]
        # ind � l'indice dell'elemento con ValoreMedio maggiore
        funzO.append(funz[ind])
        del funz[ind]
    # adesso funzO � ordinata, ma bisogna portare ignoto in fondo
# ATTENZIONE - potrebbero capitare DUE 'ignoto'
    for ind in range(len(funzO)):
        if funzO[ind][0][0]=='ignoto':
            funzO.append(funzO[ind]); del funzO[ind]
            for ind2 in range(len(funzO)-1): # se ci fosse il secondo
                if funzO[ind2][0][0]=='ignoto':
                    funzO.append(funzO[ind2]); del funzO[ind2]
# esempio: [[['pieve'],90,10,46], [['convento', 'pieve'],88,14,24], [['ignoto'],42,2,30]]
    return funzO
# -------------------------------------------------------------------------------

#
#   CODICI DI ERRORE
#    5 - Identificatore del Bene errato
#    6 - Query errara - Anno1 e Anno2 non corretti
#   10 - Indefinito
#   11 - Il Bene non � nella lista dei Beni
#   12 - Nessun record per il Bene
#   14 - Nessun record riguardante il bene fornito di Data
#   17 - Un record funzione riguardante il Bene ha data errata
#   18 - Non ci sono record riguardanti il bene con Data valida
#   36 - Errore nella costruzione delle lista KM