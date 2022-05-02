module TC_Splitter16 (in, out0, out1);
    input [15:0] in;
    output [7:0] out0;
    output [7:0] out1;
    
    assign {out1, out0} = in;
endmodule

