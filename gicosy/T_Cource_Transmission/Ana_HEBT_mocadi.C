void Ana_HEBT_mocadi(char* filename){

  int n_PF[]={1,7,9};
  char* name_PF[]={"e00","e11","e12"};
  TChain *ch = new TChain("T");
  ch->Add(filename);
  TH1D *H1_brho = new TH1D("H1_brho","H1_brho",120,1.382,1.388);
  ch->Draw("brho[0]>>H1_brho");
  double brho_beam = H1_brho->GetMean();

  ch->SetAlias("delta",Form("(brho[0] - %lf)/%lf*100.",brho_beam,brho_beam));
  TH1D *H1_delta = new TH1D("H1_delta","H1_delta",100,-1.0,1.0);
  ch->Draw("delta>>H1_delta");
  double sigma_delta = H1_delta->GetRMS();
  
  TCanvas *C_HEBT_h = new TCanvas("C_HEBT_h","C_HEBT_h",1200,800);
  TCanvas *C_HEBT_v = new TCanvas("C_HEBT_v","C_HEBT_v",800,800);
  
  C_HEBT_h->Divide(3,3);
  C_HEBT_v->Divide(2,3);
  for(int iPF = 0;iPF < 3;iPF++){
    C_HEBT_h->cd(3 * iPF + 1);
    ch->Draw(Form("x[%d]*10.>>hx_PF%s(240,-30,30)",n_PF[iPF],name_PF[iPF]));
    C_HEBT_h->cd(3 * iPF + 2);
    ch->Draw(Form("a[%d]:x[%d]*10.>>hxa_PF%s(240,-30,30,240,-30,30)",n_PF[iPF],n_PF[iPF],name_PF[iPF]),"","colz");
    C_HEBT_h->cd(3 * iPF + 3);
    ch->Draw(Form("x[%d]*10.:delta>>hdx_PF%s(240,-1.0,1.0,240,-30,30)",n_PF[iPF],name_PF[iPF]),"","colz");
    ((TH2D*)gROOT->FindObject(Form("hdx_PF%s",name_PF[iPF])))->ProfileX();
    ((TProfile*)gROOT->FindObject(Form("hdx_PF%s_pfx",name_PF[iPF])))->Fit("pol1","","",-1.0 * sigma_delta, sigma_delta);    
    gStyle->SetOptFit();
    ((TH2D*)gROOT->FindObject(Form("hdx_PF%s",name_PF[iPF])))->Draw("colz");
    ((TProfile*)gROOT->FindObject(Form("hdx_PF%s_pfx",name_PF[iPF])))->Draw("same");

    C_HEBT_v->cd(2 * iPF + 1);
    ch->Draw(Form("y[%d]*10.>>hy_PF%s(240,-30,30)",n_PF[iPF],name_PF[iPF]));
    C_HEBT_v->cd(2 * iPF + 2);
    ch->Draw(Form("b[%d]:y[%d]*10.>>hyb_PF%s(240,-30,30,240,-30,30)",n_PF[iPF],n_PF[iPF],name_PF[iPF]),"","colz");
    
  }

  TCanvas *C_HEBT_G3T = new TCanvas("C_HEBT_G3T","C_HEBT_G3T",800,800);
  C_HEBT_G3T->Divide(2,2);
  C_HEBT_G3T->cd(1);
  ch->Draw("y[12]*10.:x[12]*10.>>hxy_G3T(100,-10,10,100,-10,10)","","colz");
  C_HEBT_G3T->cd(2);
  ch->Draw("a[12]    :x[12]*10.>>hxa_G3T(100,-10,10,100,-10,10)","","colz");  
  C_HEBT_G3T->cd(3);
  ch->Draw("b[12]    :y[12]*10.>>hyb_G3T(100,-10,10,100,-10,10)","","colz");
  C_HEBT_G3T->cd(4);
  ch->Draw("x[12]*10.:delta    >>hdx_G3T(100,-1.0,1.0,100,-10,10)","","colz");
}
