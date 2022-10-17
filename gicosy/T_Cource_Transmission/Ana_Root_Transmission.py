from ROOT import TFile, TTree, TChain, TH1I, TCanvas

element_name = [
    "e00",   ##0			  
    "QTe01a",##1			  
    "QTe01b",##2			  
    "QTe01c",##3			  
    "DMe1",  ##4			  
    "DSe11", ##5			  
    "DSe12", ##6			  
    "DMe2",  ##7			  
    "DSe21", ##8			  
    "DSe22", ##9			  
    "DMy1",  ##10			  
    "QDya",  ##11		  
    "QDyb",  ##12		  
    "DMy2",  ##13		  
    "TA"  ,  ##14
    "pass"   ##15
]

element_name_GARIS = [
    "e00_fp",##0			  
    "e00",   ##1			  
    "QTe01a",##2			  
    "QTe01b",##3			  
    "QTe01c",##4			  
    "DMe1",  ##5			  
    "DSe11", ##6
    "PFe11", ##7			  
    "DSe11", ##8
    "PFe12", ##9			  
    "QDa",   ##10			  
    "QDb",   ##11			  
    "TA",    ##12
    "pass"   ##13
]


def Ana_transmission(filename_root,nelement, ratio_loss_last = 0.1):
    chain = TChain("T")
    chain.Add(filename_root)
    hist_transmission = TH1I("hist_transmission","hist_transmission",nelement+1,0,nelement+1)
    nentries = chain.GetEntries()
    for jentry in range(nentries):
        chain.GetEntry(jentry)
        hist_transmission.Fill(chain.n)
    nall = hist_transmission.Integral()
    print("nall = %d"%nall)
    loss_local=[]
    for ibin in range(nelement):
        loss_local.append(hist_transmission.GetBinContent(ibin+1)/nall*100.)
        print("loss at %s: %.1lf"%(element_name[ibin],loss_local[-1]))
    loss_local.append(hist_transmission.GetBinContent(nelement+1)/nall*100.)
    print("%s: %.1lf"%(element_name[nelement],loss_local[-1]))
        
    print("loss all = %.1lf"%(100 - loss_local[-1]))
    eval_func=sum(loss_local[:nelement - 1]) + loss_local[nelement -1] * ratio_loss_last
    #print("eval_func = %.1lf"%eval_func)

    return eval_func

def Ana_transmission_all(filename_root,nelement):
    chain = TChain("T")
    chain.Add(filename_root)
    hist_transmission = TH1I("hist_transmission","hist_transmission",nelement+1,0,nelement+1)
    nentries = chain.GetEntries()
    for jentry in range(nentries):
        chain.GetEntry(jentry)
        hist_transmission.Fill(chain.n)
    nall = hist_transmission.Integral()
    print("nall = %d"%nall)
    loss_local=[]
    for ibin in range(nelement):
        loss_local.append(hist_transmission.GetBinContent(ibin+1)/nall*100.)
        print("loss at %s: %.1lf"%(element_name[ibin],loss_local[-1]))
    loss_local.append(hist_transmission.GetBinContent(nelement+1)/nall*100.)
    print("%s: %.1lf"%(element_name[nelement],loss_local[-1]))
        
    return loss_local

def Ana_transmission_inverse(filename_root,nelement):
    chain = TChain("T")
    chain.Add(filename_root)
    hist_transmission = TH1I("hist_transmission","hist_transmission",nelement+1,0,nelement+1)
    nentries = chain.GetEntries()
    for jentry in range(nentries):
        chain.GetEntry(jentry)
        hist_transmission.Fill(chain.n)
    nall = hist_transmission.Integral()
    print("nall = %d"%nall)
    loss_local=[]
    for ibin in range(nelement):
        loss_local.append(hist_transmission.GetBinContent(ibin+1)/nall*100.)
        print("loss at %s: %.1lf"%(element_name[ibin],loss_local[-1]))
    loss_local.append(hist_transmission.GetBinContent(nelement+1)/nall*100.)
    print("%s: %.1lf"%(element_name[nelement],loss_local[-1]))
        
    print("loss all = %.1lf"%(100 - loss_local[-1]))
    eval_func=100 - loss_local[-1]
    print("eval_func = %.1lf"%eval_func)

    return eval_func

def Ana_transmission_GARIS3(filename_root,nelement):
    chain = TChain("T")
    chain.Add(filename_root)
    hist_transmission = TH1I("hist_transmission","hist_transmission",nelement+1,0,nelement+1)
    nentries = chain.GetEntries()
    for jentry in range(nentries):
        chain.GetEntry(jentry)
        hist_transmission.Fill(chain.n)
    nall = hist_transmission.Integral()
    print("nall = %d"%nall)
    loss_local=[]
    for ibin in range(nelement):
        loss_local.append(hist_transmission.GetBinContent(ibin+1)/nall*100.)
        print("loss at %s: %.1lf"%(element_name_GARIS[ibin],loss_local[-1]))
    loss_local.append(hist_transmission.GetBinContent(nelement+1)/nall*100.)
    print("%s: %.1lf"%(element_name_GARIS[nelement],loss_local[-1]))
        
    print("loss all = %.1lf"%(100 - loss_local[-1]))
    eval_func=sum(loss_local[:nelement])
    print("eval_func = %.1lf"%eval_func)

    return eval_func
