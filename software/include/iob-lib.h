#ifndef H_IOB__LIB_H
#define H_IOB__LIB_H

#include <stdint.h>

// IOB_TYPES
#define IOB_UINT8_T    uint8_t
#define IOB_UINT16_T   uint16_t
#define IOB_UINT32_T   uint32_t
#define IOB_UINT64_T   uint64_t
#define IOB_INT8_T     int8_t
#define IOB_INT16_T    int16_t
#define IOB_INT32_T    int32_t
#define IOB_INT64_T    int64_t

#ifndef PC
// Embedded version

#define IO_GET(type, base, addr)          (*( (volatile type *) ( (base) + (addr) ) ))
#define IO_SET(type, base, addr, value)   (*( (volatile type *) ( (base) + (addr) ) ) = (value))
#define MEM_GET(type, base, addr)         (*( (type *) ( (base) + (addr) ) ))
#define MEM_SET(type, base, addr, value)  (*( (type *) ( (base) + (addr) ) ) = (value))

#else   // ifdef PC
// PC-Emul version

#define IO_SET(type, base, addr, value) \
    (io_set_int( (addr), (int64_t) (value)))

#define IO_GET(type, base, addr) \
    ((type) io_get_int( addr ))

/* CPU Word level accesses 
 * address_shift = log2(CPU_W/8) 
 */
#define BASE(addr) (base[(addr)>>2])


/* Implement functions with the following signature for each core driver:

    static void io_set_int(int addr, int64_t value);
    static int64_t io_get_int(int addr);

*/
#endif // ifndef PC

#endif //ifndef H_IOB__LIB_H
