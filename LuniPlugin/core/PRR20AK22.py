# ====================================================================================
# ====================================================================================
#                                                                                  ===
# ===                ATTENZIONE - QUESTA NON E' UNA ROUTINE                        ===
# ===  Questo è un programma stand alone che deve essere eseguito per creare ...   ===
# ===  ... su un file su disco una tabella che le routine PRR20Bxx useranno ...    ===
# ===  ... per calcolare velocemente Prob. di Presenza e Ruolo di un Bene          ===
# ===  Pertanto il MAIN alla fine fa parte del tutto                               ===
# ===  La tabella ("megaLista") conterrà dati per tutti i beni del progetto        ===
# ===  (Stimati 400 byte/Bene, ma di più se ci saranno più funzioni)               ===
# ===  Questo programma va adattato per dargli le corrette liste di ingresso ...   ===
# ===  (liste degli attributi dei record Beni e Funzioni) e il corretto file ...   ===
# ===  ... dove scrivere la megaLista. megaLista è scritta in BINARIO, uso Dump    ===
# ===  Lo stesso file sarà letto da PRR20Bxx
#                                                                                  ===
# ====================================================================================
# ====================================================================================







# -*- coding: cp1252 -*-

# ====================================================================================
def PRRA20 (Bene,LBenInput,LFunInput):
# ------------------------------------------------------------------------------------
# ---         ROUTINE DI LIVELLO 1                             --
# ------------------------------------------------------------------------------------
# Riceve ID di un Bene (string) e ...                                               --
#    ... le liste degli attributi di Beni e Funzioni. (E' una lista di liste)       --
#                                                                                   --
# Restituisce per il Bene: le lista necessarie ai progr. PPRBxx per calcolare...    --
# --- le Probabilità di Presenza e di Ruolo
# La lista "log" contiene messaggi dettagliati per il debug dell'operazione         --
# La Prob.di Presenza è sempre <100; per i ruoli la somma delle Prob è sempre < 100 -- 
#
# ------------------------------------------------------------------------------------
    import sys
    import time
    log=[]
    annocorrente = time.localtime()[0]
# QUI SI CONTROLLA IL PARAMETRO DELLE ATTENUAZIONI:  periodocritico = 100	    --
    periodocritico = 100	# PARAMETRO CHE CONTROLLA LE ATTENUAZIONI DI PP e PR
#   Analisi della correttezza formale dell'ID del Bene
    if not VFstringaDiNumeri(Bene):
        return 5,[],[]

# Beni:       ID;Lotto;Ident;Descr;MEO;MEC;Topo;Esist;Comune;Bibl;Sched;Note
# Funzioni:   ID;Lotto;Denom;data;data_poste;tipodata;Ruolo;Funz;IDR;DenomR;RuoloR;Bibl;Sched;Note
    MDBeniInizio=['id','esist'];       # Attributi necessari	   # indici posizione
    MDFunzInizio=['id_bene','data_ante','data_poste','tipodata','ruolo','funzione','id_bener','ruolor']

    DicB={'id':0, 'esist':1}
    DicF={'id_bene':0, 'data_ante':1, 'data_poste':2, 'tipodata':3, 'ruolo':4, 'funzione':5, 'id_bener':6, 'ruolor':7}
    
# Verifica se gli attributi richiesti sono presenti nei dati forniti
# Restituisce la lista completa, ma con estratti solo i campi utili !!!
    LBen,rc1,rctext=PRR20selectDati(MDBeniInizio,LBenInput)
    log.append('\n.... Analisi modello dati Beni')
    for reclog in rctext: log.append(reclog)
    LFun,rc2,rctext=PRR20selectDati(MDFunzInizio,LFunInput)
    log.append('\n.... Analisi modello dati Funzioni')
    for reclog in rctext: log.append(reclog)
    if rc1!=0 or rc2!=0: return 10,[],[]

#Elimina record 0 (nomi dei campi)
    r1=LBen[0];LBen.remove(r1)
    r1=LFun[0];LFun.remove(r1)

# ELIMINA i None e TRASFORMA tutto in STRINGA
    for inF in range(len(LFun)):
        for inr in range(8):
            if LFun[inF][inr] is None:
                LFun[inF][inr]=''
            else: LFun[inF][inr] = str(LFun[inF][inr])
    for iB in range(len(LBen)):
        for ir in range(2):
            if LBen[iB][ir] is None: LBen[iB][ir]=''
            else: LBen[iB][ir] = str(LBen[iB][ir])
            
#    print ('crea la lista di funzioni con ID = Bene o IDR = Bene') 
#    for i in LBen: print (i)       # DEBUG
#    print (' ')                    # DEBUG
#    for i in LFun: print (i)       # DEBUG
#    print (' ')                    # DEBUG
    
#   crea una lista delle funzioni relative al Bene più un record fittizio se Bene esistente
    listaFun=[]
    for lF in LFun:				# Seleziona se Bene è ID o IDR !!!!!
        if lF[DicF['id_bene']]==Bene or lF[DicF['id_bener']]==Bene: listaFun.append(lF)
    if len(listaFun)==0:
        log.append('\nXXXX nessun record funzione per il Bene '+Bene)
#   aggiungi record esistenza
    BinB=False
    for lB in LBen:
        if lB[DicB['id']]==Bene:
            BinB=True
            valEsist=lB[DicB['esist']]
            if valEsist is None: esiste=False
            else:
                valEsist=valEsist.strip()
                if valEsist=='': esiste=False
                elif valEsist.lower()=='no' : esiste=False
                else: esiste=True
            if esiste: 
                log.append('\n++++ Il bene è esistente')
                listaFun.append([Bene,str(annocorrente),'','','ruoloattuale','','',''])  
#               ... un finto record Funzione con ruolo "speciale"
            else: log.append("\n++++ Il bene è attualmente 'non esistente'")
    if BinB == False:
        log.append('XXXX Il Bene non risulta nella lista dei Beni - ERRORE')
        return 11,[],[]
    
    log.append('++++ Selezionati i record relativi al Bene con id = '+Bene)
    if len(listaFun)==0:
        log.append('XXXX Nessun record - Restituisce lista vuota')
        return 12,[],[] # àààààààààààààààààààààààààààààààààààààààààààààààààà
    elif len(listaFun)==1  and esiste:
        log.append("???? Esiste solo il record dovuto all'esistenza del Bene")
    log.append('++++ Ci sono '+str(len(listaFun))+' record riguardanti il bene (con possibilità di Data assente) ')

#----------------------------------------------------------------------------
#   Se in listaFun esistono record con data "", la data era mancante...
#   La Funzione è inutile, quindi elimina
#----------------------------------------------------------------------------
    #print ('\nListaFun selezionate relative al bene ',Bene)
    #for i in listaFun:             # DEBUG
    #    print (i)                  # DEBUG
    ind=0	 
    while ind <= len(listaFun)-1:
        record = listaFun[ind]
        if record[DicF['data_ante']]=="" or record[DicF['data_ante']] is None:
            listaFun.remove(record)
            ind=ind-1
        ind=ind+1	
    log.append('\n++++ Ci sono '+str(len(listaFun))+' record riguardanti il bene con Data presente ')
    if len(listaFun)==0: 
        log.append('Esco')
        return 14,[],[]
#   ATTENZIONE: in listaFun la Data è una stringa
#    print ('\nListaFun dopo eliminazione per data assente:')
#    for i in listaFun:             # DEBUG
#        print (i)                  # DEBUG

#----------------------------------------------------------------------------
# Controlla la validità dei campi data - dopo di questo si assume sempre valida
#   Dovrebbe essere valida perchè viene dall'archivio ufficiale !!
#----------------------------------------------------------------------------
    for rF in listaFun:
        da=rF[1]; dp=rF[2]; dt=rF[3]
        if (not ternaVera(da,dp,dt)) or da=='' or da is None:
            log.append('XXXX Una funzione riguardante il Bene ha la data ERRATA')
            return 17,[],[]
        # ATTENZIONE: Una data IGNOTA è comunque una data VALIDA, anche se
        # i record con Data IGNOTA sono stati eliminati prima
	
# listaFun viene trasformata in listaFunOrdinata. Il primo è il più antico
    listaFunOrd=[]					
    while len(listaFun)>0:				# finchè ci sono record Fun ...
        lastanno=99999					# cerca tra i record Fun il più antico ... 
        for ib in range (len(listaFun)):		
            listaj = listaFun[ib]
            # ATTENZIONE - Se Data Invalida risultati NON predicibili
            dant,dpost,dtip=ternaConverti(listaj[DicF['data_ante']],listaj[DicF['data_poste']],listaj[DicF['tipodata']])
            if dant<lastanno: 				# Se c'è un 'periodo' conta la data iniziale !!!
                                                        # (ATTENZIONE: se data assente trova dant= 9999
                idok=ib					# #idok indica il più antico
                lastanno=dant
        listaFunOrd.append(listaFun[idok])	        # ... e mettilo nella lista nuova
        del listaFun[idok]				# e infine toglilo da quella di partenza
#   ATTENZIONE: in listaFunOrd la Data è una stringa
#    print ('\nListaFun Ordinata, ci sono ',str(len(listaFunOrd)),' elementi')        # DEBUG
#    for i in listaFunOrd:           # DEBUG
#        print (i)                   # DEBUG
    log.append('++++ Ci sono '+str(len(listaFunOrd))+' record riguardanti il Bene, ordinati per DATA')
    if len(listaFunOrd)==0:
        log.append('\nXXXX Non ci sono record riguardanti il bene con Data valida ')
        return 18,[],[]
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
#   Costruzione lista per Presenza e lista per Ruolo  
#
    listaKMP,listaKMF,retcode,retlog = PRR20KmpKmf(listaFunOrd,DicF,Bene,annocorrente,periodocritico)   
    log.append ('\n++++ Costruite KMP e KMF - retcode = '+str(retcode))
    log.append ('++++ Costruite KMP e KMF di lunghezza: '+str(len(listaKMP))+'  e  '+str(len(listaKMF))  )
    for ir in retlog: log.append(ir)
    if retcode!=0: return 36,[],[]
    else: return 0,listaKMP,listaKMF
     
 

    
# ---------------------------------------------------------------------------------
def VFstringaDiNumeri(STR):
    if STR is None: return False
    STRS=STR.strip()
    if len(STRS)==0: return False
    if not STRS.isdigit(): return False
    return True


# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
# ---                                 PRR20selectDati                               --
# ------------------------------------------------------------------------------------
def PRR20selectDati(Lrich,Ldati):
#   Riceve la lista degli attributi richiesti e una lista di dati (Ben o Funz)
#   Restituisce la Lista degli attributi, ma solo gli attributi richiesti; ...
#   ... La prima sottolista contiene e nomi dei campi estratti
#   Per esempio    MDBeniInizio=['id','Esist']
#   Restituisce ListaUtile, codice di errore e log
    log=[]; rc=0
    LdatiMD=Ldati[0]; Ldatimd=[]
    for campo in LdatiMD: Ldatimd.append(campo.lower())
    Ind=[]
    for campoR in Lrich:
        if not campoR.lower() in Ldatimd:
            rc=1; log.append('XXXX Routine PRR20selectDati; campo '+campoR+' non trovato')
        else:
            Ind.append(Ldatimd.index(campoR.lower()))
    if rc!=0: return ([],rc,log)
#   I campi ci sono tutti alle posizioni indicate nella lista "Ind"
    Lout=[]    
    for listina in Ldati:
        listinaR=[]
        for j in Ind:
            listinaR.append(listina[j])
        Lout.append(listinaR)
    log.append('++++ Routine PRR20selectDati: eseguita con codice ritorno 0')
    log.append('++++ Lista in input: '+str(len(Ldati))+' elementi;     selezionati '+str(len(Lrich))+' campi')
    return Lout,rc,log
# Fine -------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
# ---                                 Gestione DATA                                 --
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
def dataVera(DS):	# verifica che una stringa sia una data vera
# riceve in ingresso una stringa (1300, 13001231 ,XII, XI inizio, ...)
# la stringa può essere:
# a) un qualsiasi numero in formato stringa. Se ha 4 char o meno ('321') è un anno; se ha 5-8 char è a[aaa]mmgg  ATTENZIONE
# b) un numero romano: I,II,III,IV o IIII,V,VI,VII,VIII,IX,X,XI, XII, XIII, XIV, XV, XVI, XVII, XVIII, XIX, XX, XXI
# c) una stringa formata da (b) e seguita da inizio, fine, meta, prima meta, primameta, seCOnda meta, secondameta 
# In questa versione la risoluzione è l'anno e manca 'a.C.'
# Restituisce True se è una data valida, altrimenti False
# NULL è considerato un valore valido per il campo. Controlli successivi valuteranno se è un valore coerente
# "" è considerato un valore valido per il campo.   Controlli successivi valuteranno se è un valore coerente 
# "   " è considerato un valore NON valido per il campo.
# Elenco date che vengono definite vere (e false): 0,1,101,('1 01'),'',2000, 2019, (2020),(9999),11111,160229,(170229),170228, ...
# ... X, I, XX, (XXI), xinizio, 'x i n i zio',(inizio), xmeta, (xmeta)
    import datetime
    from datetime import date
    annomax = date.today().year			# ANNO CORRENTE cone anno max
    if DS is None: return True                  # Se è NULL va bene (data ignota)
    if len(DS)==0: return True			# Se è stringa lunga 0 va bene (data ignota)
    #sin = DS.replace(' ','')                    # Elimina tutti i blank NO !    '1300 1400' è un errore (??)
    sin=DS.strip()                              # VIA eventuali blank iniziali e finali
    if len(sin)==0: return False		# Era una stringa di blank !!!
    if sin.isdigit():				# se ci sono solo numeri ...
        if len(sin)<=4:         		# numero di <= 4 cifre: è solo anno
            if int(sin)>annomax: return False   # anno futuro = False
            else: return True                   
        elif len(sin)>8: return False           # 5,6,7,8 cifre - se più di 8 cifre False
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

        
    # la stringa NON è tutta numerica
    sin = sin.replace(' ','')                   # ORA considero la stringa tutta packed
    for secolo in RomToArab:
        if type(secolo) == str:
            for frazione in RomDett:
                ipotesi = (secolo+frazione).lower()
                if ipotesi == sin.lower():
                    return True
    return False


#   VERSIONE PRECEDENTE CON BUG    
#    sinrem=sin
#    for dett in RomDett:                        #
#        i=sin.lower().find(dett)                # se nella stringa c'è inizio, fine o altro, inizia da i; else i=-1
#        if i >=0:                               # 'XIprima meta' resta 'XI'
#            sinrem=sin[:i]            
#    if sinrem.upper() not in RomToArab: return False
#    return True



# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
def dataTipoVera(TS):        # verifica che una stringa sia un tipodataata vera
# riceve una stringa che può essere None (NULL), '', 'normale','niente prima','primaniente',
# ... 'niente dopo','dopo niente', 'niente prima e dopo','prima e dopo niente'
# NULL è considerato un valore valido per il campo. Controlli successivi valuteranno se è un valore coerente
# ... anzi, si fa di tutto perchè None NON arrivi qui, ma sia già diventato ''
# I blank non contano: è corretto 'prima e dopo   ni ente' !!
# restituisce True se TS è null o appartiene all'insieme; else False
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
# ------------------------------------------------------------------------------------
def dataConverti (DS):     			# Converti stringa in datante-data_posteost standard
# riceve in ingresso una stringa (1300, XII, 8001225, XI inizio, ...)
# la stringa può essere:
# a) un qualsiasi numero in formato stringa ('1321' '29071946'  '25120')
# b) un numero romano: I,II,III,IV o IIII,V,VI,VII,VIII,IX,X,XI, XII, XIII, XIV, XV, XVI, XVII, XVIII, XIX, XX, XXI
# c) una stringa formata da (b) e seguita da inizio, fine, meta, primameta, seconda    meta 
# In questa versione la risoluzione è l'anno e manca 'a.C.'
# RESTITUISCE UNA LISTA       MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# Restituisce [data1, data2] relativi alla data DS
# Se data ignota, restituisce [9999,9999]
# Prima controlla se DataValida e se non valida restituisce [-1,-1]
# Se le due date sono uguali era un singolo anno; se diverse era un periodo romano
# Restituisce due valori (annoA,annoP)  -  Se sono 9999,9999 l'anno è sconosciuto
# NULL e stringa lunga 0 è considerato un valore che indica Data sconosciuta.
# ... anzi, si fa di tutto perchè None NON arrivi qui, ma sia già diventato ''
    if not dataVera(DS): return (-1,-1)     
    if DS is None: return[9999,9999]            # 9999 indica Data Sconosciuta <<<<<<!=>>>>>>
    if len(DS)==0: return[9999,9999]		# MI SEMBRA CHE DOVREBBE ESSERE TRUE - Perchè ??????????????????
    sin = DS.replace(' ','')                    # Elimina tutti i blank                         	                      
    if sin.isdigit():				# se ci sono solo numeri ...
        if len(sin)<=4: return [int(sin),int(sin)]  # numero di <= 4 cifre: è solo anno
        else: return [int(sin[:-4]),int(sin[:-4])]  # cifre dalla quintultima in su
   				
    RomToArab1 = ['I',1,'II',2,'III',3,'IIII',4,'IV',4,'V',5,'VI',6,'VII',7,'VIII',8,'IX',9,'VIIII',9,'X',10]
    RomToArab2 = ['XI',11,'XII',12,'XIII',13,'XIIII',14,'XIV',14,'XV',15,'XVI',16,'XVII',17,'XVIII',18,'XVIIII',19,'XIX',19,'XX',20,'XXI',21]
    RomToArab = RomToArab1 + RomToArab2
    RomDett = ['inizio','fine','metà','primametà','secondametà']

    sispart=''                                  # inizializzazione
    sinsec=sin                                  # cerca il secolo. forse è solo ...
    for dett in RomDett:                        # ... a meno che ...
        i=sin.lower().find(dett)                # ... nella stringa ci sia inizio, fine o altro ...
        if i >=0:                               # Se c'è "inizio" o altro ...
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
# ------------------------------------------------------------------------------------
def ternaVera(data, data_poste, DataTipo):	# CONTROLLO dei tre valori di Data3
# riceve una Data3 formata da data, data_poste, DataTipo.
# Prima controlla che i valori siano "validi" come valori isolati
# Restituisce True, se la terna ha coerenza tra i 3 valori; altrimenti False
# NULL è un valore valido che, nei calcoli, è trattato come '', ma nel DB resta NULL ...
# ... anzi, si fa di tutto perchè None NON arrivi qui, ma sia già diventato ''
# ATTENZIONE: datavera è TRUE se il campo DATA è vuoto, cioè 9999 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if not dataVera(data) or not dataVera(data_poste) or not dataTipoVera(DataTipo): return False
    data2=dataConverti(data)          # data2 è una lista [Data1, Data2]
    data_poste2=dataConverti(data_poste)
    if DataTipo is None: DataTipo=''

    if data2[0]==9999:
        if data_poste2[0]==9999 and DataTipo=='':
            return True                # Data sconosciuta
        else: return False             # Data errata (data sconosciuta e valori sul resto)
    if data_poste2[1]<data2[0]: return False
    else: return True
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
def ternaConverti(data, data_poste, DataTipo):
# riceve una Data3 formata da data, data_poste, DataTipo.
# Prima controlla la validità totale con 'ternaVera'
# Restituisce anno1 e anno2 come estremi dell'intervallo (anche uguali)
# None è un valore valido che, nei calcoli, è trattato come '', ma nel DB resta None ...
# ... anzi, si fa di tutto perchè None NON arrivi qui, ma sia già diventato ''
# Restituisce 9999,9999 se il dato è ignoto o -1,-1 se trova un errore
# C'è RIDONDANZA nei controlli - BENE
    if not ternaVera(data, data_poste, DataTipo): return -1,-1,DataTipo
    data2=dataConverti(data)
    data_poste2=dataConverti(data_poste)
    if DataTipo is None: DataTipo=''
    
    if data2[0]==9999:                     # Se primo valore sconosciuto ...
        return 9999,9999,DataTipo           # ...  Data mancante (9999,9999
    elif data_poste2[0]==9999:                   # Se primo valore OK e secondo mancante ...
        return data2[0],data2[1], DataTipo    # ... vale solo il primo (1200-1200) oppure XI (1001-1100)
    return data2[0],data_poste2[1],DataTipo     # Se tutti noti, vale l'intervallo (anche X-XII come 901-1200)   
# ------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
def PRR20KmpKmf (lista,DicF,bene,annocorrente,intersigni):

# Riceve una [lista] di recordFunzioni, tutti relativi allo stesso Bene, ...
# ... con record  [ID,data,data_poste,tipodata,RuoloID,Funz,IDR,RuoloIDR]               -----
# Tutti i record hanno una data valida. Il bene può essere in ID o in IDR
# Esiste almeno un record, ma non è detto che abbia il ruolo 
# Se l'ultimo record della lista ha Data=annocorrente significa "bene esistente"
#
# 1 - Costruisce [listaB"] dove ogni elemento è [bene, anno, Ruolo, codice]      -----
#   ... cioè in "anno" ho questo "Ruolo" con codice 99(data esatte), 90(estremi ... --
#   ... di un periodo, e.g "XII"), 98(se esistenza attuale". 98 è un indicatore
#
# 2 - ListaB viene ordinata per Anno, si eliminano i doppioni
#   Ci possono essere più record con stesso bene, anno, codice, MA RUOLO DIVERSO
#   Questa ListaB sarà usata per i calcoli sui Ruoli. 
#
# 3 - Inizio analisi Prob. di PRESENZA. Costruisco ListaBP e quindi...
#   ... costruisce la lista [funz] fatta di record [x1,v1,x2,v2,k,m] dove ...
#   ... x1 e x2 sono estremi di un periodo (in anni).
#   La Prob. di Presenza all'anno "x" è PP(x) = k*x+m   per x1<=x<=x2
#   Il numero minimo di elementi di [funz] è 2
#




# intersigni = intervallo significativo: intero, anni
#
# 9 - Restituisce [GrafPP, GrafRuolo, retcode, listalog]                         -----
#   GrafPP è una lista di [annoda, PPda, annoa, PPa,k, m]...
#   ...La Probabilità di Presenza in anno (annoda<=anno<=annoa) è "k*anno+m"
#   GrafRuolo è una lista di [x1,PRPx1,x2,PRPx2,k,m,RuoloPrinc,RuoloSecond] ...  -----
#   ... dove PRPx1 è la Probabilità che il ruolo sia RuoloPrincipale in x1;
#   ... 99-PRPx1 è la Probabilità che il ruolo sia RuoloSecondario (anche "ignoto"
#
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
# --- Verifica che la lista ricevuta non sia vuota

    log=[]; retcode=0
    if len(lista)==0:
        log.append('\nXXX Costruzione KmpKmf  ha ricevuto una lista vuota'); retcode=31
        return [],[], retcode, log
#
# ------------------------------------------------------------------------------------
# --- Trasforma la lista ricevuta [ID,data,data_poste,tipodata,RuoloID,Funz,IDR,RuoloIDR] ---
# --- ... in listaB [Bene, Anno, Ruolo, Codice]. Anno è int
# --- ListaB contiene almeno un record, però potrebbe essere con ruolo = ''
# --- ListaB viene ordinata per Anno

    listaB=[]
    for listaj in lista:
        beneID=listaj[DicF['id_bene']]; beneIDR=listaj[DicF['id_bener']]
        ruolo=listaj[DicF['ruolo']]; ruoloIDR=listaj[DicF['ruolor']]
        dant,dpost,dtip=ternaConverti(listaj[DicF['data_ante']],listaj[DicF['data_poste']],listaj[DicF['tipodata']])
        if dant==annocorrente: codice=98        # Viene da ESISTENZA - non c'è ruolo
        else: codice=99
        if bene==beneIDR:               	# ruolo di IDR
            ruolo=ruoloIDR
            if ruolo is None: ruolo = ''
        if dant==dpost: listaB.append([bene,dant,ruolo,codice])	# record con anno esatto o annocorrente
        else: 	
            codice=90 						# è un record con periodo ...
            listaB.append ([bene,dant,ruolo,codice])		# e le date sono DUE
            listaB.append ([bene,dpost,ruolo,codice])
#    print ('\nPRR20KmpKmf/1 - Stampo listaB non ordinata e con possibili doppioni')    
#    for j in listaB:                           # DEBUG
#        print (j)                              # DEBUG
    listaB.sort(key=key1)		        # Ordina la lista su anno
#
# ------------------------------------------------------------------------------------
# --- Elimina i doppioni da ListaB [Bene, Anno, Ruolo, Codice]
# --- Questo servirà sia per Presenza che per Ruolo

    i1=0                                    # listaB  [bene, anno, Ruolo, codice(90,98,99)]
    while i1<=len(listaB)-2:		    # dal primo al penultimo
        i2=i1+1                             # se la listaB è lunga 1, non fa nulla
        if listaB[i1][1]==listaB[i2][1] and listaB[i1][2]==listaB[i2][2]:
        # Se hanno lo stesso anno e lo stesso ruolo. scegli quello con codice maggiore
        # SE hanno RUOLO diverso LASCIA TUTTO: SONO "RUOLI CONTEMPORANEI"
            listaB[i1][3] = max(listaB[i1][3],listaB[i2][3]) 	
            del listaB[i2]
            i1=i1-1
            if i1<0: i1=0
        else: i1=i1+1
    #print ('\n\nPRR20KmpKmf/2 - Stampo listaB (Lista di base) ordinata e senza doppioni')
    #for j in listaB:                       # DEBUG
    #    print (j)                          # DEBUG
    log.append('\nSono in "PRR20KmpKmf" - Lista dei '+str(len(listaB))+' record utili + codice')

# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
#   Inizio trattamento per PRESENZA
#   Ho listaB  [bene, anno, Ruolo, codice(90,98,99)] e ci possono essere ...
#   ... più record alla stessa data, perchè ruoli diversi contemporanei sono ammessi
#   Prima di fare grafico di Presenza, quindi COSTRUiSCO "listaBP" senza doppioni 
#   Qui il Ruolo non serve a nulla ma il modello dati è lo stesso di listaB

    listaBP=[]
    for i in listaB: listaBP.append(i)
    i1=0                                    # listaB  [bene, anno, Ruolo, codice(90,98,99)]
    while i1<=len(listaBP)-2:		    # dal primo al penultimo
        i2=i1+1                             # se la listaB è lunga 1, non fa nulla
        if listaBP[i1][1]==listaBP[i2][1]:
            listaBP[i1][2]=max(listaBP[i1][2],listaBP[i2][2])
            del listaBP[i2]
            i1=i1-1
            if i1<0: i1=0
        else: i1=i1+1
#
# ------------------------------------------------------------------------------------
#   COSTRUZIONE valori base per grafici di PRESENZA
#   Si costruisce una lista [funz] fatta di record [x1,v1,x2,v2,k,m] dove ...
#   ... x1 e x2 sono estremi di un periodo (in anni).
#   La Prob. di Presenza all'anno "x" è PP(x) = k*x+m   per x1<=x<=x2
#
    funz=[]                         
    ind=0
    while ind<len(listaB):
        # è il primo e faccio la coda di sinistra. Tagliare a sinistra a Anno 0
        if ind==0:                              
            x1=0; y1=5; x2=listaBP[ind][1]-3*intersigni; y2=5
            if x2>x1:
                x1,x2,k,m=matkm(x1,y1,x2,y2)
                funz.append([x1,y1,x2,y2,k,m])
            x1=listaBP[ind][1]-3*intersigni
            if x1<0: x1=0
            y1=5; x2=listaBP[ind][1]-intersigni; y2=50
            if x2>x1:
                x1,x2,k,m=matkm(x1,y1,x2,y2)
                funz.append([x1,y1,x2,y2,k,m])

            x1=listaBP[ind][1]-intersigni
            if x1<0: x1=0
            y1=50; x2=listaBP[ind][1]; y2=listaBP[ind][3]
            x1,x2,k,m=matkm(x1,y1,x2,y2); funz.append([x1,y1,x2,y2,k,m])	
        # ----------------------------  # è l'ultimo e faccio la coda di destra
        if ind==len(listaBP)-1 and listaBP[ind][3]!=98:             	
        # è l'ultimo e faccio la coda di destra (ma se è 98 sono all'anno corrente ...
        # ...e non devo fare nulla). Quando la cosa raggiunge annocorrente devo troncare
        # Metto IF e NON "elif": il primo può essere anche l'ultimo !!!
            x1=listaBP[ind][1]; y1=listaBP[ind][3]; x2=listaBP[ind][1]+intersigni; y2=70 
            x1,x2,k,m=matkm(x1,y1,x2,y2)
            if x2>annocorrente:                 # ricalcola valore in x2
                x2n=annocorrente; y2n=annocorrente*k+m; funz.append([x1,y1,x2n,y2n,k,m]) 
            else:
                funz.append([x1,y1,x2,y2,k,m])
                x1=listaBP[ind][1]+intersigni; y1=70; x2=listaBP[ind][1]+3*intersigni;y2=30
                x1,x2,k,m = matkm(x1,y1,x2,y2)
                if x2>annocorrente:              # ricalcola valore in x2 
                    x2n=annocorrente; y2n=annocorrente*k+m; funz.append([x1,y1,x2n,y2n,k,m]) 
                else:
                    funz.append([x1,y1,x2,y2,k,m])
                    x1=listaBP[ind][1]+3*intersigni; y1=30; x2=annocorrente; y2=30
                    x1,x2,k,m=matkm(x1,y1,x2,y2); funz.append([x1,y1,x2,y2,k,m])
        # ----------------------------  # è un intermedio e devo fare il raccordo
        if ind<len(listaBP)-1:			
            x1=listaBP[ind][1]; y1=listaBP[ind][3]; x2=listaBP[ind+1][1]; y2=listaBP[ind+1][3]  
            x1,x2,k,m=matkm(x1,y1,x2,y2); funz.append([x1,y1,x2,y2,k,m])
        # ----------------------------  # Continua il loop
        ind=ind+1
    #print ('\nSono in PRR20KmpKmf/3 - Fatte funzioni per presenza') 
    #for rec in funz: print (rec)        # DEBUG - Old=print(mgb.wrirec(rec))
    log.append('Sono in PRR20KmpKmf - Fatte funzioni per presenza')#

# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
#   Inizio trattamento per RUOLO
#   Da listaB  [bene, anno, Ruolo, codice(90,98,99)] costruisco listaBF ...
#   ... con lo stesso modello dati, ma con valore di ruolo utilizzabile
#   Seleziona solo i record da cui posso estrarre un ruolo valido
#   Se non ne resta nessuno, creo un ruolo fittizio di "ignoto" e ...
#   creo la lista delle funzioni con solo ruolo ignoto a 99

    listaBF=[]
    for i in range(len(listaB)):
        record = listaB[i]
        if record[3]!=98 and record[2]!='' : listaBF.append(record)	# ATTENZIONE il 98 è critico
        # in listaBF ci sono solo record da cui è ricavabile il ruolo
 
    if len(listaBF)==0:         # ATTENZIONE - I record potrebbero essere ZERO !!!!
        log.append('Sono in PRR20KmpKmf - Non ci sono funzioni per calcolare grafico di ruolo ...')
        log.append('... Creo un record fittizio con "ignoto"')
#        print('Sono in PRR20KmpKmf - Non ci sono funzioni per calcolare grafico di ruolo')
        listaBF.append([bene,annocorrente,'ignoto',88]) # CODICE 88 mi serve per il riconoscimento
#
#   in listaBF ci sono n(>0) record di cui almeno 1 ha un valore per ruolo
    #print ('\nStampo listaBF  con valore valido per RUOLO')    # DEBUG
    #for j in listaBF:  print (j)                                        # DEBUG

    funzF=[]
    if len(listaBF)==1 and listaBF[0][3]==88:   # Questo è IGNOTO SEMPRE
        funzF.append([0,99,1000,99,0,99,'ignoto','ignoto'])
        funzF.append([1000,99,2000,99,0,99,'ignoto','ignoto'])
        funzF.append([2000,99,annocorrente,99,0,99,'ignoto','ignoto'])
        log.append('???? Nessun record funzione ha un ruolo valido - Simulato ruolo "ignoto"')
        return funz,funzF,0,log
#   Escluso il caso artificioso di record SENZA MAI UN RUOLO, ...
#   ... in listaBF ci sono n(>0) record di cui almeno 1 ha un valore per ruolo
#
# ------------------------------------------------------------------------------------
#   Da listaBF creo una lista simile listaBF2 con ruolo = lista di ruoli ...
#   ... e ci metto più ruoli se si riferiscono allo stesso anno

    listaBF2=[]
    for rec in listaBF:                         # Creata nuova lista dove RUOLO è una lista
        ltemp=[]; ltemp.append(rec[2])          # [bene, anno, Ruolo, codice(90,98,99)]
        listaBF2.append([rec[0],rec[1],ltemp,rec[3]])
#
    #print('\nH creato listaBF2 dove ruolo sta in una lista')    # DEBUG
    #for rec in listaBF2: print(rec)                             # DEBUG
#
#   Compatto listaBF2: tutti i ruoli di uno stesso anno in un unico record
    ind=0;   
    while ind<len(listaBF2)-1 and len(listaBF2)>=2:   # per i record dal primo(0) al penultimo (len(listaBF)-1)
        r1=listaBF2[ind]; r2=listaBF2[ind+1]    # [bene, anno, Ruolo, codice(90,98,99)]      
        if r1[1]!=r2[1]:                        # caso 1: anni diversi (NOP)
            ind=ind+1
        elif r1[2]==r2[2]:                      # caso 2: stesso anno, stesso ruolo (codice max + elimina)
            listaBF2[ind][3]=max(r1[3],r2[3])
            del listaBF1[ind+1]
            # ind resta lo stesso !!
        else:                                   # caso 3: stesso anno, ruolo diverso (aggiungi ruolo, codice max + elimina)
            listaBF2[ind][2].append(listaBF2[ind+1][2][0])
            listaBF2[ind][3]=max(r1[3],r2[3])
            del listaBF2[ind+1]
            # ind resta lo  stesso !!
#
    for rec in listaBF2: rec[2].sort()            # ordina i ruoli alfabeticamente
            
#
    #print('\nHo creato listaBF2 dove diversi ruoli compattati e ordinati')  # DEBUG
    #for rec in listaBF2: print(rec)                             # DEBUG
#   Da qui creo funzF con tanti record [x1,PRuoloPrinc,x2,PRuoloSecond,k,m,RuoloPrinc,RuoloSecond]			
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
#   COSTRUZIONE valori base per grafici di RUOLO 
#   Si costruisce una lista [funz] fatta di record [x1,v1,x2,v2,k,m] dove ...
#   ... x1 e x2 sono estremi di un periodo (in anni).
#   La Prob. di Presenza all'anno "x" è PP(x) = k*x+m   per x1<=x<=x2
# ------------------------------------------------------------------------------------

    ind=0    
    while ind<len(listaBF2):			# stiamo trattando un unico bene. Non serve idBene
#        deb='Entro nel WHILE con indice '+str(ind)+' su '+str(len(listaBF2))   	DEBUG
#        print deb								DEBUG

        if ind==0:
# è il primo e faccio la coda di sinistra -------------------------------------------------------------
            RP= listaBF2[ind][2]; RS=['ignoto']      # SONO LISTE         
            x1=0; y1=30; x2=listaBF2[ind][1]-3*intersigni; y2=30 
            x1,x2,k,m=matkm(x1,y1,x2,y2); funzF.append([x1,y1,x2,y2,k,m,RP,RS])
            
            x1=listaBF2[ind][1]-3*intersigni; y1=30; x2=listaBF2[ind][1]-intersigni; y2=60 
            x1,x2,k,m=matkm(x1,y1,x2,y2); funzF.append([x1,y1,x2,y2,k,m,RP,RS])
            
            x1=listaBF2[ind][1]-intersigni; y1=60; x2=listaBF2[ind][1]; y2=listaBF2[ind][3]
            x1,x2,k,m=matkm(x1,y1,x2,y2); funzF.append([x1,y1,x2,y2,k,m,RP,RS])	

        if ind==len(listaBF2)-1:		# NON "elif": il primo può essere anche l'ultimo. Il 98 NON esiste
# è l'ultimo e faccio la coda di destra e se raggiungo annocorrente devo troncare
            RP= listaBF2[ind][2]; RS=['ignoto']      # SONO LISTE       
            x1=listaBF2[ind][1]; y1=listaBF2[ind][3]; x2=listaBF2[ind][1]+intersigni; y2=80 
            x1,x2,k,m=matkm(x1,y1,x2,y2)
            if x2>annocorrente: 
                x2n=annocorrente; y2n=annocorrente*k+m; funzF.append([x1,y1,x2n,y2n,k,m,RP,RS]) # ricalcola valore in x2
            else:
                funzF.append([x1,y1,x2,y2,k,m,RP,RS])
                x1=listaBF2[ind][1]+intersigni; y1=80; x2=annocorrente;y2=80
                x1,x2,k,m = matkm(x1,y1,x2,y2)
                funzF.append([x1,y1,x2,y2,k,m,RP,RS])

        if ind<len(listaBF2)-1:			# se true, ce n'è almeno un altro dopo
# sono in mezzo tra due
            RP= listaBF2[ind][2]; RS=listaBF2[ind+1][2]	# RP è quello ante; RS si fa con il RP di post
            x1=listaBF2[ind][1]; y1=listaBF2[ind][3]; x2=listaBF2[ind+1][1];  y2=listaBF2[ind+1][3]
# ..... se sono UGUALI li collego brutalmente  -----------------------------------------
            if RP == RS:                        # SONO ORDINATI ALFABETICAMENTE
                x1,x2,k,m=matkm(x1,y1,x2,y2); funzF.append([x1,y1,x2,y2,k,m,RP,RP])
# ..... se sono DIVERSI probabilità 50% al punto centrale  -----------------------------------------
            else:
                xm=(x2+x1)/2; ym=50
                x1,xm,k,m=matkm(x1,y1,xm,ym); funzF.append([x1,y1,xm,ym,k,m,RP,RS])
                xm,x2,k,m=matkm(xm,ym,x2,y2); funzF.append([xm,ym,x2,y2,k,m,RS,RP])
        ind=ind+1

    return funz,funzF,retcode,log

# Fine -------------------------------------------------------------------------
# Fine -------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ---------    matkm calcola i parametri di una funzione di grado 1   ----------
# ---  Riceve due punti (x1,y1 e x2,y2 e restituisce k,m tali che y = kx+m  ----
# --  x1,x2,k,m = matkm(x1,y1,x2,y2)   (restituisce anche x1 e x2 che sono ...--
# --  l'intervallo in cui la funzione è utilizzabile  --------------------------
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
# ------------------------------------------------------------------------------
# ----    matValPuntoDaFunzConVal calcola il valore di una funzione al punto x  ------
# ---  Riceve una lista di tipo "listakm" e un valore x (intero o float) e ..---
# ---  .. restituisce il valore FLOAT della funzione in x                    ---
# ------------------------------------------------------------------------------
def matValPuntoDaFunzConVal(listakmv,x):
#   listaKMV:  [x1,y1,x2,y2,k,m,'Ruolo1','Ruolo2']
    xf=float(x)
    for rec in listakmv:
        if xf>=rec[0] and xf<=rec[2]:		# òòòòòòòòòòòòòòòòòòòòòòòòòò 
            k=rec[4]; m=rec[5]
            z=xf*k+m
            RP=rec[6]; RS=rec[7]	# z si riferisce a RP. Prob. di RS è 99-RP
            return z,RP,RS
    return -9999
# ------------------------------------------------------------------------------
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
        if punto[0]>x1 and punto[0]<x2:	    #  con > e < l'insieme è aperto
            punti.append([punto[0],punto[1]])
    y=matValPuntoDaFunz(listakm,x2f); punti.append([int(round(x2f)),int(round(y))])	# ultimo punto
# punti[] è l'elenco di tutti i punti [x,y] dove la funzione (fatta da segmenti) cambia direzione

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
# ------------------------------------------------------------------------------
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
        if punto[0]>x1 and punto[0]<x2:		# se sì, l'estremo inferiore sta nell'intervallo
            punti.append([punto[0],punto[1],punto[6],punto[7]])
    PR1,R1,R2 = matValPuntoDaFunzConVal(listaKMF,x2f)
    punti.append([int(round(x2f)),int(round(PR1)),R1,R2])	# calcola ultimo punto
# punti[x,y,RuoloP,RuoloS] è l'elenco di tutti i punti dove la funzione (fatta da segmenti) ...
# ... cambia direzione sia per RuoloP che per RuoloS
# -----------------------------------------------
    #print ('emergency 1')
    #for ip in punti: print (ip)
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

    #print (" Stampa creazione dell'integrale 2")
    #for i in range(len(RuoliL)): print (RuoliV[i], RuoliL[i], RuoliL[i], RuoliP[i])

    funz=[]
    for i in range(len(RuoliV)):
        funz.append([RuoliL[i],RuoliP[i][0],RuoliP[i][1],RuoliV[i]])
    
    funzO=[]
    while len(funz)>0:
        RVmax=-1; ind=-1            # scorri funz e cerca max
        for i in range(len(funz)):
            if funz[i][3]>RVmax:
                ind=i; RVmax=funz[i][3]
        # ind è l'indice dell'elemento con ValoreMedio maggiore
        funzO.append(funz[ind])
        del funz[ind]
    # adesso funzO è ordinata, ma bisogna portare ignoto in fondo
# ATTENZIONE - potrebbero capitare DUE 'ignoto'
    for ind in range(len(funzO)):
        if funzO[ind][0][0]=='ignoto':
            funzO.append(funzO[ind]); del funzO[ind]
            for ind2 in range(len(funzO)-1): # se ci fosse il secondo
                if funzO[ind2][0][0]=='ignoto':
                    funzO.append(funzO[ind2]); del funzO[ind2]
# esempio: [[['pieve'],90,10,46], [['convento', 'pieve'],88,14,24], [['ignoto'],42,2,30]]
    return funzO
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
def key0(el):		# primo elemento
    return el[0]
def key1(el):		# secondo elemento
    return el[1]
def key2(el):		# terzo elemento
    return el[2]
def key3(el):		# quarto elemento
    return el[3]
#lista.sort(key=mgb.key0)
# -------------------------------------------------------------------------------

def getPRRTable(LBen9,LFun9,listaIniz):
    from pathlib import Path
    import sys, os, pickle
    megaLista=[]            # Lista di uscita da scrivere su disco

    for idBene in listaIniz:    # per ciascun Bene calcola le liste ...
        retcode,listaP,listaR=PRRA20 (str(idBene),LBen9,LFun9) # LBen9,LFun9 da ADATTARE
        megaLista.append([idBene,retcode,listaP,listaR]) # ... e le aggiunge a megaLista

    fileDumpNome=str(Path(__file__).parents[1])+'\\DumpPRR20'
    fileDump=open(fileDumpNome,'wb')
    pickle.dump(megaLista,fileDump)
    fileDump.close()