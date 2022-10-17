void Ana_MOCADI(char* filename_root, int fp_num = 9,char* filename_output = "_tmp"){
  TH2D *H2_start_h = new TH2D("H2_start_h","H2_start_h",100,-10,10,100,-10,10);
  TH2D *H2_start_v = new TH2D("H2_start_v","H2_start_v",100,-10,10,100,-10,10);

  TH2D *H2_fp_h = new TH2D("H2_fp_h","H2_fp_h",100,-10,10,100,-10,10);
  TH2D *H2_fp_v = new TH2D("H2_fp_v","H2_fp_v",100,-10,10,100,-10,10);

  TH1D *H1_delta = new TH1D("H1_delta","H1_delta",100,-1,1);

  TChain *ch = new TChain("h1");
  ch->Add(filename_root);

  TCanvas *C_result = new TCanvas("C_result","C_result",1200,800);
  C_result->Divide(2,3);
  C_result->cd(1);
  ch->Draw("A[0]:X[0] * 10 >> H2_start_h","","colz");
  C_result->cd(2);
  ch->Draw("B[0]:Y[0] * 10 >> H2_start_v","","colz");
  C_result->cd(3);
  ch->Draw(Form("A[%d]:X[%d] * 10 >> H2_fp_h",fp_num,fp_num),"","colz");
  C_result->cd(4);
  ch->Draw(Form("B[%d]:Y[%d] * 10 >> H2_fp_v",fp_num,fp_num),"","colz");
  C_result->cd(5);
  ch->Draw(" Brho >>h_brho");
  double mean_brho = ((TH1F*)gROOT->FindObject("h_brho"))->GetMean();
  ch->Draw(Form("(Brho[0] - %lf)/%lf * 100.>> H1_delta",mean_brho,mean_brho));
  C_result->Print(Form("MonteCalro_Result%s.eps",filename_output));
  
  FILE *fp ;
  fp = fopen(Form("MonteCarlo_Result%s.txt",filename_output), "w");
  //          x_s  a_s  y_s  b_s delta x_f,  y_f transmission
  fprintf(fp,"%lf, %lf, %lf, %lf, %lf,  %lf, %lf, %lf \n",
	  H2_start_h->GetRMS(1),
	  H2_start_h->GetRMS(2),
	  H2_start_v->GetRMS(1),
	  H2_start_v->GetRMS(2),
	  H1_delta  ->GetRMS(1),
	  H2_fp_h   ->GetRMS(1),
	  H2_fp_v   ->GetRMS(1),
	  H2_fp_h->GetEntries()/H2_start_h->GetEntries()
	  );
  fclose(fp);
}
