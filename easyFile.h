#include <iostream>
#include <string>
#include <fstream>
#include <sstream>

class easyFile {
  private:
    std::ifstream file_;
    easyFile(const easyFile&); // prevent copying: no copy constructor defined
                               // on std::ifstream
    easyFile& operator=( easyFile& );
  public:
    easyFile(std::string filename="")
      { file_.open(filename.c_str(), std::ios::in); }
    ~easyFile()
      { file_.close(); }
    
    template<class T> friend easyFile& operator>>(easyFile& f, T& t);

};

template<typename T> easyFile& operator>>( easyFile& f, T& t )
{ 
  f.file_ >> t;
  return f;
}
