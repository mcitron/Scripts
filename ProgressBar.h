/*
 *  Samuel Rogerson 2011 
 *    - Allow you to create custom progress bars in loops; can take over control
 *      in a for loop, or just be called in while loop
 *      e.g.
 *        ProgressBar pb(divisions); // divisions is some int that tell you how
 *                                   // many steps you want to represent
 *
 *        for(int i=starti; i<maxnum; pb.step(i,maxnum,starti,true,false) )
 *
 *        for(int i=starti; i<=maxnum;pb.step(i,maxnum,starti,true,true) )
 *
 *        while(x->get(entry++)){
 *            pb.step(entry,nentry,startentry,false,false)
 *            ....
 *        }
 *        Doesn't work at the moment! something wrong in the counting, but meh
 */

#ifndef H_ProgressBar
#define H_ProgressBar


#include <iostream>
#include <iomanip>
#include <string>
#include <cmath>

// need to fix this

class ProgressBar {
    private:
        int numsteps_, progress_;
        std::string startmarker_, endmarker_, increment_, sterminator_, 
            cmessage_;
        bool drawPC_;
        bool first_step_;
    public:
        ProgressBar(int numsteps, std::string startmarker="[", 
            std::string endmarker="]", std::string increment="=", 
            std::string sterminator=">", std::string cmessage="done!", 
            bool drawPC = true)
        : numsteps_(numsteps), progress_(0), startmarker_(startmarker), 
            endmarker_(endmarker), increment_(increment), 
            sterminator_(sterminator), cmessage_(cmessage), drawPC_(drawPC),
            first_step_(true) {}

        void step(int& i, const int& maxi, int mini = 0, bool incr_i = false,
            bool lteq = false);
};

void ProgressBar::step(int& i,const int& maxi, int mini, bool incr_i, bool lteq)
{
  using std::cout;
  using std::string;
  using std::endl;

  if( i<mini || i>maxi ) return;
  
  // make relative to 0
  int POS = i - mini;
  int MAX_POS = maxi-mini;

  if( !lteq ) POS+=1;
  
  // Number of steps between increments

  double STEP_POS = (double)MAX_POS/(double)numsteps_;
  // Number of current steps taken
  int N_STEPS = (int) floor( POS / STEP_POS );

  bool drawProgress = N_STEPS>progress_ || first_step_;
  if(drawProgress)
  {
    progress_ = N_STEPS; 
    cout << "\r\t\t" << startmarker_;
    for( int j = 0; j<progress_; ++j ) {
        cout << increment_;
    }
    int n_whitespace = numsteps_-progress_;
    int n_spaces = n_whitespace*increment_.size();
    string whitespace = " ";
    if( (progress_ < numsteps_) && !first_step_ ) {
        string sterm(sterminator_);
        if( (int)sterminator_.size() > n_spaces) {
            sterm.resize(n_spaces);
        }
        cout << sterm;
        n_spaces -= sterm.size();
    }
    for( int j = 0; j< n_spaces; ++j) {
        cout << whitespace;
    }
    cout << endmarker_ << " " << std::flush;
    if( drawPC_ ) {
        cout << "     ";
    }
    first_step_=false;
  }
  int freq = MAX_POS/100; 
  if( freq > 0 && !(POS%freq) && drawPC_ ) 
  {
     cout << "\b\b\b\b\b" << std::setprecision(0) << std::setw(3) << 
        std::fixed << POS/static_cast<double>(MAX_POS)*100 << "% " << 
        std::flush << std::setprecision(4);
  }
  if(incr_i){ ++i; }

  if( N_STEPS==numsteps_ ) cout << cmessage_ << endl;
}

#endif    /* H_ProgressBar */
