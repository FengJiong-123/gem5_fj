/*
 * Copyright (c) 2019 ARM Limited
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

#include <unordered_map>

#include "mem/ruby/structures/PerfectCacheMemory.hh"


namespace gem5
{

namespace ruby
{

template<class ENTRY>
inline std::ostream&
operator<<(std::ostream& out, const PerfectCacheMemory<ENTRY>& obj)
{
    obj.print(out);
    out << std::flush;
    return out;
}

template<class ENTRY>
inline
PerfectCacheMemory<ENTRY>::PerfectCacheMemory()
{
}

// tests to see if an address is present in the cache
template<class ENTRY>
inline bool
PerfectCacheMemory<ENTRY>::isTagPresent(Addr address, uint bits_size, uint assoc) const
{
    // get assoc index
    uint64_t assoc_index = bitSelect(address, 6, 
                                              6 + bits_size - assoc - 1); // 6 for cache line size
    if (m_map.count(assoc_index) > 0) {
        return m_map[assoc_index].count(makeLineAddress(address)) > 0;
    } else {
        return false;
    }
}

template<class ENTRY>
inline bool
PerfectCacheMemory<ENTRY>::cacheAvail(Addr address) const
{
    return true;
}

// find an Invalid or already allocated entry and sets the tag
// appropriate for the address
template<class ENTRY>
inline void
PerfectCacheMemory<ENTRY>::allocate(Addr address)
{
    PerfectCacheLineState<ENTRY> line_state;
    line_state.m_permission = AccessPermission_Invalid;
    line_state.m_entry = ENTRY();
    line_state.m_entry_tick = 0;
    m_map[0][makeLineAddress(address)] = line_state;
}

// find an Invalid or already allocated entry and sets the tag
// appropriate for the address, considering the size limitation
template<class ENTRY>
inline bool
PerfectCacheMemory<ENTRY>::allocate(Addr address, uint bits_size, uint assoc, Tick tick)
{
    assert(m_map.size() <= (1<<(bits_size - assoc)));
    // get assoc index
    uint64_t assoc_index = bitSelect(address, 6, 
                                              6 + bits_size - assoc - 1); // 6 for cache line size
    if (m_map.count(assoc_index) > 0) {
        // this set has exist
        assert(m_map.count(assoc_index) == 1);
        if (m_map[assoc_index].size() < (1<<assoc)) {
            // could allocate dir entry
            PerfectCacheLineState<ENTRY> line_state;
            line_state.m_permission = AccessPermission_Invalid;
            line_state.m_entry = ENTRY();
            line_state.m_entry_tick = tick;
            m_map[assoc_index][makeLineAddress(address)] = line_state;
            return true;
        } else {
            return false;
        }
    } else {
        // insert a new set
        // could allocate dir entry
        PerfectCacheLineState<ENTRY> line_state;
        line_state.m_permission = AccessPermission_Invalid;
        line_state.m_entry = ENTRY();
        line_state.m_entry_tick = tick;
        m_map[assoc_index][makeLineAddress(address)] = line_state;
        return true;
    }
}

// deallocate entry
template<class ENTRY>
inline void
PerfectCacheMemory<ENTRY>::deallocate(Addr address, uint bits_size, uint assoc)
{
    assert(m_map.size() <= (1<<(bits_size - assoc)));
    // get assoc index
    uint64_t assoc_index = bitSelect(address, 6, 
                                              6 + bits_size - assoc - 1); // 6 for cache line size
    assert(m_map.count(assoc_index) == 1);
    [[maybe_unused]] auto num_erased = m_map[assoc_index].erase(makeLineAddress(address));
    assert(num_erased == 1);
}

// Returns with the physical address of the conflicting cache line
template<class ENTRY>
inline Addr
PerfectCacheMemory<ENTRY>::cacheProbe(Addr newAddress, uint bits_size, uint assoc) const
{
    // Add the replacement policy in the perfectcache
    // panic("cacheProbe called in perfect cache");
    // currently, we only support LRU and full-assoc here
    //assert(m_map.size() == (1<<bits_size));
    // unordered_map<Addr, PerfectCacheLineState<ENTRY> >::iterator it_victim;
    assert(m_map.size() <= (1<<(bits_size - assoc)));
    // get assoc index
    uint64_t assoc_index = bitSelect(newAddress, 6, 
                                                 6 + bits_size - assoc - 1); // 6 for cache line size
    Tick temp_tick = 0;
    Addr addr_victim;
    assert(m_map.count(assoc_index) == 1);
    for (auto it = m_map[assoc_index].begin(); it != m_map[assoc_index].end(); it ++) {
        if (temp_tick < it->second.m_entry_tick) {
            // switch
            // it_victim = it;
            addr_victim = it->first;
            temp_tick = it->second.m_entry_tick;
        }
    }
    return addr_victim;
}

// looks an address up in the cache
template<class ENTRY>
inline ENTRY*
PerfectCacheMemory<ENTRY>::lookup(Addr address, Tick tick, uint bits_size, uint assoc)
{
    assert(m_map.size() <= (1<<(bits_size - assoc)));
    // get assoc index
    uint64_t assoc_index = bitSelect(address, 6, 
                                              6 + bits_size - assoc - 1); // 6 for cache line size
    assert(m_map.count(assoc_index) == 1);
    m_map[assoc_index][makeLineAddress(address)].m_entry_tick = tick;
    return &m_map[assoc_index][makeLineAddress(address)].m_entry;
}

// looks an address up in the cache
template<class ENTRY>
inline const ENTRY*
PerfectCacheMemory<ENTRY>::lookup(Addr address, Tick tick, uint bits_size, uint assoc) const
{
    assert(m_map.size() <= (1<<(bits_size - assoc)));
    // get assoc index
    uint64_t assoc_index = bitSelect(address, 6, 
                                              6 + bits_size - assoc - 1); // 6 for cache line size
    assert(m_map.count(assoc_index) == 1);
    m_map[assoc_index][makeLineAddress(address)].m_entry_tick = tick;
    return &m_map[assoc_index][makeLineAddress(address)].m_entry;
}

template<class ENTRY>
inline AccessPermission
PerfectCacheMemory<ENTRY>::getPermission(Addr address) const
{
    return m_map[0][makeLineAddress(address)].m_permission;
}

template<class ENTRY>
inline void
PerfectCacheMemory<ENTRY>::changePermission(Addr address,
                                            AccessPermission new_perm)
{
    Addr line_address = makeLineAddress(address);
    PerfectCacheLineState<ENTRY>& line_state = m_map[0][line_address];
    line_state.m_permission = new_perm;
}

template<class ENTRY>
inline void
PerfectCacheMemory<ENTRY>::print(std::ostream& out) const
{
}

} // namespace ruby
} // namespace gem5

