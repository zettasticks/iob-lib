/*****************************************************************************

  Description: IOB_INOUT 3-State Buffer

  Copyright (C) 2020 IObundle, Lda  All rights reserved

******************************************************************************/
`timescale 1ns / 1ps

module iob_iobuf
  (
   input  i,   // from core
   input  t_i, // from core: tristate control
   input  n_i, // from core: inversion control
   output o,   // to core
   inout  io   // to device IO
   );

   wire   o_int;

`ifdef XILINX
   IOBUF IOBUF_inst
     (
      .I(i),
      .T(t_i),
      .O(o_int),
      .IO(io)
      );
`else
   assign io = t_i? 1'bz : i;
   assign o_int = io;
`endif

   assign o = n_i^o_int;

endmodule