#include <vector>
#include <string>
#include <utility>
#include <map>
#include <boost/shared_ptr.hpp>

#ifndef HEADER_B
#define HEADER_B

#include "A.hpp"

enum testB {
    BB, BBB
};


class Bklass {
    public:
        int i_;
        Bklass(int i): i_(i) { };
        Bklass(const Bklass & i): i_(i.i_) { };

    enum KlassE { B1, B2, B3};
    struct KlassKlass { int k_; };
};

class B_second {
    public:
        int i_;
        B_second(int i): i_(i) { };
        B_second(const B_second & i): i_(i.i_) { };
        void processA(const Aklass & a) {i_ = a.i_ + 10;}
};

#endif
