void Ana_MOCADI_v2(char* filename_root, int fp_num = 12,char* filename_output = "_tmp"){
  TH2D *H2_start_h = new TH2D("H2_start_h","H2_start_h",200,-10,10,200,-10,10);
  TH2D *H2_start_v = new TH2D("H2_start_v","H2_start_v",200,-10,10,200,-10,10);

  TH2D *H2_fp_h = new TH2D("H2_fp_h","H2_fp_h",200,-10,10,200,-10,10);
  TH2D *H2_fp_v = new TH2D("H2_fp_v","H2_fp_v",200,-10,10,200,-10,10);

  TH1D *H1_delta = new TH1D("H1_delta","H1_delta",200,-1,1);

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


  float x[16],a[16],y[16],b[16];
  int    N;
  ch->SetBranchAddress("N",&N);
  ch->SetBranchAddress("X", x);
  ch->SetBranchAddress("A", a);
  ch->SetBranchAddress("Y", y);
  ch->SetBranchAddress("B", b);
  
  int nentries = ch->GetEntries();
  int n_lost_dipole_in[3]  = {0,0,0};
  int n_lost_dipole_in_LRUD[3][4];
  int n_lost_dipole_out[3] = {0,0,0};
  int n_lost_dipole_out_LRUD[3][4];
  for(int idipole = 0;idipole < 3;idipole++){
    n_lost_dipole_in[idipole]  = 0;
    n_lost_dipole_out[idipole] = 0;
    for(int iLRUD = 0;iLRUD < 4;iLRUD++){
      n_lost_dipole_in_LRUD[idipole][iLRUD]  = 0;
      n_lost_dipole_out_LRUD[idipole][iLRUD] = 0;
    }
  }
  
  printf("%d entries\n",nentries);
  for(int ientry = 0;ientry < nentries;ientry++){
    ch->GetEntry(ientry);
    for(int idipole = 0;idipole < 3;idipole++){
      if(N==4 + 3*idipole){
	n_lost_dipole_in[idipole]++;
	if(fabs(y[3 + 3*idipole]) < fabs(x[3 + 3*idipole])){
	  if(x[3 + 3*idipole] < 0)n_lost_dipole_in_LRUD[idipole][0]++;
	  else                    n_lost_dipole_in_LRUD[idipole][1]++;
	}
	else{
	  if(y[3 + 3*idipole] > 0)n_lost_dipole_in_LRUD[idipole][2]++;
	  else                    n_lost_dipole_in_LRUD[idipole][3]++;
	}
      }
      if(N==5 + 3*idipole){
	n_lost_dipole_out[idipole]++;
	if(fabs(y[3 + 3*idipole]) < fabs(x[3 + 3*idipole])){
	  if(x[3 + 3*idipole] < 0)n_lost_dipole_out_LRUD[idipole][0]++;
	  else                    n_lost_dipole_out_LRUD[idipole][1]++;
	}
	else{
	  if(y[3 + 3*idipole] > 0)n_lost_dipole_out_LRUD[idipole][2]++;
	  else                    n_lost_dipole_out_LRUD[idipole][3]++;
	}

      }
    }
  }
  
  for(int idipole = 0;idipole < 3;idipole++){
    fprintf(fp,"Dipole#%d  in: ",idipole);
    fprintf(fp,"%5d, %5d, %5d, %5d, %5d\n",
	    n_lost_dipole_in_LRUD[idipole][0],
	    n_lost_dipole_in_LRUD[idipole][1],
	    n_lost_dipole_in_LRUD[idipole][2],
	    n_lost_dipole_in_LRUD[idipole][3],
	    n_lost_dipole_in[idipole]
	    );
    printf("%d, %d, %d, %d, %d\n",
	   n_lost_dipole_in_LRUD[idipole][0],
	   n_lost_dipole_in_LRUD[idipole][1],
	   n_lost_dipole_in_LRUD[idipole][2],
	   n_lost_dipole_in_LRUD[idipole][3],
	   n_lost_dipole_in[idipole]
	   );

    
    fprintf(fp,"Dipole#%d out: ",idipole);
    fprintf(fp,"%5d, %5d, %5d, %5d, %5d\n",
	    n_lost_dipole_out_LRUD[idipole][0],
	    n_lost_dipole_out_LRUD[idipole][1],
	    n_lost_dipole_out_LRUD[idipole][2],
	    n_lost_dipole_out_LRUD[idipole][3],
	    n_lost_dipole_out[idipole]
	    );
    printf("%d, %d, %d, %d, %d\n",
	   n_lost_dipole_out_LRUD[idipole][0],
	   n_lost_dipole_out_LRUD[idipole][1],
	   n_lost_dipole_out_LRUD[idipole][2],
	   n_lost_dipole_out_LRUD[idipole][3],
	   n_lost_dipole_out[idipole]
	   );
    
  }
  
  fprintf(fp,"%lf, %lf, %lf, %lf, %lf,  %lf, %lf, %d, %d\n",
  	  H2_start_h->GetRMS(1),
  	  H2_start_h->GetRMS(2),
  	  H2_start_v->GetRMS(1),
  	  H2_start_v->GetRMS(2),
  	  H1_delta  ->GetRMS(1),
  	  H2_fp_h   ->GetRMS(1),
  	  H2_fp_v   ->GetRMS(1),
	  (int)H2_start_h->GetEntries(),
  	  (int)H2_fp_h->GetEntries()
  	  );
  fclose(fp);
}
