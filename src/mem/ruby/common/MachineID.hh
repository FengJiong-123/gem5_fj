/*
 * Copyright (c) 2020 ARM Limited
 * All rights reserved.
 *
 * The license below extends only to copyright in the software and shall
 * not be construed as granting a license to any other intellectual
 * property including but not limited to intellectual property relating
 * to a hardware implementation of the functionality of the software
 * licensed hereunder.  You may use the software subject to the license
 * terms below provided that you ensure that this notice is replicated
 * unmodified and in its entirety in all distributions of the software,
 * modified or unmodified, in source code or in binary form.
 *
 * Copyright (c) 1999-2008 Mark D. Hill and David A. Wood
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met: redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer;
 * redistributions in binary form must reproduce the above copyright
 * notice, this list of conditions and the following disclaimer in the
 * documentation and/or other materials provided with the distribution;
 * neither the name of the copyright holders nor the names of its
 * contributors may be used to endorse or promote products derived from
 * this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#ifndef __MEM_RUBY_COMMON_MACHINEID_HH__
#define __MEM_RUBY_COMMON_MACHINEID_HH__

#include <iostream>
#include <string>

#include "base/cprintf.hh"
#include "mem/ruby/protocol/MachineType.hh"

namespace gem5
{

namespace ruby
{

struct MachineID
{
    MachineID() : type(MachineType_NUM), num(0) { }
    MachineID(MachineType mach_type, NodeID node_id)
        : type(mach_type), num(node_id) { }

    MachineType type;
    //! range: 0 ... number of this machine's components in system - 1
    NodeID num;

    MachineType getType() const { return type; }
    NodeID getNum() const { return num; }

    bool isValid() const { return type != MachineType_NUM; }

    MachineID getMIDplus(int adder) {return MachineID(type, (num+adder));}
    MachineID getMIDsub(int subtracter) {return MachineID(type, (num-subtracter));}
    MachineID getMIDmul(int multiplier) {return MachineID(type, (num*multiplier));}
    MachineID getMIDdiv(int divider) {return MachineID(type, (num/divider));}
    bool getMIDequal(const MachineID & obj1) {return (type == obj1.type && num == obj1.num);}

    bool sameCluster(const MachineID & obj1, int cluster_num, int core_num, int rnv_num) {
        int domain_size = (core_num+rnv_num) / cluster_num;
        NodeID IDgap = 0;
        assert(type == obj1.type);
        if (num > obj1.num) {
            IDgap = num - obj1.num;
        } else if (num < obj1.num) {
            IDgap = obj1.num - num;
        } else {
            // the same ID
            assert(num == obj1.num);
            return true;
        }

        assert(IDgap > 0);
        return ((IDgap % domain_size) == 0);
    }
};

inline std::string
MachineIDToString(MachineID machine)
{
    return csprintf("%s_%d", MachineType_to_string(machine.type), machine.num);
}

inline bool
operator==(const MachineID & obj1, const MachineID & obj2)
{
    return (obj1.type == obj2.type && obj1.num == obj2.num);
}

inline bool
operator!=(const MachineID & obj1, const MachineID & obj2)
{
    return (obj1.type != obj2.type || obj1.num != obj2.num);
}

inline bool
operator>(const MachineID & obj1, const MachineID & obj2)
{
    assert(obj1.type == obj2.type);
    return (obj1.num > obj2.num);
}

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
    return MachineID(obj1.type, (obj1.num-subtracter));
}

// Output operator declaration
::std::ostream& operator<<(::std::ostream& out, const MachineID& obj);

inline ::std::ostream&
operator<<(::std::ostream& out, const MachineID& obj)
{
    if ((obj.type < MachineType_NUM) && (obj.type >= MachineType_FIRST)) {
        out << MachineType_to_string(obj.type);
    } else {
        out << "NULL";
    }
    out << "-";
    out << obj.num;
    out << ::std::flush;
    return out;
}

} // namespace ruby
} // namespace gem5

namespace std
{
    template<>
    struct hash<gem5::ruby::MachineID>
    {
        inline size_t operator()(const gem5::ruby::MachineID& id) const
        {
            size_t hval = gem5::ruby::MachineType_base_level(
                id.type) << 16 | id.num;
            return hval;
        }
    };
} // namespace std

#endif // __MEM_RUBY_COMMON_MACHINEID_HH__
