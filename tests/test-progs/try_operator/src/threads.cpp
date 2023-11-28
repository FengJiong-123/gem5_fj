#include <iostream> 
#include <thread> 
#include <mutex> 
#include <stdlib.h> 
#include <sys/time.h> 
#include <time.h> 
#include <sys/mman.h> 
#include <sys/types.h>
#include <string.h>
//#include "mops.h"

struct MachineID
{
    //MachineID() : type(MachineType_NUM), num(0) { }
    MachineID(int mach_type, int node_id)
        : type(mach_type), num(node_id) { }

    int type;
    //! range: 0 ... number of this machine's components in system - 1
    int num;

    int getType() const { return type; }
    int getNum() const { return num; }

};

inline MachineID
operator/(const MachineID & obj1, int divider)
{
    return MachineID(obj1.type, (obj1.num/divider));
}

inline MachineID
operator*(const MachineID & obj1, int multiplier)
{
    return MachineID(obj1.type, (obj1.num*multiplier));
}

inline MachineID
operator+(const MachineID & obj1, int adder)
{
    return MachineID(obj1.type, (obj1.num+adder));
}

inline MachineID
operator-(const MachineID & obj1, int subtracter)
{
    return MachineID(obj1.type, (obj1.num+subtracter));
}

//::std::ostream& operator<<(::std::ostream& out, const MachineID& obj);

int main()
{
    MachineID A = MachineID(1, 1);
    std::cout<<A.getNum()<<std::endl;
    MachineID B = A * 5;
    std::cout<<B.getNum()<<std::endl;
    return 0;
}