
char element_name[][256]={
			  "e00_fp",   //#0			  
			  "e00",   //#1			  
			  "QTe01a",//#2			  
			  "QTe01b",//#3			  
			  "QTe01c",//#4			  
			  "DMe1",  //#5			  
			  "DSe11", //#6			  
			  "DSe12", //#7			  
			  "QDa",  //#8			  
			  "QDb", //#9			  
			  "Ta"   //#10			  
};
void Ana_mocadi_result(char* filename,int n_fp_end = 11){
  TChain *ch = new TChain("T");
  ch->Add(filename);
  TCanvas *C = new TCanvas("C_Alpha","Alpha",1200,800);

  TH2D *H2_xa_e00     = new TH2D("H2_xa_e00","H2_xa_e00",60,-30,30,60,-30,30);
  TH2D *H2_xa_e00_pass= new TH2D("H2_xa_e00_pass","H2_xa_e00_pass",60,-30,30,60,-30,30);
  TH2D *H2_yb_e00     = new TH2D("H2_yb_e00","H2_yb_e00",60,-30,30,60,-30,30);
  TH2D *H2_yb_e00_pass= new TH2D("H2_yb_e00_pass","H2_yb_e00_pass",60,-30,30,60,-30,30);
  TH2D *H2_xy_e00     = new TH2D("H2_xy_e00","H2_xy_e00",60,-30,30,60,-30,30);
  TH2D *H2_xy_e00_pass= new TH2D("H2_xy_e00_pass","H2_xy_e00_pass",60,-30,30,60,-30,30);
  TH2D *H2_xa_TA      = new TH2D("H2_xa_TA","H2_xa_TA"  ,60,-30,30,60,-30,30);
  TH2D *H2_yb_TA      = new TH2D("H2_yb_TA","H2_yb_TA"  ,60,-30,30,60,-30,30);
  TH2D *H2_xy_TA      = new TH2D("H2_xy_TA","H2_xy_TA"  ,60,-30,30,60,-30,30);
  
  C->Divide(3,2);
  C->cd(1);
  ch->Draw("a[1]:x[1]*10.>>H2_xa_e00","","colz");
  ch->Draw("a[1]:x[1]*10.>>H2_xa_e00_pass",Form("n == %d",n_fp_end),"box");
  H2_xa_e00_pass->SetLineColor(2);
  H2_xa_e00->Draw("colz");
  H2_xa_e00_pass->Draw("same box");
  gPad->SetGrid();
  C->cd(2);
  ch->Draw("b[1]:y[1]*10.>>H2_yb_e00","","colz");
  ch->Draw("b[1]:y[1]*10.>>H2_yb_e00_pass",Form("n == %d",n_fp_end),"box");
  H2_yb_e00_pass->SetLineColor(2);
  H2_yb_e00->Draw("colz");
  H2_yb_e00_pass->Draw("same box");
  gPad->SetGrid();
  C->cd(3);
  ch->Draw("y[1]*10.:x[1]*10.>>H2_xy_e00","","colz");
  ch->Draw("y[1]*10.:x[1]*10.>>H2_xy_e00_pass",Form("n == %d",n_fp_end),"box");
  H2_xy_e00_pass->SetLineColor(2);
  H2_xy_e00->Draw("colz");
  H2_xy_e00_pass->Draw("same box");

  gPad->SetGrid();
  C->cd(4);
  ch->Draw(Form("a[%d]:x[%d]*10.>>H2_xa_TA",n_fp_end-1,n_fp_end-1),"","colz");
  gPad->SetGrid();
  C->cd(5);
  ch->Draw(Form("b[%d]:y[%d]*10.>>H2_yb_TA",n_fp_end-1,n_fp_end-1),"","colz");
  gPad->SetGrid();
  C->cd(6);
  ch->Draw(Form("y[%d]*10:x[%d]*10.>>H2_xy_TA",n_fp_end-1,n_fp_end-1),"","colz");
  gPad->SetGrid();
  TCanvas *C_transmission = new  TCanvas("C_transmisssion","C_transmission",800,600);
  C_transmission->Divide(1,2);
  C_transmission->cd(1);

  //C->cd(7);
  TH1D *H1_transmission = new TH1D("H1_transmission","H1_transmission",n_fp_end+1,0,n_fp_end+1);
  ch->Draw("n >> H1_transmission");
  //gPad->SetLogy();
  int nall = H1_transmission->Integral();
  int loss_local;
  double loss_local_percent = 0;
  double loss_total_percent = 0;
  for(int ifp = 0;ifp < n_fp_end;ifp++){
    loss_local = H1_transmission->GetBinContent(ifp+1);
    loss_local_percent = (double)loss_local / nall * 100.;
    loss_total_percent += loss_local_percent;
    printf("at %s loss %.2lf %% \n",element_name[ifp],loss_local_percent);
  }
  printf("total loss %.2lf %% \n",loss_total_percent);
  //C->cd(8);
  ch->Draw(Form("n==%d",n_fp_end));

  C_transmission->cd(1);
  H2_xa_e00->Draw("colz");
  H2_xa_e00_pass->Draw("same box");
  C_transmission->cd(2);
  H2_yb_e00->Draw("colz");
  H2_yb_e00_pass->Draw("same box");
  
  // double max_count_h = H2_xa_e00->GetMaximum();
  // printf("max_count_h = %lf \n",max_count_h);
  // double contours[4];
  // contours[0] = 3;
  // contours[1] = max_count_h *TMath::Exp(-0.1) ;
  // contours[2] = max_count_h *TMath::Exp(-0.3) ;
  // contours[3] = max_count_h *TMath::Exp(-0.5) ;
  // // contours[4] = max_count_h *TMath::Exp(-2.0) ;
  // // contours[5] = max_count_h *TMath::Exp(-2.5) ;
  // H2_xa_e00->SetContour(4,contours);
  // H2_xa_e00->Draw("cont3");
  
}
