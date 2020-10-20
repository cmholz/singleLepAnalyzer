void plotSignalEff(){

  gStyle->SetOptStat(0);

  TH1D *h2016 = new TH1D("h2016",";T quark mass [GeV];Signal efficiency",11,750,1850);
  TH1D *h2017 = new TH1D("h2017","",11,750,1850);
  TH1D *h2018 = new TH1D("h2018","",11,750,1850);

  h2016->SetBinContent(2,0.055); //0.061);
  h2016->SetBinContent(3,0.069);//0.061);
  h2016->SetBinContent(4,0.081);//0.062);
  h2016->SetBinContent(5,0.090);//0.062);
  h2016->SetBinContent(6,0.097);//0.063);
  h2016->SetBinContent(7,0.102);//0.062);
  h2016->SetBinContent(8,0.108);//0.063);
  h2016->SetBinContent(9,0.112);//0.063);
  h2016->SetBinContent(10,0.117);//0.064);
  h2016->SetBinContent(11,0.119);//0.064);

  h2017->SetBinContent(3,0.071);//0.052);
  h2017->SetBinContent(4,0.082);//0.052);
  h2017->SetBinContent(5,0.091);//0.053);
  h2017->SetBinContent(6,0.099);//0.052);
  h2017->SetBinContent(7,0.105);//0.053);
  h2017->SetBinContent(8,0.110);//0.053);
  h2017->SetBinContent(9,0.116);//0.053);
  h2017->SetBinContent(10,0.123);//0.053);
  h2017->SetBinContent(11,0.126);//0.052);

  h2018->SetBinContent(4,0.085);//0.027);
  h2018->SetBinContent(5,0.094);//0.034);
  h2018->SetBinContent(6,0.102);//0.039);
  h2018->SetBinContent(7,0.106);//0.041);
  h2018->SetBinContent(8,0.116);//0.043); 
  h2018->SetBinContent(9,0.123);//0.044);
  h2018->SetBinContent(10,0.124);//0.045);
  h2018->SetBinContent(11,0.126);//0.046);

  TPaveText *pt = new TPaveText(0.085,0.90,0.72,0.97,"blNDC");
  pt->SetBorderSize(0);
  pt->SetFillColor(0);
  pt->SetFillStyle(0);
  pt->SetTextFont(42);

  TCanvas *c1 = new TCanvas("c1","c1",800,600);
  h2016->GetYaxis()->SetRangeUser(0,0.25);
  h2016->GetYaxis()->SetTitleOffset(1.2);
  h2016->SetLineWidth(2);
  h2016->SetMarkerStyle(20);
  h2016->SetLineColor(1);
  h2016->SetMarkerColor(1);
  h2017->SetLineWidth(2);
  h2017->SetMarkerStyle(21);
  h2017->SetLineColor(2);
  h2017->SetMarkerColor(2);
  h2018->SetLineWidth(2);
  h2018->SetMarkerStyle(22);
  h2018->SetLineColor(7);
  h2018->SetMarkerColor(7);
  
  h2016->Draw("LP");
  h2017->Draw("LP same");
  h2018->Draw("LP same");

  pt->AddText("CMS Simulation Preliminary, (13TeV)");
  pt->Draw();

  TLegend *leg = new TLegend(0.44,0.60,0.92,0.89);
  leg->AddEntry(h2016,"2016 Signal Efficiencies","pl");
  leg->AddEntry(h2017,"2017 Signal Efficiencies","pl");
  leg->AddEntry(h2018,"2018 Signal Efficiencies","pl");
  leg->SetBorderSize(0);
  leg->SetFillStyle(0);
  leg->Draw();

  c1->SaveAs("SignalEffTT/SignalEffsTT.png");
  c1->SaveAs("SignalEffTT/SignalEffTT.pdf");
  c1->SaveAs("SignalEffTT/SignalEffsTT.root");
  //  c1->Update();

}
